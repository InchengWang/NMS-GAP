"""Prepare immutable VALID-only targets after a separate explicit export gate.

Default development work is metadata-only or synthetic. A real export requires
the complete five-fit/audit/analysis authorization JSON. This is a development
diagnostic, not a new untouched test set. Shared native CSV hashes read all bytes;
only the selected VALID interpolation rows have signal values converted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import build_train_targets as helpers

HERE = Path(__file__).resolve().parent
VERSION = 'staged_VALID_sensor_and_rootrelative_targets_v1'
EXPECTED_PARENTS, EXPECTED_FRAMES = 12, 7238
ENDPOINT_POLICY = 'same_frozen_modality_maxgap_prefreeze_clock_metadata_amendment_v2'
MODES = ('direct', 'auxiliary_only', 'latent_bottleneck',
         'strict_staged', 'residual_staged')
METADATA = dict(helpers.METADATA,
    matching='marker_recall_20261021/matching_v2/ordered_matching_results.json',
    episodes='marker_recall_20261021/imu_episode_inventory.json')
canonical = helpers.canonical
digest_file = helpers.digest_file
digest_array = helpers.digest_array
immutable_json = helpers.immutable_json
immutable_npz = helpers.immutable_npz
parent_sort = helpers.parent_sort


def load_metadata(experiments_root):
    """Only JSON metadata; no data hash, NPZ read or raw CSV scan."""
    root = Path(experiments_root).resolve()
    paths = {k: root / rel for k, rel in METADATA.items()}
    snapshots = {k: p.read_bytes() for k, p in paths.items()}
    meta = {k: json.loads(value) for k, value in snapshots.items()}
    release = {r['parent_id']: r for r in meta['release']['trials']}
    candidates = {r['parent_id']: r for r in meta['candidates']['trials']}
    matching = {r['parent_id']: r for r in meta['matching']['rows']
                if r['accepted_identity_candidate']}
    if len(release) != 53 or set(release) != set(candidates):
        raise RuntimeError('Expected the immutable 53-parent role inventory.')
    if any(release[p]['split'] != candidates[p]['split'] for p in release):
        raise RuntimeError('Release and candidate roles disagree.')
    valid = sorted((p for p in release if release[p]['split'] == 'VALID'), key=parent_sort)
    if len(valid) != EXPECTED_PARENTS or sum(release[p]['frames'] for p in valid) != EXPECTED_FRAMES:
        raise RuntimeError('Expected all12 original VALID parents / 7238 frames, without crop.')
    folders = {str(Path(f['folder']).resolve()): f for f in meta['inventory']['source_folders']}
    sessions = {s['session_id']: s for s in meta['episodes']['sessions']}
    episodes = {e['episode_id']: e for e in meta['episodes']['episodes']}
    data = dict(root=root, metadata_paths=paths, metadata_bytes=snapshots,
                metadata=meta, release=release, candidates=candidates,
                matching=matching, valid=valid, folders=folders,
                sessions=sessions, episodes=episodes)
    for parent in valid:
        r, c, m = release[parent], candidates[parent], matching[parent]
        if m['original_split'] != 'VALID' or m['episode_id'] != c['episode_id']:
            raise RuntimeError('Frozen matching identity/role differs.')
        if m['native_epoch_offset_ms'] != c['native_epoch_offset_ms']:
            raise RuntimeError('Frozen matching offset differs; no new alignment is allowed.')
        if not np.array_equal(c['input_epoch_bounds_ms'], m['source_walk_epoch_bounds_ms']):
            raise RuntimeError('Original full walking query endpoints differ.')
        if r['frames'] != c['frames'] or abs(c['input_epoch_bounds_ms'][1] -
                c['input_epoch_bounds_ms'][0] - (r['frames'] - 1) * 10) > 1e-5:
            raise RuntimeError('Frozen frame count / 100Hz support differs.')
        ep = episodes[c['episode_id']]
        se = sessions[m['session_id']]
        runs = [z for z in se['runs'] if z['run_id'] == m['run_id']]
        if len(runs) != 1 or ep['session_id'] != m['session_id'] or ep['run_id'] != m['run_id']:
            raise RuntimeError('Original native episode/run identity differs.')
        if str(Path(se['raw_folder']).resolve()) != str(Path(m['raw_folder']).resolve()):
            raise RuntimeError('Native run and matching source folder differ.')
        bounds = own_native_context_bounds(data, parent)
        qlo, qhi = c['input_epoch_bounds_ms']
        if qlo < bounds[0] or qhi > bounds[1]:
            raise RuntimeError('Original full walking support leaves its episode/run.')
        # Source bytes are not inspected: these intervals are frozen metadata.
        for other, o in candidates.items():
            if other == parent or release[other]['split'] == 'VALID':
                continue
            if str(Path(o['native_sources'][0]['path']).resolve().parent) != str(Path(m['raw_folder']).resolve()):
                continue
            olo, ohi = o['input_epoch_bounds_ms']
            if max(qlo, olo) <= min(qhi, ohi):
                raise RuntimeError('VALID full query overlaps another role walking interval.')
    return data


def own_native_context_bounds(data, parent):
    c, m = data['candidates'][parent], data['matching'][parent]
    ep = data['episodes'][c['episode_id']]
    run = next(r for r in data['sessions'][m['session_id']]['runs'] if r['run_id'] == m['run_id'])
    return [max(ep['native_epoch_bounds_ms'][0], run['native_epoch_bounds_ms'][0]),
            min(ep['native_epoch_bounds_ms'][1], run['native_epoch_bounds_ms'][1])]


def guard_requested(data, parents):
    """Reject TRAIN/TEST/unknown before any source or authorization hash/read."""
    requested = list(data['valid'] if not parents else parents)
    if not requested or len(requested) != len(set(requested)):
        raise PermissionError('Empty or duplicate VALID request.')
    for parent in requested:
        if (parent not in data['valid'] or data['release'][parent]['split'] != 'VALID'
                or data['candidates'][parent]['split'] != 'VALID'):
            raise PermissionError(f'Only the frozen VALID allowlist is permitted: {parent}')
    return sorted(requested, key=parent_sort)


def source_plan(data):
    plans = {}
    for parent in data['valid']:
        r, c, m = data['release'][parent], data['candidates'][parent], data['matching'][parent]
        folder = str(Path(c['native_sources'][0]['path']).resolve().parent)
        if folder != str(Path(m['raw_folder']).resolve()) or folder not in data['folders']:
            raise RuntimeError('Native source folder identity is not frozen.')
        f = data['folders'][folder]
        if f['subject'] != r['subject']:
            raise RuntimeError('Native source subject differs.')
        targets = []
        for sensor in helpers.SENSORS:
            for modality in helpers.MODALITIES:
                found = [z for z in f['files'] if z['sensor'] == sensor and z['modality'] == modality]
                if len(found) > 1:
                    raise RuntimeError('Ambiguous source cannot be called missing.')
                if not found:
                    targets.append(dict(sensor=sensor, modality=modality, available=False,
                        reason='modality_file_absent_in_frozen_inventory'))
                    continue
                z = found[0]
                if any(z[k] for k in ('duplicate_timestamp_count', 'decreasing_timestamp_count', 'nonfinite_values')):
                    raise RuntimeError('Present source inventory marks an unsafe signal.')
                if z['gaps_over_25_1ms'] != 0:
                    raise RuntimeError('Present source inventory has an unsupported clock gap.')
                targets.append(dict(sensor=sensor, modality=modality, available=True,
                    path=str(Path(z['path']).resolve()), sha256=z['sha256'],
                    native_unit=z['native_unit'], output_unit=z['output_unit'],
                    inventory_epoch_bounds_ms=[z['epoch_start_ms'], z['epoch_end_ms']]))
        plans[parent] = dict(parent_id=parent, subject=r['subject'], split='VALID',
            source_npz=str(Path(r['source_npz']).resolve()), source_npz_sha256=r['source_sha256'],
            frames=r['frames'], crop=None, full_query_epoch_bounds_ms=c['input_epoch_bounds_ms'],
            point_source=str(Path(c['point_labels']).resolve()), point_source_sha256=c['point_sha256'],
            native_epoch_offset_ms=c['native_epoch_offset_ms'], episode_id=c['episode_id'],
            session_id=m['session_id'], run_id=m['run_id'],
            native_episode_and_run_context_bounds_ms=own_native_context_bounds(data, parent),
            sensor_targets=targets)
    return plans


def gate_template(data):
    return dict(status='PENDING_NOT_AUTHORIZED', permitted_dynamic_role='VALID',
        allowed_parent_ids=data['valid'], expected_frames=EXPECTED_FRAMES,
        support='full_original_no_crop', producer_code_sha256='FILL_AFTER_SOURCE_FREEZE',
        helper_code_sha256='0f2d93a450b1484cb5d4652362b2fa2caab43afa5ede07a9bae33d92f5868e4c',
        prerequisites={key: dict(path=str(HERE / rel), sha256='FILL_AFTER_PASS_AND_FREEZE')
            for key, rel in [('TRAIN_independent_target_audit','train_v1/independent_train_target_audit.json'),
                ('TRAIN_training_audit','pilot_v1/independent_training_audit.json'),
                ('VALID_analysis_contract','pilot_v1/VALID_analysis_contract.json')]},
        prerequisite_assertions={key: False for key in ('all_five_final50_fits_complete',
            'TRAIN_target_audit_passed','TRAIN_training_audit_passed',
            'VALID_analysis_contract_frozen_before_any_VALID_dynamic_read')},
        five_frozen_weights=[dict(mode=mode, epochs=50, path='FILL_TRAIN_ONLY_CHECKPOINT_PATH',
                                  sha256='FILL_AFTER_COMPLETED_FIT') for mode in MODES])


def verify_authorization(data, authorization, artifact_root=HERE):
    """Gate hashes only code/TRAIN artifacts before any VALID source operation."""
    if authorization is None:
        raise PermissionError('Real VALID export requires a separately frozen authorization JSON.')
    path = Path(authorization).resolve()
    gate_bytes = path.read_bytes()
    gate = json.loads(gate_bytes)
    if (gate.get('status') != 'authorized_once_VALID_development_diagnostic'
            or gate.get('permitted_dynamic_role') != 'VALID'
            or gate.get('allowed_parent_ids') != data['valid']
            or gate.get('expected_frames') != EXPECTED_FRAMES
            or gate.get('support') != 'full_original_no_crop'):
        raise PermissionError('VALID export authorization is incomplete or has a different support.')
    expected_assertions = set(gate_template(data)['prerequisite_assertions'])
    assertions = gate.get('prerequisite_assertions', {})
    if set(assertions) != expected_assertions or any(v is not True for v in assertions.values()):
        raise PermissionError('All five fits, TRAIN audits and pre-VALID analysis freeze must pass.')
    prereq = gate.get('prerequisites', {})
    if set(prereq) != set(gate_template(data)['prerequisites']):
        raise PermissionError('Three separately frozen prerequisite artifacts are required.')
    weights = gate.get('five_frozen_weights', [])
    if len(weights) != 5 or {w['mode'] for w in weights} != set(MODES) or any(w['epochs'] != 50 for w in weights):
        raise PermissionError('Exactly five final50 checkpoints must be frozen.')
    if len({w['path'] for w in weights}) != 5:
        raise PermissionError('Five distinct TRAIN checkpoint paths are required.')
    artifact_root = Path(artifact_root).resolve()
    artifacts = list(prereq.values()) + weights
    for item in artifacts:
        p = Path(item['path']).resolve()
        if not p.is_relative_to(artifact_root) or p.suffix.lower() in ('.csv', '.npz'):
            raise PermissionError('Gate artifacts must be local study code/TRAIN artifacts, not dynamic sources.')
        if len(item['sha256']) != 64 or any(c not in '0123456789abcdef' for c in item['sha256']):
            raise PermissionError('A prerequisite SHA is not frozen.')
    code_sha, helper_sha = digest_file(__file__), digest_file(helpers.__file__)
    if gate.get('producer_code_sha256') != code_sha or gate.get('helper_code_sha256') != helper_sha:
        raise PermissionError('VALID producer/helper source is not the separately authorized version.')
    for item in artifacts:
        if digest_file(item['path']) != item['sha256']:
            raise RuntimeError('A separately frozen prerequisite/checkpoint changed.')
    # No self-reference: the independent authorization binds the analysis contract,
    # and the generated target contract binds this authorization's SHA.
    if path.read_bytes() != gate_bytes:
        raise RuntimeError('Authorization changed while its prerequisites were checked.')
    return dict(path=str(path), sha256=hashlib.sha256(gate_bytes).hexdigest(),
                producer_sha256=code_sha, helper_sha256=helper_sha, gate=gate)


class ValidAccess:
    def __init__(self, data, requested, authorization):
        self.data, self.authorization = data, authorization
        self.requested = frozenset(guard_requested(data, requested))
        if authorization is None:
            raise PermissionError('ValidAccess requires a verified separate authorization.')
        self.events = []

    def require(self, parents, operation):
        parents = tuple(parents)
        if not parents:
            raise PermissionError('Every source access needs a VALID owner.')
        for p in parents:
            if p not in self.requested or self.data['release'][p]['split'] != 'VALID':
                raise PermissionError(f'Forbidden before {operation}: {p}')

    def checked_hash(self, path, expected, parents, kind):
        self.require(parents, 'hash_' + kind)
        actual = digest_file(path)
        self.events.append(dict(operation='mechanical_full_file_sha256', kind=kind,
            path=str(Path(path).resolve()), owners=sorted(parents), sha256=actual,
            bytes_read=Path(path).stat().st_size,
            shared_native_source_TRAIN_TEST_bytes_may_be_hashed=kind == 'native_csv'))
        if actual != expected:
            raise RuntimeError('Frozen VALID source SHA mismatch: ' + str(path))
        return actual

    def load_valid_npz(self, parent):
        self.require([parent], 'load_valid_npz')
        row, c = self.data['release'][parent], self.data['candidates'][parent]
        path = Path(row['source_npz']).resolve()
        expected = (self.data['root'] / 'marker_recall_20261021/ordered_native_candidates_v2' / c['path']).resolve()
        if path != expected or row['source_sha256'] != c['sha256']:
            raise RuntimeError('VALID source path/SHA metadata disagrees.')
        self.checked_hash(path, row['source_sha256'], [parent], 'valid_npz')
        self.require([parent], 'np_load_VALID')
        keys = ('x','y_angles','time','input_epoch_ms','optic_absolute_time')
        with np.load(path, allow_pickle=False) as z:
            if str(z['parent_id'].item()) != parent or str(z['split'].item()) != 'VALID':
                raise RuntimeError('NPZ parent/role differs from the VALID allowlist.')
            a = {k: z[k].copy() for k in keys}
        self.checked_hash(path, row['source_sha256'], [parent], 'valid_npz')
        n = row['frames']
        if a['x'].shape != (n,12) or a['y_angles'].shape != (n,6):
            raise RuntimeError('Unexpected VALID x/y shape.')
        if a['x'].dtype != np.float32 or a['y_angles'].dtype != np.float32:
            raise RuntimeError('Original float32 VALID x/y must be preserved.')
        if any(not np.isfinite(v).all() for v in a.values()):
            raise RuntimeError('Nonfinite VALID source cannot be excluded or masked.')
        for k in keys[2:]:
            if a[k].shape != (n,) or np.any(np.diff(a[k]) <= 0):
                raise RuntimeError('Invalid original VALID clock: ' + k)
        if np.max(np.abs(np.diff(a['input_epoch_ms']) - 10)) > .001:
            raise RuntimeError('Original VALID query is not the fixed 100Hz grid.')
        if np.max(np.abs(a['input_epoch_ms'] - (a['optic_absolute_time'] * 1000 + c['native_epoch_offset_ms']))) > 1e-5:
            raise RuntimeError('Original candidate clock equation differs; no alignment refit allowed.')
        if np.max(np.abs(a['input_epoch_ms'][[0,-1]] - c['input_epoch_bounds_ms'])) > 1e-5:
            raise RuntimeError('Original full VALID query endpoints differ.')
        self.events.append(dict(operation='dynamic_VALID_npz_fields_read', parent=parent,
                                fields=list(keys), frames=n, crop=None))
        return a


def stream_source(path, sha, owners, queries, *, native, columns, factor, max_gap,
                  access, inventory_bounds=None):
    owners = tuple(sorted(set(owners), key=parent_sort))
    access.require(owners, 'VALID_time_first_source_scan')
    kind = 'native_csv' if native else 'point_csv'
    access.checked_hash(path, sha, owners, kind)
    header, clock, clock_name = helpers.scan_csv_clock(path, native)
    if any(c not in header for c in columns):
        raise RuntimeError('Required explicit value column is missing.')
    if native and inventory_bounds is not None and not np.array_equal(clock[[0,-1]], inventory_bounds):
        raise RuntimeError('Native source endpoints differ from the frozen inventory.')
    brackets, support, parts = {}, {}, []
    for parent in owners:
        q = queries[parent]
        left, right, alpha = helpers.interpolation_brackets(clock, q, max_gap)
        ids = np.unique(np.r_[left,right])
        qlo, qhi = q[0], q[-1]
        scale = 1.0 if native else 1000.0
        before = float(max(0.0, qlo - clock[ids[0]]) * scale)
        after = float(max(0.0, clock[ids[-1]] - qhi) * scale)
        context_limit_ms = max_gap * scale
        if max(before, after) > context_limit_ms + 1e-4:
            raise PermissionError('A full-query endpoint flank exceeds the fixed source interpolation gap policy.')
        epoch = clock[ids].astype(np.float64) if native else clock[ids] * 1000 + access.data['candidates'][parent]['native_epoch_offset_ms']
        lo, hi = own_native_context_bounds(access.data, parent)
        if np.any(epoch < lo - 1e-5) or np.any(epoch > hi + 1e-5):
            raise PermissionError('An endpoint bracket leaves the original native episode/run.')
        own_folder = str(Path(access.data['matching'][parent]['raw_folder']).resolve())
        for other, c in access.data['candidates'].items():
            if other == parent or access.data['release'][other]['split'] == 'VALID':
                continue
            if str(Path(c['native_sources'][0]['path']).resolve().parent) != own_folder:
                continue
            olo, ohi = c['input_epoch_bounds_ms']
            if np.any((epoch >= olo - 1e-5) & (epoch <= ohi + 1e-5)):
                raise PermissionError('A VALID numeric interpolation row enters another role walking interval.')
        outer = ids[(clock[ids] < qlo) | (clock[ids] > qhi)]
        support[parent] = dict(query_frames=len(q), query_bounds=[float(qlo),float(qhi)],
            full_original_query_no_crop=True, selected_source_rows=len(ids),
            source_row_index_bounds=[int(ids[0]),int(ids[-1])],
            external_adjacent_rows_outside_full_query_interval=len(outer),
            external_adjacent_row_indices=outer.tolist(),
            external_adjacent_source_times=clock[outer].tolist(),
            endpoint_context_before_ms=before, endpoint_context_after_ms=after,
            endpoint_context_limit_ms=context_limit_ms,
            endpoint_context_policy=ENDPOINT_POLICY,
            native_episode_and_run_bounds_ms=[lo,hi],
            all_selected_rows_inside_original_native_episode_and_run=True,
            selected_rows_outside_other_roles_walking_intervals=True)
        brackets[parent] = (left,right,alpha)
        parts.extend((left,right))
    selected = np.unique(np.concatenate(parts))
    access.require(owners, 'decode_SELECTED_VALID_bracket_values')
    values, token_sha = helpers.read_selected_values(path, header, clock, clock_name,
        selected, columns, factor, native)
    access.checked_hash(path, sha, owners, kind)
    output = {}
    for parent,(left,right,alpha) in brackets.items():
        li,ri = np.searchsorted(selected,left),np.searchsorted(selected,right)
        value = values[li] + alpha[:,None] * (values[ri]-values[li])
        if not np.isfinite(value).all():
            raise RuntimeError('Nonfinite VALID interpolation is fatal.')
        output[parent] = dict(values=value,left=left,right=right,alpha=alpha)
    within = np.zeros(len(selected),bool)
    for q in queries.values():
        within |= (clock[selected] >= q[0]) & (clock[selected] <= q[-1])
    row_sha = hashlib.sha256()
    row_sha.update(np.asarray(selected,dtype='<i8').tobytes())
    row_sha.update(np.asarray(clock[selected],dtype='<i8' if native else '<f8').tobytes())
    row_sha.update(np.asarray(values,dtype='<f8').tobytes())
    receipt = dict(path=str(Path(path).resolve()),sha256=sha,kind=kind,role='VALID',
        owners=list(owners), all_rows_clock_metadata_scanned=len(clock),
        all_rows_read_as_CSV_text_each_pass=True, numeric_value_rows_decoded=len(selected),
        numeric_value_columns_decoded=list(columns), numeric_value_cells_decoded=int(values.size),
        source_row_indices_zero_based_after_header=selected.tolist(),
        selected_rows_text_tokens_sha256=token_sha,
        selected_rows_indices_clock_and_SI_values_sha256=row_sha.hexdigest(),
        selected_rows_hash_encoding='indices<i8 + clock<i8(native)or<f8(point) + values<f8; C order',
        factor_to_output_units=factor,
        external_adjacent_unique_rows_outside_all_full_query_intervals=int((~within).sum()),
        source_full_file_hash_before_and_after=True,
        shared_native_full_file_bytes_can_include_TRAIN_TEST_intervals=native,
        unselected_numeric_signal_values_converted=False, per_parent_support=support)
    access.events.append(dict(operation='VALID_time_first_selected_numeric_decode',kind=kind,
        path=str(Path(path).resolve()),owners=list(owners),all_clock_metadata_rows=len(clock),
        selected_numeric_rows=len(selected),unselected_numeric_signal_values_converted=False))
    return output,receipt


def make_contract(data, plans, authorization):
    metadata_sha = {k:hashlib.sha256(v).hexdigest() for k,v in data['metadata_bytes'].items()}
    if any(digest_file(data['metadata_paths'][k]) != v for k,v in metadata_sha.items()):
        raise RuntimeError('Metadata changed after the original VALID role validation.')
    return dict(version=VERSION,date='2026-10-25',
        producer_code_sha256=authorization['producer_sha256'],helper_code_sha256=authorization['helper_sha256'],
        authorization_sha256=authorization['sha256'],authorization=authorization['gate'],
        analysis_contract_sha256=authorization['gate']['prerequisites']['VALID_analysis_contract']['sha256'],
        metadata_sha256=metadata_sha, permitted_dynamic_role='VALID',
        development_diagnostic_only=True, complete_release_parent_count=EXPECTED_PARENTS,
        complete_release_frames=EXPECTED_FRAMES, crop=None, fixed_query_rate_hz=100.0,
        query_policy='exact_original_input_epoch_ms_and_optic_absolute_time_no_new_lag_axis_search',
        sensor_target_order=[f'{s}_{m}_{a}' for s in helpers.SENSORS for m in ('acc','gyro') for a in 'xyz'],
        sensor_target_frame='each_measured_sensor_native_xyz',sensor_target_units='ACC_m/s^2_GYRO_rad/s',
        native_ACC_g_factor=9.80665,native_GYRO_deg_s_factor=float(np.pi/180),
        missing_targets='zero_storage_fill_false_mask_only_for_frozen_inventory_absence',
        present_source_failure='fatal_no_mask_no_crop_no_trial_exclusion',
        position_names=list(helpers.POINT_NAMES),position_units='meters',
        position_definition='(float64_interpolated_point_xyz_mm-bilateral_hip_midpoint_mm)/1000_then_float32',
        position_frame='legacy_candidate_pelvis_axes_joint_landmark_proxy_not_JCS_or_IMU_centers',
        final_angle_target='unchanged_full_original_y_angles_float32',
        model_input_keys=['x'],auxiliary_target_keys=['sensor_target','sensor_mask','positions'],
        final_target_keys=['y'],clock_and_row_arrays_are_audit_metadata_not_model_inputs=True,
        native_max_interpolation_gap_ms=helpers.MAX_NATIVE_GAP_MS,
        point_max_interpolation_gap_s=helpers.MAX_POINT_GAP_S,
        endpoint_context_rule=dict(policy=ENDPOINT_POLICY,
            native_limit_each_end_ms=helpers.MAX_NATIVE_GAP_MS,
            point_limit_each_end_s=helpers.MAX_POINT_GAP_S,
            point_limit_each_end_ms=helpers.MAX_POINT_GAP_S * 1000,
            limits_equal_preexisting_source_interpolation_gap_policy=True,
            amendment_basis='preexisting_native_timestamp_jitter_metadata_not_VALID_errors_or_performance',
            minimal_adjacent_interpolation_rows_only=True,
            original_native_episode_and_run_containment_required=True,
            other_role_walking_interval_entry_forbidden=True,
            explicitly_not_a_claim_that_flanks_are_inside_exact_walking_query=True),
        source_read_policy=dict(shared_native_full_bytes_hashed_before_after=True,
            TRAIN_TEST_bytes_may_be_mechanically_hashed=True,all_rows_read_as_strings=True,
            all_clock_metadata_parsed=True,only_selected_VALID_bracket_values_converted=True),
        no_new_lag_axis_bias_filter_fit=True,scaler_fits=0,neural_fits=0,
        TRAIN_TEST_dynamic_arrays_read=0,untouched_TEST_source_byte_claim=False,
        VALID_parents_and_sources=[plans[p] for p in data['valid']])


def build_release(experiments_root, output_dir, parents=None, authorization=None, *, artifact_root=HERE):
    data = load_metadata(experiments_root)
    requested = guard_requested(data, parents)  # precedes all hashes / dynamic source access
    auth = verify_authorization(data,authorization,artifact_root)
    access = ValidAccess(data,requested,auth)
    plans = source_plan(data)
    contract = make_contract(data,plans,auth)
    cb = (json.dumps(contract,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    contract_sha = hashlib.sha256(cb).hexdigest()
    output = Path(output_dir).resolve()
    helpers.immutable_bytes(output/'contract.json',cb)
    arrays = {p:access.load_valid_npz(p) for p in requested}
    jobs = {}
    for parent in requested:
        for target in plans[parent]['sensor_targets']:
            if target['available']:
                job = jobs.setdefault(target['path'],dict(source=target,owners=[]))
                if job['source'] != target:
                    raise RuntimeError('One native path has inconsistent source metadata.')
                job['owners'].append(parent)
    native_values,receipts = {},[]
    for path,job in sorted(jobs.items()):
        z = job['source']; acc = z['modality']=='Accelerometer'
        unit,factor = ('g',9.80665) if acc else ('deg/s',float(np.pi/180))
        value,receipt = stream_source(path,z['sha256'],job['owners'],
            {p:arrays[p]['input_epoch_ms'] for p in job['owners']},native=True,
            columns=[f'{a}-axis ({unit})' for a in 'xyz'],factor=factor,
            max_gap=helpers.MAX_NATIVE_GAP_MS,access=access,
            inventory_bounds=z['inventory_epoch_bounds_ms'])
        native_values[path] = value;receipts.append(receipt)
    rows = []
    for parent in requested:
        plan,a = plans[parent],arrays[parent];n=plan['frames']
        target=np.zeros((n,18),np.float32);mask=np.zeros((n,18),bool)
        left=np.full((n,6),-1,np.int64);right=left.copy();alpha=np.zeros((n,6),np.float64)
        for j,z in enumerate(plan['sensor_targets']):
            if z['available']:
                v=native_values[z['path']][parent]
                target[:,j*3:j*3+3]=v['values'].astype(np.float32);mask[:,j*3:j*3+3]=True
                left[:,j],right[:,j],alpha[:,j]=v['left'],v['right'],v['alpha']
        point,pr=stream_source(plan['point_source'],plan['point_source_sha256'],[parent],
            {parent:a['optic_absolute_time']},native=False,columns=helpers.POINT_COLUMNS,
            factor=1.0,max_gap=helpers.MAX_POINT_GAP_S,access=access)
        receipts.append(pr);p=point[parent];mm=p['values'].reshape(n,8,3)
        root=(mm[:,0]+mm[:,4])/2
        positions=((mm-root[:,None])/1000).reshape(n,24).astype(np.float32)
        if not np.isfinite(positions).all():
            raise RuntimeError('Nonfinite root-relative VALID target.')
        provenance=dict(version=VERSION,parent_id=parent,split='VALID',contract_sha256=contract_sha,
            producer_code_sha256=auth['producer_sha256'],helper_code_sha256=auth['helper_sha256'],
            authorization_sha256=auth['sha256'],source_npz_sha256=plan['source_npz_sha256'],
            source_point_sha256=plan['point_source_sha256'],sensor_sources=plan['sensor_targets'],
            point_source_receipt=pr,crop=None,
            extra_sensor_and_point_supervision_are_not_deployment_inputs=True)
        out=dict(x=a['x'].copy(),y=a['y_angles'].copy(),sensor_target=target,sensor_mask=mask,
            positions=positions,time=a['time'].copy(),input_epoch_ms=a['input_epoch_ms'].copy(),
            optic_absolute_time=a['optic_absolute_time'].copy(),source_frame_indices=np.arange(n,dtype=np.int64),
            sensor_source_left_indices=left,sensor_source_right_indices=right,sensor_interp_alpha=alpha,
            point_source_left_indices=p['left'],point_source_right_indices=p['right'],point_interp_alpha=p['alpha'],
            subject=np.asarray(plan['subject']),parent_id=np.asarray(parent),split=np.asarray('VALID'),
            contract_sha256=np.asarray(contract_sha),provenance_json=np.asarray(canonical(provenance)))
        access.require([parent],'persist_or_validate_VALID_output')
        filename=parent.replace('/','__')+'_staged_VALID.npz';path=output/filename
        immutable_npz(path,out)
        available={f'{s["sensor"]}_{s["modality"]}':bool(s['available']) for s in plan['sensor_targets']}
        rows.append(dict(parent_id=parent,subject=plan['subject'],split='VALID',path=filename,
            sha256=digest_file(path),frames=n,crop=None,sample_seconds=n/100,
            sample_timestamp_span_seconds=(n-1)/100,sensor_modality_availability=available,
            sensor_modality_supervised_sample_seconds={k:n/100 if v else 0.0 for k,v in available.items()},
            sensor_supervised_channel_frames=int(mask.sum()),sensor_total_storage_channel_frames=int(mask.size),
            point_target_sample_seconds=n/100,source_npz_sha256=plan['source_npz_sha256'],
            array_sha256={k:digest_array(v) for k,v in out.items() if np.asarray(v).ndim>0}))
    full=requested==data['valid']
    if full and (len(rows)!=EXPECTED_PARENTS or sum(r['frames'] for r in rows)!=EXPECTED_FRAMES):
        raise RuntimeError('A complete VALID release must preserve all12 parents / 7238 frames.')
    # Recheck the independently authorized source and prerequisite identities.
    if verify_authorization(data,authorization,artifact_root)!=auth:
        raise RuntimeError('Authorization/source state changed during export.')
    manifest=dict(status='complete_VALID_only_staged_targets_built_pending_independent_audit' if full else
        'partial_VALID_only_staged_targets_built_not_complete_release',version=VERSION,date='2026-10-25',
        complete_release=full,contract_sha256=contract_sha,producer_code_sha256=auth['producer_sha256'],
        helper_code_sha256=auth['helper_sha256'],authorization_sha256=auth['sha256'],
        analysis_contract_sha256=auth['gate']['prerequisites']['VALID_analysis_contract']['sha256'],
        requested_VALID_parents=requested,roles=dict(TRAIN=0,VALID=len(rows),TEST=0),
        frames=sum(r['frames'] for r in rows),crop=None,
        unique_target_sample_seconds=sum(r['frames'] for r in rows)/100,
        unique_native_source_files=len(jobs),
        native_numeric_rows_decoded=sum(r['numeric_value_rows_decoded'] for r in receipts if r['kind']=='native_csv'),
        point_numeric_rows_decoded=sum(r['numeric_value_rows_decoded'] for r in receipts if r['kind']=='point_csv'),
        external_adjacent_native_rows_outside_full_queries=sum(r['external_adjacent_unique_rows_outside_all_full_query_intervals'] for r in receipts if r['kind']=='native_csv'),
        external_adjacent_point_rows_outside_full_queries=sum(r['external_adjacent_unique_rows_outside_all_full_query_intervals'] for r in receipts if r['kind']=='point_csv'),
        all_full_queries_preserved_without_crop=True,endpoint_context_policy=ENDPOINT_POLICY,
        native_endpoint_context_limit_each_end_ms=helpers.MAX_NATIVE_GAP_MS,
        point_endpoint_context_limit_each_end_s=helpers.MAX_POINT_GAP_S,
        point_endpoint_context_limit_each_end_ms=helpers.MAX_POINT_GAP_S * 1000,
        all_selected_rows_inside_original_native_episode_and_run=True,
        selected_numeric_rows_outside_other_roles_walking_intervals=True,
        shared_native_source_full_bytes_mechanically_hashed=True,TRAIN_TEST_source_bytes_may_be_hashed=True,
        unselected_numeric_signal_values_converted=False,TRAIN_TEST_dynamic_arrays_read=0,
        scaler_fits=0,model_fits=0,diagnostic_ready_before_independent_audit=False,
        development_only_not_patient_excluded_generalization=True,
        parents=rows,source_value_read_receipts=receipts)
    selection=hashlib.sha256(canonical(requested).encode()).hexdigest()[:16]
    name='manifest.json' if full else f'partial_manifest_{selection}.json'
    immutable_json(output/name,manifest)
    run=dict(version=VERSION,permitted_dynamic_role='VALID',requested_parents=requested,
        complete_release_invocation=full,contract_sha256=contract_sha,authorization_sha256=auth['sha256'],
        manifest_name=name,manifest_sha256=digest_file(output/name),access_events=access.events,
        no_claim_of_zero_TRAIN_TEST_source_byte_reads=True)
    rid=hashlib.sha256(canonical(run).encode()).hexdigest()[:20]
    immutable_json(output/'run_receipts'/f'run_{rid}.json',run)
    return dict(status=manifest['status'],output=str(output),manifest=name,
        manifest_sha256=digest_file(output/name),contract_sha256=contract_sha,
        parents=len(rows),frames=manifest['frames'],new_fits=0)


def metadata_check(experiments_root):
    data=load_metadata(experiments_root);plans=source_plan(data)
    parents=[]
    for p in data['valid']:
        plan=plans[p];lo,hi=plan['full_query_epoch_bounds_ms'];elo,ehi=plan['native_episode_and_run_context_bounds_ms']
        parents.append(dict(parent_id=p,frames=plan['frames'],full_query_epoch_bounds_ms=[lo,hi],
            episode_and_run_margin_before_ms=lo-elo,episode_and_run_margin_after_ms=ehi-hi,
            modality_availability={f'{z["sensor"]}_{z["modality"]}':z['available'] for z in plan['sensor_targets']}))
    return dict(status='VALID_metadata_only_preflight_complete_not_dynamic_authorization',
        roles=dict(TRAIN=0,VALID=EXPECTED_PARENTS,TEST=0),frames=EXPECTED_FRAMES,crop=None,
        metadata_sha256={k:hashlib.sha256(v).hexdigest() for k,v in data['metadata_bytes'].items()},
        real_dynamic_arrays_read=0,shared_raw_CSV_files_hashed=0,raw_signal_numeric_values_read=0,
        query_clocks_read_from_npz=False,endpoint_numeric_support_verified=False,
        metadata_endpoint_support_is_not_a_numeric_bracket_audit=True,
        pending_numerical_gates=['all_original_NPZ_clocks_x_y_SHA_and_shape_match',
            'every_present_source_SHA_clock_brackets_gap_and_finite_values_match',
            'each_endpoint_context_le_corresponding_frozen_maxgap_and_inside_own_original_episode_run',
            'all_selected_numeric_rows_outside_other_roles_walking_intervals',
            'point_mm_to_m_bilateral_hip_center_and_mask_independent_audit'],
        endpoint_context_policy=ENDPOINT_POLICY,
        native_endpoint_context_limit_each_end_ms=helpers.MAX_NATIVE_GAP_MS,
        point_endpoint_context_limit_each_end_s=helpers.MAX_POINT_GAP_S,
        context_policy_basis='preexisting_timestamp_jitter_metadata_before_any_VALID_dynamic_read',
        parents=parents)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiments-root',type=Path)
    parser.add_argument('--output-dir',type=Path,default=HERE/'valid_v1')
    parser.add_argument('--authorization',type=Path)
    parser.add_argument('--parent',action='append',help='Only a frozen VALID parent, repeatable.')
    parser.add_argument('--synthetic-test',action='store_true')
    parser.add_argument('--metadata-check',action='store_true')
    args=parser.parse_args()
    if args.synthetic_test:
        import test_build_valid_targets
        print(json.dumps(test_build_valid_targets.run_tests(),ensure_ascii=False));return
    if args.experiments_root is None:
        parser.error('--experiments-root is required')
    if args.metadata_check:
        report=metadata_check(args.experiments_root)
        immutable_json(HERE/'valid_metadata_preflight_v2.json',report)
        immutable_json(HERE/'valid_export_authorization.template.json',gate_template(load_metadata(args.experiments_root)))
        print(json.dumps(report,ensure_ascii=False));return
    print(json.dumps(build_release(args.experiments_root,args.output_dir,args.parent,args.authorization),ensure_ascii=False))


if __name__=='__main__':
    main()
