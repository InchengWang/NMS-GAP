"""Independent audit of the staged TRAIN target release.

This file never imports the producer. Native and point CSVs are scanned for
clock metadata first; only the union of permitted TRAIN interpolation rows is
converted to numerical signal/point values. Whole-file identity hashing and
full CSV text scans can read bytes belonging to held-out intervals, and are
explicitly distinguished from numerical array access.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import re
import tempfile

import numpy as np

ROOT = Path(__file__).resolve().parent
META = {
    'release': 'native_training_release_20261021/dataset_release.json',
    'candidates': 'marker_recall_20261021/ordered_native_candidates_v2/manifest.json',
    'inventory': 'raw_source_rebuild_20261021/raw_source_manifest.json',
}
POINTS = ('left_hip', 'left_knee', 'left_ankle', 'left_foot',
          'right_hip', 'right_knee', 'right_ankle', 'right_foot')
PCOLS = tuple(f'all_lower_joint_gt_{p}_pelvis_{a}_mm' for p in POINTS for a in 'xyz')
MODS = (('S3','Accelerometer'), ('S3','Gyroscope'),
        ('S4','Accelerometer'), ('S4','Gyroscope'),
        ('S5','Accelerometer'), ('S5','Gyroscope'))


def jread(path):
    return json.loads(Path(path).read_text())


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(2**20), b''):
            h.update(block)
    return h.hexdigest()


def array_sha(value):
    a = np.ascontiguousarray(value)
    h = hashlib.sha256(canonical({'dtype':a.dtype.str, 'shape':list(a.shape)}).encode())
    h.update(a.tobytes())
    return h.hexdigest()


def write_once(path, value):
    p = Path(path)
    data = (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       indent=2, allow_nan=False) + '\n').encode()
    if p.exists():
        if p.read_bytes() != data:
            raise RuntimeError('Independent audit receipt conflict; do not overwrite it.')
    else:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)


def ordered_parent(p):
    return (int(p.split('/')[0][1:]), p)


class Access:
    """The allowlist is checked before every dynamic-file hash/load/parse."""
    def __init__(self, release, candidates):
        self.release = release
        self.candidates = candidates
        self.allowed = frozenset(p for p,r in release.items()
                                 if r['split']=='TRAIN' and candidates[p]['split']=='TRAIN')
        self.dynamic_npz = set()
        self.dynamic_csv_files = set()
        self.hash_events = []

    def require(self, owners):
        ps = tuple(owners)
        if not ps or any(p not in self.allowed for p in ps):
            raise PermissionError('An independent read was refused before data access.')
        return ps

    def checked_hash(self, path, expected, owners, kind):
        ps=self.require(owners)
        got=sha(path)
        if got!=expected:
            raise RuntimeError(f'Source/artifact identity mismatch: {path}')
        self.hash_events.append({'kind':kind,'sha256':got,'owners':sorted(ps),
                                 'bytes':Path(path).stat().st_size,
                                 'shared_heldout_bytes_possible':kind=='native_csv'})
        return got

    def npz(self, path, expected, owners, fields, kind):
        ps=self.require(owners)
        self.checked_hash(path,expected,ps,kind)
        with np.load(path,allow_pickle=False) as z:
            out={key:z[key].copy() for key in fields}
        self.checked_hash(path,expected,ps,kind)
        self.dynamic_npz.add((kind,str(Path(path).resolve())))
        return out


def stamp_decoder(header):
    m=re.search(r'\(([+-])(\d{2})(\d{2})\)',header)
    if m is None:
        raise ValueError('Native time header has no explicit timezone.')
    minutes=(int(m[2])*60+int(m[3]))*(1 if m[1]=='+' else -1)
    local_zone=timezone(timedelta(minutes=minutes))
    epoch=datetime(1970,1,1,tzinfo=timezone.utc)
    def decode(value):
        local=datetime.strptime(value,'%Y-%m-%dT%H.%M.%S.%f').replace(tzinfo=local_zone)
        d=local.astimezone(timezone.utc)-epoch
        return d.days*86400000+d.seconds*1000+d.microseconds//1000
    return decode


def clocks_only(path, native):
    times=[]
    with Path(path).open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.reader(stream)
        header=[v.strip() for v in next(reader)]
        if len(header)!=len(set(header)):
            raise ValueError('Nonunique source fields.')
        if native:
            choices=[n for n in header if n.startswith('timestamp')]
            if len(choices)!=1:
                raise ValueError('Ambiguous native timestamp.')
            clock_name=choices[0]; convert=stamp_decoder(clock_name)
        else:
            clock_name='time';convert=float
        tindex=header.index(clock_name)
        for fields in reader:
            if len(fields)!=len(header):
                raise ValueError('Malformed CSV clock row.')
            times.append(convert(fields[tindex]))
    t=np.asarray(times,dtype=np.int64 if native else np.float64)
    if len(t)<2 or not np.isfinite(t).all() or np.any(t[1:]<=t[:-1]):
        raise ValueError('Unsafe source clock metadata.')
    return header,clock_name,t


def bracket_indices(t,q,native):
    """Independent two-sided lookup; exact rows do not need a previous value."""
    q=np.asarray(q,dtype=np.float64)
    if q.ndim!=1 or not len(q) or not np.isfinite(q).all() or np.any(np.diff(q)<=0):
        raise ValueError('Unsafe allowed query.')
    if q[0]<t[0] or q[-1]>t[-1]:
        raise ValueError('Extrapolation is outside the declared support.')
    lower=np.searchsorted(t,q,side='right')-1
    upper=np.searchsorted(t,q,side='left')
    if np.any(lower<0) or np.any(upper>=len(t)):
        raise ValueError('No two-sided source support.')
    exact=t[upper]==q
    lower[exact]=upper[exact]
    gap=t[upper]-t[lower]
    if np.any((~exact)&(gap>(25.1 if native else .0251))):
        raise ValueError('The native bracket exceeds the fixed gap rule.')
    a=np.zeros(len(q),dtype=np.float64)
    not_same=upper!=lower
    a[not_same]=(q[not_same]-t[lower[not_same]])/gap[not_same]
    return lower.astype(np.int64),upper.astype(np.int64),a


def read_numeric_rows(path,header,clock_name,t,selected,columns,factor,native):
    """No float() is applied to a signal/point token outside selected rows."""
    selected=np.asarray(selected,np.int64)
    selected_set=set(selected.tolist())
    converted={}
    token=hashlib.sha256()
    decode=stamp_decoder(clock_name) if native else float
    with Path(path).open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.reader(stream)
        actual=[v.strip() for v in next(reader)]
        if actual!=header:
            raise RuntimeError('Header changed between independent passes.')
        vi=[header.index(c) for c in columns];ti=header.index(clock_name)
        count=0
        for index,row in enumerate(reader):
            count+=1
            if len(row)!=len(header):
                raise ValueError('Malformed CSV row.')
            if index not in selected_set:
                continue
            if decode(row[ti])!=t[index]:
                raise RuntimeError('A selected source timestamp changed.')
            raw=[row[i] for i in vi]
            arr=np.asarray([float(v) for v in raw],np.float64)*factor
            if not np.isfinite(arr).all():
                raise ValueError('Present source has a nonfinite selected value.')
            converted[index]=arr
            token.update((canonical([index,row[ti],raw])+'\n').encode())
    if count!=len(t) or set(converted)!=selected_set:
        raise RuntimeError('Source row count changed or allowed rows were not read.')
    v=np.stack([converted[int(i)] for i in selected])
    h=hashlib.sha256()
    h.update(np.asarray(selected,dtype='<i8').tobytes())
    h.update(np.asarray(t[selected],dtype='<i8' if native else '<f8').tobytes())
    h.update(np.asarray(v,dtype='<f8').tobytes())
    return v,token.hexdigest(),h.hexdigest()


def independent_source(job,access):
    ps=access.require(job['owners'])
    access.checked_hash(job['path'],job['sha256'],ps,job['kind'])
    native=job['kind']=='native_csv'
    header,name,t=clocks_only(job['path'],native)
    for c in job['columns']:
        if c not in header:raise ValueError('Expected explicit value field missing.')
    bracket={};all_selected=[];support={}
    for p in ps:
        lo,hi,a=bracket_indices(t,job['query'][p],native)
        lower,upper=job['full_bounds'][p]
        tol=1e-5 if native else 1e-9
        if np.any(t[lo]<lower-tol) or np.any(t[hi]>upper+tol):
            raise PermissionError('A numerical flank escapes the full owning TRAIN trial.')
        bracket[p]=(lo,hi,a);all_selected.extend([lo,hi])
        own_ids=np.unique(np.r_[lo,hi])
        own_query=job['query'][p]
        adjacent=own_ids[(t[own_ids]<own_query[0])|(t[own_ids]>own_query[-1])]
        support[p]={'query_frames':len(own_query),
                    'query_bounds':[float(own_query[0]),float(own_query[-1])],
                    'selected_source_rows':len(own_ids),
                    'source_row_index_bounds':[int(own_ids[0]),int(own_ids[-1])],
                    'external_adjacent_rows_outside_cropped_query_interval':len(adjacent),
                    'external_adjacent_row_indices':adjacent.tolist(),
                    'selected_brackets_inside_owning_full_TRAIN_support':True}
    ids=np.unique(np.concatenate(all_selected))
    access.require(ps)
    values,tok_sha,row_sha=read_numeric_rows(job['path'],header,name,t,ids,
                                            job['columns'],job['factor'],native)
    access.dynamic_csv_files.add(str(Path(job['path']).resolve()))
    access.checked_hash(job['path'],job['sha256'],ps,job['kind'])
    # The reconstruction uses np.interp on selected timestamps, independently
    # of the producer's gathered-left/right weighted interpolation expression.
    origin=t[ids[0]]
    compact_time=t[ids]-origin
    interp={p:np.column_stack([np.interp(job['query'][p]-origin,compact_time,values[:,k])
                               for k in range(len(job['columns']))]) for p in ps}
    in_any=np.zeros(len(ids),bool)
    for query in job['query'].values():
        in_any|=(t[ids]>=query[0])&(t[ids]<=query[-1])
    return {'interpolated':interp,'brackets':bracket,'ids':ids,
            'token_sha256':tok_sha,'rows_sha256':row_sha,
            'metadata_rows_scanned':len(t),'numeric_rows_decoded':len(ids),
            'numeric_cells_decoded':int(values.size),'per_parent_support':support,
            'external_adjacent_unique_rows_outside_all_cropped_query_intervals':int((~in_any).sum())}


def compare_float32(actual, expected64, name):
    if actual.dtype!=np.float32:
        raise AssertionError(name+': float32 storage changed.')
    expected=np.asarray(expected64,dtype=np.float32)
    if actual.shape!=expected.shape or not np.isfinite(actual).all():
        raise AssertionError(name+': shape or finite gate.')
    difference=np.abs(actual.astype(np.float64)-expected.astype(np.float64))
    tolerance=2*np.spacing(np.abs(expected)).astype(np.float64)+1e-9
    if np.any(difference>tolerance):
        raise AssertionError(name+': independent reconstruction mismatch.')
    return float(difference.max(initial=0))


def run_audit(experiments_root,release_dir,output=None):
    e=Path(experiments_root).resolve();d=Path(release_dir).resolve()
    source={k:jread(e/rel) for k,rel in META.items()}
    source_hash={k:sha(e/rel) for k,rel in META.items()}
    records={r['parent_id']:r for r in source['release']['trials']}
    candidates={r['parent_id']:r for r in source['candidates']['trials']}
    if len(records)!=53 or set(records)!=set(candidates):
        raise AssertionError('The accepted metadata inventory changed.')
    if any(records[p]['split']!=candidates[p]['split'] for p in records):
        raise AssertionError('Metadata role disagreement.')
    access=Access(records,candidates)
    parents=sorted(access.allowed,key=ordered_parent)
    if len(parents)!=31 or sum(records[p]['frames']-200 for p in parents)!=12665:
        raise AssertionError('Expected 31 fixed TRAIN parents / 12665 cropped frames.')
    m=jread(d/'manifest.json');c=jread(d/'contract.json')
    if m['status']!='complete_TRAIN_only_staged_targets_built_pending_independent_audit' or not m['complete_release']:
        raise AssertionError('Only the complete, unaudited TRAIN release is accepted.')
    if m['requested_TRAIN_parents']!=parents or m['roles']!={'TRAIN':31,'VALID':0,'TEST':0} or m['frames']!=12665:
        raise AssertionError('Release parent/role/frame contract disagreement.')
    if c['metadata_sha256']!=source_hash or m['contract_sha256']!=sha(d/'contract.json'):
        raise AssertionError('Metadata or data contract fingerprint mismatch.')
    producer=ROOT/'build_train_targets.py'
    producer_sha=sha(producer)
    if m['producer_code_sha256']!=producer_sha or c['producer_code_sha256']!=producer_sha:
        raise AssertionError('Frozen producer fingerprint mismatch.')
    if c['permitted_dynamic_role']!='TRAIN' or c['position_definition']!='(interpolated_point_xyz_mm - bilateral_hip_midpoint_mm)/1000':
        raise AssertionError('Semantic target definition changed.')
    required_contract={'complete_release_parent_count':31,'complete_release_cropped_frames':12665,
                       'fixed_crop_source_indices':'[100:-100]','fixed_query_rate_hz':100.0,
                       'sensor_target_frame':'each_measured_sensor_native_xyz',
                       'sensor_target_units':'ACC_m/s^2_GYRO_rad/s','position_units':'meters',
                       'position_names':list(POINTS),
                       'position_frame':'legacy_candidate_pelvis_axes_not_clinical_JCS_not_hardware_sensor_centers',
                       'position_computation_dtype':'float64_interpolate_and_center_then_float32_final',
                       'model_input_keys':['x'],'auxiliary_target_keys':['sensor_target','sensor_mask','positions'],
                       'final_target_keys':['y'],'clock_and_row_arrays_are_audit_metadata_not_model_inputs':True,
                       'native_max_interpolation_gap_ms':25.1,'point_max_interpolation_gap_s':.0251,
                       'native_ACC_g_factor':9.80665,'native_GYRO_deg_s_factor':float(np.pi/180),
                       'scaler_fits':0,'neural_fits':0,'untouched_test_claim':False}
    if any(c.get(k)!=v for k,v in required_contract.items()):
        raise AssertionError('Frozen frame/unit/layout/cost contract differs.')
    if c['sensor_target_order']!=[f'{s}_{kind}_{axis}' for s in ('S3','S4','S5') for kind in ('acc','gyro') for axis in 'xyz']:
        raise AssertionError('Dense measured channel order changed.')
    rows={r['parent_id']:r for r in m['parents']}
    if len(m['parents'])!=31 or set(rows)!=set(parents):
        raise AssertionError('Duplicate or wrong output parents.')
    manifest_receipts={r['path']:r for r in m['source_value_read_receipts']}
    if len(manifest_receipts)!=len(m['source_value_read_receipts']):
        raise AssertionError('Duplicated source value read receipt.')
    if any(m.get(k)!=v for k,v in {'VALID_TEST_dynamic_arrays_read':0,'scaler_fits':0,'model_fits':0,
                                 'unselected_numeric_signal_values_converted':False,
                                 'all_value_brackets_within_full_owning_TRAIN_trial':True,
                                 'training_ready_before_independent_audit':False}.items()):
        raise AssertionError('Producer role/read/fit accounting differs.')
    original={};out={};plans={};jobs={}
    folders={str(Path(f['folder']).resolve()):f for f in source['inventory']['source_folders']}
    flds=('x','y_angles','time','input_epoch_ms','optic_absolute_time','parent_id','split')
    oflds=('x','y','sensor_target','sensor_mask','positions','time','input_epoch_ms',
           'optic_absolute_time','source_frame_indices','sensor_source_left_indices',
           'sensor_source_right_indices','sensor_interp_alpha','point_source_left_indices',
           'point_source_right_indices','point_interp_alpha','parent_id','subject','split','contract_sha256')
    for p in parents:
        access.require([p]);r=records[p];z=candidates[p];rr=rows[p]
        expected=(e/'marker_recall_20261021/ordered_native_candidates_v2'/z['path']).resolve()
        if Path(r['source_npz']).resolve()!=expected or r['source_sha256']!=z['sha256']:
            raise AssertionError('Original NPZ identity mismatch.')
        a=access.npz(expected,r['source_sha256'],[p],flds,'original_TRAIN_npz')
        if str(a['parent_id'].item())!=p or str(a['split'].item())!='TRAIN':
            raise AssertionError('Original stored role differs.')
        op=(d/rr['path']).resolve()
        if op.parent!=d or rr['split']!='TRAIN' or rr['subject']!=r['subject']:
            raise AssertionError('Escaping output path or wrong output role.')
        b=access.npz(op,rr['sha256'],[p],oflds,'staged_TRAIN_npz')
        if str(b['parent_id'].item())!=p or str(b['subject'].item())!=r['subject'] or str(b['split'].item())!='TRAIN' or str(b['contract_sha256'].item())!=sha(d/'contract.json'):
            raise AssertionError('Stored staged identity differs.')
        n=r['frames']-200
        if a['x'].shape!=(r['frames'],12) or a['y_angles'].shape!=(r['frames'],6):
            raise AssertionError('Original TRAIN dimensions differ from metadata.')
        if any(a[k].shape!=(r['frames'],) or not np.isfinite(a[k]).all() or np.any(np.diff(a[k])<=0)
               for k in ('time','input_epoch_ms','optic_absolute_time')):
            raise AssertionError('Original TRAIN query clock shape/order differs.')
        if np.max(np.abs(np.diff(a['input_epoch_ms'])-10.0))>.001 or not np.allclose(a['input_epoch_ms'][[0,-1]],z['input_epoch_bounds_ms'],rtol=0,atol=1e-5):
            raise AssertionError('Inherited 100 Hz query grid/endpoints differ.')
        if rr['frames']!=n or b['x'].shape!=(n,12) or b['y'].shape!=(n,6) or b['sensor_target'].shape!=(n,18) or b['positions'].shape!=(n,24) or b['sensor_mask'].shape!=(n,18) or b['sensor_mask'].dtype!=bool:
            raise AssertionError('Unexpected output layout.')
        layouts={'sensor_source_left_indices':((n,6),np.dtype('int64')),
                 'sensor_source_right_indices':((n,6),np.dtype('int64')),
                 'sensor_interp_alpha':((n,6),np.dtype('float64')),
                 'point_source_left_indices':((n,),np.dtype('int64')),
                 'point_source_right_indices':((n,),np.dtype('int64')),
                 'point_interp_alpha':((n,),np.dtype('float64')),
                 'source_frame_indices':((n,),np.dtype('int64'))}
        if any(b[k].shape!=shape or b[k].dtype!=dtype for k,(shape,dtype) in layouts.items()):
            raise AssertionError('Unexpected provenance shape or dtype.')
        for k,sourcekey in [('x','x'),('y','y_angles'),('time','time'),('input_epoch_ms','input_epoch_ms'),('optic_absolute_time','optic_absolute_time')]:
            if not np.array_equal(b[k],a[sourcekey][100:-100]):
                raise AssertionError('Original x/y/query crop was not preserved: '+k)
        if not np.array_equal(b['source_frame_indices'],np.arange(100,r['frames']-100)):
            raise AssertionError('Crop lineage differs.')
        if not np.allclose(a['input_epoch_ms'],a['optic_absolute_time']*1000+z['native_epoch_offset_ms'],rtol=0,atol=1e-5):
            raise AssertionError('Inherited optical/native clock equation differs.')
        original[p]=a;out[p]=b
        folder=str(Path(z['native_sources'][0]['path']).resolve().parent)
        inventory=folders[folder]
        if inventory['subject']!=r['subject']:
            raise AssertionError('Native folder identity differs.')
        plans[p]=[]
        for group,(sensor,mod) in enumerate(MODS):
            matches=[q for q in inventory['files'] if q['sensor']==sensor and q['modality']==mod]
            if len(matches)>1:raise AssertionError('Ambiguous original measured target source.')
            if not matches:
                if (r['subject'],sensor,mod) not in {('P6','S5','Accelerometer'),('P17','S5','Gyroscope')}:
                    raise AssertionError('Unaccounted missing target source.')
                plans[p].append(None);continue
            q=matches[0]
            if any(q[k] for k in ('duplicate_timestamp_count','decreasing_timestamp_count','nonfinite_values')):
                raise AssertionError('Source inventory safety flag.')
            path=str(Path(q['path']).resolve());plans[p].append(path)
            kind='native_csv';factor=9.80665 if mod=='Accelerometer' else float(np.pi/180)
            unit='g' if mod=='Accelerometer' else 'deg/s'
            j=jobs.setdefault(path,{'path':path,'sha256':q['sha256'],'kind':kind,'owners':[],
                                    'columns':[f'{a}-axis ({unit})' for a in 'xyz'],
                                    'factor':factor,'query':{},'full_bounds':{}})
            if j['sha256']!=q['sha256']:raise AssertionError('Source SHA ambiguity.')
            j['owners'].append(p);j['query'][p]=b['input_epoch_ms'];j['full_bounds'][p]=a['input_epoch_ms'][[0,-1]]
        path=str(Path(z['point_labels']).resolve())
        if path in jobs:raise AssertionError('A point source unexpectedly has multiple parent identities.')
        jobs[path]={'path':path,'sha256':z['point_sha256'],'kind':'point_csv','owners':[p],
                    'columns':list(PCOLS),'factor':1.0,'query':{p:b['optic_absolute_time']},
                    'full_bounds':{p:a['optic_absolute_time'][[0,-1]]}}
    if set(jobs)!=set(manifest_receipts):
        raise AssertionError('Expected source-file set differs from producer receipts.')
    rebuilt={};source_audits=[]
    for path,job in sorted(jobs.items()):
        q=independent_source(job,access);rebuilt[path]=q;mr=manifest_receipts[path]
        if mr['kind']!=job['kind'] or mr['sha256']!=job['sha256'] or set(mr['owners'])!=set(job['owners']):
            raise AssertionError('Source ownership receipt differs.')
        if q['ids'].tolist()!=mr['source_row_indices_zero_based_after_header']:
            raise AssertionError('Decoded row set differs from minimal allowed brackets.')
        if q['token_sha256']!=mr['selected_rows_text_tokens_sha256'] or q['rows_sha256']!=mr['selected_rows_indices_clock_and_SI_values_sha256']:
            raise AssertionError('Selected numerical source values/units differ.')
        if q['metadata_rows_scanned']!=mr['all_rows_clock_metadata_scanned'] or q['numeric_rows_decoded']!=mr['numeric_value_rows_decoded'] or q['numeric_cells_decoded']!=mr['numeric_value_cells_decoded']:
            raise AssertionError('Numerical-read accounting differs.')
        if mr['numeric_value_columns_decoded']!=job['columns'] or mr['factor_to_output_units']!=job['factor'] or mr['per_parent_support']!=q['per_parent_support'] or mr['external_adjacent_unique_rows_outside_all_cropped_query_intervals']!=q['external_adjacent_unique_rows_outside_all_cropped_query_intervals']:
            raise AssertionError('Independent units, columns or interpolation support cost differs.')
        source_audits.append({'source_sha256':job['sha256'],'kind':job['kind'],
                              'owners':sorted(job['owners'],key=ordered_parent),
                              'clock_metadata_rows_scanned':q['metadata_rows_scanned'],
                              'numeric_rows_decoded':q['numeric_rows_decoded'],
                              'numeric_cells_decoded':q['numeric_cells_decoded'],
                              'selected_rows_SI_sha256':q['rows_sha256'],
                              'external_adjacent_rows':q['external_adjacent_unique_rows_outside_all_cropped_query_intervals']})
    max_signal=0.;max_position=0.;max_alpha=0.;group_available=np.zeros(6,np.int64);group_frames=np.zeros(6,np.int64)
    for p in parents:
        b=out[p];n=len(b['x']);expected_mask=np.zeros((n,18),bool)
        for group,path in enumerate(plans[p]):
            sl=slice(group*3,(group+1)*3)
            if path is None:
                if np.any(b['sensor_target'][:,sl]!=0) or np.any(b['sensor_mask'][:,sl]) or np.any(b['sensor_source_left_indices'][:,group]!=-1) or np.any(b['sensor_source_right_indices'][:,group]!=-1) or np.any(b['sensor_interp_alpha'][:,group]!=0):
                    raise AssertionError('Missing modality is not a masked placeholder.')
                continue
            expected_mask[:,sl]=True;group_available[group]+=1;group_frames[group]+=n
            rec=rebuilt[path];l,r,a=rec['brackets'][p]
            if not np.array_equal(b['sensor_source_left_indices'][:,group],l) or not np.array_equal(b['sensor_source_right_indices'][:,group],r):
                raise AssertionError('Native interpolation lineage differs.')
            diff=float(np.abs(b['sensor_interp_alpha'][:,group]-a).max(initial=0));max_alpha=max(max_alpha,diff)
            if diff>1e-12:raise AssertionError('Native interpolation weight differs.')
            max_signal=max(max_signal,compare_float32(b['sensor_target'][:,sl],rec['interpolated'][p],'measured dense target'))
        if not np.array_equal(b['sensor_mask'],expected_mask):
            raise AssertionError('Missingness mask differs from source availability.')
        z=candidates[p];pr=rebuilt[str(Path(z['point_labels']).resolve())];l,r,a=pr['brackets'][p]
        if not np.array_equal(b['point_source_left_indices'],l) or not np.array_equal(b['point_source_right_indices'],r):
            raise AssertionError('Point interpolation lineage differs.')
        diff=float(np.abs(b['point_interp_alpha']-a).max(initial=0));max_alpha=max(max_alpha,diff)
        if diff>1e-12:raise AssertionError('Point interpolation weight differs.')
        mm=pr['interpolated'][p].reshape(n,8,3)
        root=np.mean(mm[:,[0,4],:],axis=1)
        xyz=((mm-root[:,None,:])/1000).reshape(n,24)
        max_position=max(max_position,compare_float32(b['positions'],xyz,'root-relative position'))
        if np.max(np.abs(b['positions'].reshape(n,8,3)[:,0]+b['positions'].reshape(n,8,3)[:,4]))>1e-7:
            raise AssertionError('Bilateral hip midpoint is not zero.')
        for key,expected_sha in rows[p]['array_sha256'].items():
            # Audited arrays are decoded here. Non-model provenance fields remain
            # covered by the whole-artifact SHA rather than silently read as data.
            if key in b and array_sha(b[key])!=expected_sha:
                raise AssertionError('Stored array fingerprint differs: '+key)
    if group_available.tolist()!=[31,31,31,31,28,29]:
        raise AssertionError('Unexpected modality coverage.')
    if m['native_numeric_rows_decoded']!=sum(q['numeric_rows_decoded'] for q in source_audits if q['kind']=='native_csv') or m['point_numeric_rows_decoded']!=sum(q['numeric_rows_decoded'] for q in source_audits if q['kind']=='point_csv'):
        raise AssertionError('Manifest read totals differ.')
    if sha(producer)!=producer_sha:
        raise RuntimeError('Producer changed during independent audit.')
    result={'status':'passed_independent_TRAIN_staged_target_audit','date':'2026-10-25',
            'producer_sha256':producer_sha,'audit_source_sha256':sha(Path(__file__)),
            'manifest_sha256':sha(d/'manifest.json'),'contract_sha256':sha(d/'contract.json'),
            'metadata_sha256':source_hash,'parents':31,'frames':12665,
            'roles':{'TRAIN':31,'VALID':0,'TEST':0},'all_original_x_y_queries_exactly_preserved':True,
            'max_sensor_float32_difference_SI':max_signal,'max_position_float32_difference_m':max_position,
            'max_interpolation_alpha_difference':max_alpha,
            'modality_available_parent_counts':dict(zip([f'{s}_{m}' for s,m in MODS],group_available.tolist())),
            'modality_supervised_sample_seconds':dict(zip([f'{s}_{m}' for s,m in MODS],(group_frames/100).tolist())),
            'signal_mask_valid_channel_frames':int(sum(out[p]['sensor_mask'].sum() for p in parents)),
            'numerical_npz_arrays_opened':{'original_TRAIN':31,'staged_TRAIN':31,'VALID':0,'TEST':0},
            'cost':{'target_sample_seconds':126.65,
                    'original_TRAIN_sample_seconds_read':sum(records[p]['frames'] for p in parents)/100,
                    'native_clock_metadata_rows_scanned':sum(q['clock_metadata_rows_scanned'] for q in source_audits if q['kind']=='native_csv'),
                    'point_clock_metadata_rows_scanned':sum(q['clock_metadata_rows_scanned'] for q in source_audits if q['kind']=='point_csv'),
                    'native_numeric_rows_decoded':sum(q['numeric_rows_decoded'] for q in source_audits if q['kind']=='native_csv'),
                    'point_numeric_rows_decoded':sum(q['numeric_rows_decoded'] for q in source_audits if q['kind']=='point_csv'),
                    'numeric_value_cells_decoded':sum(q['numeric_cells_decoded'] for q in source_audits),
                    'whole_file_mechanical_hash_calls':len(access.hash_events),
                    'whole_file_mechanical_hash_bytes_including_repeated_hashes':sum(q['bytes'] for q in access.hash_events),
                    'shared_native_mechanical_hash_bytes_including_repeated_hashes':sum(q['bytes'] for q in access.hash_events if q['kind']=='native_csv')},
            'source_files':len(source_audits),'source_audits':source_audits,
            'whole_shared_source_bytes_mechanically_hashed':True,'heldout_source_bytes_may_be_hashed':True,
            'all_CSV_rows_read_as_text_for_clock_scans':True,
            'unselected_numeric_signal_or_point_tokens_converted':False,
            'all_numeric_interpolation_flanks_within_full_owning_TRAIN':True,
            'zero_heldout_bytes_read_claim':False,'new_scaler_fits':0,'new_neural_fits':0,
            'independent_numeric_reconstruction_uses_producer_functions':False,
            'training_ready_in_scoped_engineering_sense':True,
            'new_clinical_or_hardware_synchronization_certification':False}
    target=Path(output) if output else d/'independent_train_target_audit.json'
    write_once(target,result)
    return {'status':result['status'],'receipt':str(target),'sha256':sha(target),
            'parents':31,'frames':12665,'maximum_signal_difference':max_signal,
            'maximum_position_difference':max_position,'VALID_TEST_dynamic_reads':0}


def synthetic_checks():
    checks={}
    # A deliberately unusable nonselected token must never be decoded.
    with tempfile.TemporaryDirectory(prefix='staged-independent-audit-') as td:
        p=Path(td)/'native.csv'
        p.write_text('timestamp (+0900),x-axis (g),y-axis (g),z-axis (g)\n'
                     '2024-03-16T11.00.00.000,unselected,unselected,unselected\n'
                     '2024-03-16T11.00.00.010,1,2,3\n'
                     '2024-03-16T11.00.00.020,2,4,6\n'
                     '2024-03-16T11.00.00.030,unselected,unselected,unselected\n')
        h,name,t=clocks_only(p,True)
        q=np.array([float(t[1]),float(t[1])+5,float(t[2])])
        l,r,a=bracket_indices(t,q,True)
        assert l.tolist()==[1,1,2] and r.tolist()==[1,2,2] and a.tolist()==[0,.5,0]
        v,_,_=read_numeric_rows(p,h,name,t,np.array([1,2]),['x-axis (g)','y-axis (g)','z-axis (g)'],9.80665,True)
        assert np.allclose(v,[[9.80665,19.6133,29.41995],[19.6133,39.2266,58.8399]],rtol=0,atol=1e-12)
        checks['time_first_selected_tokens_only']=True
        checks['explicit_timezone_and_SI']=bool(t[0]==1710554400000)
        assert checks['explicit_timezone_and_SI']
        checks['independent_brackets_and_exact_rows']=True
    for t,q,native in [(np.array([0,100]),np.array([50.]),True),
                       (np.array([0.,.1]),np.array([.05]),False),
                       (np.array([0,10]),np.array([-1.]),True)]:
        try:bracket_indices(t,q,native)
        except ValueError:pass
        else:raise AssertionError('Invalid bracket did not fail.')
    checks['gap_and_extrapolation_fail_closed']=True
    access=Access({'ok':{'split':'TRAIN'},'bad':{'split':'TEST'}},
                  {'ok':{'split':'TRAIN'},'bad':{'split':'TEST'}})
    try:access.checked_hash('/does/not/exist','', ['bad'],'native_csv')
    except PermissionError:pass
    else:raise AssertionError('Role check did not precede path access.')
    assert not access.hash_events
    checks['role_guard_precedes_hash_and_path_access']=True
    mm=np.arange(48,dtype=float).reshape(2,8,3)
    centered=(mm-mm[:,[0,4]].mean(axis=1)[:,None])/1000
    assert np.array_equal(centered[:,0]+centered[:,4],np.zeros((2,3)))
    checks['root_center_and_mm_to_m']=True
    receipt={'status':'passed_independent_target_audit_synthetic_checks','date':'2026-10-25',
             'checks':checks,'code_sha256':sha(Path(__file__)),'real_data_or_models_read':False,
             'optimizer_steps':0,'producer_imported':False}
    write_once(ROOT/'target_audit_synthetic_v3.json',receipt)
    return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--experiments-root',type=Path)
    p.add_argument('--release-dir',type=Path,default=ROOT/'train_v1')
    p.add_argument('--output',type=Path)
    p.add_argument('--synthetic-test',action='store_true')
    args=p.parse_args()
    if args.synthetic_test:
        print(json.dumps(synthetic_checks()));return
    if args.experiments_root is None:p.error('--experiments-root required for a real audit')
    print(json.dumps(run_audit(args.experiments_root,args.release_dir,args.output)))


if __name__=='__main__':main()
