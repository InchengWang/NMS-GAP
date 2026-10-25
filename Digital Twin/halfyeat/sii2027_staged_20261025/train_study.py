"""Fixed five-arm TRAIN-only staged-reconstruction development pilot.

This file never loads VALID or TEST arrays. New auxiliary labels are TRAIN
supervision, not deployment inputs. A separate, gated analysis is required
before any development-validation reconstruction or metric can be reported.
"""
from pathlib import Path
import argparse,hashlib,json,math,time,platform
import numpy as np
import torch
from torch import nn
from models import MODES,SEMANTIC_MODES,build_model,LossWeights,reconstruction_losses

HERE=Path(__file__).resolve().parent
DATA=HERE/'train_v1'
OUT=HERE/'pilot_v1'
SEED=20261025
BOUND_SOURCES=('train_study.py','models.py','build_train_targets.py','audit_train_targets.py','STUDY_DESIGN_ZH.md')
CFG={'seed':SEED,'data_seed':SEED+101,'dropout_seed':SEED+211,
     'epochs':50,'batch_size':64,'lr':3e-4,'weight_decay':1e-4,'clip_norm':1.,
     'window':120,'stride':20,'width':64,'decoder_width':64,'dropout':.15,
     'encoder':'tcn','angle_weight':1.,'signal_weight':.25,'position_weight':.25,
     'threads':2,'checkpoint':'fixed_final50','unique_TRAIN_frames':12665}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False)
def jhash(o):return hashlib.sha256(canonical(o).encode()).hexdigest()
def write_once(p,o):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);b=(json.dumps(o,indent=2,allow_nan=False)+'\n').encode()
    if p.exists():
        if p.read_bytes()!=b:raise RuntimeError('Immutable artifact mismatch: '+str(p))
        return
    with p.open('xb') as f:f.write(b)

def tensor_sha(state):
    h=hashlib.sha256()
    for k,v in sorted(state.items()):
        a=v.detach().cpu().contiguous().numpy();h.update(k.encode());h.update(str(a.dtype).encode());h.update(canonical(list(a.shape)).encode());h.update(a.tobytes())
    return h.hexdigest()

def starts(n):
    if n<CFG['window']:raise ValueError('A parent is shorter than the common window.')
    q=list(range(0,n-CFG['window']+1,CFG['stride']))
    if q[-1]!=n-CFG['window']:q.append(n-CFG['window'])
    return q

def verified_metadata():
    m=read(DATA/'manifest.json');audit=read(DATA/'independent_train_target_audit.json')
    if not m['complete_release'] or m['roles']!={'TRAIN':31,'VALID':0,'TEST':0}:
        raise RuntimeError('Only the complete new TRAIN release is allowed.')
    if m['frames']!=12665 or len(m['parents'])!=31:raise RuntimeError('Unexpected TRAIN support.')
    if audit['status']!='passed_independent_TRAIN_staged_target_audit' or audit.get('training_ready_in_scoped_engineering_sense') is not True:
        raise RuntimeError('Independent target audit has not passed.')
    if audit['manifest_sha256']!=sha(DATA/'manifest.json') or audit['roles']!={'TRAIN':31,'VALID':0,'TEST':0} or audit['parents']!=31 or audit['frames']!=12665:
        raise RuntimeError('Target audit does not bind the allowed release/support.')
    contract_sha=sha(DATA/'contract.json')
    if m['contract_sha256']!=contract_sha:raise RuntimeError('Target contract identity changed.')
    if sha(HERE/'build_train_targets.py')!=m['producer_code_sha256']:raise RuntimeError('Producer source changed.')
    if audit['contract_sha256']!=contract_sha or audit['producer_sha256']!=m['producer_code_sha256'] or audit['audit_source_sha256']!=sha(HERE/'audit_train_targets.py'):
        raise RuntimeError('Target audit source/contract identity changed.')
    for r in m['parents']:
        if r['split']!='TRAIN':raise PermissionError('A heldout row was requested before any array hash/read.')
        p=(DATA/r['path']).resolve()
        if p.parent!=DATA.resolve():raise PermissionError('Unexpected data path.')
    return m,audit

