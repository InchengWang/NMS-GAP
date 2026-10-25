"""Build immutable TRAIN-only dense-sensor and root-relative point targets.

Only fixed Stroke53 TRAIN parents and their [100:-100] support are permitted.
Native CSV files are shared across roles: full-file hashes mechanically read
all bytes, and clock scans read every row as text. Numeric signal values are
decoded only for the permitted TRAIN interpolation brackets. This is not a
claim that held-out source bytes were never read. No scaler/model is fitted.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

import numpy as np

HERE = Path(__file__).resolve().parent
VERSION = 'staged_TRAIN_sensor_and_rootrelative_targets_v1'
CROP = 100
RATE = 100.0
MAX_NATIVE_GAP_MS = 25.1
MAX_POINT_GAP_S = 0.0251
SENSORS = ('S3', 'S4', 'S5')
MODALITIES = ('Accelerometer', 'Gyroscope')
POINT_NAMES = ('left_hip', 'left_knee', 'left_ankle', 'left_foot',
               'right_hip', 'right_knee', 'right_ankle', 'right_foot')
POINT_COLUMNS = tuple(f'all_lower_joint_gt_{p}_pelvis_{a}_mm'
                      for p in POINT_NAMES for a in 'xyz')
METADATA = {
    'release': 'native_training_release_20261021/dataset_release.json',
    'candidates': 'marker_recall_20261021/ordered_native_candidates_v2/manifest.json',
    'inventory': 'raw_source_rebuild_20261021/raw_source_manifest.json',
}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      allow_nan=False, separators=(',', ':'))


def digest_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def digest_array(a):
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(canonical({'dtype': a.dtype.str, 'shape': list(a.shape)}).encode())
    h.update(a.tobytes())
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def immutable_bytes(path, content):
    """Create atomically without overwrite; a conflicting existing file is fatal."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != content:
            raise RuntimeError(f'Immutable artifact differs: {path}')
        return
    fd, tmp = tempfile.mkstemp(prefix='.pending-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        try:
            os.link(tmp, path)
        except FileExistsError:
            if path.read_bytes() != content:
                raise RuntimeError(f'Concurrent immutable artifact differs: {path}')
    finally:
        Path(tmp).unlink(missing_ok=True)


def immutable_json(path, value):
    immutable_bytes(path, (json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     indent=2, allow_nan=False) + '\n').encode())


