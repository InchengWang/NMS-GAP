# Novelty Boundaries and Nearest Prior Work

**Evidence cutoff:** 2026-09-01  
**Rule:** every proposed advancement is defined relative to the nearest work found during counter-evidence search. The proposal does not claim that online calibration, sparse sensing, fatigue modeling, patient-specific simulation, or uncertainty-aware control are individually new.

## Claim-to-prior matrix

| Proposed advancement to test | Nearest prior work | What that work already establishes | Residual condition tested here | Language permitted in the proposal |
|---|---|---|---|---|
| Decision-specific sensor selection with calibrated posterior uncertainty across patient sessions | [Rabbi et al. (2024)](https://doi.org/10.1007/s10237-024-01825-7); [Bueno & Montano (2017)](https://doi.org/10.1088/1741-2552/aa58f5); [Zhang et al. (2023)](https://doi.org/10.3389/fnins.2023.1254088) | Sparse EMG can preserve a knee-contact-force estimate; online Bayesian self-calibration and NMS-informed uncertainty have both been demonstrated. | Whether a deployable multimodal subset preserves a prespecified NMS state or decision across days, with identifiable parameters, calibrated coverage, and explicit failure detection. | “Tests the unresolved joint requirement of cross-session observability, calibrated uncertainty, and decision preservation.” |
| Longitudinal two-timescale patient-state update | [MyoSuite](https://proceedings.mlr.press/v168/caggiano22a.html); [Pizzolato et al. (2020)](https://doi.org/10.3389/fbioe.2020.00878); [100-day EMG adaptation study](https://doi.org/10.3389/fresc.2022.981990) | Simulation supports fatigue/pathology perturbations; personalized tissue strain and long-term neuromuscular adaptation have been studied separately. | Whether within-session fatigue and across-week adaptation can be separately identified, externally anchored, and used to improve locked future-session prediction in the same patient-bound NMS model. | “Integrates and tests two physiological timescales that nearest studies address separately.” |
| Uncertainty-gated safe assistance under dropout and shift | [Zhang et al. (2023)](https://doi.org/10.3389/fnins.2023.1254088); [Jin & Guo (2023)](https://doi.org/10.1038/s41598-023-46885-4); [Xu et al. (2025)](https://doi.org/10.1109/TCYB.2025.3545064); [minimal-sensor policy distillation](https://doi.org/10.1186/s12984-025-01854-y) | Confidence-bound assistance, disturbance-robust control, human–robot parameter estimation and reduced-sensor policies already exist. | Whether posterior miscalibration, sensor loss and physiological load constraints can jointly determine abstention or fallback in a patient-conditioned NMS loop. | “Evaluates a combined uncertainty-to-action safety contract not established by the nearest component studies.” |
| Locked prediction of an unseen context or assistance condition | [NMSM Pipeline](https://doi.org/10.1186/s12984-025-01629-5); [Uhlrich et al. (2025)](https://doi.org/10.1016/S2665-9913(25)00151-1); [experiment-free exoskeleton assistance](https://doi.org/10.1038/s41586-024-07382-4) | Executable patient-specific treatment optimization, clinical benefit from personalized gait retraining, and simulation-to-hardware assistance have been demonstrated. | Whether a synchronized mechanistic NMS posterior predicts an individual response outside calibration before refitting, and whether that prediction remains safe enough to change a rehabilitation/device decision. | “Extends nearest work through preregistered, held-out patient-response prediction; it does not claim model-guided intervention is new.” |
| Patient-conditioned Embodied-AI evaluation | [MyoSuite](https://proceedings.mlr.press/v168/caggiano22a.html); [Ou et al. (2026)](https://doi.org/10.3390/healthcare14111523); [MyoAssist 1.0](https://doi.org/10.64898/2026.08.25.746839) | Muscle-driven control benchmarks, pathology-informed policies using stroke data, and standardized human–device simulations are available. | Whether a policy conditioned on an identified patient posterior improves out-of-distribution response without exploiting simulator errors or violating physiological constraints. | “Patient-posterior-conditioned and exploitation-audited extension of existing embodied NMS platforms.” |

## Claims explicitly excluded

The proposal must not state or imply that:

- it is the first human digital twin, NMS model, EMG-driven model, or uncertainty-aware controller;
- sparse or minimal sensing is inherently novel;
- IMU reconstruction establishes neural, muscle or tissue-state observability;
- fatigue, motor learning or tissue remodeling have not been studied;
- model-guided intervention has not improved clinical outcomes;
- a generic MyoSuite/MyoAssist policy is a patient digital twin;
- accurate joint angles, joint moments or reward alone validate internal NMS states;
- completion of Aim 1 or Aim 2 alone constitutes an `L5` digital twin.

## Digital-twin claim gate

The integrated system may be described as approaching a longitudinal NMS digital twin only if it demonstrates all of the following:

1. explicit binding to an identified patient;
2. repeated physical-to-digital updates across sessions;
3. a neural–muscle–skeletal mechanistic or physiologically constrained state;
4. validation outside calibration data;
5. calibrated uncertainty that changes an action, abstention, or fallback;
6. externally measured functional or biomechanical consequences.

If any item is missing, the output should be named more narrowly: a personalized model (`L1`), digital shadow (`L2`), predictive model (`L3`), or closed-loop prototype (`L4`).

## Proposal evidence provenance

The nearest-work set above is inherited from:

- [`../01_literature_mapping/`](../01_literature_mapping/), the 60-paper first-pass map;
- [`../02_paper_critiques/`](../02_paper_critiques/), the 49 core-paper critical reading;
- [`../03_gap_validation/`](../03_gap_validation/), including counter-evidence searches and controlled verdicts.

The proposal should be re-searched immediately before submission because G01, G03, G05, G07 and G08 are active `partially-addressed` areas.

