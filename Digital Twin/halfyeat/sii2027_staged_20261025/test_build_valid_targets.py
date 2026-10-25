"""Synthetic-only preflight for the separately gated VALID target producer."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

import numpy as np
import build_valid_targets as v
import build_train_targets as b
from test_build_train_targets import expect_error, fixture_metadata, stamp, write_csv

HERE=Path(__file__).resolve().parent


def fixture(root):
    e,_,_,_,relative=fixture_metadata(root)
    meta={k:json.loads((e/rel).read_text()) for k,rel in b.METADATA.items()}
    first='P1/valid31';base=datetime(2024,1,1,9)
    base_ms=b.native_timestamp_parser('timestamp (+0900)')(stamp(base,0))
    native_folder=Path(meta['inventory']['source_folders'][0]['folder'])
    files=[]
    for j,(sensor,modality) in enumerate((s,m) for s in b.SENSORS for m in b.MODALITIES):
        if sensor=='S5' and modality=='Gyroscope':continue
        unit='g' if modality=='Accelerometer' else 'deg/s'
        path=native_folder/f'{sensor}_valid_synthetic_{modality}.csv'
        rows=[]
        for i in range(-1,702):
            t=i/100
            values=[repr(j+1+t*(a+1)) for a in range(3)] if 0<=i<=600 else ['FORBIDDEN_TOKEN']*3
            rows.append([stamp(base,i*10),*values])
        write_csv(path,['timestamp (+0900)',*[f'{a}-axis ({unit})' for a in 'xyz']],rows)
        files.append(dict(sensor=sensor,modality=modality,path=str(path),sha256=b.digest_file(path),
            native_unit=unit,output_unit='m/s^2' if modality=='Accelerometer' else 'rad/s',
            duplicate_timestamp_count=0,decreasing_timestamp_count=0,nonfinite_values=0,
            gaps_over_25_1ms=0,epoch_start_ms=base_ms-10,epoch_end_ms=base_ms+7010))
    meta['inventory']['source_folders'][0]['files']=files
    point=root/'valid_points.csv'
    relative_mm=relative*1000
    rows=[]
    for i in range(841):
        t=i/120
        value=(relative_mm+np.array([200+100*t,-70+30*t,1000])).reshape(-1)
        tokens=[repr(float(x)) for x in value] if i<=719 else ['FORBIDDEN_POSITION_TOKEN']*24
        rows.append([repr(t),*tokens])
    write_csv(point,['time',*b.POINT_COLUMNS],rows)
    point_sha=b.digest_file(point)
    matching=[];episodes=[];valid_i=0
    for r,c in zip(meta['release']['trials'],meta['candidates']['trials']):
        parent=r['parent_id'];valid=r['split']=='VALID'
        if valid:
            n=638 if valid_i==11 else 600;valid_i+=1
            r['frames']=c['frames']=n
            bounds=[base_ms+.25,base_ms+(n-1)*10+.25]
        else:
            bounds=[base_ms-200000,base_ms-100000]
        c.update(input_epoch_bounds_ms=bounds,episode_id=parent+'__episode',
            point_labels=str(point),point_sha256=point_sha)
        if parent==first:
            n=r['frames'];q=np.arange(n)/100+.00025
            x=(np.arange(n*12).reshape(n,12)/1000).astype(np.float32)
            y=(np.arange(n*6).reshape(n,6)/100).astype(np.float32)
            source=Path(r['source_npz']);source.parent.mkdir(parents=True,exist_ok=True)
            np.savez_compressed(source,x=x,y_angles=y,time=np.arange(n)/100,
                input_epoch_ms=q*1000+base_ms,optic_absolute_time=q,parent_id=parent,split='VALID')
            r['source_sha256']=c['sha256']=b.digest_file(source)
        matching.append(dict(parent_id=parent,accepted_identity_candidate=True,
            original_split=r['split'],episode_id=c['episode_id'],native_epoch_offset_ms=base_ms,
            source_walk_epoch_bounds_ms=bounds,session_id='P1__synthetic',run_id=0,
            raw_folder=str(native_folder)))
        episodes.append(dict(episode_id=c['episode_id'],session_id='P1__synthetic',run_id=0,
            native_epoch_bounds_ms=[base_ms-10000,base_ms+20000]))
    meta['matching']=dict(rows=matching)
    meta['episodes']=dict(episodes=episodes,sessions=[dict(session_id='P1__synthetic',
        raw_folder=str(native_folder),runs=[dict(run_id=0,native_epoch_bounds_ms=[base_ms-10000,base_ms+20000])])])
    for k,rel in v.METADATA.items():
        path=e/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(meta[k])+'\n')
    data=v.load_metadata(e)
    gate=v.gate_template(data)
    gate.update(status='authorized_once_VALID_development_diagnostic',
        producer_code_sha256=v.digest_file(v.__file__),helper_code_sha256=v.digest_file(b.__file__))
    gate['prerequisite_assertions']={k:True for k in gate['prerequisite_assertions']}
    for k in gate['prerequisites']:
        path=root/'allowed_artifacts'/(k+'.json');path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(dict(status='passed_synthetic_fixture_only',prerequisite=k))+'\n')
        gate['prerequisites'][k]=dict(path=str(path),sha256=v.digest_file(path))
    for item in gate['five_frozen_weights']:
        path=root/'allowed_artifacts'/(item['mode']+'.pt')
        path.write_bytes(('synthetic_only_'+item['mode']).encode())
        item.update(path=str(path),sha256=v.digest_file(path))
    auth=root/'authorization.json';auth.write_text(json.dumps(gate)+'\n')
    return e,first,auth,x,y,relative,base_ms


def run_tests():
    checks={}
    with tempfile.TemporaryDirectory(prefix='staged_valid_synthetic_') as tmp:
        root=Path(tmp);e,parent,auth,x,y,relative,base_ms=fixture(root)
        data=v.load_metadata(e)
        report=v.metadata_check(e)
        assert report['frames']==7238 and report['roles']==dict(TRAIN=0,VALID=12,TEST=0)
        assert report['real_dynamic_arrays_read']==report['shared_raw_CSV_files_hashed']==0
        checks['metadata_preflight_does_not_authorize_dynamic_values']=True
        with patch.object(v,'digest_file',side_effect=AssertionError('HASH_BEFORE_GUARD')),\
             patch.object(v.np,'load',side_effect=AssertionError('NP_LOAD_BEFORE_GUARD')):
            for wrong in ('P1/train00','P1/test43','P99/unknown'):
                out=root/('bad_'+wrong.replace('/','_'))
                expect_error(PermissionError,v.build_release,e,out,[wrong],auth,artifact_root=root)
                assert not out.exists()
            expect_error(PermissionError,v.build_release,e,root/'no_auth',[parent],None,artifact_root=root)
        checks['TRAIN_TEST_unknown_and_missing_authorization_block_before_hash_or_np_load']=True
        template=root/'template.json';template.write_text(json.dumps(v.gate_template(data)))
        with patch.object(v,'digest_file',side_effect=AssertionError('HASH_WITHOUT_GATE')):
            expect_error(PermissionError,v.verify_authorization,data,template,root)
            for change in ('assertion','frames','weights'):
                gate=json.loads(auth.read_text())
                if change=='assertion':gate['prerequisite_assertions']['TRAIN_training_audit_passed']=False
                elif change=='frames':gate['expected_frames']=7237
                else:gate['five_frozen_weights']=gate['five_frozen_weights'][:-1]
                bad=root/f'gate_{change}.json';bad.write_text(json.dumps(gate))
                expect_error(PermissionError,v.verify_authorization,data,bad,root)
        checks['pending_gate_or_incomplete_fits_audits_analysis_cannot_hash_sources']=True
        gate=json.loads(auth.read_text());gate['prerequisites']['TRAIN_training_audit']['path']=str(root/'signals.csv')
        bad=root/'bad_artifact_path.json';bad.write_text(json.dumps(gate))
        with patch.object(v,'digest_file',side_effect=AssertionError('HASH_BAD_ARTIFACT')):
            expect_error(PermissionError,v.verify_authorization,data,bad,root)
        checks['gate_cannot_hash_a_CSV_or_dynamic_NPZ_as_prerequisite']=True
        verification=v.verify_authorization(data,auth,root)
        assert verification['sha256']==hashlib.sha256(auth.read_bytes()).hexdigest()
        checks['separate_authorization_binds_code_three_prerequisites_and_five_weights']=True
        gate=json.loads(auth.read_text());gate['five_frozen_weights'][0]['sha256']='0'*64
        bad=root/'changed_weight.json';bad.write_text(json.dumps(gate))
        expect_error(RuntimeError,v.verify_authorization,data,bad,root)
        checks['frozen_prerequisite_or_checkpoint_hash_mismatch_is_fatal']=True
        out=root/'valid_v1'
        result=v.build_release(e,out,[parent],auth,artifact_root=root)
        assert result['parents']==1 and result['frames']==600
        assert not (out/'manifest.json').exists()
        manifest=json.loads((out/result['manifest']).read_text());row=manifest['parents'][0]
        assert manifest['roles']==dict(TRAIN=0,VALID=1,TEST=0) and not manifest['complete_release']
        contract=json.loads((out/'contract.json').read_text())
        analysis_sha=json.loads(auth.read_text())['prerequisites']['VALID_analysis_contract']['sha256']
        assert contract['analysis_contract_sha256']==manifest['analysis_contract_sha256']==analysis_sha
        checks['manifest_and_contract_explicitly_bind_same_analysis_contract_sha256']=True
        target=out/row['path']
        with np.load(target,allow_pickle=False) as z:
            assert str(z['split'].item())=='VALID'
            assert np.array_equal(z['x'],x) and np.array_equal(z['y'],y)
            assert np.array_equal(z['source_frame_indices'],np.arange(600))
            assert np.allclose(z['positions'].reshape(600,8,3),relative[None],atol=1e-7)
            assert np.allclose(z['sensor_target'][:,0],(1+z['optic_absolute_time'])*9.80665,atol=1e-5)
            assert z['sensor_mask'][:,:15].all() and not z['sensor_mask'][:,15:].any()
            assert not z['sensor_target'][:,15:].any()
            assert (z['sensor_source_left_indices'][:,5]==-1).all()
            assert (z['sensor_source_right_indices'][:,5]==-1).all()
        checks['VALID_full_no_crop_x_y_queries_indices_and_position_proxy_are_preserved']=True
        checks['missing_modality_zero_fill_has_false_mask_and_minus_one_indices']=True
        checks['time_first_streaming_does_not_decode_poisoned_unselected_signal_or_point_tokens']=True
        for receipt in manifest['source_value_read_receipts']:
            assert receipt['role']=='VALID' and receipt['owners']==[parent]
            support=receipt['per_parent_support'][parent]
            assert support['full_original_query_no_crop']
            assert support['external_adjacent_rows_outside_full_query_interval']==2
            assert max(support['endpoint_context_before_ms'],support['endpoint_context_after_ms'])<=support['endpoint_context_limit_ms']+.0001
            assert support['endpoint_context_limit_ms']==25.1
            assert support['endpoint_context_policy']==v.ENDPOINT_POLICY
            assert support['all_selected_rows_inside_original_native_episode_and_run']
        checks['external_full_query_endpoint_brackets_are_explicit_and_le_frozen_maxgap']=True
        old_sha=v.digest_file(target)
        assert v.build_release(e,out,[parent],auth,artifact_root=root)==result
        assert v.digest_file(target)==old_sha
        checks['identical_rerun_is_immutable_and_subset_cannot_claim_full12_release']=True
        access=v.ValidAccess(data,[parent],verification)
        plan=v.source_plan(data)[parent];source=plan['sensor_targets'][0]
        columns=[f'{a}-axis (g)' for a in 'xyz']
        queries={parent:base_ms+np.array([.25,5990.25])}
        kwargs=dict(native=True,columns=columns,factor=9.80665,max_gap=25.1,access=access,
            inventory_bounds=source['inventory_epoch_bounds_ms'])
        ep=data['episodes'][plan['episode_id']];saved=ep['native_epoch_bounds_ms'][:]
        ep['native_epoch_bounds_ms'][1]=base_ms+5991
        expect_error(PermissionError,v.stream_source,source['path'],source['sha256'],[parent],queries,**kwargs)
        ep['native_epoch_bounds_ms']=saved
        checks['flanks_outside_original_native_episode_or_run_are_rejected']=True
        other=data['candidates']['P1/train00'];saved=other['input_epoch_bounds_ms'][:]
        other['input_epoch_bounds_ms']=[base_ms-1,base_ms]
        expect_error(PermissionError,v.stream_source,source['path'],source['sha256'],[parent],queries,**kwargs)
        other['input_epoch_bounds_ms']=saved
        checks['flanks_entering_another_role_walking_interval_are_rejected']=True
        short=root/'known_11ms_timestamp_jitter.csv';base=datetime(2024,1,1,9)
        write_csv(short,['timestamp (+0900)',*columns],[[stamp(base,0),1,2,3],
            [stamp(base,11),2,3,4],[stamp(base,22),3,4,5]])
        _,jitter_receipt=v.stream_source(short,v.digest_file(short),[parent],
            {parent:base_ms+np.array([.25,11.25])},native=True,columns=columns,factor=9.80665,
            max_gap=25.1,access=access)
        jitter_support=jitter_receipt['per_parent_support'][parent]
        assert jitter_support['endpoint_context_after_ms']==10.75
        assert jitter_support['endpoint_context_limit_ms']==25.1
        badgap=root/'over_frozen_maxgap.csv'
        write_csv(badgap,['timestamp (+0900)',*columns],[[stamp(base,0),1,2,3],[stamp(base,30),2,3,4]])
        expect_error(ValueError,v.stream_source,badgap,v.digest_file(badgap),[parent],
            {parent:base_ms+np.array([.25,11.25])},native=True,columns=columns,factor=9.80665,
            max_gap=25.1,access=access)
        checks['prefreeze_metadata_known_11ms_jitter_allowed_and_over_frozen_maxgap_rejected']=True
        expect_error(RuntimeError,v.stream_source,source['path'],'0'*64,[parent],queries,**kwargs)
        checks['present_source_failure_does_not_create_a_new_mask_or_exclusion']=True
        with np.load(target,allow_pickle=False) as z:corrupt={k:z[k].copy() for k in z.files}
        corrupt['x'][0,0]+=1
        with target.open('wb') as f:np.savez_compressed(f,**corrupt)
        bad_sha=v.digest_file(target)
        expect_error(RuntimeError,v.build_release,e,out,[parent],auth,artifact_root=root)
        assert v.digest_file(target)==bad_sha
        checks['existing_conflicting_output_is_fatal_and_never_overwritten']=True
    result=dict(status='passed_synthetic_only_VALID_target_preflight',date='2026-10-25',
        scope='synthetic guards separate authorization endpoint context SI interpolation proxy masks immutability',
        checks=checks,checks_passed=len(checks),source_sha256={
            'build_valid_targets.py':v.digest_file(v.__file__),
            'build_train_targets.py':v.digest_file(b.__file__),
            'test_build_valid_targets.py':v.digest_file(__file__)},
        real_experiment_metadata_opened=False,real_TRAIN_VALID_TEST_arrays_read=False,
        real_raw_signal_values_read=False,real_shared_raw_CSV_files_hashed=0,
        new_real_exports=0,model_fits=0,numerical_real_VALID_endpoint_gate_passed=False)
    b.immutable_json(HERE/'valid_synthetic_preflight_v3.json',result)
    return result


if __name__=='__main__':
    print(json.dumps(run_tests(),ensure_ascii=False))