def construct(mode):
    torch.manual_seed(CFG['seed'])
    return build_model(mode,encoder='tcn',width=64,decoder_width=64,dropout=.15,angle_channels=6)

def environment():
    return {'python':platform.python_version(),'numpy':np.__version__,'torch':torch.__version__,
            'device':'cpu','deterministic_algorithms':True,'threads':2}

def prepare():
    m,a=verified_metadata();reports={};initial={}
    for mode in MODES:
        model=construct(mode);reports[mode]=model.parameter_report();initial[mode]=tensor_sha(model.state_dict())
    if initial['latent_bottleneck']!=initial['strict_staged']:raise RuntimeError('Paired bottleneck initializations differ.')
    lineage=[(r['parent_id'],i) for r in m['parents'] for i in starts(r['frames'])]
    value={'status':'frozen_before_training_TRAIN_only_development_pilot','date':'2026-10-25',
           'modes':list(MODES),'cfg':CFG,'model_reports':reports,'initial_state_sha256':initial,
           'TRAIN_manifest_sha256':sha(DATA/'manifest.json'),'TRAIN_contract_sha256':sha(DATA/'contract.json'),
           'independent_target_audit_sha256':sha(DATA/'independent_train_target_audit.json'),
           'source_sha256':{n:sha(HERE/n) for n in BOUND_SOURCES},'environment':environment(),
           'parent_count':31,'subject_count':8,'unique_frames':12665,'windows':len(lineage),
           'window_lineage_sha256':jhash(lineage),'updates_per_fit':50*math.ceil(len(lineage)/64),
           'planned_fits':5,'planned_updates':5*50*math.ceil(len(lineage)/64),
           'scope':'pooled_TRAIN_people_development_not_patient_excluded_generalization',
           'extra_supervision_cost_recorded_in_target_manifest':True,'augmentation':'none_one_real_view',
           'VALID_or_TEST_array_access_in_this_trainer':False,'target_checkpoint_selection':False,
           'independent_data_order_and_post_construction_dropout_seed':True,
           'latent_channels_not_physical_reconstruction':True,'no_true_intermediate_forward_input':True}
    write_once(OUT/'training_contract.json',value);return value

def check_contract():
    c=read(OUT/'training_contract.json')
    if c['cfg']!=CFG or c['modes']!=list(MODES) or set(c['source_sha256'])!=set(BOUND_SOURCES) or c['environment']!=environment():
        raise RuntimeError('Stored configuration/source set/environment differs from this fixed runner.')
    for n,want in c['source_sha256'].items():
        if sha(HERE/n)!=want:raise RuntimeError('Frozen source changed: '+n)
    for name,key in [('manifest.json','TRAIN_manifest_sha256'),('contract.json','TRAIN_contract_sha256'),('independent_train_target_audit.json','independent_target_audit_sha256')]:
        if sha(DATA/name)!=c[key]:raise RuntimeError('Data/audit identity changed.')
    return c

def stats(a,mask=None):
    v=np.asarray(a,np.float64);mask=np.ones(v.shape,bool) if mask is None else np.asarray(mask,bool)
    count=mask.sum(0)
    if np.any(count==0):raise RuntimeError('Global TRAIN statistics have no observed labels for a channel.')
    mean=np.where(mask,v,0).sum(0)/count
    variance=np.where(mask,(v-mean)**2,0).sum(0)/count
    sd=np.sqrt(variance);sd=np.where(sd<1e-8,1.,sd)
    return {'mean':mean.tolist(),'std':sd.tolist(),'count':count.tolist()}

