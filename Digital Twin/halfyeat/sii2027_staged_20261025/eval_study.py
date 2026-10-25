"""One frozen same-person VALID development diagnosis; never loads TEST.

Only predicted intermediates reach motion decoding. Target arrays are used
after inference for metrics. No model, scaler, checkpoint or weight is tuned.
"""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
import torch
from models import MODES,SEMANTIC_MODES,build_model
from train_study import sha,read,write_once,normalized,check_contract,HERE,OUT

VALID=HERE/'valid_v1'
RESULTS=OUT/'valid_diagnostic_v1'
ANALYSIS=OUT/'VALID_analysis_contract.json'
ANGLES=('left_hip','left_knee','left_ankle','right_hip','right_knee','right_ankle')
GROUPS=('S3_ACC','S3_GYRO','S4_ACC','S4_GYRO','S5_ACC','S5_GYRO')

def freeze(experiments_root):
    check_contract();done=read(OUT/'all_fits_complete.json');audit=read(OUT/'independent_training_audit.json')
    if done['fits']!=5 or done['optimizer_updates']!=2000 or done['VALID_dynamic_reads'] or done['TEST_dynamic_reads']:
        raise RuntimeError('The five fixed TRAIN fits must be complete before unlocking VALID.')
    if audit['status']!='passed_independent_TRAIN_pilot_audit' or audit['training_contract_sha256']!=sha(OUT/'training_contract.json') or audit['all_fits_complete_sha256']!=sha(OUT/'all_fits_complete.json'):
        raise RuntimeError('Independent training gate does not bind these completed fits.')
    release_path=Path(experiments_root)/'native_training_release_20261021/dataset_release.json'
    release=read(release_path);rows=sorted((r for r in release['trials'] if r['split']=='VALID'),key=lambda r:r['parent_id'])
    if len(rows)!=12 or sum(r['frames'] for r in rows)!=7238 or len({r['subject'] for r in rows})!=8:
        raise RuntimeError('Unexpected VALID support.')
    weights=[]
    for mode in MODES:
        r=read(OUT/'runs'/mode/'complete.json');p=OUT/'runs'/mode/'final.pt'
        if done['fit_completes'][mode]!=sha(OUT/'runs'/mode/'complete.json') or r['contract_sha256']!=sha(OUT/'training_contract.json'):
            raise RuntimeError('A completed fit differs from the audited TRAIN completion.')
        if r['mode']!=mode or r['epochs']!=50 or sha(p)!=r['final']['sha256']:
            raise RuntimeError('Final weights differ from the fixed training receipt.')
        weights.append({'mode':mode,'epochs':50,'path':str(p),'sha256':sha(p)})
    value={'status':'frozen_once_VALID_development_diagnostic_before_new_VALID_dynamic_read','date':'2026-10-25',
        'training_contract_sha256':sha(OUT/'training_contract.json'),'all_fits_complete_sha256':sha(OUT/'all_fits_complete.json'),
        'training_audit_sha256':sha(OUT/'independent_training_audit.json'),'scalers_sha256':sha(OUT/'scalers.json'),
        'dataset_release_metadata_path':str(release_path),'dataset_release_metadata_sha256':sha(release_path),
        'source_sha256':{n:sha(HERE/n) for n in ('eval_study.py','models.py','train_study.py','build_valid_targets.py','build_train_targets.py','audit_train_pilot.py','audit_valid_diagnostic.py')},
        'allowed_VALID_rows':[{k:r[k] for k in ('parent_id','subject','split','frames','affected_side')} for r in rows],
        'five_frozen_weights':weights,'parent_count':12,'subject_count':8,'frames':7238,
        'support':'full_original_no_crop','scope':'same_people_new_trials_development_not_LOSO_not_independent_TEST',
        'checkpoint':'fixed_final50_no_selection','scalers':'frozen_unique_TRAIN_only_no_refit',
        'inference':'one_full_parent_causal_sequence_reset_per_parent_no_future_context',
        'primary_motion_metrics':'per_parent_per_angle_RMSE_degrees_then_mean_trials_within_person_then_equal_8_people',
        'motion_summaries':{'six_angles':'mean_six_RMSEs','bilateral_knee':'mean_left_and_right_knee_RMSEs','paretic_knee':'affected_side_left_index1_or_right_index4'},
        'angle_order':list(ANGLES),'startup_secondary':'same_metrics_after_first84frames_each_parent_no_reselection',
        'sensor_metrics':'per_sensor_modality_RMSE_over_valid_xyz_elements_in_SI_then_equal_trials_within_person_then_equal_available_people',
        'sensor_groups':list(GROUPS),'sensor_units':['m/s^2','rad/s']*3,
        'position_metric':'MPJPE_mean_euclidean_error_over_8_landmarks_then_time_mm_then_equal_trials_within_person_then_equal_people',
        'constant_reference':'frozen_TRAIN_channel_mean_for_angles_signals_positions_no_additional_fit',
        'dependency_diagnostics':['replace_semantic_intermediates_by_standardized_zero_TRAIN_target_mean_or_untyped_latent_by_its_coordinate_origin','circular_shift_all_predicted_intermediates_together_by_floor_parent_length_div2'],
        'dependency_diagnostics_scope':'deliberate_internal_distribution_change_not_new_sensor_perturbation_or_causal_mechanism_proof',
        'circular_shift_is_offline_noncausal_intervention_not_a_deployable_prediction':True,
        'direct_aux_motion_path_expected_unchanged_by_intermediate_intervention':True,
        'no_oracle_intermediate_motion_inputs':True,'no_hyperparameter_or_mode_selection_from_diagnostic':True,
        'planned_statistical_tests':0,'neural_fits_in_analysis':0,'TEST_dynamic_reads':0,
        'new_validation_labels_for_diagnosis_not_independent_confirmation':True}
    write_once(ANALYSIS,value);return value

