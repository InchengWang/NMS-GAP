# Literature-motivated baseline prototypes

These independently written modules support a proposed matched-input benchmark. They are **not full paper reproductions and not a completed training/evaluation pipeline**.

- `architecture_baselines.py`: three-layer unidirectional Hur-style LSTM128 and project-specific LSTM85 capacity control. Input `[B,T,12]`, output `[B,T,6]` or `[B,T,2]`; each call resets recurrent state. Compared with the source article, measured inputs, task head and common context are adapted.
- `measurement_augmentations.py`: fixed-SD SI noise and parent-constant gyro bias, motivated by Choi and Lee 2023. These are orientation-to-joint-regression adaptations, not measured device-noise distributions.

The probes use synthetic arrays only, perform no optimizer step and load no patient data or checkpoint. Run them with a Python environment containing NumPy and PyTorch:

```bash
python probe_architecture_baselines.py
python probe_measurement_augmentations.py
```

The first writes `probe_receipt.json`; the second writes `measurement_probe_receipt.json`. Published receipts record the local versions and source hashes. They establish interface/property checks only. Parent/view RNG ownership, full-parent generation before windowing, TRAIN-only access, scaling, model selection, independent training audit and performance evaluation belong to a future benchmark runner and remain unimplemented here.

`noise_plus_bias` is available for later experiments but is outside the primary six-cell plan. No author repository source was copied into these modules. Literature details and the proposed comparison matrix are in [the baseline report](../SII2027_LITERATURE_BASELINES_20261025_ZH.md).
