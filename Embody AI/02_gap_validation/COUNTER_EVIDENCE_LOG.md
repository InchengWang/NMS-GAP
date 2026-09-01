# Counter-Evidence Search Log — Human NMS Embodied AI

**Search date:** 2026-09-01  
**Sources searched:** existing NMS-GAP map and 49-paper critique; PubMed/PMC; publisher pages; PMLR/NeurIPS; recent preprints and project documentation; targeted web search; selected rehabilitation trials.  
**Purpose:** find work that would invalidate each candidate, including adjacent prosthetics, rehabilitation robotics, biomechanics and motor-control terminology.

## Query and nearest-work log

| Gap | Counter-query families | Strongest counter-evidence inspected | Why it does not fully close the residual |
|---|---|---|---|
| EAI-G01 | `patient-specific musculoskeletal RL`; `posterior-conditioned policy`; `pathology-informed exoskeleton`; `Bayesian NMS control`; stroke physical transfer | Berman 2024; Durandau 2019; Ou 2026 | Patient binding, control and pathology adaptation exist, but not identifiable/calibrated patient posterior → held-out physical policy benefit. |
| EAI-G02 | `musculoskeletal RL sim-to-real`; `experiment-free assistance`; `SMAT`; patient EMG/kinetics validation | Luo 2024; SMAT 2026; Ou 2026 | Physical transfer is healthy; patient work is offline; internal NMS validation is not jointly demonstrated. |
| EAI-G03 | `human–robot co-adaptation`; `longitudinal exoskeleton`; `myoelectric co-learning`; `AAN weeks`; retention/neuroplasticity | Hahne 2015; Di Domenico 2026; SMAT; stroke aAAN; multi-week AAN trials | Co-learning, repeated therapy and outcomes exist separately; mechanistic patient NMS state and controller are not co-identified over two timescales. |
| EAI-G04 | `uncertainty-aware NMS control`; Bayesian torque bounds; safe/prescribed-performance RL; sensor dropout; robust MPC | Zhang 2023 NMS-BNN; Zhang 2026 SPP-RL; minimal-sensor distillation; robust MSK-RL | Mechanical bounds and uncertainty estimates exist, but calibrated compound-failure → physiology-aware patient fallback is not established. |
| EAI-G05 | EMG/EEG engagement; muscle-effort AAN; tissue load/strain feedback; metabolic HIL; multi-objective rehab control | stroke aAAN; EMG hand AAN; Pizzolato 2020; Wang 2026; Zhang 2017 | Neural engagement and tissue/load objectives are not jointly controlled and tied to retained recovery. |
| EAI-G06 | `musculoskeletal RL EMG validation`; physiological plausibility; synergy-guided RL; motion imitation | KINESIS; MuscleMimic; MUSIC; Han 2026 | These directly falsify the broad claim; only patient/pathology-specific physiological validation remains. |
| EAI-G07 | sparse/dense IMU; minimal sensors; privileged distillation; OpenSense/OpenCap; sparse EMG | minimal-sensor policy distillation; Rabbi 2024; wearable pipelines | Sensor reduction is established as an engineering method; action/safety preservation remains task-specific. |
| EAI-G08 | adaptive/AAN RCT; active vs passive robot; stroke/SCI retention; neuroplasticity | stroke six-week AAN RCT; SCI AAN trial; 2026 active/passive RCT; multicenter exoskeleton trials | Adaptive robot therapy and outcomes exist; benefit attributable to an identifiable patient NMS policy remains unclear. |
| EAI-G09 | MyoAssist; MyoChallenge; AddBiomechanics; patient OpenSim datasets; stroke sim-to-real | MyoAssist 1.0; AddBiomechanics; Ou 2026 | Platform, data and patient policy work are separate; no single patient-bound real–sim–device benchmark with locked metrics. |
| EAI-G10 | demographic representation; sex/age/BMI; anthropometry; device fit; pathology randomization; universal controller | Kazemi 2026 review; Leibman & Choi 2023; robust weakness-randomized policies | Components are studied, but subgroup calibration/safety of the complete embodied pipeline is weak. |

## Selected counter-evidence register

