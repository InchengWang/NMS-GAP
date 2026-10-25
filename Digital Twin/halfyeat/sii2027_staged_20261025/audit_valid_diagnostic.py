"""Independent VALID target and frozen-model diagnosis audits.

The targets phase must pass before production inference. Results use an already
independent literal TCN, never production model/evaluation code. Default
synthetic checks open no real dynamic data. Native full-file hashing/text scans
can include other-role bytes; only allowed VALID bracket values are decoded.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import numpy as np
import torch
from torch.nn import functional as F
import audit_train_targets as clock_helpers
import audit_train_pilot as literal_helpers

ROOT=Path(__file__).resolve().parent
VALID=ROOT/'valid_v1'
PILOT=ROOT/'pilot_v1'
ANALYSIS=PILOT/'VALID_analysis_contract.json'
RESULTS=PILOT/'valid_diagnostic_v1'
HELPER_SHA={'audit_train_targets.py':'20b7162e342ba9527c94e4ab8c282b5161bb2e677ae7ee03cb47ce85b7f43527',
            'audit_train_pilot.py':'bbf570cb0a2e6b55394e730ca252caf34cec4477bc1c1c4ab8912c13f26180a8'}
META=dict(clock_helpers.META,
 matching='marker_recall_20261021/matching_v2/ordered_matching_results.json',
 episodes='marker_recall_20261021/imu_episode_inventory.json')
MODES=('direct','auxiliary_only','latent_bottleneck','strict_staged','residual_staged')
SEMANTIC=('auxiliary_only','strict_staged','residual_staged')
ANGLES=('left_hip','left_knee','left_ankle','right_hip','right_knee','right_ankle')
GROUPS=('S3_ACC','S3_GYRO','S4_ACC','S4_GYRO','S5_ACC','S5_GYRO')
POLICY='same_frozen_modality_maxgap_prefreeze_clock_metadata_amendment_v2'
ROLES={'TRAIN':0,'VALID':12,'TEST':0}
sha=clock_helpers.sha
read=clock_helpers.jread
write_once=clock_helpers.write_once
require=literal_helpers.require


def helpers_unchanged():
    for name,want in HELPER_SHA.items():require(sha(ROOT/name)==want,'Independent helper changed: '+name)


def analysis_gate():
    """Only code/metadata/TRAIN artifacts are accessed in this gate."""
    helpers_unchanged();c=read(ANALYSIS)
    require(c['status']=='frozen_once_VALID_development_diagnostic_before_new_VALID_dynamic_read','Analysis not frozen.')
    rows=c['allowed_VALID_rows'];wanted={r['parent_id']:r for r in rows}
    require(len(rows)==12 and len(wanted)==12 and sum(r['frames'] for r in rows)==7238 and len({r['subject'] for r in rows})==8,'Wrong frozen VALID support.')
    require(all(r['split']=='VALID' and r['affected_side'] in ('left','right') for r in rows),'Wrong frozen role or side.')
    require(c['parent_count']==12 and c['frames']==7238 and c['subject_count']==8 and c['support']=='full_original_no_crop','Wrong analysis support.')
    require(c['TEST_dynamic_reads']==0 and c['neural_fits_in_analysis']==0 and c['no_oracle_intermediate_motion_inputs'] is True and c['no_hyperparameter_or_mode_selection_from_diagnostic'] is True,'Analysis scope changed.')
    expected_sources={'eval_study.py','models.py','train_study.py','build_valid_targets.py','build_train_targets.py','audit_train_pilot.py','audit_valid_diagnostic.py'}
    require(set(c['source_sha256'])==expected_sources,'Analysis source allowlist differs.')
    for name,want in c['source_sha256'].items():require(sha(ROOT/name)==want,'Analysis source changed: '+name)
    for name,key in [('training_contract.json','training_contract_sha256'),('all_fits_complete.json','all_fits_complete_sha256'),('independent_training_audit.json','training_audit_sha256'),('scalers.json','scalers_sha256')]:
        require(sha(PILOT/name)==c[key],'Frozen TRAIN prerequisite changed: '+name)
    ta=read(PILOT/'independent_training_audit.json')
    require(ta['status']=='passed_independent_TRAIN_pilot_audit' and ta['training_contract_sha256']==c['training_contract_sha256'] and ta['all_fits_complete_sha256']==c['all_fits_complete_sha256'],'Independent TRAIN audit differs.')
    require(ta['audit_source_sha256']==HELPER_SHA['audit_train_pilot.py'],'Literal auditor is not the audited source.')
    require(len(c['five_frozen_weights'])==5 and {w['mode'] for w in c['five_frozen_weights']}==set(MODES),'Five frozen modes required.')
    require(len({w['path'] for w in c['five_frozen_weights']})==5 and all(w['epochs']==50 for w in c['five_frozen_weights']),'Wrong frozen checkpoint support.')
    return c,wanted


class ValidAccess:
    """Explicit VALID allowlist, independent of the TRAIN helper Access class."""
    def __init__(self,records,candidates,allowed):
        self.records=records;self.candidates=candidates;self.allowed=frozenset(allowed)
        require(all(p in records and p in candidates and records[p]['split']=='VALID' and candidates[p]['split']=='VALID' for p in self.allowed),'Invalid VALID access construction.')
        self.hash_events=[];self.dynamic_npz=set();self.dynamic_csv_files=set()
    def require(self,owners):
        ps=tuple(owners)
        if not ps or any(p not in self.allowed or self.records[p]['split']!='VALID' or self.candidates[p]['split']!='VALID' for p in ps):
            raise PermissionError('Only frozen VALID owners may access dynamic sources.')
        return ps
    def checked_hash(self,path,expected,owners,kind):
        ps=self.require(owners);got=sha(path);require(got==expected,'Dynamic file identity changed.')
        self.hash_events.append({'kind':kind,'owners':sorted(ps),'bytes':Path(path).stat().st_size,'sha256':got})
        return got
    def npz(self,path,expected,parent,fields,kind):
        self.require([parent]);self.checked_hash(path,expected,[parent],kind)
        with np.load(path,allow_pickle=False) as z:
            require(z['split'].item()=='VALID' and z['parent_id'].item()==parent,'Stored role/parent refused before array extraction.')
            out={k:z[k].copy() for k in fields}
        self.checked_hash(path,expected,[parent],kind);self.dynamic_npz.add((kind,str(Path(path).resolve())))
        return out


def context_bounds(source,candidates,matching,parent):
    z=candidates[parent];m=matching[parent]
    eps={e['episode_id']:e for e in source['episodes']['episodes']}
    sessions={s['session_id']:s for s in source['episodes']['sessions']}
    ep=eps[z['episode_id']];se=sessions[m['session_id']]
    runs=[r for r in se['runs'] if r['run_id']==m['run_id']]
    require(len(runs)==1 and ep['session_id']==m['session_id'] and ep['run_id']==m['run_id'],'Episode/run mismatch.')
    require(Path(se['raw_folder']).resolve()==Path(m['raw_folder']).resolve(),'Run source folder differs.')
    return [max(ep['native_epoch_bounds_ms'][0],runs[0]['native_epoch_bounds_ms'][0]),min(ep['native_epoch_bounds_ms'][1],runs[0]['native_epoch_bounds_ms'][1])]


def independent_source(job,access):
    """Independent np.interp reconstruction with explicit VALID flank guards."""
    ps=access.require(job['owners']);native=job['kind']=='native_csv'
    access.checked_hash(job['path'],job['sha256'],ps,job['kind'])
    header,name,t=clock_helpers.clocks_only(job['path'],native)
    require(all(k in header for k in job['columns']),'Explicit source column missing.')
    if native:require(np.array_equal(t[[0,-1]],job['inventory_bounds']),'Inventory endpoints differ.')
    brackets={};parts=[];support={}
    for p in ps:
        q=job['query'][p];lo,hi,a=clock_helpers.bracket_indices(t,q,native);ids=np.unique(np.r_[lo,hi]);parts.extend((lo,hi))
        scale=1. if native else 1000.;limit=25.1 if native else .0251*1000
        before=float(max(0.,q[0]-t[ids[0]])*scale);after=float(max(0.,t[ids[-1]]-q[-1])*scale)
        require(max(before,after)<=limit+1e-4,'Endpoint flank exceeds pre-frozen maxgap policy.')
        epoch=t[ids].astype(np.float64) if native else t[ids]*1000+job['offsets'][p]
        lower,upper=job['context'][p]
        if np.any(epoch<lower-1e-5) or np.any(epoch>upper+1e-5):raise PermissionError('Bracket leaves original native episode/run.')
        for olo,ohi in job['other_role_bounds'][p]:
            if np.any((epoch>=olo-1e-5)&(epoch<=ohi+1e-5)):raise PermissionError('VALID value bracket enters another-role walk.')
        outer=ids[(t[ids]<q[0])|(t[ids]>q[-1])]
        support[p]={'query_frames':len(q),'query_bounds':[float(q[0]),float(q[-1])],
          'full_original_query_no_crop':True,'selected_source_rows':len(ids),
          'source_row_index_bounds':[int(ids[0]),int(ids[-1])],
          'external_adjacent_rows_outside_full_query_interval':len(outer),
          'external_adjacent_row_indices':outer.tolist(),'external_adjacent_source_times':t[outer].tolist(),
          'endpoint_context_before_ms':before,'endpoint_context_after_ms':after,'endpoint_context_limit_ms':limit,
          'endpoint_context_policy':POLICY,'native_episode_and_run_bounds_ms':[lower,upper],
          'all_selected_rows_inside_original_native_episode_and_run':True,'selected_rows_outside_other_roles_walking_intervals':True}
        brackets[p]=(lo,hi,a)
    ids=np.unique(np.concatenate(parts));access.require(ps)
    values,token_sha,row_sha=clock_helpers.read_numeric_rows(job['path'],header,name,t,ids,job['columns'],job['factor'],native)
    access.dynamic_csv_files.add(str(Path(job['path']).resolve()));access.checked_hash(job['path'],job['sha256'],ps,job['kind'])
    origin=t[ids[0]]
    rebuilt={p:np.column_stack([np.interp(job['query'][p]-origin,t[ids]-origin,values[:,k]) for k in range(len(job['columns']))]) for p in ps}
    inside=np.zeros(len(ids),bool)
    for q in job['query'].values():inside|=(t[ids]>=q[0])&(t[ids]<=q[-1])
    return {'interpolated':rebuilt,'brackets':brackets,'ids':ids,'token_sha256':token_sha,'rows_sha256':row_sha,
      'metadata_rows_scanned':len(t),'numeric_rows_decoded':len(ids),'numeric_cells_decoded':int(values.size),
      'per_parent_support':support,'external_adjacent_unique_rows_outside_all_full_query_intervals':int((~inside).sum())}


def targets_audit(experiments_root):
    c,wanted=analysis_gate();e=Path(experiments_root).resolve();m=read(VALID/'manifest.json');dc=read(VALID/'contract.json')
    source={k:read(e/rel) for k,rel in META.items()};meta_sha={k:sha(e/rel) for k,rel in META.items()}
    records={r['parent_id']:r for r in source['release']['trials']};candidates={r['parent_id']:r for r in source['candidates']['trials']}
    require(len(records)==53 and set(records)==set(candidates) and all(records[p]['split']==candidates[p]['split'] for p in records),'Original metadata role inventory differs.')
    parents=sorted((p for p in records if records[p]['split']=='VALID'),key=clock_helpers.ordered_parent)
    require(set(parents)==set(wanted) and len(parents)==12,'Frozen and original VALID allowlists differ.')
    require(sum(records[p]['frames'] for p in parents)==7238 and len({records[p]['subject'] for p in parents})==8,'Original VALID support differs.')
    for p in parents:
        require(all(records[p][k]==wanted[p][k] for k in ('subject','frames','split','affected_side')),'Frozen row metadata differs.')
    require(m['status']=='complete_VALID_only_staged_targets_built_pending_independent_audit' and m['complete_release'] is True and m['roles']==ROLES and m['frames']==7238 and m['crop'] is None,'Only complete full-support VALID export is allowed.')
    require(m['requested_VALID_parents']==parents and len(m['parents'])==12 and len({r['parent_id'] for r in m['parents']})==12,'Wrong or duplicate exported parents.')
    require(m['contract_sha256']==sha(VALID/'contract.json') and m['analysis_contract_sha256']==sha(ANALYSIS) and dc['analysis_contract_sha256']==sha(ANALYSIS),'Analysis/data contract binding differs.')
    require(dc['metadata_sha256']==meta_sha,'Metadata SHA differs.')
    for key,name in [('producer_code_sha256','build_valid_targets.py'),('helper_code_sha256','build_train_targets.py')]:
        require(m[key]==sha(ROOT/name) and dc[key]==sha(ROOT/name),'Producer/helper code differs.')
    auth=dc['authorization'];require(auth['status']=='authorized_once_VALID_development_diagnostic' and auth['permitted_dynamic_role']=='VALID' and auth['allowed_parent_ids']==parents,'Export lacks explicit VALID authorization.')
    require(auth['prerequisites']['VALID_analysis_contract']['sha256']==sha(ANALYSIS) and auth['prerequisites']['TRAIN_training_audit']['sha256']==c['training_audit_sha256'],'Export prerequisite binding differs.')
    required={'permitted_dynamic_role':'VALID','complete_release_parent_count':12,'complete_release_frames':7238,'crop':None,'fixed_query_rate_hz':100.,
      'sensor_target_frame':'each_measured_sensor_native_xyz','sensor_target_units':'ACC_m/s^2_GYRO_rad/s','position_units':'meters',
      'position_names':list(clock_helpers.POINTS),'position_definition':'(float64_interpolated_point_xyz_mm-bilateral_hip_midpoint_mm)/1000_then_float32',
      'position_frame':'legacy_candidate_pelvis_axes_joint_landmark_proxy_not_JCS_or_IMU_centers',
      'model_input_keys':['x'],'auxiliary_target_keys':['sensor_target','sensor_mask','positions'],'final_target_keys':['y'],
      'native_max_interpolation_gap_ms':25.1,'point_max_interpolation_gap_s':.0251,'native_ACC_g_factor':9.80665,'native_GYRO_deg_s_factor':float(np.pi/180),
      'scaler_fits':0,'neural_fits':0,'TRAIN_TEST_dynamic_arrays_read':0}
    require(all(dc.get(k)==v for k,v in required.items()),'Unit/frame/query/cost contract differs.')
    require(dc['sensor_target_order']==[f'{s}_{kind}_{a}' for s in ('S3','S4','S5') for kind in ('acc','gyro') for a in 'xyz'],'Sensor order differs.')
    require(dc['endpoint_context_rule']['policy']==POLICY and m['endpoint_context_policy']==POLICY,'Endpoint policy differs.')
    for k,v in {'TRAIN_TEST_dynamic_arrays_read':0,'scaler_fits':0,'model_fits':0,'unselected_numeric_signal_values_converted':False,'all_full_queries_preserved_without_crop':True,'diagnostic_ready_before_independent_audit':False}.items():require(m.get(k)==v,'Export accounting differs: '+k)
    access=ValidAccess(records,candidates,parents);rows={r['parent_id']:r for r in m['parents']};matching={r['parent_id']:r for r in source['matching']['rows'] if r['accepted_identity_candidate']}
    folders={str(Path(f['folder']).resolve()):f for f in source['inventory']['source_folders']}
    receipts={r['path']:r for r in m['source_value_read_receipts']};require(len(receipts)==len(m['source_value_read_receipts']),'Duplicate source receipts.')
    afields=('x','y_angles','time','input_epoch_ms','optic_absolute_time')
    bfields=('x','y','sensor_target','sensor_mask','positions','time','input_epoch_ms','optic_absolute_time','source_frame_indices','sensor_source_left_indices','sensor_source_right_indices','sensor_interp_alpha','point_source_left_indices','point_source_right_indices','point_interp_alpha','subject','contract_sha256')
    arrays={};jobs={};plans={};point_paths={}
    for p in parents:
        r=records[p];z=candidates[p];row=rows[p];match=matching[p];n=r['frames'];access.require([p])
        require(row['split']=='VALID' and row['subject']==r['subject'] and row['frames']==n and row['crop'] is None,'Exported row support differs.')
        src=(e/'marker_recall_20261021/ordered_native_candidates_v2'/z['path']).resolve()
        require(src==Path(r['source_npz']).resolve() and z['sha256']==r['source_sha256'],'Original source identity differs.')
        op=(VALID/row['path']).resolve();require(op.parent==VALID.resolve(),'Output path escapes VALID directory.')
        a=access.npz(src,r['source_sha256'],p,afields,'original_VALID_npz');b=access.npz(op,row['sha256'],p,bfields,'staged_VALID_npz')
        require(b['subject'].item()==r['subject'] and b['contract_sha256'].item()==m['contract_sha256'],'Stored output provenance differs.')
        for key,old,channels in [('x','x',12),('y','y_angles',6)]:
            require(a[old].dtype==np.float32 and a[old].shape==(n,channels) and np.isfinite(a[old]).all() and b[key].dtype==np.float32 and np.array_equal(a[old],b[key]),'Original full x/y changed.')
        for key in afields[2:]:
            require(a[key].shape==(n,) and np.isfinite(a[key]).all() and np.all(np.diff(a[key])>0) and np.array_equal(a[key],b[key]),'Original full clock changed.')
        require(np.max(np.abs(np.diff(a['input_epoch_ms'])-10.))<=.001 and np.allclose(a['input_epoch_ms'][[0,-1]],z['input_epoch_bounds_ms'],rtol=0,atol=1e-5),'Original 100Hz support changed.')
        require(np.allclose(a['input_epoch_ms'],a['optic_absolute_time']*1000+z['native_epoch_offset_ms'],rtol=0,atol=1e-5),'Original time equation changed.')
        require(np.array_equal(b['source_frame_indices'],np.arange(n,dtype=np.int64)),'VALID crop/source lineage differs.')
        require(b['sensor_mask'].dtype==bool and b['sensor_mask'].shape==(n,18),'Invalid sensor mask.')
        for key,ch in [('sensor_target',18),('positions',24)]:require(b[key].dtype==np.float32 and b[key].shape==(n,ch) and np.isfinite(b[key]).all(),'Output target layout differs.')
        for key,shape,dtype in [('sensor_source_left_indices',(n,6),np.int64),('sensor_source_right_indices',(n,6),np.int64),('sensor_interp_alpha',(n,6),np.float64),('point_source_left_indices',(n,),np.int64),('point_source_right_indices',(n,),np.int64),('point_interp_alpha',(n,),np.float64),('source_frame_indices',(n,),np.int64)]:
            require(b[key].shape==shape and b[key].dtype==dtype,'Output lineage layout differs.')
        require(match['original_split']=='VALID' and match['episode_id']==z['episode_id'] and match['native_epoch_offset_ms']==z['native_epoch_offset_ms'] and np.array_equal(match['source_walk_epoch_bounds_ms'],z['input_epoch_bounds_ms']),'Original matching identity changed.')
        context=context_bounds(source,candidates,matching,p);require(a['input_epoch_ms'][0]>=context[0] and a['input_epoch_ms'][-1]<=context[1],'Full query leaves episode/run.')
        folder=str(Path(z['native_sources'][0]['path']).resolve().parent);require(folder==str(Path(match['raw_folder']).resolve()) and folders[folder]['subject']==r['subject'],'Native folder identity differs.')
        other=[zz['input_epoch_bounds_ms'] for pp,zz in candidates.items() if pp!=p and records[pp]['split']!='VALID' and str(Path(zz['native_sources'][0]['path']).resolve().parent)==folder]
        require(all(max(a['input_epoch_ms'][0],lo)>min(a['input_epoch_ms'][-1],hi) for lo,hi in other),'Full VALID query overlaps another-role walk.')
        plans[p]=[]
        def job_common(path,expected,kind,columns,factor,query):
            j=jobs.setdefault(path,{'path':path,'sha256':expected,'kind':kind,'owners':[],'columns':columns,'factor':factor,'query':{},'context':{},'offsets':{},'other_role_bounds':{}})
            require(j['sha256']==expected and j['columns']==columns,'Ambiguous source metadata.')
            j['owners'].append(p);j['query'][p]=query;j['context'][p]=context;j['offsets'][p]=z['native_epoch_offset_ms'];j['other_role_bounds'][p]=other
            return j
        for sensor,mod in clock_helpers.MODS:
            found=[q for q in folders[folder]['files'] if q['sensor']==sensor and q['modality']==mod];require(len(found)<=1,'Ambiguous sensor modality.')
            if not found:plans[p].append(None);continue
            q=found[0];require(all(q[k]==0 for k in ('duplicate_timestamp_count','decreasing_timestamp_count','nonfinite_values','gaps_over_25_1ms')),'Present native source unsafe.')
            path=str(Path(q['path']).resolve());plans[p].append(path);acc=mod=='Accelerometer';unit='g' if acc else 'deg/s'
            j=job_common(path,q['sha256'],'native_csv',[f'{axis}-axis ({unit})' for axis in 'xyz'],9.80665 if acc else float(np.pi/180),a['input_epoch_ms'])
            j['inventory_bounds']=[q['epoch_start_ms'],q['epoch_end_ms']]
        path=str(Path(z['point_labels']).resolve());require(path not in jobs,'Point source reused across parent identities.');point_paths[p]=path
        job_common(path,z['point_sha256'],'point_csv',list(clock_helpers.PCOLS),1.,a['optic_absolute_time']);arrays[p]=b
    require(set(jobs)==set(receipts),'Source receipt set differs.')
    rebuilt={};source_audits=[]
    for path,job in sorted(jobs.items()):
        q=independent_source(job,access);rebuilt[path]=q;mr=receipts[path]
        require(mr['role']=='VALID' and mr['kind']==job['kind'] and mr['sha256']==job['sha256'] and set(mr['owners'])==set(job['owners']),'Source ownership differs.')
        for mk,qk in [('source_row_indices_zero_based_after_header','ids'),('selected_rows_text_tokens_sha256','token_sha256'),('selected_rows_indices_clock_and_SI_values_sha256','rows_sha256'),('all_rows_clock_metadata_scanned','metadata_rows_scanned'),('numeric_value_rows_decoded','numeric_rows_decoded'),('numeric_value_cells_decoded','numeric_cells_decoded'),('per_parent_support','per_parent_support'),('external_adjacent_unique_rows_outside_all_full_query_intervals','external_adjacent_unique_rows_outside_all_full_query_intervals')]:
            expected=q[qk].tolist() if qk=='ids' else q[qk];require(mr[mk]==expected,'Independent source read/support receipt differs: '+mk)
        require(mr['factor_to_output_units']==job['factor'] and mr['numeric_value_columns_decoded']==job['columns'],'SI conversion/column order differs.')
        source_audits.append({'kind':job['kind'],'source_sha256':job['sha256'],'owners':sorted(job['owners']),'numeric_rows_decoded':q['numeric_rows_decoded'],'numeric_cells_decoded':q['numeric_cells_decoded'],'clock_rows_scanned':q['metadata_rows_scanned'],'selected_rows_SI_sha256':q['rows_sha256']})
    max_signal=max_position=max_alpha=0.;coverage=np.zeros(6,np.int64);group_frames=np.zeros(6,np.int64)
    for p,b in arrays.items():
        n=len(b['x']);mask=np.zeros((n,18),bool)
        for g,path in enumerate(plans[p]):
            sl=slice(g*3,g*3+3)
            if path is None:
                require(np.all(b['sensor_target'][:,sl]==0) and not b['sensor_mask'][:,sl].any() and np.all(b['sensor_source_left_indices'][:,g]==-1) and np.all(b['sensor_source_right_indices'][:,g]==-1) and np.all(b['sensor_interp_alpha'][:,g]==0),'Missing modality placeholder differs.');continue
            mask[:,sl]=True;coverage[g]+=1;group_frames[g]+=n;rec=rebuilt[path];lo,hi,a=rec['brackets'][p]
            require(np.array_equal(b['sensor_source_left_indices'][:,g],lo) and np.array_equal(b['sensor_source_right_indices'][:,g],hi),'Signal row lineage differs.')
            error=float(np.max(np.abs(b['sensor_interp_alpha'][:,g]-a)));max_alpha=max(max_alpha,error);require(error<=1e-12,'Signal interpolation alpha differs.')
            max_signal=max(max_signal,clock_helpers.compare_float32(b['sensor_target'][:,sl],rec['interpolated'][p],'VALID dense signal'))
        require(np.array_equal(b['sensor_mask'],mask),'Mask differs from inventory absence.')
        point=rebuilt[point_paths[p]];lo,hi,a=point['brackets'][p]
        require(np.array_equal(b['point_source_left_indices'],lo) and np.array_equal(b['point_source_right_indices'],hi),'Point row lineage differs.')
        error=float(np.max(np.abs(b['point_interp_alpha']-a)));max_alpha=max(max_alpha,error);require(error<=1e-12,'Point interpolation alpha differs.')
        mm=point['interpolated'][p].reshape(n,8,3);root=mm[:,[0,4]].mean(axis=1);positions=((mm-root[:,None])/1000).reshape(n,24)
        max_position=max(max_position,clock_helpers.compare_float32(b['positions'],positions,'VALID relative position'))
        require(np.max(np.abs(b['positions'].reshape(n,8,3)[:,0]+b['positions'].reshape(n,8,3)[:,4]))<=1e-7,'Hip midpoint not zero.')
        for key,want in rows[p]['array_sha256'].items():
            if key in b:require(clock_helpers.array_sha(b[key])==want,'Stored array fingerprint differs: '+key)
    for kind,key in [('native_csv','native_numeric_rows_decoded'),('point_csv','point_numeric_rows_decoded')]:require(m[key]==sum(q['numeric_rows_decoded'] for q in source_audits if q['kind']==kind),'Read total differs.')
    helpers_unchanged();require(sha(ANALYSIS)==m['analysis_contract_sha256'],'Analysis changed during audit.')
    for k,rel in META.items():require(sha(e/rel)==meta_sha[k],'Metadata changed during audit.')
    value={'status':'passed_independent_VALID_staged_target_audit','date':'2026-10-25','audit_source_sha256':sha(__file__),'independent_helper_sha256':HELPER_SHA,
      'manifest_sha256':sha(VALID/'manifest.json'),'contract_sha256':sha(VALID/'contract.json'),'analysis_contract_sha256':sha(ANALYSIS),'producer_sha256':sha(ROOT/'build_valid_targets.py'),
      'metadata_sha256':meta_sha,'parents':12,'subjects':8,'frames':7238,'roles':ROLES,'crop':None,
      'all_original_x_y_queries_exactly_preserved':True,'max_sensor_float32_difference_SI':max_signal,'max_position_float32_difference_m':max_position,'max_interpolation_alpha_difference':max_alpha,
      'modality_available_parent_counts':dict(zip(GROUPS,coverage.tolist())),'modality_supervised_sample_seconds':dict(zip(GROUPS,(group_frames/100).tolist())),
      'signal_mask_valid_channel_frames':int(sum(b['sensor_mask'].sum() for b in arrays.values())),
      'source_audits':source_audits,'source_files':len(source_audits),'dynamic_npz_arrays_opened':{'original_VALID':12,'staged_VALID':12,'TRAIN':0,'TEST':0},
      'endpoint_policy':POLICY,'all_selected_rows_inside_original_episode_run':True,'selected_numeric_rows_outside_other_roles_walks':True,
      'unselected_signal_or_point_tokens_converted':False,'shared_native_bytes_mechanically_hashed':True,'zero_other_role_source_bytes_read_claim':False,
      'mechanical_hash_calls':len(access.hash_events),'mechanical_hash_bytes_with_repeats':sum(r['bytes'] for r in access.hash_events),
      'new_neural_fits':0,'scaler_refits':0,'TEST_dynamic_reads':0,'performance_or_generalization_conclusion':False}
    path=VALID/'independent_valid_target_audit.json';write_once(path,value)
    return {'status':value['status'],'receipt':str(path),'sha256':sha(path),'parents':12,'frames':7238}


def motion_metrics(predicted,target,side,offset=0):
    """Independent six-channel RMSE, retaining the anatomical angle order."""
    require(side in ('left','right') and predicted.shape==target.shape and len(target)>offset,'Invalid motion metric input.')
    columns=[]
    for k in range(6):
        error=np.asarray(predicted[offset:,k],np.float64)-np.asarray(target[offset:,k],np.float64)
        columns.append(float(np.sqrt(np.dot(error,error)/len(error))))
    return {**dict(zip(ANGLES,columns)),'six_angles':sum(columns)/6.,'bilateral_knee':(columns[1]+columns[4])/2.,'paretic_knee':columns[1 if side=='left' else 4]}


def restored(array,scaler):
    return np.asarray(array,np.float64)*np.asarray(scaler['std'],np.float64)[None,:]+np.asarray(scaler['mean'],np.float64)[None,:]


@torch.no_grad()
def independent_predictions(state,mode,x,scalers):
    """Own interventions/decoder; only the pinned independent TCN is shared."""
    pred=literal_helpers.independent_forward(state,mode,x)
    package={'angles_hat_deg':restored(pred['angles_hat'][0].numpy(),scalers['y'])}
    if mode in ('direct','auxiliary_only'):
        for name in ('zero','shift'):package[name+'_angles_hat_deg']=package['angles_hat_deg'].copy()
    else:
        intermediate=pred['latent_hat'] if mode=='latent_bottleneck' else torch.cat((pred['signals_hat'],pred['positions_hat']),dim=-1)
        for name in ('zero','shift'):
            value=torch.zeros_like(intermediate) if name=='zero' else torch.roll(intermediate,shifts=x.shape[1]//2,dims=1)
            decoder_input=torch.cat((x,value),-1) if mode=='residual_staged' else value
            hidden=F.relu(F.linear(decoder_input,state['motion_decoder.0.weight'],state['motion_decoder.0.bias']))
            bad=F.linear(hidden,state['motion_decoder.3.weight'],state['motion_decoder.3.bias'])
            package[name+'_angles_hat_deg']=restored(bad[0].numpy(),scalers['y'])
    if mode in SEMANTIC:
        package['signals_hat_SI']=restored(pred['signals_hat'][0].numpy(),scalers['signals'])
        package['positions_hat_m']=restored(pred['positions_hat'][0].numpy(),scalers['positions'])
    require(all(np.isfinite(v).all() for v in package.values()),'Nonfinite independent prediction.')
    return package


def all_metrics(package,arrays,side,scalers,mode):
    y=arrays['y'];pred=package['angles_hat_deg'];result=motion_metrics(pred,y,side)
    constant=np.repeat(np.asarray(scalers['y']['mean'],np.float64)[None],len(y),axis=0)
    result.update({'TRAIN_mean_'+k:v for k,v in motion_metrics(constant,y,side).items()})
    result.update({'steady_'+k:v for k,v in motion_metrics(pred,y,side,84).items()})
    for name in ('zero','shift'):
        bad=package[name+'_angles_hat_deg']
        result.update({name+'_'+k:v for k,v in motion_metrics(bad,y,side).items()})
        result[name+'_max_prediction_change_deg']=float(np.max(np.abs(bad-pred)))
    if mode in SEMANTIC:
        shat=package['signals_hat_SI'];phat=package['positions_hat_m']
        for g,name in enumerate(GROUPS):
            channels=np.arange(g*3,g*3+3);valid=arrays['sensor_mask'][:,channels]
            if np.any(valid):
                error=(shat[:,channels]-arrays['sensor_target'][:,channels])[valid]
                result[name+'_RMSE']=float(np.sqrt(np.dot(error,error)/len(error)))
                reference=np.repeat(np.asarray(scalers['signals']['mean'],np.float64)[None,channels],len(y),axis=0)
                delta=(reference-arrays['sensor_target'][:,channels])[valid]
                result[name+'_TRAIN_mean_RMSE']=float(np.sqrt(np.dot(delta,delta)/len(delta)))
            else:result[name+'_RMSE']=None;result[name+'_TRAIN_mean_RMSE']=None
        def mpjpe(value):
            difference=(value-arrays['positions']).reshape(len(y),8,3)
            distances=np.sqrt(np.sum(difference*difference,axis=2))
            return float(np.sum(distances)/distances.size*1000.)
        result['position_MPJPE_mm']=mpjpe(phat)
        reference=np.repeat(np.asarray(scalers['positions']['mean'],np.float64)[None],len(y),axis=0)
        result['position_TRAIN_mean_MPJPE_mm']=mpjpe(reference)
    return result


def independently_aggregate(rows):
    result={}
    for mode in MODES:
        selected=[r for r in rows if r['mode']==mode];people=sorted(set(r['subject'] for r in selected));by_person={}
        for person in people:
            trials=[r['metrics'] for r in selected if r['subject']==person]
            names=sorted(set().union(*(t.keys() for t in trials)));values={}
            for name in names:
                available=[t[name] for t in trials if t.get(name) is not None]
                if available:values[name]=float(sum(available)/len(available))
            by_person[person]=values
        names=sorted(set().union(*(v.keys() for v in by_person.values()))) if by_person else []
        means={};counts={}
        for name in names:
            available=[v[name] for v in by_person.values() if name in v];means[name]=float(sum(available)/len(available));counts[name]=len(available)
        result[mode]={'parents':len(selected),'people':len(people),'equal_person_mean':means,'metric_people_counts':counts,'by_person':by_person}
    return result


def numeric_equal(actual,expected,label,rtol=3e-6,atol=3e-5):
    """Recursive structure check, with explicit finite/tolerance checks."""
    if isinstance(expected,dict):
        require(isinstance(actual,dict) and set(actual)==set(expected),label+': keys differ.')
        return max((numeric_equal(actual[k],v,label+'/'+k,rtol,atol) for k,v in expected.items()),default=0.)
    if expected is None or isinstance(expected,(str,bool,int)):
        require(actual==expected,label+': literal value differs.');return 0.
    aa=np.asarray(actual,np.float64);bb=np.asarray(expected,np.float64)
    require(aa.shape==bb.shape and np.isfinite(aa).all() and np.isfinite(bb).all(),label+': shape/finite gate.')
    require(np.allclose(aa,bb,rtol=rtol,atol=atol),label+': independent numeric comparison failed.')
    return float(np.max(np.abs(aa-bb),initial=0.))


def results_audit():
    c,wanted=analysis_gate();m=read(VALID/'manifest.json');target_receipt=read(VALID/'independent_valid_target_audit.json')
    target_receipt_sha=sha(VALID/'independent_valid_target_audit.json')
    require(target_receipt['status']=='passed_independent_VALID_staged_target_audit' and target_receipt['audit_source_sha256']==sha(__file__),'Target audit source/status differs.')
    require(target_receipt['manifest_sha256']==sha(VALID/'manifest.json') and target_receipt['contract_sha256']==sha(VALID/'contract.json') and target_receipt['analysis_contract_sha256']==sha(ANALYSIS),'Target audit lineage differs.')
    require(target_receipt['roles']==ROLES and target_receipt['parents']==12 and target_receipt['frames']==7238 and m['roles']==ROLES and m['frames']==7238 and m['complete_release'] is True,'Target support differs.')
    require(len(m['parents'])==12 and {r['parent_id'] for r in m['parents']}==set(wanted),'Target parent allowlist differs.')
    records={p:dict(r) for p,r in wanted.items()};access=ValidAccess(records,records,wanted)
    completed=read(RESULTS/'evaluation_complete.json')
    require(completed['status']=='completed_one_VALID_development_diagnostic_pending_independent_evaluation_audit' and completed['parents']==12 and completed['subjects']==8 and completed['frames']==7238 and completed['prediction_packages_count']==60,'Incomplete diagnosis.')
    require(completed['new_neural_fits']==0 and completed['scaler_refits']==0 and completed['TEST_dynamic_reads']==0 and completed['no_selection_or_independent_generalization_claim'] is True,'Diagnosis scope differs.')
    require(completed['analysis_contract_sha256']==sha(ANALYSIS) and completed['VALID_manifest_sha256']==sha(VALID/'manifest.json') and completed['VALID_target_audit_sha256']==target_receipt_sha,'Diagnosis input lineage differs.')
    require(completed['aggregate_sha256']==sha(RESULTS/'aggregate.json') and completed['per_trial_sha256']==sha(RESULTS/'per_trial_private.json'),'Metric artifact identity differs.')
    package_rows=completed['prediction_packages'];packages={(r['parent_id'],r['mode']):r for r in package_rows}
    require(len(package_rows)==60 and len(packages)==60 and set(packages)=={(p,mode) for p in wanted for mode in MODES},'Prediction package grid differs.')
    for (parent,mode),row in packages.items():
        access.require([parent]);path=Path(row['path']).resolve()
        require(path.parent==(RESULTS/'predictions_private').resolve() and path.name==parent.replace('/','__')+'__'+mode+'.npz','Prediction archive path differs.')
    stored_rows=read(RESULTS/'per_trial_private.json');stored={(r['parent_id'],r['mode']):r for r in stored_rows}
    require(len(stored_rows)==60 and len(stored)==60 and set(stored)==set(packages),'Trial metric grid differs.')
    scalers=read(PILOT/'scalers.json');states={};torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    for w in c['five_frozen_weights']:
        mode=w['mode'];path=Path(w['path']).resolve();require(path==(PILOT/'runs'/mode/'final.pt').resolve(),'Weight path differs.')
        ck=literal_helpers.checkpoint(path,w['sha256'],c['training_contract_sha256'],c['scalers_sha256'],c['source_sha256']['models.py'],mode,50)
        states[mode]=ck['state_dict']
    independent_rows=[];prediction_error={};metric_error=0.;archives_checked=0
    for row in m['parents']:
        p=row['parent_id'];access.require([p]);require(row['split']=='VALID' and row['frames']==wanted[p]['frames'] and row['subject']==wanted[p]['subject'],'Target row metadata differs.')
        path=(VALID/row['path']).resolve();require(path.parent==VALID.resolve(),'Target path escapes VALID.')
        arrays=access.npz(path,row['sha256'],p,('x','y','sensor_target','sensor_mask','positions'),'staged_VALID_npz')
        n=wanted[p]['frames'];require(arrays['sensor_mask'].dtype==bool,'Mask dtype differs.')
        for name,ch in [('x',12),('y',6),('sensor_target',18),('sensor_mask',18),('positions',24)]:require(arrays[name].shape==(n,ch) and np.isfinite(arrays[name]).all(),'Target shape/finite gate.')
        standardized=((arrays['x'].astype(np.float64)-np.asarray(scalers['x']['mean']))/np.asarray(scalers['x']['std'])).astype(np.float32)
        x=torch.from_numpy(standardized[None])
        for mode in MODES:
            expected=independent_predictions(states[mode],mode,x,scalers);pr=packages[p,mode];archive=Path(pr['path'])
            access.checked_hash(archive,pr['sha256'],[p],'prediction_VALID_npz')
            with np.load(archive,allow_pickle=False) as z:
                require(set(z.files)==set(expected),'Prediction output names differ.');observed={key:z[key].copy() for key in z.files}
            access.checked_hash(archive,pr['sha256'],[p],'prediction_VALID_npz');archives_checked+=1
            for key,value in expected.items():
                error=numeric_equal(observed[key],value,p+'/'+mode+'/'+key,rtol=2e-6,atol=2e-5 if 'deg' in key else 2e-6)
                prediction_error[key]=max(prediction_error.get(key,0.),error)
            side=wanted[p]['affected_side'];metrics=all_metrics(expected,arrays,side,scalers,mode)
            record={'mode':mode,'parent_id':p,'subject':wanted[p]['subject'],'split':'VALID','frames':n,'affected_side':side,'metrics':metrics}
            metric_error=max(metric_error,numeric_equal(stored[p,mode],record,p+'/'+mode+'/metrics'))
            independent_rows.append(record)
    aggregates=independently_aggregate(independent_rows);aggregate_error=numeric_equal(read(RESULTS/'aggregate.json'),aggregates,'equal_person_aggregates')
    helpers_unchanged();require(target_receipt_sha==sha(VALID/'independent_valid_target_audit.json') and completed['analysis_contract_sha256']==sha(ANALYSIS),'Prerequisite changed during audit.')
    require(completed['aggregate_sha256']==sha(RESULTS/'aggregate.json') and completed['per_trial_sha256']==sha(RESULTS/'per_trial_private.json'),'Metrics changed during audit.')
    value={'status':'passed_independent_VALID_diagnostic_results_audit','date':'2026-10-25','audit_source_sha256':sha(__file__),'independent_helper_sha256':HELPER_SHA,
      'analysis_contract_sha256':sha(ANALYSIS),'manifest_sha256':sha(VALID/'manifest.json'),'VALID_target_audit_sha256':target_receipt_sha,
      'evaluation_complete_sha256':sha(RESULTS/'evaluation_complete.json'),'aggregate_sha256':sha(RESULTS/'aggregate.json'),'per_trial_sha256':sha(RESULTS/'per_trial_private.json'),
      'roles':ROLES,'parents':12,'subjects':8,'frames':7238,'prediction_packages':archives_checked,'frozen_checkpoints_opened':5,
      'prediction_max_abs_differences_by_array':prediction_error,'per_trial_metrics_max_abs_difference':metric_error,'aggregate_max_abs_difference':aggregate_error,
      'all_60_full_sequence_predictions_recomputed':True,'all_60_zero_and_shift_interventions_recomputed':True,
      'all_60_motion_and_TRAIN_mean_metrics_recomputed':True,'all_36_semantic_sensor_and_position_metric_sets_recomputed':True,
      'all_equal_person_and_available_person_counts_recomputed':True,'all_full_original_VALID_x_only_forward_inputs':True,
      'production_model_or_metric_functions_called':False,'literal_forward_source':'audit_train_pilot.py independent_forward, SHA pinned in this source',
      'mocap_or_auxiliary_GT_as_forward_inputs':False,'all_metrics_use_frozen_unique_TRAIN_scalers_without_refit':True,
      'new_neural_fits':0,'new_optimizer_steps':0,'scaler_refits':0,'TRAIN_TEST_dynamic_arrays_read':0,'TEST_dynamic_reads':0,
      'startup_secondary_omits_frames':84,'shift_is_offline_noncausal_internal_intervention':True,'same_people_new_trials_development_only':True,
      'independent_generalization_or_causal_mechanism_claim':False}
    path=RESULTS/'independent_results_audit.json';write_once(path,value)
    return {'status':value['status'],'receipt':str(path),'sha256':sha(path),'prediction_packages':archives_checked,'prediction_max_abs_differences':prediction_error,'aggregate_max_abs_difference':aggregate_error}


def synthetic_checks():
    """Only generated local arrays/layers and temporary CSV are opened."""
    helpers_unchanged();torch.set_num_threads(2);checks={}
    records={'P1/a':{'split':'VALID'},'P1/train':{'split':'TRAIN'}}
    access=ValidAccess(records,records,['P1/a'])
    for bad in ('P1/train','P99/unknown'):
        try:access.checked_hash('/does/not/exist','irrelevant',[bad],'synthetic')
        except PermissionError:pass
        else:raise AssertionError('Invalid role reached source hashing.')
    checks['TRAIN_and_unknown_rejected_before_hash']=True
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'points.csv'
        path.write_text('time,a,b\n0.000,0,10\n0.011,11,21\n0.020,20,30\n0.030,INVALID_UNSELECTED,INVALID_UNSELECTED\n')
        query=np.array([.001,.010,.019]);job={'path':str(path),'sha256':sha(path),'kind':'point_csv','owners':['P1/a'],
          'columns':['a','b'],'factor':1.,'query':{'P1/a':query},'context':{'P1/a':[0.,20.]},'offsets':{'P1/a':0.},'other_role_bounds':{'P1/a':[]}}
        q=independent_source(job,access)
        require(np.allclose(q['interpolated']['P1/a'],np.column_stack([query*1000,query*1000+10])),'Synthetic interpolation failed.')
        require(q['ids'].tolist()==[0,1,2] and q['numeric_rows_decoded']==3,'Selected-only conversion failed.')
        require(q['per_parent_support']['P1/a']['endpoint_context_before_ms']==1. and q['per_parent_support']['P1/a']['endpoint_context_limit_ms']==25.1,'Endpoint allowance differs.')
        bad=dict(job);bad['context']={'P1/a':[1.,20.]}
        try:independent_source(bad,access)
        except PermissionError:pass
        else:raise AssertionError('Episode escape accepted.')
        bad=dict(job);bad['other_role_bounds']={'P1/a':[[10.,12.]]}
        try:independent_source(bad,access)
        except PermissionError:pass
        else:raise AssertionError('Another-role selected row accepted.')
    checks['selected_rows_only_clock_and_11ms_jitter_interpolation']=True
    checks['episode_and_other_role_flanks_fail_closed']=True
    lo,hi,alpha=clock_helpers.bracket_indices(np.array([0.,10.,20.]),np.array([0.,10.,20.]),True)
    require(np.array_equal(lo,hi) and np.all(alpha==0),'Exact row provenance failed.')
    checks['exact_brackets_no_extra_neighbor']=True
    target=np.zeros((100,6));pred=np.tile(np.arange(1,7),(100,1))
    mm=motion_metrics(pred,target,'left');require(mm['six_angles']==3.5 and mm['bilateral_knee']==3.5 and mm['paretic_knee']==2.,'Motion metrics wrong.')
    require(motion_metrics(pred,target,'right',84)['paretic_knee']==5.,'Side/startup metric wrong.')
    checks['per_angle_side_and_startup_metrics']=True
    scalers={'y':{'mean':[0.]*6,'std':[1.]*6},'signals':{'mean':[0.]*18,'std':[1.]*18},'positions':{'mean':[0.]*24,'std':[1.]*24}}
    data={'y':target,'sensor_target':np.zeros((100,18)),'sensor_mask':np.ones((100,18),bool),'positions':np.zeros((100,24))}
    data['sensor_mask'][:,3:6]=False
    package={'angles_hat_deg':pred,'zero_angles_hat_deg':pred,'shift_angles_hat_deg':pred,'signals_hat_SI':np.ones((100,18)),'positions_hat_m':np.tile([.003,.004,0.],(100,8))}
    metrics=all_metrics(package,data,'left',scalers,'strict_staged')
    require(metrics['S3_ACC_RMSE']==1. and metrics['S3_GYRO_RMSE'] is None and np.isclose(metrics['position_MPJPE_mm'],5.),'Sensor mask/SI/MPJPE metrics failed.')
    checks['mask_empty_group_and_SI_MPJPE_mm']=True
    rr=[{'mode':'direct','subject':'P1','metrics':{'q':0.,'missing':None}}, {'mode':'direct','subject':'P1','metrics':{'q':2.,'missing':None}}, {'mode':'direct','subject':'P2','metrics':{'q':10.,'missing':4.}}]
    agg=independently_aggregate(rr)['direct'];require(agg['equal_person_mean']['q']==5.5 and agg['metric_people_counts']['missing']==1,'Person weighting failed.')
    checks['trial_then_equal_person_and_available_counts']=True
    generator=torch.Generator().manual_seed(991);x=torch.randn(1,100,12,generator=generator)
    for mode in MODES:
        state=literal_helpers.independent_initial(mode);out=independent_predictions(state,mode,x,scalers)
        require(out['angles_hat_deg'].shape==(100,6),'Literal full sequence shape.')
        if mode in ('direct','auxiliary_only'):require(np.array_equal(out['angles_hat_deg'],out['zero_angles_hat_deg']) and np.array_equal(out['angles_hat_deg'],out['shift_angles_hat_deg']),'Direct/aux intervention changed path.')
        prefix=literal_helpers.independent_forward(state,mode,x[:,:57])['angles_hat'];full=literal_helpers.independent_forward(state,mode,x)['angles_hat']
        require(torch.allclose(prefix,full[:,:57],rtol=2e-6,atol=2e-6),'Literal prefix not causal.')
    checks['all_five_fullseq_literal_paths_interventions_and_prefixes']=True
    try:numeric_equal({'a':1.},{'a':2.},'negative_probe')
    except AssertionError:pass
    else:raise AssertionError('Changed metric accepted.')
    checks['numeric_comparison_fail_closed']=True
    result={'status':'passed_independent_VALID_diagnostic_synthetic_checks','date':'2026-10-25','audit_source_sha256':sha(__file__),'independent_helper_sha256':HELPER_SHA,'checks':checks,
      'real_TRAIN_VALID_TEST_arrays_or_weights_read':False,'new_neural_fits':0,'optimizer_steps':0,'scaler_fits':0,'analysis_contract_or_real_targets_opened':False}
    path=ROOT/('valid_audit_synthetic_'+result['audit_source_sha256'][:12]+'.json');write_once(path,result)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('phase',choices=['synthetic','targets','results']);parser.add_argument('--experiments-root',type=Path);args=parser.parse_args()
    if args.phase=='synthetic':value=synthetic_checks()
    elif args.phase=='targets':
        if args.experiments_root is None:parser.error('targets requires --experiments-root')
        value=targets_audit(args.experiments_root)
    else:value=results_audit()
    print(json.dumps(value,allow_nan=False))


if __name__=='__main__':main()
