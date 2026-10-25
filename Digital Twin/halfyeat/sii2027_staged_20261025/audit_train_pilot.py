"""Independent artifact audit of the fixed five-arm TRAIN-only pilot.

The independent initialization and eval-time forward below are literal local
implementations. Production model.forward is used only as a comparator. This
audit verifies stored evidence; it does not replay the optimization trajectory.
Real checkpoints are opened only by the explicitly invoked complete-pilot audit.
"""
from __future__ import annotations

import argparse
from collections import OrderedDict
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

ROOT=Path(__file__).resolve().parent
MODES=('direct','auxiliary_only','latent_bottleneck','strict_staged','residual_staged')
SEMANTIC=('auxiliary_only','strict_staged','residual_staged')
SEED=20261025
EXPECTED_CFG={'seed':SEED,'data_seed':SEED+101,'dropout_seed':SEED+211,
              'epochs':50,'batch_size':64,'lr':3e-4,'weight_decay':1e-4,'clip_norm':1.,
              'window':120,'stride':20,'width':64,'decoder_width':64,'dropout':.15,
              'encoder':'tcn','angle_weight':1.,'signal_weight':.25,'position_weight':.25,
              'threads':2,'checkpoint':'fixed_final50','unique_TRAIN_frames':12665}


def read(path):return json.loads(Path(path).read_text())


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(2**20),b''):h.update(block)
    return h.hexdigest()


def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)


def jhash(value):return hashlib.sha256(canonical(value).encode()).hexdigest()


def write_once(path,value):
    p=Path(path);data=(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if p.exists():
        if p.read_bytes()!=data:raise RuntimeError('Independent audit receipt conflict; retain the original.')
    else:
        p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as stream:stream.write(data)


def require(condition,message):
    if not condition:raise AssertionError(message)


def tensor_sha(state):
    h=hashlib.sha256()
    for name,value in sorted(state.items()):
        a=value.detach().cpu().contiguous().numpy()
        h.update(name.encode());h.update(str(a.dtype).encode())
        h.update(canonical(list(a.shape)).encode());h.update(a.tobytes())
    return h.hexdigest()


def independent_initial(mode,seed=SEED):
    """Construct individual standard layers in the frozen module RNG order.

    No production model, encoder, initializer, or factory is called here.
    There are no state_dict buffers in this architecture.
    """
    require(mode in MODES,'Unknown mode.')
    result=OrderedDict()
    def add(prefix,module):
        for name,value in module.state_dict().items():result[prefix+'.'+name]=value.detach().clone()
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seed)
        for level,dilation in enumerate((1,2,4)):
            inc=12 if level==0 else 64;base=f'encoder.blocks.{level}'
            add(base+'.conv_first.operation',nn.Conv1d(inc,64,7,dilation=dilation))
            add(base+'.conv_second.operation',nn.Conv1d(64,64,7,dilation=dilation))
            add(base+'.norm_first',nn.LayerNorm(64))
            add(base+'.norm_second',nn.LayerNorm(64))
            if level==0:add(base+'.residual',nn.Conv1d(12,64,1))
        decoder_in=64 if mode in ('direct','auxiliary_only') else 54 if mode=='residual_staged' else 42
        add('motion_decoder.0',nn.Linear(decoder_in,64))
        add('motion_decoder.3',nn.Linear(64,6))
        if mode!='direct':
            add('bottleneck_first',nn.Linear(64,18))
            add('bottleneck_second',nn.Linear(64,24))
    return result


def independent_report(mode,state):
    count=lambda prefix:sum(v.numel() for k,v in state.items() if k.startswith(prefix))
    enc=count('encoder.');decoder=count('motion_decoder.');heads=count('bottleneck_')
    return {'mode':mode,'encoder':'tcn','encoder_parameters':enc,
            'motion_decoder_parameters':decoder,'intermediate_head_parameters':heads,
            'total_trainable_parameters':enc+decoder+heads,
            'parameters_on_motion_path':enc+decoder+(heads if mode in ('latent_bottleneck','strict_staged','residual_staged') else 0),
            'motion_decoder_input_channels':64 if mode in ('direct','auxiliary_only') else 54 if mode=='residual_staged' else 42,
            'semantic_auxiliary_supervision':mode in SEMANTIC,
            'observed_input_skip_to_motion_decoder':mode=='residual_staged',
            'receptive_field_frames':1+2*6*(1+2+4),'decoder_temporal_context_added':0,
            'all_channels_TRAIN_standardized':True,'clinical_JCS_or_sensor_position_claim':False,
            'forward_accepts_ground_truth':False}


