# Novelty Boundaries and Nearest Prior Work

**Proposal:** Human neuromusculoskeletal Embodied AI  
**Evidence cutoff:** 2026-09-01  
**Source dossier:** [`../02_gap_validation/`](../02_gap_validation/)  
**Rule:** every advancement below is a hypothesis to test against named prior work. The proposal does not use publication scarcity as evidence of novelty.

## Claim-to-prior matrix

| Proposed advancement to test | Validated gap | Nearest prior work | Already established | Residual condition tested here | Permitted wording |
|---|---|---|---|---|---|
| An identifiable patient NMS posterior that changes embodied action under an unseen condition | EAI-G01, `partially-addressed` | [Berman et al. (2024)](https://doi.org/10.1109/TNSRE.2024.3483150); [Durandau et al. (2019)](https://doi.org/10.1186/s12984-019-0559-z); [Ou et al. (2026)](https://doi.org/10.3390/healthcare14111523) | Rapid NMS personalization, patient neuromechanical robot control and pathology-informed stroke-policy adaptation each exist. | Whether a calibrated posterior over a small, interpretable patient state is practically identifiable and improves a locked action/response relative to point, kinematic and coarse-pathology conditioning. | “Tests the unresolved joint requirement of posterior identifiability, calibration and held-out control relevance.” |
| Patient-grounded simulation-to-interaction with independent internal NMS validation | EAI-G02, `partially-addressed` | [Luo et al. (2024)](https://doi.org/10.1038/s41586-024-07382-4); [SMAT](https://arxiv.org/abs/2603.07618); [SMAT physiological study](https://arxiv.org/abs/2608.00715); [Ou et al. (2026)](https://doi.org/10.3390/healthcare14111523) | Muscle-driven policies have transferred to healthy-user hardware, achieved physiological benefit and used patient gait for offline pathology adaptation. | Whether the target patient's EMG/kinetics independently validate the policy's internal NMS behavior under an interaction condition excluded from training. | “Extends existing sim-to-real work to patient-bound internal-state validation under locked conditions.” |
| Uncertainty-to-action safety under compound sensing and model shift | EAI-G04, `partially-addressed` | [Zhang et al. (2023)](https://doi.org/10.3389/fnins.2023.1254088); [soft prescribed-performance RL](https://doi.org/10.1109/TCYB.2025.3632289); [minimal-sensor policy distillation](https://doi.org/10.1186/s12984-025-01854-y) | NMS confidence bounds, control safety envelopes and reduced-sensor policies have been demonstrated separately. | Whether calibrated sensing/model uncertainty and a physiological constraint jointly select `continue`, `attenuate`, `fallback` or `abstain`, reducing false-safe actions in patient-conditioned control. | “Evaluates a combined uncertainty-to-action contract beyond the nearest component solutions.” |
| Control that preserves voluntary engagement without worsening a validated load proxy | EAI-G05, `partially-addressed` | [EMG hand-exoskeleton AAN](https://pubmed.ncbi.nlm.nih.gov/34206714/); [stroke physiological aAAN](https://doi.org/10.1371/journal.pone.0292627); [Pizzolato et al. (2020)](https://doi.org/10.3389/fbioe.2020.00878); [Wang et al. (2026)](https://doi.org/10.1109/TNSRE.2026.3663395) | EMG/EEG engagement-aware assistance, personalized tissue feedback and imaging-informed robotic targeting exist. | Whether one controller can act on voluntary engagement and an independently checked internal-load proxy while matching external task success. | “Tests joint internal-objective control; it does not claim engagement-aware or tissue-aware rehabilitation is absent.” |
| Two-timescale patient NMS–controller co-adaptation across repeated sessions | EAI-G03, `confirmed-open` | [Concurrent human–machine myoelectric adaptation](https://pubmed.ncbi.nlm.nih.gov/25680209/); [Di Domenico et al. (2026)](https://doi.org/10.1109/TNSRE.2026.3657400); [SMAT](https://arxiv.org/abs/2603.07618); [stroke physiological aAAN](https://doi.org/10.1371/journal.pone.0292627) | Online human–machine learning, incremental prosthesis adaptation, staged exoskeleton co-adaptation and physiological adaptive rehabilitation have all been demonstrated. | Whether an identifiable patient NMS state and one controller parameter can be co-updated while separating fast fatigue/recovery from slower across-session change and predicting retention. | “Tests a narrow joint criterion not found in the nearest work; co-adaptation itself is not claimed as new.” |
| Retained benefit attributable to a patient-conditioned NMS mechanism | EAI-G08, `partially-addressed` | [Six-week stroke AAN trial](https://www.sciencedirect.com/science/article/pii/S0003999318313959); [SCI AAN trial](https://pmc.ncbi.nlm.nih.gov/articles/PMC5469353/); [active-versus-passive stroke trial](https://doi.org/10.1016/j.apmr.2025.08.021) | Adaptive robotic rehabilitation and functional/neurophysiological outcomes already have controlled clinical evidence. | Whether a state-adaptive controller changes retained outcome at matched therapy dose, and whether the identified patient state mediates that change. | “Examines mechanism-attributable retention; it does not claim adaptive robot therapy lacks clinical evidence.” |
| A patient-bound real–sim–device evaluation package | EAI-G09, `partially-addressed` | [MyoAssist 1.0](https://doi.org/10.64898/2026.08.25.746839); [AddBiomechanics](https://doi.org/10.1371/journal.pone.0295152); [Ou et al. (2026)](https://doi.org/10.3390/healthcare14111523) | Reusable human–device simulators, large biomechanics data and patient-data policy adaptation exist separately. | Whether synchronized patient data, calibrated NMS state, device/task model, locked splits and failure metrics can be released as one reproducible test of patient conditioning. | “Provides a patient-bound benchmark for the thesis hypotheses; benchmark packaging alone is not the scientific claim.” |

## Claims explicitly excluded

The proposal must not state or imply that:

- muscle-driven Embodied AI, musculoskeletal reinforcement learning or human–robot co-adaptation is new;
- simulation-to-hardware exoskeleton assistance has not been achieved;
- patient-specific NMS modeling or EMG-driven wearable-robot control is absent;
- uncertainty-aware control, robust control, safety envelopes or minimal-sensor policies are individually new;
- learned muscle policies have never been compared with human EMG or biomechanics;
- sparse-to-dense IMU reconstruction is a neuromusculoskeletal Embodied-AI contribution by itself;
- more accurate joint angles, reconstructed signals, task reward or tracking prove a valid internal NMS representation;
- a small acute feasibility study demonstrates rehabilitation efficacy;
- a subject-specific simulator is automatically a digital twin.

## Subject-specific digital-representation gate

The proposal uses a subject-specific digital representation only if all four conditions are met:

1. it is bound to measurements from the target participant;
2. its selected latent states or parameters pass practical-identifiability and calibration checks;
3. it predicts an interaction condition not used for fitting;
4. replacing it with a generic, point-personalized or kinematic-only representation changes a prespecified action, safety decision or response prediction.

If these conditions fail, the component must be named an estimator, personalized model or policy context—not a digital twin. The overall thesis remains Embodied AI because its defining object is the closed perception–body–action–interaction loop.

## Publication-level claim templates

- **Aim 1:** “We evaluate whether a calibrated low-dimensional patient NMS posterior is identifiable and action-sufficient under held-out interaction.”
- **Aim 2:** “We test whether combining patient-state uncertainty, sensor/model shift and physiological constraints reduces false-safe assistance relative to established robust and confidence-bound controllers.”
- **Aim 3:** “We test whether separating fast and slow patient changes improves longitudinal co-adaptation and retained prediction relative to static, session-recalibrated and one-timescale alternatives.”

These statements should be re-run against current nearest work immediately before submission.