def immutable_npz(path, arrays):
    """Existing outputs are compared numerically/structurally, never overwritten."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    def check_existing():
        try:
            with np.load(path, allow_pickle=False) as old:
                if set(old.files) != set(arrays):
                    raise RuntimeError(f'Immutable NPZ keys differ: {path}')
                for key, value in arrays.items():
                    a, b = old[key], np.asarray(value)
                    if a.dtype != b.dtype or a.shape != b.shape or not np.array_equal(a, b):
                        raise RuntimeError(f'Immutable NPZ mismatch: {path}, key={key}')
        except RuntimeError:
            raise
        except Exception as error:
            raise RuntimeError(f'Cannot validate existing immutable NPZ: {path}') from error

    if path.exists():
        check_existing()
        return
    fd, tmp = tempfile.mkstemp(prefix='.pending-', suffix='.npz', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            np.savez_compressed(f, **arrays)
            f.flush()
            os.fsync(f.fileno())
        try:
            os.link(tmp, path)
        except FileExistsError:
            check_existing()
    finally:
        Path(tmp).unlink(missing_ok=True)


def parent_sort(parent):
    sub, _ = parent.split('/', 1)
    return int(sub[1:]), parent


def load_metadata(experiments_root):
    e = Path(experiments_root).resolve()
    paths = {k: e / rel for k, rel in METADATA.items()}
    metadata_bytes = {k: p.read_bytes() for k, p in paths.items()}
    meta = {k: json.loads(b) for k, b in metadata_bytes.items()}
    release = {r['parent_id']: r for r in meta['release']['trials']}
    candidates = {r['parent_id']: r for r in meta['candidates']['trials']}
    if len(release) != 53 or set(release) != set(candidates):
        raise RuntimeError('Expected identical immutable 53-parent metadata inventories.')
    if any(release[p]['split'] != candidates[p]['split'] for p in release):
        raise RuntimeError('Role disagreement between accepted metadata inventories.')
    train = sorted((p for p in release if release[p]['split'] == 'TRAIN'), key=parent_sort)
    if len(train) != 31 or sum(release[p]['frames'] - 2 * CROP for p in train) != 12665:
        raise RuntimeError('TRAIN cohort or fixed-crop support differs from the declared release.')
    folders = {str(Path(f['folder']).resolve()): f for f in meta['inventory']['source_folders']}
    return {'root': e, 'metadata_paths': paths, 'metadata_bytes': metadata_bytes,
            'metadata': meta, 'release': release,
            'candidates': candidates, 'train': train, 'folders': folders}


def guard_requested(data, parents):
    """Must precede all requested-parent hashes, NPZ loading or source decoding."""
    requested = list(data['train'] if not parents else parents)
    if not requested or len(requested) != len(set(requested)):
        raise PermissionError('Empty or duplicate parent request.')
    for p in requested:
        r = data['release'].get(p)
        c = data['candidates'].get(p)
        if r is None or c is None or r['split'] != 'TRAIN' or c['split'] != 'TRAIN':
            raise PermissionError(f'Only declared TRAIN parents are permitted: {p}')
        if p not in data['train']:
            raise PermissionError(f'Parent is not in the fixed TRAIN allowlist: {p}')
    return sorted(requested, key=parent_sort)


class TrainAccess:
    def __init__(self, data, requested):
        self.data = data
        self.requested = frozenset(guard_requested(data, requested))
        self.events = []

    def require(self, parents, operation):
        parents = tuple(parents)
        if not parents:
            raise PermissionError('Every source access needs at least one TRAIN owner.')
        for p in parents:
            if p not in self.requested or self.data['release'][p]['split'] != 'TRAIN':
                raise PermissionError(f'Forbidden before {operation}: {p}')

    def checked_hash(self, path, expected, parents, kind):
        self.require(parents, f'hash_{kind}')
        actual = digest_file(path)
        self.events.append({'operation': 'mechanical_full_file_sha256', 'kind': kind,
                            'path': str(Path(path).resolve()), 'owners': sorted(parents),
                            'sha256': actual, 'bytes_read': Path(path).stat().st_size,
                            'shared_source_heldout_bytes_may_be_hashed': kind == 'native_csv'})
        if actual != expected:
            raise RuntimeError(f'Frozen source SHA mismatch: {path}')
        return actual

    def load_train_npz(self, parent):
        self.require([parent], 'load_train_npz')
        row, candidate = self.data['release'][parent], self.data['candidates'][parent]
        p = Path(row['source_npz']).resolve()
        expected_path = (self.data['root'] / 'marker_recall_20261021/ordered_native_candidates_v2'
                         / candidate['path']).resolve()
        if p != expected_path or row['source_sha256'] != candidate['sha256']:
            raise RuntimeError('TRAIN source path/SHA metadata disagreement.')
        self.checked_hash(p, row['source_sha256'], [parent], 'train_npz')
        self.require([parent], 'np_load')
        with np.load(p, allow_pickle=False) as z:
            if str(z['parent_id'].item()) != parent or str(z['split'].item()) != 'TRAIN':
                raise RuntimeError('NPZ parent/role differs from its declared identity.')
            keys = ('x', 'y_angles', 'time', 'input_epoch_ms', 'optic_absolute_time')
            result = {k: z[k].copy() for k in keys}
        self.checked_hash(p, row['source_sha256'], [parent], 'train_npz')
        n = row['frames']
        if result['x'].shape != (n, 12) or result['y_angles'].shape != (n, 6):
            raise RuntimeError('Unexpected TRAIN x/y layout.')
        if result['x'].dtype != np.float32 or result['y_angles'].dtype != np.float32:
            raise RuntimeError('Preserve the accepted float32 x/y values.')
        if n <= 2 * CROP or any(not np.isfinite(v).all() for v in result.values()):
            raise RuntimeError('Invalid TRAIN sample support.')
        for key in ('time', 'input_epoch_ms', 'optic_absolute_time'):
            if result[key].shape != (n,) or np.any(np.diff(result[key]) <= 0):
                raise RuntimeError(f'Invalid TRAIN clock {key}.')
        if np.max(np.abs(np.diff(result['input_epoch_ms']) - 10.0)) > 0.001:
            raise RuntimeError('Expected the fixed 100 Hz native query grid.')
        if np.max(np.abs(result['input_epoch_ms'] -
                         (result['optic_absolute_time'] * 1000 + candidate['native_epoch_offset_ms']))) > 1e-5:
            raise RuntimeError('Frozen optical/native clock equation differs.')
        if np.max(np.abs(result['input_epoch_ms'][[0, -1]] -
                         np.asarray(candidate['input_epoch_bounds_ms']))) > 1e-5:
            raise RuntimeError('Frozen native query endpoints differ.')
        self.events.append({'operation': 'dynamic_TRAIN_npz_fields_read', 'parent': parent,
                            'fields': list(keys), 'full_TRAIN_frames_read': n,
                            'cropped_frames_kept': n - 2 * CROP})
        return result


def native_timestamp_parser(header):
    match = re.search(r'\(([+-])(\d{2})(\d{2})\)', header)
    if match is None:
        raise ValueError('Native timestamp needs an explicit timezone.')
    shift = (1 if match[1] == '+' else -1) * (int(match[2]) * 60 + int(match[3])) * 60000
    epoch = datetime(1970, 1, 1)

    def parse(value):
        # Vendor form YYYY-MM-DDTHH.MM.SS.fff; no signal fields are inspected.
        if len(value) < 19 or value[10] != 'T' or value[13] != '.' or value[16] != '.':
            raise ValueError('Unexpected native timestamp encoding.')
        normalized = value[:13] + ':' + value[14:16] + ':' + value[17:]
        dt = datetime.fromisoformat(normalized)
        if dt.tzinfo is not None:
            raise ValueError('Timestamp value must use the explicit header timezone only.')
        delta = dt - epoch
        return delta.days * 86400000 + delta.seconds * 1000 + delta.microseconds // 1000 - shift
    return parse


def interpolation_brackets(clock, query, max_gap):
    t, q = np.asarray(clock), np.asarray(query, np.float64)
    if t.ndim != 1 or len(t) < 2 or q.ndim != 1 or not len(q):
        raise ValueError('Need nonempty one-dimensional clocks.')
    if not np.isfinite(t).all() or not np.isfinite(q).all() or np.any(np.diff(t) <= 0) or np.any(np.diff(q) <= 0):
        raise ValueError('Clocks must be finite and strictly increasing.')
    if q[0] < t[0] or q[-1] > t[-1]:
        raise ValueError('No interpolation extrapolation.')
    right = np.minimum(np.searchsorted(t, q, side='left'), len(t) - 1)
    left = np.maximum(right - 1, 0)
    # No irrelevant preceding row is decoded for an exact native sample.
    exact = t[right] == q
    left[exact] = right[exact]
    span = t[right] - t[left]
    if np.any((~exact) & (span > max_gap)):
        raise ValueError('Requested interpolation bracket exceeds the fixed gap limit.')
    alpha = np.divide(q - t[left], span, out=np.zeros(len(q), np.float64), where=span != 0)
    if np.any(alpha < -1e-10) or np.any(alpha > 1 + 1e-10):
        raise ValueError('Invalid interpolation weights.')
    return left.astype(np.int64), right.astype(np.int64), alpha


def scan_csv_clock(path, native):
    """Read all rows as text, but convert only timestamp/time metadata."""
    times = []
    with Path(path).open(newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = [v.strip() for v in next(reader)]
        if len(header) != len(set(header)):
            raise ValueError('CSV header contains duplicate column names.')
        if native:
            names = [v for v in header if v.startswith('timestamp')]
            if len(names) != 1:
                raise ValueError('Exactly one native timestamp column is required.')
            clock_name = names[0]
            parse = native_timestamp_parser(clock_name)
        else:
            clock_name, parse = 'time', float
        if clock_name not in header:
            raise ValueError('Required explicit source clock missing.')
        index = header.index(clock_name)
        for row in reader:
            if len(row) != len(header):
                raise ValueError('Malformed CSV row cannot be silently dropped.')
            times.append(parse(row[index]))
    time = np.asarray(times, np.int64 if native else np.float64)
    if len(time) < 2 or not np.isfinite(time).all() or np.any(np.diff(time) <= 0):
        raise ValueError('Full source clock metadata is not monotonic and finite.')
    return header, time, clock_name


def read_selected_values(path, expected_header, clock, clock_name, selected,
                         columns, factor, native):
    """Second pass: only selected numeric signal/position fields are converted."""
    selected = np.asarray(selected, np.int64)
    if len(selected) == 0 or np.any(np.diff(selected) <= 0):
        raise ValueError('Selected row set must be nonempty, unique and sorted.')
    parse = native_timestamp_parser(clock_name) if native else float
    values = np.empty((len(selected), len(columns)), np.float64)
    token_digest = hashlib.sha256()
    cursor = 0
    with Path(path).open(newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = [v.strip() for v in next(reader)]
        if header != expected_header:
            raise RuntimeError('CSV header changed between metadata and value passes.')
        indices = [header.index(c) for c in columns]
        ti = header.index(clock_name)
        total = 0
        for row_index, row in enumerate(reader):
            total += 1
            if len(row) != len(header):
                raise RuntimeError('CSV row width changed between passes.')
            if cursor >= len(selected) or row_index != int(selected[cursor]):
                continue
            if parse(row[ti]) != clock[row_index]:
                raise RuntimeError('Selected clock changed between passes.')
            decoded = np.asarray([float(row[i]) for i in indices], np.float64) * factor
            if not np.isfinite(decoded).all():
                raise ValueError('Nonfinite selected values cannot be hidden with a mask.')
            values[cursor] = decoded
            token_digest.update((canonical([row_index, row[ti], [row[i] for i in indices]]) + '\n').encode())
            cursor += 1
    if total != len(clock) or cursor != len(selected):
        raise RuntimeError('CSV row count or selected rows changed between passes.')
    return values, token_digest.hexdigest()


def stream_source(path, expected_sha, owners, queries, full_bounds, *, native,
                  columns, factor, max_gap, access):
    owners = tuple(sorted(set(owners), key=parent_sort))
    access.require(owners, 'stream_source')
    kind = 'native_csv' if native else 'point_csv'
    access.checked_hash(path, expected_sha, owners, kind)
    header, clock, clock_name = scan_csv_clock(path, native)
    if any(c not in header for c in columns):
        raise ValueError(f'Missing explicitly named {kind} value columns.')
    brackets = {}
    selected_parts = []
    for parent in owners:
        left, right, alpha = interpolation_brackets(clock, queries[parent], max_gap)
        selected_parts.extend((left, right))
        lo, hi = full_bounds[parent]
        tol = 1e-5 if native else 1e-9
        if np.any(clock[left] < lo - tol) or np.any(clock[right] > hi + tol):
            raise PermissionError('An interpolation flank escapes its owning full TRAIN parent.')
        brackets[parent] = (left, right, alpha)
    selected = np.unique(np.concatenate(selected_parts))
    access.require(owners, 'decode_selected_value_rows')
    values, token_sha = read_selected_values(path, header, clock, clock_name,
                                             selected, columns, factor, native)
    access.checked_hash(path, expected_sha, owners, kind)
    output, support = {}, {}
    for parent, (left, right, alpha) in brackets.items():
        li, ri = np.searchsorted(selected, left), np.searchsorted(selected, right)
        interp = values[li] + alpha[:, None] * (values[ri] - values[li])
        if not np.isfinite(interp).all():
            raise ValueError('Invalid interpolated source values.')
        output[parent] = {'values': interp, 'left': left, 'right': right, 'alpha': alpha,
                          'left_time': clock[left], 'right_time': clock[right]}
        ids = np.unique(np.r_[left, right])
        q = queries[parent]
        outer = ids[(clock[ids] < q[0]) | (clock[ids] > q[-1])]
        support[parent] = {'query_frames': len(q), 'query_bounds': [float(q[0]), float(q[-1])],
                           'selected_source_rows': int(len(ids)),
                           'source_row_index_bounds': [int(ids[0]), int(ids[-1])],
                           'external_adjacent_rows_outside_cropped_query_interval': int(len(outer)),
                           'external_adjacent_row_indices': outer.tolist(),
                           'selected_brackets_inside_owning_full_TRAIN_support': True}
    in_any_query_interval = np.zeros(len(selected), bool)
    for q in queries.values():
        in_any_query_interval |= (clock[selected] >= q[0]) & (clock[selected] <= q[-1])
    row_sha = hashlib.sha256()
    row_sha.update(np.asarray(selected, dtype='<i8').tobytes())
    row_sha.update(np.asarray(clock[selected], dtype='<i8' if native else '<f8').tobytes())
    row_sha.update(np.asarray(values, dtype='<f8').tobytes())
    receipt = {'path': str(Path(path).resolve()), 'sha256': expected_sha, 'kind': kind,
               'owners': list(owners), 'all_rows_clock_metadata_scanned': len(clock),
               'all_rows_read_as_CSV_text_each_pass': True,
               'numeric_value_rows_decoded': len(selected), 'numeric_value_columns_decoded': list(columns),
               'numeric_value_cells_decoded': int(values.size),
               'source_row_indices_zero_based_after_header': selected.tolist(),
               'selected_rows_text_tokens_sha256': token_sha,
               'selected_rows_indices_clock_and_SI_values_sha256': row_sha.hexdigest(),
               'selected_rows_hash_encoding': 'indices<i8 + clock<i8(native)or<f8(point) + values<f8; C order',
               'factor_to_output_units': factor,
               'external_adjacent_unique_rows_outside_all_cropped_query_intervals': int((~in_any_query_interval).sum()),
               'source_full_file_hash_before_and_after': True,
               'full_source_bytes_include_heldout_intervals_possible': native,
               'all_selected_brackets_within_owning_full_TRAIN_support': True,
               'per_parent_support': support}
    access.events.append({'operation': 'time_first_numeric_source_decode', 'kind': kind,
                          'path': str(Path(path).resolve()), 'owners': list(owners),
                          'all_clock_metadata_rows': len(clock),
                          'selected_numeric_rows': len(selected),
                          'selected_numeric_columns': list(columns),
                          'unselected_signal_values_converted': False})
    return output, receipt


def source_plan(data, all_train):
    """Plan all TRAIN sources using metadata only, without hashing data files."""
    result = {}
    for parent in all_train:
        r, c = data['release'][parent], data['candidates'][parent]
        folder = str(Path(c['native_sources'][0]['path']).resolve().parent)
        if folder not in data['folders']:
            raise RuntimeError('Accepted native folder absent from inventory.')
        f = data['folders'][folder]
        if f['subject'] != r['subject']:
            raise RuntimeError('Native folder subject differs.')
        targets = []
        for sid in SENSORS:
            for modality in MODALITIES:
                found = [z for z in f['files'] if z['sensor'] == sid and z['modality'] == modality]
                if len(found) > 1:
                    raise RuntimeError('Ambiguous sensor source is not a missing modality.')
                if not found:
                    targets.append({'sensor': sid, 'modality': modality, 'available': False,
                                    'reason': 'modality_file_absent_in_frozen_inventory'})
                    continue
                z = found[0]
                if any(z[k] for k in ('duplicate_timestamp_count', 'decreasing_timestamp_count', 'nonfinite_values')):
                    raise RuntimeError('Inventory marks a present target source unsafe.')
                targets.append({'sensor': sid, 'modality': modality, 'available': True,
                                'path': str(Path(z['path']).resolve()), 'sha256': z['sha256'],
                                'native_unit': z['native_unit'], 'output_unit': z['output_unit']})
        result[parent] = {'parent_id': parent, 'subject': r['subject'], 'split': 'TRAIN',
                          'source_npz': str(Path(r['source_npz']).resolve()),
                          'source_npz_sha256': r['source_sha256'], 'original_frames': r['frames'],
                          'cropped_frames': r['frames'] - 2 * CROP,
                          'point_source': str(Path(c['point_labels']).resolve()),
                          'point_source_sha256': c['point_sha256'],
                          'native_epoch_offset_ms': c['native_epoch_offset_ms'],
                          'sensor_targets': targets}
    return result


def make_contract(data, plans, code_sha):
    metadata_sha = {k: hashlib.sha256(data['metadata_bytes'][k]).hexdigest()
                    for k in data['metadata_paths']}
    if any(digest_file(p) != metadata_sha[k] for k, p in data['metadata_paths'].items()):
        raise RuntimeError('Metadata changed between role validation and contract freeze.')
    return {'version': VERSION, 'date': '2026-10-25', 'producer_code_sha256': code_sha,
            'metadata_sha256': metadata_sha,
            'permitted_dynamic_role': 'TRAIN', 'complete_release_parent_count': 31,
            'complete_release_cropped_frames': 12665, 'fixed_crop_source_indices': '[100:-100]',
            'fixed_query_rate_hz': RATE,
            'sensor_target_order': [f'{sid}_{mod}_{a}' for sid in SENSORS
                                    for mod in ('acc', 'gyro') for a in 'xyz'],
            'sensor_target_frame': 'each_measured_sensor_native_xyz',
            'sensor_target_units': 'ACC_m/s^2_GYRO_rad/s',
            'native_ACC_g_factor': 9.80665, 'native_GYRO_deg_s_factor': float(np.pi / 180),
            'missing_targets': 'zero_storage_fill_with_separate_false_mask_only_for_inventory_absence',
            'present_source_failure': 'fatal_not_new_mask_or_cohort_exclusion',
            'position_names': list(POINT_NAMES), 'position_units': 'meters',
            'position_definition': '(interpolated_point_xyz_mm - bilateral_hip_midpoint_mm)/1000',
            'position_computation_dtype': 'float64_interpolate_and_center_then_float32_final',
            'position_frame': 'legacy_candidate_pelvis_axes_not_clinical_JCS_not_hardware_sensor_centers',
            'final_angle_target': 'unchanged_source_y_angles_crop_float32',
            'model_input_keys': ['x'],
            'auxiliary_target_keys': ['sensor_target', 'sensor_mask', 'positions'],
            'final_target_keys': ['y'],
            'clock_and_row_arrays_are_audit_metadata_not_model_inputs': True,
            'native_max_interpolation_gap_ms': MAX_NATIVE_GAP_MS,
            'point_max_interpolation_gap_s': MAX_POINT_GAP_S,
            'source_read_policy': {'native_shared_CSV_full_bytes_hashed_before_after': True,
                                   'heldout_bytes_may_be_mechanically_hashed': True,
                                   'all_timestamps_and_row_strings_scanned': True,
                                   'numeric_values_only_selected_TRAIN_brackets': True,
                                   'bracket_flanks_must_stay_inside_full_owning_TRAIN_trial': True},
            'no_new_lag_axis_bias_or_filter_fit': True, 'scaler_fits': 0, 'neural_fits': 0,
            'untouched_test_claim': False, 'TRAIN_parents_and_sources': [plans[p] for p in data['train']]}


def build_release(experiments_root, output_dir, parents=None):
    data = load_metadata(experiments_root)
    requested = guard_requested(data, parents)  # before source hashing or dynamic loading
    access = TrainAccess(data, requested)
    plans = source_plan(data, data['train'])
    code_sha = digest_file(Path(__file__))
    contract = make_contract(data, plans, code_sha)
    output = Path(output_dir).resolve()
    contract_bytes = (json.dumps(contract, ensure_ascii=False, sort_keys=True,
                                 indent=2, allow_nan=False) + '\n').encode()
    contract_sha = hashlib.sha256(contract_bytes).hexdigest()
    immutable_bytes(output / 'contract.json', contract_bytes)
    arrays = {p: access.load_train_npz(p) for p in requested}
    crop = slice(CROP, -CROP)
    native_jobs = {}
    for parent in requested:
        for target in plans[parent]['sensor_targets']:
            if not target['available']:
                continue
            path = target['path']
            job = native_jobs.setdefault(path, {'source': target, 'owners': []})
            if job['source'] != target:
                raise RuntimeError('One native path has inconsistent source metadata.')
            job['owners'].append(parent)
    native_values, source_receipts = {}, []
    for path, job in sorted(native_jobs.items()):
        z = job['source']
        modality = z['modality']
        unit = 'g' if modality == 'Accelerometer' else 'deg/s'
        factor = 9.80665 if modality == 'Accelerometer' else float(np.pi / 180)
        cols = [f'{a}-axis ({unit})' for a in 'xyz']
        queries = {p: arrays[p]['input_epoch_ms'][crop] for p in job['owners']}
        bounds = {p: arrays[p]['input_epoch_ms'][[0, -1]] for p in job['owners']}
        values, receipt = stream_source(path, z['sha256'], job['owners'], queries, bounds,
                                         native=True, columns=cols, factor=factor,
                                         max_gap=MAX_NATIVE_GAP_MS, access=access)
        native_values[path] = values
        source_receipts.append(receipt)
    rows = []
    for parent in requested:
        plan, a = plans[parent], arrays[parent]
        n = plan['cropped_frames']
        target = np.zeros((n, 18), np.float32)
        mask = np.zeros((n, 18), bool)
        left = np.full((n, 6), -1, np.int64)
        right = np.full((n, 6), -1, np.int64)
        alpha = np.zeros((n, 6), np.float64)
        parent_native = []
        for j, z in enumerate(plan['sensor_targets']):
            if z['available']:
                value = native_values[z['path']][parent]
                target[:, j * 3:j * 3 + 3] = value['values'].astype(np.float32)
                mask[:, j * 3:j * 3 + 3] = True
                left[:, j], right[:, j], alpha[:, j] = value['left'], value['right'], value['alpha']
            parent_native.append(z)
        point_values, point_receipt = stream_source(
            plan['point_source'], plan['point_source_sha256'], [parent],
            {parent: a['optic_absolute_time'][crop]},
            {parent: a['optic_absolute_time'][[0, -1]]},
            native=False, columns=POINT_COLUMNS, factor=1.0,
            max_gap=MAX_POINT_GAP_S, access=access)
        source_receipts.append(point_receipt)
        p = point_values[parent]
        mm = p['values'].reshape(n, 8, 3)
        root = (mm[:, 0] + mm[:, 4]) / 2
        positions = ((mm - root[:, None]) / 1000).reshape(n, 24).astype(np.float32)
        if not np.isfinite(positions).all():
            raise RuntimeError('Invalid root-relative target.')
        provenance = {'version': VERSION, 'parent_id': parent, 'split': 'TRAIN',
                      'contract_sha256': contract_sha, 'producer_code_sha256': code_sha,
                      'source_npz_sha256': plan['source_npz_sha256'],
                      'source_point_sha256': plan['point_source_sha256'],
                      'sensor_sources': parent_native,
                      'point_source_receipt': point_receipt,
                      'crop': [CROP, plan['original_frames'] - CROP],
                      'zero_filled_missing_signal_values_have_false_mask': True,
                      'extra_sensor_and_point_supervision_are_not_deployment_inputs': True}
        out = {'x': a['x'][crop].copy(), 'y': a['y_angles'][crop].copy(),
               'sensor_target': target, 'sensor_mask': mask, 'positions': positions,
               'time': a['time'][crop].copy(),
               'input_epoch_ms': a['input_epoch_ms'][crop].copy(),
               'optic_absolute_time': a['optic_absolute_time'][crop].copy(),
               'source_frame_indices': np.arange(CROP, plan['original_frames'] - CROP, dtype=np.int64),
               'sensor_source_left_indices': left, 'sensor_source_right_indices': right,
               'sensor_interp_alpha': alpha,
               'point_source_left_indices': p['left'], 'point_source_right_indices': p['right'],
               'point_interp_alpha': p['alpha'],
               'subject': np.asarray(plan['subject']), 'parent_id': np.asarray(parent),
               'split': np.asarray('TRAIN'), 'contract_sha256': np.asarray(contract_sha),
               'provenance_json': np.asarray(canonical(provenance))}
        access.require([parent], 'persist_or_validate_TRAIN_output')
        filename = parent.replace('/', '__') + '_staged_TRAIN.npz'
        path = output / filename
        immutable_npz(path, out)
        availability = {f'{s["sensor"]}_{s["modality"]}': bool(s['available'])
                        for s in plan['sensor_targets']}
        rows.append({'parent_id': parent, 'subject': plan['subject'], 'split': 'TRAIN',
                     'path': filename, 'sha256': digest_file(path),
                     'frames': n, 'sample_seconds': n / RATE,
                     'sample_timestamp_span_seconds': (n - 1) / RATE,
                     'full_TRAIN_source_frames': plan['original_frames'],
                     'full_TRAIN_source_sample_seconds': plan['original_frames'] / RATE,
                     'sensor_modality_availability': availability,
                     'sensor_modality_supervised_sample_seconds': {k: n / RATE if v else 0.0 for k, v in availability.items()},
                     'sensor_supervised_channel_frames': int(mask.sum()),
                     'sensor_total_storage_channel_frames': int(mask.size),
                     'point_target_sample_seconds': n / RATE,
                     'point_context_rows_outside_cropped_query': point_receipt['per_parent_support'][parent]['external_adjacent_rows_outside_cropped_query_interval'],
                     'array_sha256': {k: digest_array(v) for k, v in out.items() if np.asarray(v).ndim > 0},
                     'source_npz_sha256': plan['source_npz_sha256']})
    full = requested == data['train']
    if full and (len(rows) != 31 or sum(r['frames'] for r in rows) != 12665):
        raise RuntimeError('A complete release must contain exactly 31 TRAIN parents / 12665 frames.')
    if digest_file(Path(__file__)) != code_sha:
        raise RuntimeError('Producer source changed during execution.')
    manifest = {'status': 'complete_TRAIN_only_staged_targets_built_pending_independent_audit'
                         if full else 'partial_TRAIN_only_staged_targets_built_not_complete_release',
                'version': VERSION, 'date': '2026-10-25', 'contract_sha256': contract_sha,
                'producer_code_sha256': code_sha, 'complete_release': full,
                'requested_TRAIN_parents': requested,
                'roles': {'TRAIN': len(rows), 'VALID': 0, 'TEST': 0},
                'frames': sum(r['frames'] for r in rows),
                'unique_target_sample_seconds': sum(r['frames'] for r in rows) / RATE,
                'full_TRAIN_source_sample_seconds_read': sum(r['full_TRAIN_source_frames'] for r in rows) / RATE,
                'unique_native_source_files': len(native_jobs),
                'native_numeric_rows_decoded': sum(r['numeric_value_rows_decoded'] for r in source_receipts if r['kind'] == 'native_csv'),
                'point_numeric_rows_decoded': sum(r['numeric_value_rows_decoded'] for r in source_receipts if r['kind'] == 'point_csv'),
                'external_adjacent_native_rows_outside_cropped_queries': sum(r['external_adjacent_unique_rows_outside_all_cropped_query_intervals'] for r in source_receipts if r['kind'] == 'native_csv'),
                'external_adjacent_point_rows_outside_cropped_queries': sum(r['external_adjacent_unique_rows_outside_all_cropped_query_intervals'] for r in source_receipts if r['kind'] == 'point_csv'),
                'all_value_brackets_within_full_owning_TRAIN_trial': True,
                'shared_native_source_full_bytes_mechanically_hashed': True,
                'heldout_source_bytes_may_be_hashed': True,
                'all_source_rows_read_as_strings_for_clock_scans': True,
                'unselected_numeric_signal_values_converted': False,
                'VALID_TEST_dynamic_arrays_read': 0, 'scaler_fits': 0, 'model_fits': 0,
                'training_ready_before_independent_audit': False,
                'parents': rows, 'source_value_read_receipts': source_receipts}
    selection = hashlib.sha256(canonical(requested).encode()).hexdigest()[:16]
    name = 'manifest.json' if full else f'partial_manifest_{selection}.json'
    immutable_json(output / name, manifest)
    run = {'version': VERSION, 'requested_parents': requested, 'complete_release_invocation': full,
           'contract_sha256': contract_sha, 'manifest_name': name,
           'manifest_sha256': digest_file(output / name), 'access_events': access.events,
           'no_claim_of_zero_heldout_source_byte_reads': True}
    run_id = hashlib.sha256(canonical(run).encode()).hexdigest()[:20]
    immutable_json(output / 'run_receipts' / f'run_{run_id}.json', run)
    return {'status': manifest['status'], 'output': str(output), 'manifest': name,
            'manifest_sha256': digest_file(output / name), 'contract_sha256': contract_sha,
            'parents': len(rows), 'frames': manifest['frames'], 'new_fits': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiments-root', type=Path)
    parser.add_argument('--output-dir', type=Path, default=HERE / 'train_v1')
    parser.add_argument('--parent', action='append', help='A fixed TRAIN parent, repeatable; omit for all31.')
    parser.add_argument('--synthetic-test', action='store_true')
    args = parser.parse_args()
    if args.synthetic_test:
        import test_build_train_targets
        print(json.dumps(test_build_train_targets.run_tests(), ensure_ascii=False))
        return
    if args.experiments_root is None:
        parser.error('--experiments-root is required for a real export')
    print(json.dumps(build_release(args.experiments_root, args.output_dir, args.parent), ensure_ascii=False))


if __name__ == '__main__':
    main()