@torch.no_grad()
def independent_forward(state,mode,observations):
    """Literal causal TCN and framewise MLP; only observed x enters forward."""
    require(mode in MODES and observations.ndim==3 and observations.shape[-1]==12,
            'Expected a declared mode and [batch,time,12] observations.')
    require(observations.shape[0]>0 and observations.shape[1]>0,'Empty context.')
    def linear(prefix,value):return F.linear(value,state[prefix+'.weight'],state[prefix+'.bias'])
    sequence=observations.transpose(1,2)
    for level,dilation in enumerate((1,2,4)):
        prefix=f'encoder.blocks.{level}';incoming=sequence
        h=F.conv1d(F.pad(incoming,(6*dilation,0)),
                   state[prefix+'.conv_first.operation.weight'],
                   state[prefix+'.conv_first.operation.bias'],dilation=dilation).transpose(1,2)
        h=F.relu(F.layer_norm(h,(64,),state[prefix+'.norm_first.weight'],state[prefix+'.norm_first.bias'],eps=1e-5))
        h=F.conv1d(F.pad(h.transpose(1,2),(6*dilation,0)),
                   state[prefix+'.conv_second.operation.weight'],
                   state[prefix+'.conv_second.operation.bias'],dilation=dilation).transpose(1,2)
        h=F.layer_norm(h,(64,),state[prefix+'.norm_second.weight'],state[prefix+'.norm_second.bias'],eps=1e-5).transpose(1,2)
        skip=F.conv1d(incoming,state[prefix+'.residual.weight'],state[prefix+'.residual.bias']) if level==0 else incoming
        sequence=F.relu(h+skip)
    hidden=sequence.transpose(1,2);result={}
    if mode=='direct':decoder_input=hidden
    else:
        first=linear('bottleneck_first',hidden);second=linear('bottleneck_second',hidden)
        intermediate=torch.cat((first,second),dim=-1)
        if mode=='latent_bottleneck':result['latent_hat']=intermediate
        else:result.update(signals_hat=first,positions_hat=second)
        decoder_input=hidden if mode=='auxiliary_only' else torch.cat((observations,intermediate),dim=-1) if mode=='residual_staged' else intermediate
    result['angles_hat']=linear('motion_decoder.3',F.relu(linear('motion_decoder.0',decoder_input)))
    require(all(torch.isfinite(v).all().item() for v in result.values()),'Nonfinite literal prediction.')
    return result


def production_comparator():
    """Import only the model module, never the training runner or its helpers."""
    spec=importlib.util.spec_from_file_location('_staged_model_comparator',ROOT/'models.py')
    # dataclasses resolves module annotations through sys.modules.
    import sys
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module


def compare_forward(module,mode,state,x):
    model=module.build_model(mode,encoder='tcn',width=64,decoder_width=64,dropout=.15,angle_channels=6)
    model.load_state_dict(state,strict=True);model.eval()
    literal=independent_forward(state,mode,x)
    with torch.no_grad():observed=model(x)
    require(set(literal)==set(observed)-{'mode'},'Forward output set differs.')
    errors={}
    for key,value in literal.items():
        require(value.shape==observed[key].shape and torch.isfinite(observed[key]).all().item(),'Production output shape/finite gate.')
        error=float(torch.max(torch.abs(value-observed[key])).item());errors[key]=error
        require(torch.allclose(value,observed[key],rtol=2e-6,atol=2e-6),'Literal/production forward differs: '+key)
    return errors


def independent_starts(frames):
    require(frames>=120,'A parent cannot support the frozen window.')
    out=[];begin=0;last=frames-120
    while begin<=last:out.append(begin);begin+=20
    if out[-1]!=last:out.append(last)
    return out


def order_hashes(windows=492):
    rng=np.random.Generator(np.random.PCG64(SEED+101));result=[]
    for _ in range(50):
        order=rng.permutation(windows)
        result.append(hashlib.sha256(np.asarray(order,dtype='<i8').tobytes()).hexdigest())
    return result


