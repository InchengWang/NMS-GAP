# Counter-Evidence Search Log

**Search date:** 2026-09-01  
**Sources searched:** existing NMS-GAP map and critiques; PubMed/PMC; publisher pages; PMLR/NeurIPS; ClinicalTrials.gov; project documentation/GitHub; targeted web and preprint searches.  
**Purpose:** find work that would invalidate each gap, including terminology-mismatched work outside explicit “digital twin” literature.

## Query and nearest-work log

| Gap | Counter-query families | Strongest counter-evidence inspected | Why it does not fully close the narrowed residual |
|---|---|---|---|
| G01 | `online NMS self-calibration`; `sequential Bayesian`; `wearable identifiability`; `NMS uncertainty exoskeleton`; `hierarchical Bayesian muscle parameters` | Bueno & Montano 2017; Zhang et al. 2023 NMS-BNN; Hambly et al. 2025; Johnson et al. 2026 preprint | Each addresses calibration, uncertainty or online control, but not calibrated multi-parameter posterior and unseen-session patient validation together. |
| G02 | `multi-timescale NMS`; `fatigue motor learning remodeling`; `longitudinal EMG adaptation`; `nonstationary MyoSuite`; `tendon mechanobiology twin` | MyoSuite fatigue/sarcopenia; Pizzolato et al. 2020 Achilles model; 100-day EMG adaptation study | Components live in separate models/studies; no patient-bound cross-timescale state inference and validation. |
| G03 | `patient-specific musculoskeletal RL`; `pathology-informed`; `domain randomization`; `experiment-free exoskeleton`; `impaired gait policy sim-to-real` | Luo et al. 2024 hardware deployment; Ou et al. 2026 stroke-data adaptation; Choi et al. 2026 preprint; MyoAssist | Patient use is offline/simulated; physical deployment is mainly healthy and not tied to a calibrated patient posterior or explicit exploitation audit. |
| G04 | `prospective treatment prediction`; `simulation-guided surgery`; `model-guided rehabilitation trial`; `predictive gait treatment`; ClinicalTrials.gov | SimCP; NMSM Pipeline; Uhlrich et al. 2025 RCT; NCT06008743 | Counterfactual simulation and clinical personalization exist, but pre-treatment mechanistic NMS prediction of the held-out patient response is not jointly established. |
| G05 | `uncertainty-aware NMS control`; `sensor dropout exoskeleton`; `robust/chance-constrained MPC`; `safety filter`; `minimal sensors` | Zhang et al. 2023 confidence-bound control; Jin & Guo 2023; Xu et al. 2025; minimal-sensor policy distillation | Mechanical robustness/torque confidence is not full physiological safety; dropout-to-safe-fallback and distribution-shift calibration remain weak. |
| G06 | `randomized personalized gait retraining`; `model-informed clinical outcome`; `pain function MRI`; ClinicalTrials.gov | Uhlrich et al. 2025, n=68, 1-year RCT; NCT06008743 model-informed stroke study | It directly falsifies the broad “no clinical endpoint evidence” claim, though it does not validate a full NMS twin. |
| G07 | `minimal multimodal sensors`; `sensor selection`; `sparse EMG synergies`; `IMU identifiability`; `privileged sensor distillation` | Rabbi et al. 2024; synergy extrapolation 2022; minimal-sensor DRL; explicit IMU identifiability analyses | Minimum sets are endpoint/task-specific; internal NMS-state observability, independent truth and cross-session uncertainty are not combined. |
| G08 | `MyoSuite patient data`; `clinical musculoskeletal benchmark`; `AddBiomechanics`; `MyoAssist`; `sim-to-real patient dataset` | AddBiomechanics; MyoAssist 0.1/1.0; MyoChallenge | Data and environments now exist, but a synchronized patient dataset bound to the simulator with locked sim-to-real metrics is not yet packaged; MyoAssist's motion library is planned. |
| G09 | `sex-specific MSK`; `age PCSA`; `pediatric scaling`; `morphology bias`; `clinical scaling validation` | Shen et al. 2026 review; Dalman et al. 2022; pediatric shape model 2024; age/sex PCSA review | Demographic components are studied, but complete pipeline failure and uncertainty across clinical populations/devices remain under-tested. |
| G10 | `HDT governance`; `ownership auditability`; `clinician uncertainty`; `ethical digital twin healthcare`; `regulatory oversight` | 2026 healthcare HDT governance review; Saxby et al. 2023; HDT master plans | General governance principles substantially exist; missing NMS implementations are an application/governance problem rather than core NMS novelty. |

