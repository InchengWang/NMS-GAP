"""Descriptive TRAIN-only auxiliary signal screen; never filters the cohort.

The numerical thresholds are descriptive reference levels. Device full-scale,
mounting and hardware synchronization are not certified by this screen.
"""
from pathlib import Path
import json,hashlib
import numpy as np

ROOT=Path(__file__).resolve().parent
NAMES=('S3_ACC','S3_GYRO','S4_ACC','S4_GYRO','S5_ACC','S5_GYRO')

def rebuild():
    p=ROOT/'train_v1/manifest.json';manifest=json.loads(p.read_text())
    if manifest['roles']!={'TRAIN':31,'VALID':0,'TEST':0}:raise PermissionError('Only complete TRAIN support is allowed.')
    values={i:[] for i in range(6)};rows=[]
    for row in manifest['parents']:
        if row['split']!='TRAIN':raise PermissionError('Heldout role refused before array hash/read.')
        q=ROOT/'train_v1'/row['path']
        if q.resolve().parent!=(ROOT/'train_v1').resolve():raise PermissionError('Unexpected source path.')
        if hashlib.sha256(q.read_bytes()).hexdigest()!=row['sha256']:raise RuntimeError('Array identity changed.')
        with np.load(q,allow_pickle=False) as z:
            if z['split'].item()!='TRAIN':raise PermissionError('Stored role differs.')
            for g in range(6):
                sl=slice(3*g,3*g+3);mask=z['sensor_mask'][:,sl]
                if mask.any():
                    if not mask.all():raise RuntimeError('Expected parent-wise modality availability.')
                    a=z['sensor_target'][:,sl].astype(np.float64);values[g].append(a)
                    rows.append({'parent_id':row['parent_id'],'group':g,'frames':len(a),'max_abs_axis_SI':float(np.abs(a).max())})
    groups={}
    for g,parts in values.items():
        a=np.concatenate(parts);acc=g%2==0;t=15.9*9.80665 if acc else 1990*np.pi/180
        groups[NAMES[g]]={'frames':len(a),'units':'m/s^2' if acc else 'rad/s','max_abs_axis':float(np.abs(a).max()),
            'norm_percentiles_0_50_99_100':np.percentile(np.linalg.norm(a,axis=1),[0,50,99,100]).tolist(),
            'fraction_axis_values_over_descriptive_threshold':float(np.mean(np.abs(a)>=t)),
            'descriptive_threshold_SI':t,'threshold_is_not_a_verified_device_fullscale':True}
    return {'status':'descriptive_TRAIN_aux_physical_screen_no_selection_or_training_change',
        'TRAIN_manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'groups':groups,
        'per_parent_maxima':rows,'VALID_TEST_arrays_read':0,'new_fits':0,
        'purpose':'screen_extreme_measurements_without_cohort_filtering_not_hardware_or_mounting_certification'}

if __name__=='__main__':
    actual=rebuild();saved=json.loads((ROOT/'TRAIN_aux_physical_qc.json').read_text())
    if actual!=saved:raise RuntimeError('Descriptive screen differs from preserved receipt.')
    print(json.dumps({'status':'reproduced_preserved_TRAIN_descriptive_screen','groups':actual['groups']}))