def independent_statistics(arrays,mask_arrays=None):
    """Select observed values separately per channel, then use mean/std ddof=0."""
    columns=arrays[0].shape[1];means=[];stds=[];counts=[]
    for channel in range(columns):
        values=np.concatenate([a[:,channel] if mask_arrays is None else a[m[:,channel],channel]
                               for a,m in zip(arrays,mask_arrays if mask_arrays is not None else [None]*len(arrays))]).astype(np.float64)
        require(len(values)>0 and np.isfinite(values).all(),'Missing or nonfinite scaler support.')
        means.append(float(np.mean(values)));sd=float(np.std(values,ddof=0))
        stds.append(1. if sd<1e-8 else sd);counts.append(len(values))
    return {'mean':means,'std':stds,'count':counts}


def compare_statistics(actual,expected):
    require(actual['count']==expected['count'],'Unique-frame scaler counts differ.')
    error={}
    for key in ('mean','std'):
        a=np.asarray(actual[key],np.float64);b=np.asarray(expected[key],np.float64)
        require(a.shape==b.shape and np.isfinite(a).all(),'Invalid stored scaler.')
        error[key]=float(np.max(np.abs(a-b)))
        require(np.allclose(a,b,rtol=3e-12,atol=1e-10),'Independent unique-frame scaler differs: '+key)
    return error


def require_finite(value):
    if torch.is_tensor(value):require(torch.isfinite(value).all().item(),'Nonfinite checkpoint tensor.')
    elif isinstance(value,(float,np.floating)):require(np.isfinite(value),'Nonfinite artifact number.')
    elif isinstance(value,dict):
        for v in value.values():require_finite(v)
    elif isinstance(value,(tuple,list)):
        for v in value:require_finite(v)


def checkpoint(path,expected_sha,contract_sha,scalers_sha,model_sha,mode,epoch):
    require(sha(path)==expected_sha,'Checkpoint identity changed before load.')
    value=torch.load(path,map_location='cpu',weights_only=True)
    require(sha(path)==expected_sha,'Checkpoint identity changed during load.')
    require(value['contract_sha256']==contract_sha and value['scalers_sha256']==scalers_sha and
            value['model_source_sha256']==model_sha and value['mode']==mode and value['epoch']==epoch,
            'Checkpoint provenance differs.')
    require_finite(value)
    return value


def audit_optimizer(optimizer,state):
    groups=optimizer['param_groups'];require(len(groups)==1,'Unexpected optimizer groups.')
    group=groups[0];ids=group['params']
    require(len(ids)==len(state) and len(set(ids))==len(ids) and set(ids)==set(optimizer['state']),
            'Optimizer parameter coverage differs.')
    require(group['lr']==3e-4 and group['weight_decay']==1e-4 and tuple(group['betas'])==(.9,.999) and
            group['eps']==1e-8 and group['amsgrad'] is False and group['maximize'] is False,
            'AdamW hyperparameters differ.')
    steps=[]
    for index,(name,parameter) in zip(ids,state.items()):
        value=optimizer['state'][index]
        require(set(value)=={'step','exp_avg','exp_avg_sq'},'Unexpected AdamW state fields.')
        step=value['step'];require(torch.is_tensor(step) and step.numel()==1 and float(step.item())==400.,'AdamW step is not 400.')
        require(value['exp_avg'].shape==parameter.shape and value['exp_avg_sq'].shape==parameter.shape,
                'Optimizer moment dimensions differ: '+name)
        require(torch.all(value['exp_avg_sq']>=0).item(),'AdamW squared moment is negative.')
        steps.append(int(step.item()))
    return {'parameter_tensors':len(ids),'minimum_step':min(steps),'maximum_step':max(steps),
            'all_moment_tensors_finite':True}