## Selected counter-evidence register

| Work | Gap(s) challenged | Key counter-evidence |
|---|---|---|
| [Bueno & Montano, 2017](https://doi.org/10.1088/1741-2552/aa58f5) | G01 | Online sequential Bayesian self-calibration from uncalibrated sEMG/kinematics in 21 subjects. |
| [Zhang et al., 2023](https://doi.org/10.3389/fnins.2023.1254088) | G01, G05 | NMS-informed BNN/GP produces torque uncertainty bounds and streams assistance to a knee exoskeleton. |
| [Hambly et al., 2025](https://doi.org/10.1109/ICORR66766.2025.11062981) | G01, G02 | Continuous real-time NMS calibration reaches offline-level performance within 15 cycles/110 s. |
| [MyoSuite](https://proceedings.mlr.press/v168/caggiano22a.html) | G02, G03, G08 | Open muscle-driven tasks include fatigue, sarcopenia, tendon transfer and assistance variations. |
| [Pizzolato et al., 2020](https://doi.org/10.3389/fbioe.2020.00878) | G02, G04 | Real-time personalized multiscale Achilles strain estimation links load to a mechanobiological target. |
| [Experiment-free exoskeleton assistance](https://doi.org/10.1038/s41586-024-07382-4) | G03 | Simulation-trained policy transfers to physical hardware and reduces healthy-user metabolic cost across tasks. |
| [Ou et al., 2026](https://doi.org/10.3390/healthcare14111523) | G03 | Pathology-informed RL uses gait data from 50 stroke survivors for offline personalized assistance evaluation. |
| [NMSM Pipeline](https://doi.org/10.1186/s12984-025-01629-5) | G04 | Open patient-specific treatment optimization and predictive simulation pipeline. |
| [Uhlrich et al., 2025](https://doi.org/10.1016/S2665-9913(25)00151-1) | G04, G06 | 68-person randomized personalized gait-retraining trial with one-year pain, load and cartilage MRI endpoints. |
| [NCT06008743](https://clinicaltrials.gov/study/NCT06008743) | G04, G06 | Ongoing 72-participant model-informed patient-specific stroke rehabilitation study. |
| [Minimal-sensor policy distillation](https://doi.org/10.1186/s12984-025-01854-y) | G05, G07 | Teacher–student policy reduces an exoskeleton controller to onboard proprioceptive sensing in simulation. |
| [Rabbi et al., 2024](https://doi.org/10.1007/s10237-024-01825-7) | G07 | Synergy-informed NMS modeling reduces EMG burden for knee-contact-force estimation in cerebral palsy. |
| [AddBiomechanics](https://addbiomechanics.org/download_data.html) | G08 | Large open physically processed human-motion/force/inverse-dynamics datasets. |
| [MyoAssist 1.0](https://doi.org/10.64898/2026.08.25.746839) | G03, G08 | Open composed human–device–task framework with 15 assistive devices and shared evaluation. |
| [Shen et al., 2026](https://doi.org/10.1080/10255842.2026.2656284) | G09 | Explicit review of the sex/gender blind spot in personalized knee modeling. |
| [Healthcare HDT review, 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13328380/) | G10 | Four-tier data/model/clinical/regulatory governance framework. |

## Areas not exhaustively searched

- Subscription-only Scopus and Web of Science citation indices were not searched exhaustively or independently duplicated.
- Trial registries outside ClinicalTrials.gov and non-English protocols may contain additional ongoing work.
- Very recent workshop papers, theses, patents and proprietary clinical/device systems may not be indexed.
- G09 needs a formal demographic-data audit across all 49 core papers rather than selected counter-evidence.
- G10 would require jurisdiction-specific analysis of medical-device, AI, privacy and data-ownership law; this review only determines relevance to the NMS technical research gap.

Because of these limits, only G02 receives `confirmed-open`; uncertain or rapidly moving areas remain `partially-addressed` rather than being called first/unexplored.
