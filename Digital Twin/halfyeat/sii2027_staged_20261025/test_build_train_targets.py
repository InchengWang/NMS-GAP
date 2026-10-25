"""Synthetic-only guards, selected-row interpolation and immutable-artifact checks.

No real experiment metadata or patient data is opened by this test module.
"""
from __future__ import annotations
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

import numpy as np
import build_train_targets as b

HERE = Path(__file__).resolve().parent


def expect_error(cls, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except cls:
        return
    raise AssertionError(f'Expected {cls.__name__} from {function.__name__}')


def write_csv(path, header, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def stamp(base, milliseconds):
    return (base + timedelta(milliseconds=milliseconds)).strftime('%Y-%m-%dT%H.%M.%S.%f')


def minimal_access(parent='P1/train0'):
    data = {'train': [parent], 'release': {parent: {'split': 'TRAIN'}},
            'candidates': {parent: {'split': 'TRAIN'}}}
    return b.TrainAccess(data, [parent])


def fixture_metadata(root):
    """31-TRAIN metadata fixture, with one materialized parent for subset export."""
    e = root / 'experiments'
    native_folder = root / 'native' / 'P1' / 'cane walking'
    native_folder.mkdir(parents=True)
    base = datetime(2024, 1, 1, 9, 0, 0)
    base_ms = b.native_timestamp_parser('timestamp (+0900)')(stamp(base, 0))
    inventory_files = []
    for j, (sensor, modality) in enumerate((s, m) for s in b.SENSORS for m in b.MODALITIES):
        if sensor == 'S5' and modality == 'Gyroscope':
            continue
        unit = 'g' if modality == 'Accelerometer' else 'deg/s'
        path = native_folder / f'{sensor}_synthetic_{modality}.csv'
        header = ['timestamp (+0900)'] + [f'{a}-axis ({unit})' for a in 'xyz']
        rows = []
        for i in range(601):
            # Only rows100..500 are brackets of the crop query. Other signal
            # tokens are deliberately unparseable, proving time-first scope.
            values = [str(j + 1 + (i / 100) * (axis + 1)) for axis in range(3)]
            if not 100 <= i <= 500:
                values = ['FORBIDDEN_VALUE_TOKEN'] * 3
            rows.append([stamp(base, i * 10), *values])
        write_csv(path, header, rows)
        inventory_files.append({'sensor': sensor, 'modality': modality, 'path': str(path),
                                'sha256': b.digest_file(path), 'native_unit': unit,
                                'output_unit': 'm/s^2' if modality == 'Accelerometer' else 'rad/s',
                                'duplicate_timestamp_count': 0, 'decreasing_timestamp_count': 0,
                                'nonfinite_values': 0})
    point = root / 'points.csv'
    relative = np.array([[-100, 0, 0], [-100, 0, -400], [-100, 0, -800], [-100, 150, -800],
                         [100, 0, 0], [100, 0, -400], [100, 0, -800], [100, 150, -800]], float)
    rows = []
    for i in range(721):
        t = i / 120
        v = (relative + np.array([200 + 100 * t, -70 + 30 * t, 1000])).reshape(-1)
        values = [repr(float(z)) for z in v]
        if not 120 <= i <= 599:
            values = ['FORBIDDEN_POSITION_TOKEN'] * 24
        rows.append([repr(t), *values])
    write_csv(point, ['time', *b.POINT_COLUMNS], rows)
    point_sha = b.digest_file(point)
    release_rows, candidate_rows = [], []
    first_parent = 'P1/train00'
    input_expected = target_expected = None
    for i in range(53):
        role = 'TRAIN' if i < 31 else 'VALID' if i < 43 else 'TEST'
        parent = f'P1/{role.lower()}{i:02}'
        frames = 600 if i != 30 else 865
        filename = parent.replace('/', '__') + '_ordered_native_SI.npz'
        source = e / 'marker_recall_20261021/ordered_native_candidates_v2' / filename
        sha = '0' * 64
        if i == 0:
            source.parent.mkdir(parents=True, exist_ok=True)
            q = np.arange(frames) / 100 + .00025
            epoch = q * 1000 + base_ms
            x = (np.arange(frames * 12).reshape(frames, 12) / 1000).astype(np.float32)
            y = (np.arange(frames * 6).reshape(frames, 6) / 100).astype(np.float32)
            np.savez_compressed(source, x=x, y_angles=y, time=np.arange(frames)/100,
                                input_epoch_ms=epoch, optic_absolute_time=q,
                                parent_id=parent, split='TRAIN')
            sha = b.digest_file(source)
            input_expected, target_expected = x[100:-100], y[100:-100]
        release_rows.append({'parent_id': parent, 'subject': 'P1', 'split': role,
                             'frames': frames, 'source_npz': str(source), 'source_sha256': sha})
        candidate_rows.append({'parent_id': parent, 'subject': 'P1', 'split': role,
                               'frames': frames, 'path': filename, 'sha256': sha,
                               'input_epoch_bounds_ms': [base_ms+.25, base_ms+(frames-1)*10+.25],
                               'native_epoch_offset_ms': base_ms, 'point_labels': str(point),
                               'point_sha256': point_sha,
                               'native_sources': [{'path': str(native_folder/'S1_reference.csv')} ]})
    metadata = {'release': {'trials': release_rows}, 'candidates': {'trials': candidate_rows},
                'inventory': {'source_folders': [{'folder': str(native_folder), 'subject': 'P1',
                                                  'files': inventory_files}]}}
    for k, rel in b.METADATA.items():
        p = e / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(metadata[k]) + '\n')
    return e, first_parent, input_expected, target_expected, relative / 1000


def run_tests():
    checks = {}
    parser = b.native_timestamp_parser('timestamp (+0900)')
    expected = int(datetime(2024, 3, 16, 2, 45, 45, 944000,
                            tzinfo=timezone.utc).timestamp() * 1000)
    assert parser('2024-03-16T11.45.45.944') == expected
    assert (b.native_timestamp_parser('timestamp (-0900)')('2024-03-16T11.45.45.944')
            - expected) == 18 * 3600 * 1000
    expect_error(ValueError, b.native_timestamp_parser, 'timestamp')
    checks['explicit_timezone_and_units_clock_parser'] = True
    left, right, alpha = b.interpolation_brackets(np.array([100,110,120,130]),
                                                 np.array([105.,110.,125.]),25.1)
    assert np.array_equal(left,[0,1,2]) and np.array_equal(right,[1,1,3])
    assert np.array_equal(alpha,[.5,0,.5])
    checks['exact_and_between_sample_brackets'] = True
    for clock,q,gap in [(np.array([0,10]),np.array([-1.]),25.1),
                        (np.array([0,10]),np.array([11.]),25.1),
                        (np.array([0,10,100]),np.array([50.]),25.1),
                        (np.array([0,0,10]),np.array([5.]),25.1),
                        (np.array([0,10]),np.array([5.,5.]),25.1)]:
        expect_error(ValueError,b.interpolation_brackets,clock,q,gap)
    checks['no_extrapolation_large_gap_or_duplicate_clocks'] = True
    with tempfile.TemporaryDirectory(prefix='staged_train_synthetic_') as tmp:
        root = Path(tmp)
        path = root/'simple_native.csv'
        base = datetime(2024,1,1,9)
        initial = parser(stamp(base,0))
        rows = []
        for i in range(10):
            values = [str(2*i),str(-i),str(i/10)] if 2<=i<=5 else ['POISON']*3
            rows.append([stamp(base,i*10),*values])
        header=['timestamp (+0900)','x-axis (g)','y-axis (g)','z-axis (g)']
        write_csv(path,header,rows)
        access=minimal_access();owner='P1/train0';q=initial+np.array([25.,35.,45.])
        values,receipt=b.stream_source(path,b.digest_file(path),[owner],{owner:q},
                                      {owner:np.array([initial+10,initial+70])},native=True,
                                      columns=header[1:],factor=9.80665,max_gap=25.1,access=access)
        actual=values[owner]['values'];expected_values=np.array([[5,-2.5,.25],[7,-3.5,.35],[9,-4.5,.45]])*9.80665
        assert np.allclose(actual,expected_values,rtol=0,atol=1e-14)
        assert receipt['numeric_value_rows_decoded']==4
        assert receipt['source_row_indices_zero_based_after_header']==[2,3,4,5]
        assert receipt['external_adjacent_unique_rows_outside_all_cropped_query_intervals']==2
        assert len(access.events)==3
        checks['streaming_decodes_only_allowed_bracket_values_and_SI_conversion']=True
        checks['external_interpolation_flanks_counted_and_retained']=True
        expect_error(PermissionError,b.stream_source,path,b.digest_file(path),[owner],{owner:q},
                     {owner:np.array([initial+25,initial+45])},native=True,
                     columns=header[1:],factor=1,max_gap=25.1,access=access)
        checks['brackets_cannot_escape_owning_full_TRAIN_support']=True
        expect_error(RuntimeError,b.stream_source,path,'f'*64,[owner],{owner:q},
                     {owner:np.array([initial+10,initial+70])},native=True,
                     columns=header[1:],factor=1,max_gap=25.1,access=access)
        checks['frozen_source_hash_mismatch_is_fatal']=True
        f=root/'immutable.npz';arrays={'x':np.zeros((2,12),np.float32),'parent_id':np.asarray(owner)}
        b.immutable_npz(f,arrays);old=b.digest_file(f);b.immutable_npz(f,arrays)
        changed={'x':np.ones((2,12),np.float32),'parent_id':np.asarray(owner)}
        expect_error(RuntimeError,b.immutable_npz,f,changed);assert b.digest_file(f)==old
        j=root/'immutable.json';b.immutable_json(j,{'v':1});expect_error(RuntimeError,b.immutable_json,j,{'v':2})
        checks['immutable_artifact_mismatch_never_overwrites']=True
        e,parent,x_expected,y_expected,pos_expected=fixture_metadata(root/'fixture')
        denied='P1/valid31'
        calls=[]
        with patch.object(b,'digest_file',side_effect=lambda *args: calls.append(args) or 'forbidden'),\
             patch.object(b.np,'load',side_effect=AssertionError('Forbidden dynamic load')):
            expect_error(PermissionError,b.build_release,e,root/'denied',[denied])
            expect_error(PermissionError,b.build_release,e,root/'denied',['P1/test43'])
            expect_error(PermissionError,b.build_release,e,root/'denied',['P1/unknown'])
        assert calls==[] and not (root/'denied').exists()
        checks['VALID_TEST_unknown_blocked_before_any_source_hash_or_npz_load']=True
        result=b.build_release(e,root/'out',[parent]);assert result['parents']==1 and result['frames']==400
        assert result['manifest'].startswith('partial_manifest_') and not (root/'out/manifest.json').exists()
        manifest=b.read_json(root/'out'/result['manifest']);assert not manifest['complete_release']
        p=root/'out'/manifest['parents'][0]['path'];output_sha=b.digest_file(p)
        with np.load(p,allow_pickle=False) as z:
            assert np.array_equal(z['x'],x_expected) and np.array_equal(z['y'],y_expected)
            assert z['positions'].shape==(400,24)
            assert np.max(np.abs(z['positions'].reshape(400,8,3)-pos_expected))<1e-7
            assert z['sensor_target'].shape==(400,18) and z['sensor_mask'].dtype==np.bool_
            assert z['sensor_mask'][:,:15].all() and not z['sensor_mask'][:,15:].any()
            assert np.array_equal(z['sensor_target'][:,15:],np.zeros((400,3),np.float32))
            assert np.all(z['sensor_source_left_indices'][:,5]==-1)
            assert z['contract_sha256'].item()==result['contract_sha256']
            qq=z['optic_absolute_time'];expected_acc=(1+qq)*9.80665
            assert np.max(np.abs(z['sensor_target'][:,0]-expected_acc))<2e-6
        checks['subset_end_to_end_preserves_x_y_and_masks_missing_modality']=True
        checks['point_time_first_interpolation_root_center_and_meters']=True
        checks['subset_cannot_claim_complete_31_parent_release']=True
        rerun=b.build_release(e,root/'out',[parent])
        assert rerun==result and b.digest_file(p)==output_sha
        checks['identical_subset_rerun_validates_without_overwriting']=True
        with np.load(p,allow_pickle=False) as z:corrupt={k:z[k].copy() for k in z.files}
        corrupt['x'][0,0]+=1;np.savez_compressed(p,**corrupt);corrupt_sha=b.digest_file(p)
        expect_error(RuntimeError,b.build_release,e,root/'out',[parent])
        assert b.digest_file(p)==corrupt_sha
        checks['existing_output_corruption_is_fatal_not_data_exclusion']=True
    receipt={'status':'passed_synthetic_only_TRAIN_target_producer_preflight','date':'2026-10-25',
             'checks':checks,'checks_passed':len(checks),
             'real_experiment_metadata_opened':False,'real_TRAIN_VALID_TEST_arrays_read':False,
             'raw_patient_signal_values_read':False,'new_real_exports':0,'model_fits':0,
             'scope':'synthetic guards, clocks, selected-row SI interpolation, point centering, masks and immutability',
             'complete_real_release_independent_audit_passed':False,
             'source_sha256':{n:b.digest_file(HERE/n) for n in ['build_train_targets.py','test_build_train_targets.py']}}
    b.immutable_json(HERE/'synthetic_preflight.json',receipt)
    return {'status':receipt['status'],'checks_passed':len(checks),'new_real_exports':0,
            'source_sha256':receipt['source_sha256']}


if __name__=='__main__':print(json.dumps(run_tests()))
