# Human Neuromusculoskeletal Embodied-AI Gap Validation

**Search cutoff:** 2026-09-01  
**Starting candidates:** ten falsifiable claims derived from the cross-cutting limitations in [`../01_core_paper_critiques/SUMMARY.md`](../01_core_paper_critiques/SUMMARY.md).  
**Evidence base:** the 60-paper literature map, 49 core-paper critiques, prior digital-twin counter-evidence, new Embodied-AI/robotics searches, selected clinical trials and recent work through the cutoff.

The dossiers judge the stated candidate—not a weaker rewritten version. A broad candidate can be `not-a-gap` while a narrower residual question remains useful.

## Summary matrix

| ID | Candidate | Primary gap type | Verdict | Feasibility for current base | Proposal decision |
|---|---|---|---|---|---|
| EAI-G01 | Identifiable patient-posterior-conditioned control | Scientific | `partially-addressed` | Medium in simulation; low for patient hardware | Advance narrowly |
| EAI-G02 | Patient-grounded sim-to-real with internal NMS validity | Engineering implementation | `partially-addressed` | Medium | Advance in stages |
| EAI-G03 | Longitudinal patient NMS–controller co-adaptation | Scientific | `confirmed-open` | Low as written; medium for two timescales | Core long-term thesis theme |
| EAI-G04 | Uncertainty-to-action safety under sensing/model shift | Robotics control | `partially-addressed` | High in simulation; medium HIL | Strong near-term pilot |
| EAI-G05 | Neural engagement and tissue safety as control objectives | Scientific | `partially-addressed` | Medium with EMG; low with tissue truth | Advance with one internal endpoint |
| EAI-G06 | Learned muscle policies lack physiological validation | Scientific | `not-a-gap` | High for a narrower patient audit | Do not use broad claim |
| EAI-G07 | Sparse/reconstructed IMUs are an Embodied-AI gap | Sensor substitution | `not-a-gap` | High technically; weak thesis novelty | Use only as enabling robustness work |
| EAI-G08 | Patient-conditioned embodied control improves durable recovery | Clinical translation | `partially-addressed` | Low without clinical partner | Late-stage collaborative aim |
| EAI-G09 | Patient-bound real–sim–device benchmark | Engineering implementation | `partially-addressed` | Medium–high as software; medium scientifically | Strong secondary contribution |
| EAI-G10 | Cross-population and device-fit validity | Clinical translation | `partially-addressed` | Low with current cohort | Prespecified validation axis |

---

## EAI-G01 — Identifiable patient-posterior-conditioned embodied control