def normalized(a,s,mask=None):
    z=(np.asarray(a,np.float64)-s['mean'])/s['std']
    if mask is not None:z=np.where(mask,z,0.)
    if not np.isfinite(z).all():raise RuntimeError('Nonfinite normalized TRAIN target.')
    return z.astype(np.float32)

def load_windows(c):
    m,_=verified_metadata();rows=[];access=[]
    for r in m['parents']:
        if r['split']!='TRAIN':raise PermissionError('Heldout rejected before dynamic read.')
        p=DATA/r['path'];assert sha(p)==r['sha256']
        with np.load(p,allow_pickle=False) as z:
            if str(z['split'].item())!='TRAIN' or str(z['parent_id'].item())!=r['parent_id']:raise RuntimeError('Wrong array role/parent.')
            row={k:z[k].copy() for k in ['x','y','sensor_target','sensor_mask','positions']}
        n=r['frames'];assert row['x'].shape==(n,12) and row['y'].shape==(n,6)
        assert row['sensor_target'].shape==(n,18) and row['sensor_mask'].dtype==bool and row['positions'].shape==(n,24)
        assert all(np.isfinite(a).all() for a in row.values())
        rows.append((r,row));access.append({'parent_id':r['parent_id'],'split':'TRAIN','sha256':r['sha256'],'frames':n,'fields':list(row)})
    cat=lambda k:np.concatenate([v[k] for _,v in rows])
    scalers={'x':stats(cat('x')),'y':stats(cat('y')),'signals':stats(cat('sensor_target'),cat('sensor_mask')),'positions':stats(cat('positions')),
             'role':'unique_TRAIN_frames_only','TRAIN_manifest_sha256':c['TRAIN_manifest_sha256'],'frames':12665}
    write_once(OUT/'scalers.json',scalers);write_once(OUT/'TRAIN_access.json',{'events':access,'roles':{'TRAIN':31,'VALID':0,'TEST':0},'shared_study_targets_not_direct_model_inputs':True})
    w={k:[] for k in ['x','y','signals','positions','signal_mask']};lineage=[]
    for r,a in rows:
        normal={'x':normalized(a['x'],scalers['x']),'y':normalized(a['y'],scalers['y']),
                'signals':normalized(a['sensor_target'],scalers['signals'],a['sensor_mask']),
                'positions':normalized(a['positions'],scalers['positions']),'signal_mask':a['sensor_mask']}
        for start in starts(r['frames']):
            sl=slice(start,start+120)
            for k in w:w[k].append(normal[k][sl])
            lineage.append((r['parent_id'],start))
    assert jhash(lineage)==c['window_lineage_sha256']
    return {k:torch.from_numpy(np.stack(v)) for k,v in w.items()},scalers

def save_checkpoint(path,model,c,mode,epoch,optimizer=None):
    p=Path(path)
    if p.exists():raise RuntimeError('Refuse to overwrite checkpoint.')
    value={'state_dict':{k:v.detach().cpu().clone() for k,v in model.state_dict().items()},
           'contract_sha256':sha(OUT/'training_contract.json'),'mode':mode,'epoch':epoch,
           'scalers_sha256':sha(OUT/'scalers.json'),'model_source_sha256':c['source_sha256']['models.py']}
    if optimizer is not None:value['optimizer_state_dict']=optimizer.state_dict()
    torch.save(value,p)
    return {'path':str(p),'sha256':sha(p),'state_sha256':tensor_sha(value['state_dict'])}