| Work | Gap(s) challenged | Key counter-evidence |
|---|---|---|
| [Berman et al., 2024](https://doi.org/10.1109/TNSRE.2024.3483150) | G01 | RL rapidly personalizes an EMG-driven NMS model and supports online virtual-hand control. |
| [Durandau et al., 2019](https://doi.org/10.1186/s12984-019-0559-z) | G01, G05 | Patient residual EMG drives subject-specific neuromechanical exoskeleton control. |
| [Ou et al., 2026](https://doi.org/10.3390/healthcare14111523) | G01, G02, G09, G10 | Pathology-informed policy adaptation uses gait data from 50 stroke survivors, but evaluation is offline. |
| [Experiment-free exoskeleton assistance](https://doi.org/10.1038/s41586-024-07382-4) | G02 | Simulation-trained policy reaches healthy-user hardware and reduces metabolic cost across tasks. |
| [SMAT](https://arxiv.org/abs/2603.07618) and [physiological follow-up](https://arxiv.org/abs/2608.00715) | G02, G03 | Models staged human/device adaptation, transfers to healthy hardware and reports metabolic benefit. |
| [Concurrent human–machine myoelectric adaptation](https://pubmed.ncbi.nlm.nih.gov/25680209/) | G03 | Demonstrates simultaneous user/controller learning in a closed myoelectric loop. |
| [Di Domenico et al., 2026](https://doi.org/10.1109/TNSRE.2026.3657400) | G03 | Incremental co-adaptation for three-DoF prosthesis control. |
| [Stroke physiological aAAN pilot](https://doi.org/10.1371/journal.pone.0292627) | G03, G05, G08 | Adaptive robot challenge is evaluated with EMG, EEG and performance in chronic stroke. |
| [Zhang et al., 2023](https://doi.org/10.3389/fnins.2023.1254088) | G04 | NMS-informed Bayesian/GP torque confidence bounds stream to knee-exoskeleton assistance. |
| [Soft prescribed-performance RL](https://doi.org/10.1109/TCYB.2025.3632289) | G04 | Physical rehabilitation-exoskeleton experiments enforce tracking safety boundaries under degradation/disturbance. |
| [Minimal-sensor policy distillation](https://doi.org/10.1186/s12984-025-01854-y) | G04, G07 | Privileged teacher–student training reduces deployable sensing to onboard measurements in simulation. |
| [Pizzolato et al., 2020](https://doi.org/10.3389/fbioe.2020.00878) | G05 | Real-time personalized tendon-strain feedback provides an internal tissue endpoint. |
| [EMG-based hand-exoskeleton AAN](https://pubmed.ncbi.nlm.nih.gov/34206714/) | G05 | Assistance changes from measured muscle effort in four stroke patients. |
| [KINESIS](https://arxiv.org/abs/2503.14637) | G06 | Learned muscle activity is compared with human EMG in a locomotion imitation framework. |
| [MuscleMimic](https://arxiv.org/abs/2603.25544) | G06, G09 | Scalable full-body muscle control includes biomechanics validation and analyzes activation fidelity. |
| [MUSIC](https://arxiv.org/abs/2604.23886) | G06 | Dexterous muscle-driven policies are checked against human EMG patterns. |
| [Han et al., 2026](https://doi.org/10.1109/TBME.2026.3651379) | G06 | Muscle synergy priors directly guide embodied musculoskeletal RL. |
| [Six-week stroke AAN trial](https://www.sciencedirect.com/science/article/pii/S0003999318313959) | G08 | Active-assist control outperforms guidance on selected functional outcomes. |
| [SCI AAN controlled trial](https://pmc.ncbi.nlm.nih.gov/articles/PMC5469353/) | G08 | Demonstrates longitudinal adaptive-therapy feasibility but not differential arm-function gain. |
| [MyoAssist 1.0](https://doi.org/10.64898/2026.08.25.746839) | G02, G09 | Standardizes composed human–device–task simulation and controller evaluation for 15 devices. |
| [AddBiomechanics](https://doi.org/10.1371/journal.pone.0295152) | G09 | Open 273-subject motion/force/dynamics benchmark. |
| [Kazemi et al., 2026](https://doi.org/10.1016/j.apergo.2026.104808) | G10 | Reviews 191 exoskeleton papers and directly audits demographic representation/outcome differences. |
| [Leibman & Choi, 2023](https://doi.org/10.1177/21695067231192559) | G10 | Tests body mass, sex and fitness effects in human–exoskeleton interaction. |

## Search limits

- Scopus and Web of Science were not exhaustively searched as independent citation databases.
- Several 2026 results are preprints or ahead-of-print articles and require rechecking before proposal submission.
- Proprietary exoskeleton controllers, device trials and non-English rehabilitation literature may contain additional counter-evidence.
- Clinical-trial registries were sampled rather than exhaustively screened for every device/population.
- EAI-G03 receives `confirmed-open` only for the narrow joint criteria; the verdict should be re-run before a doctoral proposal or grant claim.
- EAI-G10 needs a formal subgroup-data audit across the full literature, not only selected counter-evidence.

