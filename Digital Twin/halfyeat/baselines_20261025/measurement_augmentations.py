"""Independent SI measurement-error controls for a proposed regression benchmark.

Motivation: Choi and Lee, Sensors 23(17):7458 (2023),
doi:10.3390/s23177458. The source task is nine-axis orientation estimation,
not joint-angle regression. This is a fixed-magnitude, six-axis adaptation,
not a complete paper reproduction or a measured noise model of our devices.

Apply once to a full TRAIN parent/view, before the real-TRAIN scaler, and then
extract overlapping windows. Constant bias stays constant over that parent.
Labels and timestamps are not accepted by this API and are not transformed.
No data loader, parameter fitting, or split/role permission is implemented.
"""
from __future__ import annotations
import numpy as np

ACC_COLUMNS = np.array([0, 1, 2, 6, 7, 8])
GYRO_COLUMNS = np.array([3, 4, 5, 9, 10, 11])
ACC_NOISE_SD_M_S2 = 0.02
GYRO_NOISE_SD_RAD_S = float(np.deg2rad(0.15))
GYRO_BIAS_SD_RAD_S = float(np.deg2rad(0.5))
POLICIES = ('replay', 'measurement_noise', 'constant_gyro_bias', 'noise_plus_bias')

def corrupt_parent_si(measured: np.ndarray, rng: np.random.Generator,
                      policy: str) -> np.ndarray:
    """Return [T,12] measured input in m/s^2 and rad/s; never mutate input.

    Column order is left ACC xyz / GYRO xyz then right ACC xyz / GYRO xyz.
    The caller must supply an independent TRAIN-parent/view RNG and enforce
    roles. This function cannot determine whether an array belongs to TRAIN.
    Fixed SDs avoid the source paper's ambiguous signed-SD description; they
    are a declared simplification. Post-filter injection is a model-input
    corruption control, not a simulation of a complete native sensor process.
    """
    x = np.asarray(measured)
    if x.ndim != 2 or x.shape[1] != 12 or x.shape[0] < 1:
        raise ValueError('Expected a nonempty [time,12] parent.')
    if x.dtype not in (np.dtype('float32'), np.dtype('float64')):
        raise ValueError('Input must be float32 or float64 SI values.')
    if not np.isfinite(x).all():
        raise ValueError('Nonfinite input is not an augmentation candidate.')
    if policy not in POLICIES:
        raise ValueError('Unknown declared corruption policy.')
    out = x.astype(np.float64, copy=True)
    if policy in ('measurement_noise', 'noise_plus_bias'):
        out[:, ACC_COLUMNS] += rng.normal(0.0, ACC_NOISE_SD_M_S2,
                                         size=(len(x), len(ACC_COLUMNS)))
        out[:, GYRO_COLUMNS] += rng.normal(0.0, GYRO_NOISE_SD_RAD_S,
                                          size=(len(x), len(GYRO_COLUMNS)))
    if policy in ('constant_gyro_bias', 'noise_plus_bias'):
        out[:, GYRO_COLUMNS] += rng.normal(0.0, GYRO_BIAS_SD_RAD_S,
                                          size=(1, len(GYRO_COLUMNS)))
    return out.astype(x.dtype, copy=False)

def provenance() -> dict:
    return {'paper_doi':'10.3390/s23177458',
            'source_task':'nine_axis_orientation_estimation',
            'project_task':'twelve_input_joint_kinematics_regression',
            'exact_article_reproduction':False,
            'implementation':'independent_fixed_SD_SI_control',
            'ACC_noise_SD_m_s2':ACC_NOISE_SD_M_S2,
            'GYRO_noise_SD_rad_s':GYRO_NOISE_SD_RAD_S,
            'GYRO_bias_SD_rad_s':GYRO_BIAS_SD_RAD_S,
            'sample_axis':'full_parent_once_then_window',
            'bias_constant_over_time':True,
            'real_device_error_distribution_verified':False,
            'roles_enforced_by_this_module':False}