def restore(values,scaler):
    return np.asarray(values,np.float64)*np.asarray(scaler['std'])+np.asarray(scaler['mean'])

def score(yhat,y,side,offset=0):
    rmse=np.sqrt(np.mean((np.asarray(yhat[offset:],np.float64)-y[offset:])**2,axis=0))
    return {**dict(zip(ANGLES,rmse.tolist())),'six_angles':float(rmse.mean()),
            'bilateral_knee':float(rmse[[1,4]].mean()),'paretic_knee':float(rmse[1 if side=='left' else 4])}

@torch.no_grad()
def interventions(model,x,base):
    if model.mode in ('direct','auxiliary_only'):
        return {'zero':base['angles_hat'],'shift':base['angles_hat']}
    if model.mode=='latent_bottleneck':mid=base['latent_hat']
    else:mid=torch.cat((base['signals_hat'],base['positions_hat']),dim=-1)
    results={}
    for name,modified in [('zero',torch.zeros_like(mid)),('shift',torch.roll(mid,x.shape[1]//2,dims=1))]:
        inputs=torch.cat((x,modified),-1) if model.mode=='residual_staged' else modified
        results[name]=model.motion_decoder(inputs)
    return results

def aggregate(rows):
    result={}
    for mode in MODES:
        mr=[r for r in rows if r['mode']==mode];subjects=sorted({r['subject'] for r in mr});by_person={}
        for sub in subjects:
            sr=[r for r in mr if r['subject']==sub];metrics=sorted({k for r in sr for k,v in r['metrics'].items() if v is not None})
            by_person[sub]={k:float(np.mean([r['metrics'][k] for r in sr if r['metrics'].get(k) is not None])) for k in metrics}
        metrics=sorted({k for p in by_person.values() for k in p})
        result[mode]={'parents':len(mr),'people':len(subjects),
            'equal_person_mean':{k:float(np.mean([v[k] for v in by_person.values() if k in v])) for k in metrics},
            'metric_people_counts':{k:sum(k in v for v in by_person.values()) for k in metrics},'by_person':by_person}
    return result

def evaluate():
    c=read(ANALYSIS);check_contract()
    if RESULTS.exists():raise RuntimeError('Immutable diagnosis directory already exists; preserve any failure.')
    for name,want in c['source_sha256'].items():
        if sha(HERE/name)!=want:raise RuntimeError('Analysis source changed: '+name)
    if sha(OUT/'scalers.json')!=c['scalers_sha256'] or sha(OUT/'independent_training_audit.json')!=c['training_audit_sha256'] or sha(OUT/'all_fits_complete.json')!=c['all_fits_complete_sha256'] or sha(OUT/'training_contract.json')!=c['training_contract_sha256']:
        raise RuntimeError('Training prerequisites changed.')
    m=read(VALID/'manifest.json')
    if m['roles']!={'TRAIN':0,'VALID':12,'TEST':0} or m['frames']!=7238 or not m['complete_release']:
        raise PermissionError('Only complete VALID target release is allowed.')
    if m['analysis_contract_sha256']!=sha(ANALYSIS):raise RuntimeError('VALID release was not authorized by this frozen analysis.')
    target_audit=read(VALID/'independent_valid_target_audit.json')
    if target_audit['status']!='passed_independent_VALID_staged_target_audit' or target_audit['manifest_sha256']!=sha(VALID/'manifest.json') or target_audit['analysis_contract_sha256']!=sha(ANALYSIS):
        raise RuntimeError('Independent VALID target audit must pass before inference.')
    if target_audit['parents']!=12 or target_audit['frames']!=7238 or target_audit['roles']!={'TRAIN':0,'VALID':12,'TEST':0}:
        raise RuntimeError('Independent VALID target audit support differs.')
    wanted={r['parent_id']:r for r in c['allowed_VALID_rows']}
    if len(m['parents'])!=12 or {r['parent_id'] for r in m['parents']}!=set(wanted):raise PermissionError('VALID parent allowlist differs.')
    for r in m['parents']:
        if r['split']!='VALID' or r['frames']!=wanted[r['parent_id']]['frames'] or r['subject']!=wanted[r['parent_id']]['subject']:
            raise PermissionError('Wrong heldout role/support before array hashing.')
        if (VALID/r['path']).resolve().parent!=VALID.resolve():raise PermissionError('Unexpected array path.')
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    scalers=read(OUT/'scalers.json');models={}
    for w in c['five_frozen_weights']:
        if sha(w['path'])!=w['sha256']:raise RuntimeError('Frozen weight identity changed.')
        ck=torch.load(w['path'],map_location='cpu',weights_only=True)
        if ck['mode']!=w['mode'] or ck['epoch']!=50 or ck['scalers_sha256']!=c['scalers_sha256'] or ck['contract_sha256']!=c['training_contract_sha256'] or ck['model_source_sha256']!=c['source_sha256']['models.py']:
            raise RuntimeError('Unexpected model/scaler identity.')
        model=build_model(w['mode']);model.load_state_dict(ck['state_dict'],strict=True);model.eval();models[w['mode']]=model
    RESULTS.mkdir(parents=True);(RESULTS/'predictions_private').mkdir();rows=[];packages=[]
    for r in m['parents']:
        p=VALID/r['path']
        if sha(p)!=r['sha256']:raise RuntimeError('VALID array identity changed.')
        with np.load(p,allow_pickle=False) as z:
            if z['split'].item()!='VALID' or z['parent_id'].item()!=r['parent_id']:raise PermissionError('Wrong array role.')
            arrays={k:z[k].copy() for k in ('x','y','sensor_target','sensor_mask','positions')}
        if any(not np.isfinite(v).all() for v in arrays.values()):raise RuntimeError('Nonfinite VALID arrays.')
        if wanted[r['parent_id']]['affected_side'] not in ('left','right'):raise RuntimeError('Unknown affected side.')
        side=wanted[r['parent_id']]['affected_side'];x=torch.from_numpy(normalized(arrays['x'],scalers['x']))[None]
        for mode,model in models.items():
            with torch.no_grad():pred=model(x);perturbed=interventions(model,x,pred)
            numeric={k:v[0].cpu().numpy() for k,v in pred.items() if isinstance(v,torch.Tensor)}
            yhat=restore(numeric['angles_hat'],scalers['y']);metrics=score(yhat,arrays['y'],side)
            constant_angles=np.broadcast_to(scalers['y']['mean'],arrays['y'].shape)
            metrics.update({'TRAIN_mean_'+k:v for k,v in score(constant_angles,arrays['y'],side).items()})
            metrics.update({'steady_'+k:v for k,v in score(yhat,arrays['y'],side,84).items()})
            package={'angles_hat_deg':yhat}
            for name,ybad in perturbed.items():
                bad=restore(ybad[0].cpu().numpy(),scalers['y']);package[name+'_angles_hat_deg']=bad
                metrics.update({name+'_'+k:v for k,v in score(bad,arrays['y'],side).items()})
                metrics[name+'_max_prediction_change_deg']=float(np.max(np.abs(bad-yhat)))
            if mode in SEMANTIC_MODES:
                shat=restore(numeric['signals_hat'],scalers['signals']);phat=restore(numeric['positions_hat'],scalers['positions'])
                package.update(signals_hat_SI=shat,positions_hat_m=phat)
                for g,name in enumerate(GROUPS):
                    sl=slice(3*g,3*g+3);mask=arrays['sensor_mask'][:,sl]
                    metrics[name+'_RMSE']=float(np.sqrt(np.mean((shat[:,sl]-arrays['sensor_target'][:,sl])[mask]**2))) if mask.any() else None
                    constant_signal=np.broadcast_to(np.asarray(scalers['signals']['mean'])[sl],shat[:,sl].shape)
                    metrics[name+'_TRAIN_mean_RMSE']=float(np.sqrt(np.mean((constant_signal-arrays['sensor_target'][:,sl])[mask]**2))) if mask.any() else None
                error=(phat-arrays['positions']).reshape(-1,8,3)
                metrics['position_MPJPE_mm']=float(np.linalg.norm(error,axis=-1).mean()*1000.)
                constant_position=np.broadcast_to(scalers['positions']['mean'],phat.shape)
                metrics['position_TRAIN_mean_MPJPE_mm']=float(np.linalg.norm((constant_position-arrays['positions']).reshape(-1,8,3),axis=-1).mean()*1000.)
            if not all(v is None or np.isfinite(v) for v in metrics.values()):raise RuntimeError('Nonfinite diagnosis.')
            rows.append({'mode':mode,'parent_id':r['parent_id'],'subject':r['subject'],'split':'VALID','frames':r['frames'],'affected_side':side,'metrics':metrics})
            package_path=RESULTS/'predictions_private'/(r['parent_id'].replace('/','__')+'__'+mode+'.npz')
            with package_path.open('xb') as f:np.savez_compressed(f,**package)
            packages.append({'parent_id':r['parent_id'],'mode':mode,'path':str(package_path),'sha256':sha(package_path)})
    write_once(RESULTS/'per_trial_private.json',rows)
    write_once(RESULTS/'aggregate.json',aggregate(rows))
    value={'status':'completed_one_VALID_development_diagnostic_pending_independent_evaluation_audit',
        'analysis_contract_sha256':sha(ANALYSIS),'VALID_manifest_sha256':sha(VALID/'manifest.json'),
        'VALID_target_audit_sha256':sha(VALID/'independent_valid_target_audit.json'),
        'aggregate_sha256':sha(RESULTS/'aggregate.json'),'per_trial_sha256':sha(RESULTS/'per_trial_private.json'),
        'prediction_packages':packages,'parents':12,'subjects':8,'frames':7238,'prediction_packages_count':60,
        'new_neural_fits':0,'scaler_refits':0,'TEST_dynamic_reads':0,'no_selection_or_independent_generalization_claim':True}
    write_once(RESULTS/'evaluation_complete.json',value);print(json.dumps(value),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['freeze','evaluate']);p.add_argument('--experiments-root');a=p.parse_args()
    if a.phase=='freeze':print(json.dumps(freeze(a.experiments_root)))
    else:evaluate()
if __name__=='__main__':main()