- **Candidate gap:** Embodied NMS controllers are not conditioned on an identifiable posterior over a real patient's neural, muscle–tendon and impairment states.
- **Primary gap type:** **Scientific gap**, with a secondary robotics-control component. The scientific question is whether the latent patient state is identifiable and causally useful; implementing a policy conditioned on arbitrary patient parameters would only be engineering.
- **Falsifiable form:** The claim would be false if an existing physical patient study inferred a calibrated NMS posterior from patient data, conditioned control on that posterior, and showed better held-out interaction than coarse pathology parameters or trajectory conditioning.
- **Why it matters:** A controller can appear personalized while responding only to kinematic phenotype. If weakness, abnormal synergy, stiffness or fatigue are not distinguishable, the same assistance may reinforce compensation or generate unsafe internal load.
- **Supporting evidence:** The 49-paper critique separates strong subject-specific NMS estimation (NMS005, NMS009, NMS017), patient neuromechanical robot control (ROB001), fast RL-based NMS personalization (NMS010) and pathology-conditioned policies. These elements are not jointly validated.
- **Counter-evidence searched:** `patient-specific musculoskeletal RL`, `pathology-informed personalized exoskeleton`, `Bayesian NMS policy`, `subject-specific neuromusculoskeletal controller`, `posterior-conditioned policy`, stroke gait transfer and physical patient deployment.
- **Closest existing work:** [Berman et al. (2024)](https://doi.org/10.1109/TNSRE.2024.3483150) uses RL to personalize an EMG-driven model and control a virtual hand; [Durandau et al. (2019)](https://doi.org/10.1186/s12984-019-0559-z) closes a patient neuromechanical exoskeleton loop; [Ou et al. (2026)](https://doi.org/10.3390/healthcare14111523) adapts a pathology-informed policy using data from 50 stroke survivors, but the patient data are trajectory targets and evaluation is offline.
- **Remaining limitation:** The nearest work uses a fitted point model, residual EMG, virtual interaction, coarse weakness/synergy augmentation or observed kinematics. It does not show that the patient parameters are identifiable, that posterior uncertainty is calibrated, or that conditioning on that posterior improves an unseen physical interaction.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Medium in simulation/offline; low for immediate patient hardware.** Existing IMU/mocap data can condition movement phenotype but cannot identify neural/muscle states. A defensible main study needs targeted EMG and external-force constraints.
- **Next pilot test:** Estimate a small posterior over two or three interpretable states—such as paretic strength scale, synergy weight and session sensor gain—from one condition. Compare posterior-conditioned, point-estimate and kinematic-conditioned policies on a locked speed/support condition. Stop if posterior states do not contract or do not change the action/constraint profile.
- **Would change verdict:** A multi-patient physical study satisfying posterior identification, calibration, policy conditioning and held-out interaction would close the residual gap.

## EAI-G02 — Patient-grounded sim-to-real with internal NMS validity

- **Candidate gap:** Muscle-driven policies can transfer from simulation to real hardware, but their internal neural/muscle behavior is not validated in the target patient.
- **Primary gap type:** **Engineering implementation gap**, with a robotics-control validation component. The existence of a sim-to-real pipeline is engineering; whether its internal state represents the human requires scientific validation.
- **Falsifiable form:** The gap would be false if a patient-conditioned muscle-driven policy were deployed physically and independently validated against patient EMG/kinetics or another internal NMS measure under conditions not used for training.
- **Why it matters:** A policy can reduce task error or metabolic cost while exploiting simulator dynamics, using non-physiological muscle recruitment, or transferring poorly to impaired users.
- **Supporting evidence:** The core set's Embodied-AI papers are mainly `E2` simulation; the strongest physical systems are `E3–E4` but usually use generic simulation, point personalization or non-mechanistic objectives.
- **Counter-evidence searched:** `musculoskeletal RL sim-to-real`, `experiment-free exoskeleton`, `co-adaptive exoskeleton policy`, `patient-specific simulation-to-real stroke`, human EMG/biomechanical validation and MyoAssist.
- **Closest existing work:** [Luo et al. (2024)](https://doi.org/10.1038/s41586-024-07382-4) transfers a musculoskeletal simulation-trained policy to a physical hip exoskeleton and shows metabolic benefit in healthy adults; [SMAT](https://arxiv.org/abs/2603.07618) models staged human–device co-adaptation and reaches healthy-user hardware; its [physiological validation](https://arxiv.org/abs/2608.00715) reports metabolic benefit in eight healthy adults; [Ou et al. (2026)](https://doi.org/10.3390/healthcare14111523) adds stroke-data adaptation but remains offline.
- **Remaining limitation:** Healthy-user metabolic and mechanical validation do not establish patient-specific neural/muscle validity. Offline stroke trajectory matching is not physical transfer. No inspected work jointly provides patient binding, internal NMS validation, hardware interaction and an unseen-condition test.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Medium.** A recorded-data or hardware-in-the-loop bridge is feasible; patient deployment requires device access, clinical supervision and safety review.
- **Next pilot test:** Train a generic and posterior-conditioned policy, then lock an unseen speed or support condition. Compare simulated muscle activation and joint load with held-out EMG/kinetics before any hardware test. Add parameter/domain randomization and explicitly search for high reward with implausible activation or force.
- **Would change verdict:** A patient hardware study with independent internal-state validation and locked-condition transfer would make the broad gap no longer defensible.

## EAI-G03 — Longitudinal patient NMS–controller co-adaptation

- **Candidate gap:** A rehabilitation embodied agent should distinguish fast fatigue/sensor change from slow human motor recovery while the controller and patient adapt to one another over days or weeks.
- **Primary gap type:** **Scientific gap**, with clinical-translation and robotics-control dependencies. The central question is the coupled dynamics of human and controller, not merely implementing online tuning.
- **Falsifiable form:** The gap would be false if an existing patient study jointly tracked identifiable NMS states and controller changes across repeated rehabilitation sessions, separated at least two timescales, and linked them to retained functional or neurophysiological outcomes.
- **Why it matters:** A controller that interprets temporary fatigue as recovery may reduce assistance incorrectly; one that ignores motor learning may over-assist and suppress engagement. Cross-sectional personalization cannot answer this.
- **Supporting evidence:** The critique found rapid within-session adaptation, generic co-adaptive simulation, long-term prosthesis learning and multi-week robot rehabilitation, but not their joint NMS-state/controller identification.
- **Counter-evidence searched:** `human–robot co-adaptation`, `longitudinal adaptive exoskeleton`, `myoelectric co-adaptation`, `assist-as-needed weeks`, `motor learning retention`, `patient NMS adaptation`, SMAT, stroke/SCI trials and prosthesis incremental learning.
- **Closest existing work:** [Concurrent human–machine myoelectric adaptation](https://pubmed.ncbi.nlm.nih.gov/25680209/) demonstrates real-time co-learning; [Di Domenico et al. (2026)](https://doi.org/10.1109/TNSRE.2026.3657400) studies incremental co-adaptive three-DoF prosthesis control; [SMAT](https://arxiv.org/abs/2603.07618) explicitly stages human/exoskeleton adaptation in simulation and healthy hardware; a [stroke aAAN pilot](https://doi.org/10.1371/journal.pone.0292627) uses EMG/EEG and adaptive challenge; multi-week assist-as-needed trials test functional change in stroke/SCI.
- **Remaining limitation:** These studies demonstrate co-learning, physiological engagement, repeated therapy or functional outcome in different combinations. None of the inspected nearest work jointly identifies a mechanistic patient NMS state, separates fast and slow change, updates the controller from that state, and validates retained recovery.
- **Verdict:** `confirmed-open` for this narrow joint claim. This does not mean co-adaptation or longitudinal robotic rehabilitation is absent.
- **Feasibility:** **Low as written; medium for a two-timescale pilot.** It needs repeated patient sessions and clinical partnership. A PhD should start with fatigue/recovery versus cross-session baseline change rather than motor learning, plasticity and tissue remodeling together.
- **Next pilot test:** Collect two controlled bouts within each of four repeated sessions. Fit a fast fatigue/recovery state and a slow session state; compare with one-state and per-session recalibration baselines on a locked future session. Update only one controller parameter and test whether uncertainty prevents incorrect assistance changes.
- **Would change verdict:** A longitudinal patient NMS–controller study satisfying the full joint criteria would reduce this to `partially-addressed` or `not-a-gap`.

## EAI-G04 — Uncertainty-to-action safety under sensor and model shift

- **Candidate gap:** Embodied NMS systems do not reliably convert predictive uncertainty, sensor dropout and physiological constraints into verified safe assistance, attenuation or abstention.
- **Primary gap type:** **Robotics control gap**, with an engineering implementation component. Mechanical stability alone does not close the NMS physiological-safety problem.
- **Falsifiable form:** The gap would be false if a patient NMS controller demonstrated calibrated uncertainty under distribution shift, detected realistic sensing failure, activated a verified fallback and bounded both device and physiological risk.
- **Why it matters:** High-confidence model error is more dangerous than average prediction error when commands are applied to a weak or impaired person.
- **Supporting evidence:** The core physical systems rarely report posterior coverage, out-of-distribution calibration, sensor-fault detection and tissue/neural safety together.
- **Counter-evidence searched:** `uncertainty-aware NMS exoskeleton`, Bayesian torque bounds, prescribed-performance RL, safe/robust MPC, sensor dropout, policy distillation, safety filters, physiological constraints and hardware tests.
- **Closest existing work:** [Zhang et al. (2023)](https://doi.org/10.3389/fnins.2023.1254088) streams NMS-informed torque confidence bounds to a knee exoskeleton; [Zhang et al. (2026)](https://doi.org/10.1109/TCYB.2025.3632289) combines prescribed performance, safety boundaries and RL on a physical rehabilitation exoskeleton; [minimal-sensor policy distillation](https://doi.org/10.1186/s12984-025-01854-y) reduces sensing dependence; robust musculoskeletal-exoskeleton RL handles randomized impairment and interaction forces.
- **Remaining limitation:** Confidence intervals are not consistently calibrated under placement drift/dropout; control-theoretic tracking bounds do not bound muscle/tissue risk; and safe fallback is rarely evaluated in patients under compound sensing and model failure.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **High in simulation and offline replay; medium in hardware-in-the-loop.** It is the strongest immediate pilot for the user's missing-sensor and rotation expertise.
- **Next pilot test:** Inject measured dropout, rotation, drift and latency into locked sessions. Compare deterministic, ensemble/Bayesian and conformal/OOD wrappers. Predefine continue/attenuate/abstain modes and report interval coverage, false-safe rate, detection delay, decision degradation and a physiological proxy—not reconstruction PCC alone.
- **Would change verdict:** A multi-patient study validating calibration, fallback and physiological safety during realistic failures would close the residual.

## EAI-G05 — Neural engagement and tissue safety as control objectives

- **Candidate gap:** Embodied rehabilitation controllers optimize task success, kinematics or metabolic cost without jointly preserving voluntary neural engagement and safe internal tissue/muscle loading.
- **Primary gap type:** **Scientific gap**, with clinical-translation consequences. Choosing a multi-objective reward is engineering; establishing which internal states cause better recovery or safety is scientific.
- **Falsifiable form:** The gap would be false if an existing patient controller jointly measured and acted on voluntary neural engagement and a validated internal-load endpoint, then improved an external rehabilitation outcome.
- **Why it matters:** A robot can improve trajectory tracking while the user slacks, or reduce muscle effort by transferring excessive load to tissue. Neither is necessarily therapeutic.
- **Supporting evidence:** The core set contains neural-engagement measurement (ROB009), EMG-driven assistive control (ROB001), tissue-aware feedback (NMS014), imaging-guided robotic muscle targeting (NMS018) and metabolic HIL optimization (ROB005), but they optimize different endpoints.
- **Counter-evidence searched:** EMG/EEG assist-as-needed, muscle-effort control, neural engagement, tissue-load feedback, knee-contact/tendon-strain objectives, metabolic HIL, rehabilitation RCTs and multi-objective safe control.
- **Closest existing work:** [EMG-based assist-as-needed hand control](https://pubmed.ncbi.nlm.nih.gov/34206714/) adjusts robot assistance from muscle effort in four stroke patients; the [stroke aAAN pilot](https://doi.org/10.1371/journal.pone.0292627) measures EMG and EEG engagement; [Pizzolato et al. (2020)](https://doi.org/10.3389/fbioe.2020.00878) provides real-time personalized Achilles strain feedback; [Wang et al. (2026)](https://doi.org/10.1109/TNSRE.2026.3663395) uses imaging-personalized muscle targets to select robotic therapy.
- **Remaining limitation:** Engagement-aware systems generally lack validated tissue/load state; tissue-aware systems lack closed adaptive robot control and recovery outcomes. The causal relation between the combined internal objectives and durable recovery is not established.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Medium for neural engagement; low for direct tissue truth.** Start with EMG-derived voluntary contribution plus joint/load proxy; do not claim tissue safety without a validated surrogate or imaging/force reference.
- **Next pilot test:** Compare trajectory-only and engagement-aware assistance in a controlled crossover. Hold task success constant and test whether the latter increases paretic voluntary EMG without increasing joint-load proxy or instability. Use a measured-signal baseline and preregister a stop threshold.
- **Would change verdict:** A patient trial showing joint neural-engagement/internal-load control and retained functional benefit would close the stated gap.

## EAI-G06 — Physiological validation of learned muscle policies

- **Candidate gap:** Learned muscle-driven policies have not been validated against human neural or muscle activation patterns.
- **Primary gap type:** Proposed **scientific gap**.
- **Falsifiable form:** The broad claim is false if learned muscle policies have already been compared with experimental human EMG/biomechanics and shown physiological agreement beyond kinematic imitation.
- **Why it matters:** Without physiological checks, a policy may reproduce motion through unrealistic recruitment and provide misleading motor-control conclusions.
- **Supporting evidence:** Many core Embodied-AI papers primarily report reward, task success or kinematics, and the critique identifies simulator-defined outcomes as a recurring weakness.
- **Counter-evidence searched:** `musculoskeletal RL EMG validation`, physiological plausibility, muscle synergy-guided RL, motion imitation, full-body muscle control, experimental biomechanics and human activation comparison.
- **Closest existing work:** [KINESIS](https://arxiv.org/abs/2503.14637) reports human-EMG correlation for learned lower-body motion imitation; [MuscleMimic](https://arxiv.org/abs/2603.25544) validates kinematics against walking/running data and explicitly analyzes activation limitations; [MUSIC](https://arxiv.org/abs/2604.23886) compares muscle activation with human EMG; [Han et al. (2026)](https://doi.org/10.1109/TBME.2026.3651379) injects synergy priors into embodied musculoskeletal RL.
- **Remaining limitation:** Patient-specific pathological neural drive, motor-unit behavior, deep-muscle activation, tissue load and unseen-task physiology remain weak. That is a narrower validation problem, not the original broad gap.
- **Verdict:** `not-a-gap`.
- **Feasibility:** **High for a narrower audit** using public gait/EMG data and existing simulators.
- **Next pilot test:** Do not claim physiological validation is absent. Select one stroke or impaired-gait condition and compare generic versus patient-conditioned policies on held-out EMG synergy structure, timing and external mechanics. Treat mismatch as a model-falsification result.
- **Would change verdict:** Not applicable to the broad claim; future evidence can only refine which populations and internal states remain unvalidated.

## EAI-G07 — Sparse or reconstructed IMUs as an Embodied-AI research gap

- **Candidate gap:** Reducing or reconstructing IMU channels is itself an open human NMS Embodied-AI gap.
- **Primary gap type:** **Sensor substitution gap**, not a scientific gap unless tied to an independently validated state or action.
- **Falsifiable form:** The claim is false if sparse sensing, learned reconstruction or privileged-to-minimal policy transfer already preserves motion/control outputs, making the remaining work task-specific engineering.
- **Why it matters:** Lower sensor burden is useful, but treating it as the research center can disconnect the work from body-state validity, control safety and rehabilitation outcomes.
- **Supporting evidence:** Wearable burden and sensor failure limit deployment; the user's current work demonstrates that missing lower-limb IMU signals can be reconstructed and evaluated through gait events.
- **Counter-evidence searched:** sparse-to-dense IMU, minimal-sensor exoskeleton control, policy distillation, OpenSense/OpenCap, sparse EMG/synergy reconstruction, sensor selection and control under dropout.
- **Closest existing work:** [Minimal-sensor policy distillation](https://doi.org/10.1186/s12984-025-01854-y) trains a rehabilitation-exoskeleton policy using only onboard proprioception/root orientation; OpenSense/OpenCap provide reduced-burden kinematics pipelines; [Rabbi et al. (2024)](https://doi.org/10.1007/s10237-024-01825-7) reduces EMG burden for a decision-relevant NMS output.
- **Remaining limitation:** It remains useful to test whether a chosen sensor subset preserves a specific NMS state, policy action and safety decision across patients, sessions and failures. That is decision-preservation/robustness, not generic sensor reconstruction novelty.
- **Verdict:** `not-a-gap` as stated.
- **Feasibility:** **High technically, weak as standalone PhD novelty.** Existing stroke IMU data are ideal for an enabling pilot.
- **Next pilot test:** Feed measured versus reconstructed/sparse inputs into a locked controller or decision model. Report action divergence, false-safe rate and downstream clinical/functional error under session shift. Stop if reconstruction accuracy does not translate to decision preservation.
- **Would change verdict:** A reformulated claim about formal decision-specific observability or safety could be `partially-addressed`; changing sensor modality alone cannot.

## EAI-G08 — Durable rehabilitation benefit from patient-conditioned embodied control

- **Candidate gap:** Patient-conditioned embodied control has not been shown to improve retained recovery or participation relative to fixed/guidance control.
- **Primary gap type:** **Clinical translation gap**. Robot therapy efficacy in general is not the gap; attribution to a patient-conditioned embodied control mechanism is.
- **Falsifiable form:** The gap would be false if a controlled patient trial compared a patient-conditioned/adaptive controller with an appropriate fixed or guidance controller, demonstrated retained functional benefit, and linked the difference to the modeled patient state or control mechanism.
- **Why it matters:** Acute assistance and higher step counts do not necessarily induce recovery. Clinical adoption needs evidence that adaptation changes learning, engagement or function beyond therapy dose.
- **Supporting evidence:** The core `E3–E4` systems emphasize feasibility, metabolic benefit, task performance or single-patient results. Durable clinical outcomes are seldom linked to a mechanistic NMS controller.
- **Counter-evidence searched:** adaptive/assist-as-needed RCTs, exoskeleton versus conventional therapy, active versus passive robot training, stroke/SCI retention, neuroplasticity, engagement and model-informed rehabilitation.
- **Closest existing work:** A [six-week stroke RCT](https://www.sciencedirect.com/science/article/pii/S0003999318313959) found greater functional improvement for active assist-as-needed than guidance control; an [SCI controlled trial](https://pmc.ncbi.nlm.nih.gov/articles/PMC5469353/) showed controller feasibility but not differential arm-function gain; a [2026 assistive-versus-passive stroke RCT](https://doi.org/10.1016/j.apmr.2025.08.021) reports different neuronal remodeling; multicenter and other exoskeleton RCTs demonstrate clinical recovery but generally do not test a patient NMS embodied controller.
- **Remaining limitation:** Adaptive robotic rehabilitation and clinical effects are real, so “no outcome evidence” is false. What remains is causal attribution of retained benefit to an identifiable patient-conditioned NMS state/control policy rather than therapy intensity, trajectory design or generic AAN behavior.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Low without clinical partnership.** A definitive RCT is not an initial PhD experiment.
- **Next pilot test:** Run a small randomized or counterbalanced feasibility study comparing fixed and state-adaptive assistance while matching repetitions/time. Include retention, voluntary EMG and a functional measure. Use the result to estimate effect/variance rather than claim efficacy.
- **Would change verdict:** A sufficiently powered controlled trial with mechanism mediation and retained patient benefit would close the residual gap.

## EAI-G09 — Patient-bound real–sim–device benchmark

- **Candidate gap:** The field lacks an open benchmark that binds synchronized patient data to a muscle-driven simulator and assistive device with locked sim-to-real and rehabilitation metrics.
- **Primary gap type:** **Engineering implementation gap**. It becomes a scientific contribution only if the benchmark tests a meaningful hypothesis about patient conditioning, transfer or failure.
- **Falsifiable form:** The gap would be false if one open resource jointly provided patient sensor/biomechanics data, calibrated patient models, device/task environments, training splits and locked physical/clinical evaluation metrics.
- **Why it matters:** Current algorithms, models and robots are evaluated on incompatible bodies, tasks and outcomes, allowing improvements to reflect benchmark choice rather than better human embodiment.
- **Supporting evidence:** The critique found reproducible generic simulators and fragmented patient/device studies, but no common patient-bound comparison pipeline.
- **Counter-evidence searched:** MyoAssist, MyoSuite/MyoChallenge, AddBiomechanics, clinical motion datasets, stroke sim-to-real, OpenSim patient datasets, assistive-device benchmarks and standardized exoskeleton metrics.
- **Closest existing work:** [MyoAssist 1.0](https://doi.org/10.64898/2026.08.25.746839) standardizes composed human–device–task simulations across 15 devices; [AddBiomechanics](https://doi.org/10.1371/journal.pone.0295152) provides 273-subject motion/force/dynamics data; [Ou et al. (2026)](https://doi.org/10.3390/healthcare14111523) uses data from 50 stroke survivors for offline policy adaptation; MyoChallenge standardizes simulated control evaluation.
- **Remaining limitation:** Simulation platforms, human datasets and clinical policy studies exist separately. Patient-model calibration targets, sensor noise, physical device interaction and locked transfer/rehabilitation metrics are not packaged together in the inspected resources.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Medium–high as software, medium as science.** A minimal benchmark can use one patient dataset and one device/task, but missing GRF/EMG/device forces will limit physiological claims.
- **Next pilot test:** Convert a locked stroke subset to a versioned OpenSim/MyoAssist representation, publish calibration/test manifests and compare generic versus patient-conditioned policies on kinematics, available external mechanics and decision robustness. Stop if missing signals make patient parameters unidentifiable.
- **Would change verdict:** A public patient-data + bound simulator + device + locked-metric release would make the broad packaging gap `not-a-gap`.

## EAI-G10 — Cross-population, morphology and device-fit validity

- **Candidate gap:** Human NMS embodied systems are not validated across sex, age, anthropometry, impairment severity and device fit with subgroup-calibrated safety and performance.
- **Primary gap type:** **Clinical translation gap**, with scientific and engineering components. Recruiting a diverse sample alone is translation; explaining which anatomy/impairment states cause controller failure is scientific.
- **Falsifiable form:** The broad claim would be false if embodied NMS controllers were externally validated across representative patient/morphology strata and reported subgroup calibration, safety, fit and functional outcomes.
- **Why it matters:** A controller trained on generic anatomy or young healthy users can change interaction forces, comfort and assistance effectiveness in underrepresented users.
- **Supporting evidence:** The core set contains small healthy cohorts, coarse pathology randomization and very limited patient closed-loop evidence.
- **Counter-evidence searched:** demographic representation, sex/age/anthropometry, device fit, pathology domain randomization, universal controllers, patient-specific morphology and subgroup exoskeleton outcomes.
- **Closest existing work:** A [2026 systematic review](https://doi.org/10.1016/j.apergo.2026.104808) analyzes 191 occupational-exoskeleton papers and finds predominantly young male samples and limited demographic analysis; [Leibman & Choi (2023)](https://doi.org/10.1177/21695067231192559) directly evaluates body mass, sex and fitness in human–exoskeleton interaction; robust simulated controllers randomize muscle weakness; Ou et al. uses heterogeneous stroke trajectories.
- **Remaining limitation:** Demographic effects, pathology augmentation and robust control are being studied, so the topic is not untouched. Complete patient sensor→NMS state→action pipelines rarely report subgroup calibration, device fit, uncertainty and harm/failure together.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Low as the main project with the current small cohort.** It is feasible as a prespecified audit, followed by multi-site validation if a partner dataset is secured.
- **Next pilot test:** Define available strata before modeling. Fit a hierarchical error/safety model for morphology, severity and device condition; report uncertainty where subgroup size is inadequate. Do not claim fairness or generalizability from balanced mean error.
- **Would change verdict:** A representative multi-site embodied-control benchmark with subgroup-calibrated outcomes and documented failure modes would close the residual.

---

## Priority recommendation

### Advance now

**EAI-G04 + a narrowed EAI-G01/EAI-G02:** use the current missing-sensor expertise to build a failure-aware observation layer, but evaluate it through a patient-conditioned NMS action or decision. The minimum publishable pilot is locked-session policy/decision preservation with calibrated abstention—not higher reconstruction correlation.

### Core scientific PhD theme

**EAI-G03:** longitudinal patient NMS–controller co-adaptation, initially limited to two timescales and one assistance parameter. This is the strongest scientific gap but requires a clinical/robotics partner and should not be the first experiment.

### Translational expansion

**EAI-G05 + EAI-G08:** connect adaptive assistance to one internal mechanism (for example voluntary neural engagement) and one retained functional outcome. Direct tissue claims require stronger measurement.

### Strong secondary contribution

**EAI-G09:** a patient-bound benchmark can make the thesis reproducible, provided it tests a scientific transfer/failure question rather than only repackaging data.

### Do not use as primary novelty

- EAI-G06 is contradicted by recent EMG/biomechanics validation of learned muscle policies.
- EAI-G07 is sensor substitution unless it changes state observability, action or safety.
- EAI-G10 should be a prespecified validation axis until a representative cohort is available.