def run_audit():
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    data=ROOT/'train_v1';pilot=ROOT/'pilot_v1'
    # All completion/role metadata is checked before any real NPZ/weight read.
    done=read(pilot/'all_fits_complete.json');contract=read(pilot/'training_contract.json')
    manifest=read(data/'manifest.json');target_audit=read(data/'independent_train_target_audit.json')
    manifest_sha=sha(data/'manifest.json');contract_sha=sha(pilot/'training_contract.json')
    done_sha=sha(pilot/'all_fits_complete.json')
    require(done['status']=='all5_TRAIN_only_fits_complete_pending_independent_audit' and done['fits']==5 and done['optimizer_updates']==2000,
            'Only the complete five-fit pilot can be audited.')
    require(done['contract_sha256']==contract_sha and done['TRAIN_manifest_sha256']==manifest_sha,
            'Completion evidence does not bind the current contract/data.')
    require(contract['status']=='frozen_before_training_TRAIN_only_development_pilot' and contract['cfg']==EXPECTED_CFG and
            contract['modes']==list(MODES) and contract['parent_count']==31 and contract['subject_count']==8 and
            contract['unique_frames']==12665 and contract['windows']==492 and contract['updates_per_fit']==400 and
            contract['planned_fits']==5 and contract['planned_updates']==2000,'Frozen training protocol differs.')
    require(manifest['roles']=={'TRAIN':31,'VALID':0,'TEST':0} and len(manifest['parents'])==31 and manifest['frames']==12665,
            'Wrong dataset roles/support.')
    require(target_audit['status']=='passed_independent_TRAIN_staged_target_audit' and
            target_audit['manifest_sha256']==manifest_sha and target_audit['audit_source_sha256']==sha(ROOT/'audit_train_targets.py'),
            'Current TRAIN targets lack the expected independent audit.')
    require(contract['TRAIN_manifest_sha256']==manifest_sha and contract['TRAIN_contract_sha256']==sha(data/'contract.json') and
            contract['independent_target_audit_sha256']==sha(data/'independent_train_target_audit.json'),
            'Frozen data/target-audit binding differs.')
    for name,want in contract['source_sha256'].items():
        require(Path(name).name==name and sha(ROOT/name)==want,'Frozen source changed: '+name)
    require(done['VALID_dynamic_reads']==0 and done['TEST_dynamic_reads']==0 and
            contract['VALID_or_TEST_array_access_in_this_trainer'] is False and contract['target_checkpoint_selection'] is False and
            contract['augmentation']=='none_one_real_view' and contract['no_true_intermediate_forward_input'] is True,
            'Role/input/selection scope changed.')
    parents=[r['parent_id'] for r in manifest['parents']]
    require(len(set(parents))==31 and len({r['subject'] for r in manifest['parents']})==8,'Parent/subject count differs.')
    for row in manifest['parents']:
        require(row['split']=='TRAIN' and (data/row['path']).resolve().parent==data.resolve(),
                'Disallowed role/path rejected before dynamic read.')
    rows=[];arrays={};npz_read_receipts=[]
    fields=('x','y','sensor_target','sensor_mask','positions')
    for row in manifest['parents']:
        path=data/row['path'];require(sha(path)==row['sha256'],'TRAIN artifact identity changed.')
        with np.load(path,allow_pickle=False) as npz:
            require(str(npz['split'].item())=='TRAIN' and str(npz['parent_id'].item())==row['parent_id'],'Stored TRAIN role/parent differs.')
            values={key:npz[key].copy() for key in fields}
        require(sha(path)==row['sha256'],'TRAIN artifact changed during read.')
        n=row['frames']
        for key,channels in [('x',12),('y',6),('sensor_target',18),('positions',24),('sensor_mask',18)]:
            require(values[key].shape==(n,channels) and np.isfinite(values[key]).all(),'TRAIN shape/finite gate.')
        require(values['sensor_mask'].dtype==bool,'Signal mask must be boolean.')
        rows.append((row,values));arrays[row['parent_id']]=values
        npz_read_receipts.append({'parent_id':row['parent_id'],'split':'TRAIN','sha256':row['sha256'],'frames':n,'fields':list(fields)})
    require(sum(r['frames'] for r,_ in rows)==12665,'Unique TRAIN frames differ.')
    scalers=read(pilot/'scalers.json');scalers_sha=sha(pilot/'scalers.json')
    require_finite(scalers)
    require(done['scalers_sha256']==scalers_sha and scalers['frames']==12665 and scalers['role']=='unique_TRAIN_frames_only' and
            scalers['TRAIN_manifest_sha256']==manifest_sha,'Scaler provenance differs.')
    scaler_error={}
    for key,source in [('x','x'),('y','y'),('signals','sensor_target'),('positions','positions')]:
        expected=independent_statistics([a[source] for _,a in rows],
                                        [a['sensor_mask'] for _,a in rows] if key=='signals' else None)
        scaler_error[key]=compare_statistics(scalers[key],expected)
    access=read(pilot/'TRAIN_access.json')
    require(access['roles']=={'TRAIN':31,'VALID':0,'TEST':0} and access['shared_study_targets_not_direct_model_inputs'] is True and
            access['events']==npz_read_receipts,'Recorded TRAIN read ledger differs.')
    lineage=[(row['parent_id'],begin) for row,_ in rows for begin in independent_starts(row['frames'])]
    require(len(lineage)==492 and jhash(lineage)==contract['window_lineage_sha256'],'Independent window lineage differs.')
    expected_orders=order_hashes();model_module=production_comparator()
    initial_expected={mode:independent_initial(mode) for mode in MODES}
    for mode in MODES:
        require(tensor_sha(initial_expected[mode])==contract['initial_state_sha256'][mode],'Independent seed initialization differs: '+mode)
        require(independent_report(mode,initial_expected[mode])==contract['model_reports'][mode],'Independent parameter report differs.')
    common_encoder=lambda state:{k:v for k,v in state.items() if k.startswith('encoder.')}
    require(len({tensor_sha(common_encoder(s)) for s in initial_expected.values()})==1,'Five arms do not share initial encoder.')
    common_direct=lambda state:{k:v for k,v in state.items() if k.startswith(('encoder.','motion_decoder.'))}
    require(tensor_sha(common_direct(initial_expected['direct']))==tensor_sha(common_direct(initial_expected['auxiliary_only'])),
            'Direct/auxiliary common motion initialization differs.')
    require(tensor_sha(initial_expected['latent_bottleneck'])==tensor_sha(initial_expected['strict_staged']),
            'Latent/strict full initialization differs.')
    chosen=[0,len(lineage)//2,len(lineage)-1];observations=[]
    for index in chosen:
        parent,begin=lineage[index];raw=arrays[parent]['x'][begin:begin+120]
        observations.append(((raw.astype(np.float64)-np.asarray(scalers['x']['mean']))/np.asarray(scalers['x']['std'])).astype(np.float32))
    x=torch.from_numpy(np.stack(observations))
    fits={};maximum_error=0.;source_before=dict(contract['source_sha256'])
    for mode in MODES:
        run=pilot/'runs'/mode;complete=read(run/'complete.json');history=read(run/'history.json')
        require_finite(complete)
        require(done['fit_completes'][mode]==sha(run/'complete.json') and complete['history_sha256']==sha(run/'history.json'),
                'Fit/history identity differs.')
        require(complete['status']=='completed_fixed_final50_TRAIN_only_pending_independent_training_audit' and
                complete['mode']==mode and complete['contract_sha256']==contract_sha and complete['epochs']==50 and
                complete['optimizer_updates']==400 and complete['TRAIN_parent_count']==31 and
                complete['VALID_dynamic_reads']==0 and complete['TEST_dynamic_reads']==0 and
                complete['real_oracle_intermediates_as_motion_inputs'] is False,'Fit scope differs.')
        require(len(history)==50,'Incomplete epoch history.');require_finite(history)
        for epoch,item in enumerate(history,1):
            require(item['epoch']==epoch and item['updates']==epoch*8 and item['batch_order_sha256']==expected_orders[epoch-1],
                    'Independent epoch/order/update evidence differs.')
            for key in ('total','angles','signals','positions'):require(item[key]>=0,'Negative objective component.')
            expected_total=item['angles']+.25*item['signals']+.25*item['positions']
            require(np.isclose(item['total'],expected_total,rtol=3e-6,atol=3e-7),'Objective decomposition differs.')
            if mode not in SEMANTIC:require(item['signals']==0 and item['positions']==0,'Unexpected semantic supervision.')
        states={}
        for stage,epoch in [('initial',0),('final',50)]:
            record=complete[stage];path=run/(stage+'.pt')
            require(Path(record['path']).resolve()==path.resolve(),'Checkpoint path differs.')
            value=checkpoint(path,record['sha256'],contract_sha,scalers_sha,source_before['models.py'],mode,epoch)
            state=value['state_dict'];expected=initial_expected[mode]
            require(list(state)==list(expected) and all(state[k].shape==expected[k].shape and state[k].dtype==expected[k].dtype for k in state),
                    'Checkpoint state layout differs.')
            require(tensor_sha(state)==record['state_sha256'],'Recorded state fingerprint differs.')
            if stage=='initial':
                require('optimizer_state_dict' not in value and all(torch.equal(state[k],expected[k]) for k in state),
                        'Initial seed state is not independently reproduced.')
            else:optimizer_report=audit_optimizer(value['optimizer_state_dict'],state)
            states[stage]=state
        require(any(not torch.equal(states['initial'][k],states['final'][k]) for k in states['final']),
                'Final weights are identical to initialization.')
        report=independent_report(mode,states['final'])
        require(report==complete['parameter_report'],'Saved parameter report differs.')
        forward_errors=compare_forward(model_module,mode,states['final'],x)
        maximum_error=max(maximum_error,max(forward_errors.values()))
        fits[mode]={'epochs':50,'optimizer_updates':400,'initial_checkpoint_sha256':complete['initial']['sha256'],
                    'final_checkpoint_sha256':complete['final']['sha256'],'final_state_sha256':complete['final']['state_sha256'],
                    'history_sha256':sha(run/'history.json'),'parameter_report':report,
                    'optimizer_state':optimizer_report,'independent_forward_max_abs_error':forward_errors,
                    'independent_epoch_order_hashes_all_match':True}
    for name,want in source_before.items():require(sha(ROOT/name)==want,'Frozen source changed during audit.')
    require(sha(pilot/'training_contract.json')==contract_sha and sha(data/'manifest.json')==manifest_sha and
            sha(pilot/'all_fits_complete.json')==done_sha and sha(pilot/'scalers.json')==scalers_sha,
            'Source contract changed during audit.')
    result={'status':'passed_independent_TRAIN_pilot_audit','date':'2026-10-25',
            'audit_source_sha256':sha(Path(__file__)),'training_contract_sha256':contract_sha,
            'all_fits_complete_sha256':done_sha,'TRAIN_manifest_sha256':manifest_sha,
            'scalers_sha256':scalers_sha,'source_sha256':source_before,
            'roles':{'TRAIN':31,'VALID':0,'TEST':0},'subjects':8,'unique_frames':12665,'windows':492,
            'window_lineage_sha256':jhash(lineage),'fits':5,'epochs_per_fit':50,'updates_per_fit':400,'total_optimizer_updates':2000,
            'unique_frame_scaler_max_abs_differences':scaler_error,
            'all_scaler_channel_counts_independently_verified':True,
            'all_stored_model_optimizer_history_and_scaler_numbers_finite':True,
            'all_initial_states_independently_rebuilt_from_seed':True,
            'direct_auxiliary_common_motion_initialization_identical':True,
            'latent_strict_complete_initialization_identical':True,
            'all_five_initial_encoders_identical':True,
            'independent_order_generator':'numpy.Generator(PCG64(seed+101)), 50 successive permutations of 492',
            'all_250_epoch_order_hashes_independently_rebuilt':True,
            'forward_comparison_fixed_TRAIN_window_indices':chosen,
            'forward_comparison_inputs':'observed standardized x only; no y, sensor targets, positions or masks',
            'independent_forward_implementation':'local literal functional TCN+MLP; production forward only comparator',
            'independent_forward_max_abs_error':maximum_error,'fit_audits':fits,
            'VALID_TEST_dynamic_arrays_or_weights_read':0,'new_scaler_fits':0,'new_neural_fits':0,'optimizer_steps_performed_by_audit':0,
            'stored_scaler_statistics_recomputed_for_verification':True,'optimization_trajectory_recomputed':False,
            'stored_optimizer_steps_are_artifact_evidence_not_a_replayed_trajectory':True,
            'causal_model_architecture_static_and_synthetic_checks_only':True,
            'performance_or_generalization_conclusion':False}
    path=pilot/'independent_training_audit.json';write_once(path,result)
    return {'status':result['status'],'receipt':str(path),'sha256':sha(path),'fits':5,
            'total_optimizer_updates':2000,'independent_forward_max_abs_error':maximum_error,
            'training_contract_sha256':contract_sha,'all_fits_complete_sha256':result['all_fits_complete_sha256']}


def synthetic_checks():
    torch.set_num_threads(2);module=production_comparator();checks={};errors={}
    generator=torch.Generator().manual_seed(7331);x=torch.randn(2,120,12,generator=generator)
    expected_counts={'direct':155270,'auxiliary_only':158000,'latent_bottleneck':156592,'strict_staged':156592,'residual_staged':157360}
    initial={}
    for mode in MODES:
        state=independent_initial(mode);initial[mode]=state
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(SEED);production=module.build_model(mode)
        require(tensor_sha(state)==tensor_sha(production.state_dict()),'Literal standard-layer seed construction differs.')
        require(independent_report(mode,state)==production.parameter_report(),'Literal parameter report differs.')
        require(sum(v.numel() for v in state.values())==expected_counts[mode],'Unexpected count.')
        errors[mode]=compare_forward(module,mode,state,x)
        full=independent_forward(state,mode,x);prefix=independent_forward(state,mode,x[:,:43])
        for key,value in prefix.items():require(torch.allclose(value,full[key][:,:43],rtol=2e-6,atol=2e-6),'Causal prefix differs.')
    checks['five_literal_seed_states_and_parameter_reports']=True
    checks['five_literal_eval_forwards_match_production_comparator']=True
    checks['five_literal_causal_prefixes']=True
    require(tensor_sha(initial['latent_bottleneck'])==tensor_sha(initial['strict_staged']),'Paired full-state seed mismatch.')
    checks['latent_strict_complete_initialization']=True
    require(independent_starts(120)==[0] and independent_starts(141)==[0,20,21], 'Independent endpoint window coverage differs.')
    checks['window_tail_inclusion']=True
    arrays=[np.array([[1.,2.],[3.,4.],[1000.,6.]])];mask=[np.array([[True,True],[True,True],[False,True]])]
    stats=independent_statistics(arrays,mask)
    require(stats['count']==[2,3] and stats['mean']==[2.,4.] and stats['std'][0]==1.,'Mask/unique scaler statistics differ.')
    checks['masked_unique_frame_scalers']=True
    require(len(order_hashes())==50 and len(set(order_hashes()))==50,'Order generator is not advancing.')
    checks['fifty_independent_epoch_order_hashes']=True
    # No optimizer step is executed, even in synthetic tests.
    state=initial['direct'];ids=list(range(len(state)))
    opt={'param_groups':[{'params':ids,'lr':3e-4,'weight_decay':1e-4,'betas':(.9,.999),'eps':1e-8,'amsgrad':False,'maximize':False}],
         'state':{i:{'step':torch.tensor(400.),'exp_avg':torch.zeros_like(p),'exp_avg_sq':torch.zeros_like(p)} for i,p in zip(ids,state.values())}}
    require(audit_optimizer(opt,state)['minimum_step']==400,'Synthetic optimizer evidence failed.')
    opt['state'][0]['step']=torch.tensor(399.)
    try:audit_optimizer(opt,state)
    except AssertionError:pass
    else:raise AssertionError('Wrong optimizer step was accepted.')
    checks['optimizer_step_and_moment_layout_fail_closed']=True
    receipt={'status':'passed_independent_TRAIN_pilot_synthetic_checks','date':'2026-10-25','checks':checks,
             'audit_source_sha256':sha(Path(__file__)),'model_source_sha256':sha(ROOT/'models.py'),
             'forward_max_abs_errors':errors,'real_TRAIN_or_heldout_data_or_weights_read':False,
             'new_neural_fits':0,'optimizer_steps':0,'optimization_trajectory_recomputed':False}
    write_once(ROOT/('pilot_audit_synthetic_'+receipt['audit_source_sha256'][:12]+'.json'),receipt);return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--synthetic-test',action='store_true');args=p.parse_args()
    print(json.dumps(synthetic_checks() if args.synthetic_test else run_audit()))


if __name__=='__main__':main()
