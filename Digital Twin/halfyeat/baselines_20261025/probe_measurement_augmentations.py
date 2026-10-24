"""Synthetic-only property checks; not a training or data-access preflight."""
from pathlib import Path
import json,hashlib
import numpy as np
from measurement_augmentations import corrupt_parent_si,provenance,ACC_COLUMNS,GYRO_COLUMNS,POLICIES

ROOT=Path(__file__).resolve().parent
checks={}
x=np.random.default_rng(19).normal(size=(321,12)).astype(np.float64)
original=x.copy()
for policy in POLICIES:
    a=corrupt_parent_si(x,np.random.default_rng(25),policy)
    b=corrupt_parent_si(x,np.random.default_rng(25),policy)
    assert np.array_equal(a,b) and a.shape==x.shape and a.dtype==x.dtype
    assert np.array_equal(x,original) and not np.shares_memory(x,a)
    checks[policy+'_deterministic_no_input_mutation']=True
assert np.array_equal(corrupt_parent_si(x,np.random.default_rng(2),'replay'),x)
checks['replay_identity']=True
zero=np.zeros((200,12),dtype=np.float64)
b=corrupt_parent_si(zero,np.random.default_rng(3),'constant_gyro_bias')
assert np.array_equal(b[:,ACC_COLUMNS],zero[:,ACC_COLUMNS])
assert np.array_equal(b[:,GYRO_COLUMNS],np.repeat(b[:1,GYRO_COLUMNS],len(b),axis=0))
assert np.any(b[:,GYRO_COLUMNS]!=0)
checks['gyro_bias_constant_and_acc_unchanged']=True
z=np.zeros((100000,12),dtype=np.float64)
n=corrupt_parent_si(z,np.random.default_rng(33),'measurement_noise')
p=provenance();sa=float(n[:,ACC_COLUMNS].std());sg=float(n[:,GYRO_COLUMNS].std())
assert abs(sa/p['ACC_noise_SD_m_s2']-1)<.01
assert abs(sg/p['GYRO_noise_SD_rad_s']-1)<.01
checks['empirical_modality_SD_units']=True
assert corrupt_parent_si(z[:4].astype(np.float32),np.random.default_rng(4),'measurement_noise').dtype==np.float32
checks['float32_preserved']=True
blocked=0
for bad,pol in [(np.zeros((4,6)),'replay'),(np.zeros((0,12)),'replay'),(np.zeros((4,12),int),'replay'),(np.full((4,12),np.nan),'replay'),(np.zeros((4,12)),'undeclared')]:
    try:corrupt_parent_si(bad,np.random.default_rng(1),pol)
    except ValueError:blocked+=1
assert blocked==5
receipt={'status':'passed_synthetic_only_measurement_control_probe','date':'2026-10-25','checks':checks,
         'invalid_inputs_blocked':blocked,'empirical_ACC_noise_SD_m_s2':sa,'empirical_GYRO_noise_SD_rad_s':sg,
         'provenance':p,'real_data_or_weights_read':False,'optimizer_steps':0,'formal_training_fits':0,
         'benchmark_protocol_frozen':False,'training_role_guard_verified':False,
         'source_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['measurement_augmentations.py','probe_measurement_augmentations.py']}}
(ROOT/'measurement_probe_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'checks':len(checks),'invalid_inputs_blocked':blocked,'optimizer_steps':0}))