def train():
    c=check_contract();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    data,_=load_windows(c);n=len(data['x']);complete=[]
    for mode in MODES:
        d=OUT/'runs'/mode
        if d.exists():
            if not (d/'complete.json').exists():raise RuntimeError('Partial fit retained; use a new protocol/version to retry.')
            old=read(d/'complete.json')
            if old['contract_sha256']!=sha(OUT/'training_contract.json') or sha(d/'final.pt')!=old['final']['sha256']:raise RuntimeError('Existing fit identity mismatch.')
            complete.append(old);continue
        d.mkdir(parents=True);start_time=time.time();model=construct(mode)
        assert tensor_sha(model.state_dict())==c['initial_state_sha256'][mode]
        initial=save_checkpoint(d/'initial.pt',model,c,mode,0)
        optimizer=torch.optim.AdamW(model.parameters(),lr=3e-4,weight_decay=1e-4)
        # Model construction and source snapshots cannot perturb training/dropout or shuffling streams.
        torch.manual_seed(CFG['dropout_seed']);order_rng=np.random.default_rng(CFG['data_seed'])
        history=[];steps=0
        for epoch in range(1,51):
            model.train();order=order_rng.permutation(n);means={k:0. for k in ['total','angles','signals','positions']}
            for offset in range(0,n,64):
                ids=order[offset:offset+64];ix=torch.from_numpy(ids);x=data['x'][ix]
                optimizer.zero_grad(set_to_none=True);pred=model(x)
                kwargs={'angle_target':data['y'][ix]}
                if mode in SEMANTIC_MODES:kwargs.update(signal_target=data['signals'][ix],signal_mask=data['signal_mask'][ix],position_target=data['positions'][ix])
                loss=reconstruction_losses(pred,**kwargs,weights=LossWeights())
                if not torch.isfinite(loss['total']):raise RuntimeError('Nonfinite TRAIN objective.')
                loss['total'].backward();norm=nn.utils.clip_grad_norm_(model.parameters(),1.)
                if not torch.isfinite(norm):raise RuntimeError('Nonfinite TRAIN gradient norm.')
                optimizer.step();steps+=1
                for k in means:means[k]+=float(loss[k].detach())*len(ids)/n
            history.append({'epoch':epoch,'updates':steps,'batch_order_sha256':hashlib.sha256(order.astype('<i8').tobytes()).hexdigest(),**means})
        final=save_checkpoint(d/'final.pt',model,c,mode,50,optimizer)
        write_once(d/'history.json',history)
        if steps!=c['updates_per_fit']:raise RuntimeError('Unexpected optimization exposure.')
        value={'status':'completed_fixed_final50_TRAIN_only_pending_independent_training_audit',
               'mode':mode,'contract_sha256':sha(OUT/'training_contract.json'),'epochs':50,'optimizer_updates':steps,
               'initial':initial,'final':final,'history_sha256':sha(d/'history.json'),'parameter_report':model.parameter_report(),
               'TRAIN_parent_count':31,'VALID_dynamic_reads':0,'TEST_dynamic_reads':0,
               'real_oracle_intermediates_as_motion_inputs':False,'elapsed_seconds':time.time()-start_time}
        write_once(d/'complete.json',value);complete.append(value)
        print(json.dumps({'mode':mode,'status':value['status'],'updates':steps,'last_epoch':history[-1],'seconds':value['elapsed_seconds']}),flush=True)
    for n1 in range(50):
        hashes={read(OUT/'runs'/m/'history.json')[n1]['batch_order_sha256'] for m in MODES}
        if len(hashes)!=1:raise RuntimeError('Paired data order is not identical.')
    done={'status':'all5_TRAIN_only_fits_complete_pending_independent_audit','fits':5,'optimizer_updates':sum(v['optimizer_updates'] for v in complete),
          'contract_sha256':sha(OUT/'training_contract.json'),'TRAIN_manifest_sha256':c['TRAIN_manifest_sha256'],
          'fit_completes':{m:sha(OUT/'runs'/m/'complete.json') for m in MODES},'scalers_sha256':sha(OUT/'scalers.json'),
          'VALID_dynamic_reads':0,'TEST_dynamic_reads':0,'no_performance_conclusion':True}
    write_once(OUT/'all_fits_complete.json',done);print(json.dumps(done),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','train']);a=parser.parse_args()
    if a.phase=='prepare':print(json.dumps(prepare()))
    else:train()
if __name__=='__main__':main()
