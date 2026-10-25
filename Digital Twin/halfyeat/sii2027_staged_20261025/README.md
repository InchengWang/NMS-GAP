# Staged sparse-IMU development pilot (2026-10-25)

Five new TCN fits; one frozen same-person VALID diagnostic. All data, training and result audits passed. This code is an original adapter inspired by sparse-to-dense reconstruction and position-based intermediate representations; it is not an official BSN/TransPose reproduction.

The full [report](../SII2027_STAGED_RECONSTRUCTION_20261025_ZH.md), [aggregate results](../SII2027_STAGED_AGGREGATES_20261025.json), [audit summary](../SII2027_STAGED_READINESS_20261025.json) and [function/SHA index](../SII2027_STAGED_CODE_INDEX_20261025.json) define the accepted scope. `STUDY_DESIGN_ZH.md` and `valid_contract_notes.md` preserve prospective design/preparation wording; the linked report gives the completed state.

The source dataset and its earlier frozen release/matching inventories are private. Raw data, fitted scalers, checkpoints, per-frame predictions and papers are excluded. These source files make the executed logic reviewable; cloning this public directory alone does not reproduce the real-data fits.

Environment: Python3.10.12, NumPy2.2.6, PyTorch2.5.1, CPU2 threads. The model forward accepts only measured shank observations `[B,T,12]`. Auxiliary labels/masks are supplied only to loss or metrics.

Execution order: TRAIN export → independent TRAIN target audit → `train_study.py prepare` → `train_study.py train` → independent TRAIN fit audit → freeze `eval_study.py freeze --experiments-root <release-root>` → separate VALID export authorization → VALID export → `audit_valid_diagnostic.py targets --experiments-root <release-root>` → `eval_study.py evaluate` → `audit_valid_diagnostic.py results`.

`probe_models.py` and target/auditor synthetic checks can be inspected without patient data. Their saved receipts retain their exact source SHAs. Immutable outputs must not be overwritten. No TEST loading or model selection is part of this pilot.
