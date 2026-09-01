# Gap Validation Dossiers

**Search cutoff:** 2026-09-01  
**Starting candidates:** the ten “Highest-priority uncovered questions” in [`../01_literature_mapping/CLUSTERS_AND_GAPS.md`](../01_literature_mapping/CLUSTERS_AND_GAPS.md).  
**Input evidence:** the 60-paper map, 49 core-paper critiques, new counter-evidence searches, selected trial records, and newly released work through the cutoff.

The dossiers judge the original candidate, not a more convenient rewritten version. A narrower residual question can remain useful even when the broad candidate is `not-a-gap`.

## Summary matrix

| ID | Candidate | Verdict | Feasibility for current research base | Proposal decision |
|---|---|---|---|---|
| G01 | Online identifiability with posterior uncertainty | `partially-addressed` | Medium | Advance only after narrowing |
| G02 | Multi-timescale physiological adaptation | `confirmed-open` | Low as written; medium for two timescales | Long-term thesis theme, not first pilot |
| G03 | Patient-specific Embodied AI and safe adaptation | `partially-addressed` | Medium for offline/simulation; low for patient hardware | Advance as staged program |
| G04 | Causal treatment prediction outside calibration | `partially-addressed` | Low–medium | Advance only with held-out intervention data |
| G05 | Closed-loop safety under uncertainty and sensor failure | `partially-addressed` | High in simulation; medium on hardware | Strong pilot candidate |
| G06 | Model-guided decisions improve clinical endpoints | `not-a-gap` | Low for a new trial | Do not use broad novelty claim |
| G07 | Minimal multimodal set for actionable NMS observability | `partially-addressed` | High when narrowed to measurable state | Strongest near-term pilot |
| G08 | Patient-grounded Embodied-AI benchmark alignment | `partially-addressed` | Medium–high as software/benchmark work | Secondary contribution |
| G09 | Demographic and morphological failure auditing | `partially-addressed` | Low with current cohort | Include as validation axis, not main claim |
| G10 | Ownership, audit and explanation governance | `out-of-scope` | Low without governance/HCI collaborators | Treat as deployment requirement |

---

## G01 — Online identifiability with posterior uncertainty

- **Candidate gap:** Which neural, muscle–tendon and joint parameters can be updated online from realistic wearable signals, and with what calibrated posterior uncertainty?
- **Falsifiable form:** The gap would be false if an existing human study jointly demonstrated online subject-specific NMS state/parameter inference from deployable sensing, diagnosed practical identifiability, reported calibrated posterior uncertainty, and validated it on unseen tasks/sessions.
- **Supporting evidence:** The core critique found frequent parameter compensation, same-task calibration/evaluation, sparse muscle coverage and almost no uncertainty propagation. NMS009 and NMS017 show that good output fit need not recover true parameters.
- **Counter-evidence searched:** `online/self-calibration`, `sequential Bayesian`, `Kalman`, `probabilistic NMS`, `hierarchical Bayesian`, `differentiable calibration`, `wearable identifiability`, plus EMG/exoskeleton terminology.
- **Closest existing work:** [Bueno & Montano (2017)](https://doi.org/10.1088/1741-2552/aa58f5) sequentially self-calibrated an NMS model from uncalibrated sEMG and kinematics in 21 participants; [Zhang et al. (2023)](https://doi.org/10.3389/fnins.2023.1254088) used an NMS-informed Bayesian neural network to output torque confidence bounds and drive a knee exoskeleton; [Hambly et al. (2025)](https://doi.org/10.1109/ICORR66766.2025.11062981) continuously calibrated an EMG-informed model within 110 s; a [2026 hierarchical Bayesian preprint](https://doi.org/10.64898/2026.07.08.737322) estimated six subject-specific elbow parameters with uncertainty.
- **Remaining limitation:** Existing papers cover online calibration, Bayesian estimation, parameter posterior or closed-loop uncertainty in different combinations. They do not jointly show that a multi-joint patient NMS parameter set is observable from realistic sparse sensing, that the posterior is calibrated across sessions/tasks, and that uncertainty distinguishes parameter non-identifiability from sensor noise/model mismatch.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Medium.** Retrospective wearable/mocap data can support a state-estimation and identifiability pilot; neural/muscle–tendon parameters require EMG, external-force or imaging constraints that the current IMU-only layers cannot supply.
- **Next pilot test:** Select a small state/parameter vector, fit it on one session with a state-space or Bayesian differentiable model, and evaluate posterior coverage on a locked session. Compare profile likelihood/Fisher information or posterior contraction across nested sensor sets. Stop if apparently personalized parameters do not remain stable or improve held-out prediction.
- **Would change verdict:** A patient study satisfying all four conditions—online update, explicit identifiability, calibrated posterior coverage and unseen-session validation—would move it to `not-a-gap`.

## G02 — Multi-timescale physiological adaptation

- **Candidate gap:** How should millisecond neural drive, minute-scale fatigue, week-scale motor learning and month-scale tissue remodeling coexist in one patient twin?
- **Falsifiable form:** The gap would be false if an implemented patient-bound NMS system estimated and validated at least neural control, fatigue/learning and tissue adaptation on their distinct timescales, with cross-timescale predictions.
- **Supporting evidence:** The 49 core critiques contain short-session online calibration, fatigue-capable simulators, motor-learning analyses and tissue-strain models, but no longitudinal system that co-estimates them. No core study reaches `L5`.
- **Counter-evidence searched:** `multi-timescale NMS`, `longitudinal digital twin`, `fatigue + motor learning + remodeling`, tendon mechanobiology, chronic EMG adaptation, non-stationary MyoSuite and online fatigue adaptation.
- **Closest existing work:** [MyoSuite](https://proceedings.mlr.press/v168/caggiano22a.html) exposes fatigue, sarcopenia and tendon-transfer variations; [Pizzolato et al. (2020)](https://doi.org/10.3389/fbioe.2020.00878) connects real-time neural/movement input to personalized Achilles strain and a remodeling target; a [100-day EMG study](https://doi.org/10.3389/fresc.2022.981990) measured individual neuromuscular training adaptation. These are complementary, not integrated.
- **Remaining limitation:** Fatigue is often a simulator parameter, motor learning a behavioral observation, and tissue adaptation an offline mechanobiological rule. Their latent states, update rates and causal coupling have not been jointly identified and validated in a longitudinal patient twin.
- **Verdict:** `confirmed-open`.
- **Feasibility:** **Low as written.** It needs repeated human data, mechanobiology expertise, multimodal measurement and months of follow-up. A tractable PhD version must choose two timescales and one clinically relevant tissue/function endpoint.
- **Next pilot test:** Fit a two-state model to repeated sessions: a fast within-session fatigue state and a slow cross-session baseline/skill state. Test whether it predicts a locked future session better than a single-state model and whether each latent state is separately identifiable. Do not add tissue remodeling until this falsification succeeds.
- **Would change verdict:** A published longitudinal patient system with cross-timescale external validation would reduce the verdict to `partially-addressed`.

## G03 — Patient-specific Embodied AI with safe adaptation

- **Candidate gap:** Can a learned muscle-driven policy be conditioned on a calibrated patient NMS model and safely adapt without exploiting simulator error?
- **Falsifiable form:** The gap would be false if a policy trained in a patient-calibrated NMS simulator adapted on physical patient/device data, retained physiological/safety constraints, and was evaluated for simulator exploitation and clinical function.
- **Supporting evidence:** MyoSuite/MyoDex/DynSyn/MS-Human-700 remain generic simulation substrates in the core critique; ROB007 uses pathology randomization but no physical patient validation.
- **Counter-evidence searched:** `patient-specific musculoskeletal RL`, `pathology-informed`, `motion imitation impaired gait`, `domain randomization`, `simulation-to-real exoskeleton`, `experiment-free assistance`, and 2026 assistive-device benchmarks.
- **Closest existing work:** [Luo et al. (2023)](https://doi.org/10.1186/s12984-023-01147-2) randomized muscle weakness in human–exoskeleton simulation; [Luo et al. (2024)](https://doi.org/10.1038/s41586-024-07382-4) deployed a simulation-trained policy to a physical hip exoskeleton with metabolic reductions in healthy participants; [Ou et al. (2026)](https://doi.org/10.3390/healthcare14111523) adapted a pathology-informed policy using gait data from 50 stroke survivors, but only offline trajectory-level evaluation; [MyoAssist 1.0](https://doi.org/10.64898/2026.08.25.746839) now standardizes human–device simulations.
- **Remaining limitation:** Patient data are typically used as target trajectories or coarse weakness/stiffness knobs, not as a calibrated NMS posterior. Hardware demonstrations are mainly healthy; clinical safety, online patient adaptation and tests for non-physiological simulator exploitation are not jointly reported.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Medium for an offline/simulation contribution; low for patient hardware within an initial project.** The current stroke gait data can condition kinematics/context but lacks enough internal-state ground truth for a full patient policy.
- **Next pilot test:** Build generic and patient-conditioned policies for recorded stroke gait in OpenSim/MyoAssist. Lock an unseen speed or assistive-device condition; stress-test weakness, abnormal synergy, sensor noise and model mismatch. Count physiological constraint violations as well as reward. Reject the route if personalization only improves imitation in-distribution.
- **Would change verdict:** Demonstrated online patient hardware adaptation with independent physiological and functional outcomes would make the original claim substantially closed.

## G04 — Causal treatment prediction outside calibration

- **Candidate gap:** Can a patient NMS twin predict individual response to assistance, FES, surgery or training outside the calibration distribution?
- **Falsifiable form:** The gap would be false if a personalized NMS model selected or predicted a treatment, before it occurred, and the held-out post-treatment response agreed at a clinically relevant endpoint.
- **Supporting evidence:** NMS011 provides executable counterfactual optimization but only a single illustrative post-stroke case; SimCP and multiscale pipelines remain mainly simulation/feasibility studies.
- **Counter-evidence searched:** `prospective treatment prediction`, `simulation-guided surgery`, `predictive gait simulation`, `model-guided rehabilitation trial`, knee-OA gait retraining, cerebral-palsy intervention and ClinicalTrials.gov.
- **Closest existing work:** [SimCP](https://doi.org/10.3389/fnbot.2019.00054) enables patient-specific virtual orthopedic intervention; the [NMSM Pipeline](https://doi.org/10.1186/s12984-025-01629-5) performs treatment optimization; [Uhlrich et al. (2025)](https://doi.org/10.1016/S2665-9913(25)00151-1) prospectively validated individualized load-reducing gait retraining over one year, but target selection used gait-load measurements rather than an online mechanistic NMS twin; [NCT06008743](https://clinicaltrials.gov/study/NCT06008743) is an ongoing 72-participant model-informed stroke rehabilitation study.
- **Remaining limitation:** Existing work separately demonstrates counterfactual simulation or personalized clinical intervention. Direct pre-intervention NMS prediction of a patient's unseen post-intervention neural, biomechanical and functional response remains weakly validated.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Low–medium.** A causal claim requires an intervention or natural experiment and locked predictions. A retrospective cane/no-cane or speed condition can only be a preliminary transport test, not causal clinical proof.
- **Next pilot test:** Calibrate on one recorded condition, preregister directional and quantitative predictions for a held-out condition, then test against the recorded response without refitting. Compare with a generic and purely data-driven baseline. Advance only if the mechanistic model improves unseen-condition prediction and uncertainty coverage.
- **Would change verdict:** A prospective multi-patient trial in which NMS predictions select an intervention and predict the external outcome would close the residual gap.

## G05 — Closed-loop safety under uncertainty and sensor failure

- **Candidate gap:** How should predictive uncertainty, sensor dropout and physiological constraints be converted into safe robot or stimulation actions?
- **Falsifiable form:** The gap would be false if a patient NMS controller propagated calibrated sensing/model uncertainty into an explicit safety policy, handled dropout, and demonstrated bounded human/device risk in realistic patient use.
- **Supporting evidence:** The core L4 prototypes usually report control error or short-session benefit, not calibrated uncertainty, fail-safe transitions, tissue limits or cross-day sensor faults.
- **Counter-evidence searched:** `uncertainty-aware NMS exoskeleton`, Bayesian torque bounds, robust/chance-constrained MPC, sensor failure/dropout, safety filter, prescribed-performance RL and privileged minimal-sensor control.
- **Closest existing work:** [Zhang et al. (2023)](https://doi.org/10.3389/fnins.2023.1254088) generated torque confidence bounds with an NMS-informed BNN/GP and streamed assistance to a knee exoskeleton; [Jin & Guo (2023)](https://doi.org/10.1038/s41598-023-46885-4) used an observer and MPC for uncertain/disturbed exoskeleton dynamics; [Xu et al. (2025)](https://doi.org/10.1109/TCYB.2025.3545064) combined robust MPC, estimated human–exoskeleton parameters and whole-body planning; [minimal-sensor policy distillation](https://doi.org/10.1186/s12984-025-01854-y) reduces sensor dependence but remains simulation-led.
- **Remaining limitation:** Confidence bounds are not consistently calibrated under distribution shift, sensor dropout is seldom tied to a verified safe fallback, and mechanical controller robustness is not the same as physiological safety for muscle/tissue load or patient intent.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **High in simulation, medium on hardware.** The existing sparse/dense wearable setup can test dropout detection and uncertainty-gated outputs without immediately commanding a robot.
- **Next pilot test:** Inject realistic missing sensors, placement rotations and drift into held-out sessions. Calibrate predictive intervals and define an abstain/fallback rule. Report false-safe rate, time to detect failure, coverage during transition and downstream gait-event/state error—not only average reconstruction accuracy.
- **Would change verdict:** A patient device study validating uncertainty calibration, dropout recovery and physiological safety constraints would make this no longer a defensible broad gap.

## G06 — Clinical endpoints from model-guided decisions

- **Candidate gap:** Do model-guided decisions improve function, pain, participation or recovery rather than only torque/angle prediction?
- **Falsifiable form:** The broad gap is false if individualized biomechanics/model-informed decisions have already improved a patient-centered endpoint in a controlled prospective study.
- **Supporting evidence:** Most NMS twin-enabling papers in the 49-paper core set remain technical feasibility studies or small device pilots.
- **Counter-evidence searched:** randomized/controlled gait retraining, model-informed rehabilitation, personalized exoskeleton clinical trials, pain/function/MRI endpoints and ClinicalTrials.gov.
- **Closest existing work:** The [68-participant randomized trial by Uhlrich et al.](https://doi.org/10.1016/S2665-9913(25)00151-1) selected person-specific foot-progression changes that reduced knee loading and, at one year, improved medial knee pain and loading and showed a favorable cartilage MRI signal versus sham. [NCT06008743](https://clinicaltrials.gov/study/NCT06008743) explicitly studies model-informed, patient-specific stroke rehabilitation with robotics/neuromuscular modeling.
- **Remaining limitation:** This evidence does not validate a continuously synchronized NMS digital twin, and generalization to stroke, SCI, FES or tissue-aware robot control remains open. That is a narrower population/system claim, not the original broad gap.
- **Verdict:** `not-a-gap`.
- **Feasibility:** **Low as a new standalone PhD novelty claim.** A clinical-outcome trial requires clinical partners, ethics, recruitment and longitudinal follow-up.
- **Next pilot test:** Do not pilot “clinical endpoints exist” as novelty. Attach an external functional endpoint to a narrower G01/G04/G05/G07 study, or define a specific untreated population/intervention and verify the absence of prior controlled evidence.
- **Would change verdict:** Not applicable; the broad claim is already falsified. New evidence can only refine where endpoint validation remains missing.

## G07 — Minimal multimodal sensing for actionable NMS observability

- **Candidate gap:** What is the minimum multimodal sensor set—not merely the fewest IMUs—that preserves clinically actionable NMS state?
- **Falsifiable form:** The gap would be false if prior work identified a minimum deployable sensor set using formal observability/identifiability criteria and showed that it preserves an independently validated neural/muscle/tissue or decision endpoint across patients and sessions.
- **Supporting evidence:** OpenSense/OpenCap and sparse-EMG methods reduce burden, but most evaluate angles, moments or reconstruction rather than whether the latent NMS state needed for a decision remains identifiable.
- **Counter-evidence searched:** `minimal sensors`, `sensor selection`, `privileged distillation`, sparse EMG/synergy reconstruction, IMU observability/identifiability, ultrasound and multimodal fusion.
- **Closest existing work:** [Rabbi et al. (2024)](https://doi.org/10.1007/s10237-024-01825-7) used muscle synergies to reduce EMG requirements while estimating knee contact force in cerebral palsy; [synergy extrapolation](https://doi.org/10.3389/fbioe.2022.962959) estimates unmeasured excitations; [minimal-sensor exoskeleton policy distillation](https://doi.org/10.1186/s12984-025-01854-y) operates from joint encoders in simulation; IMU kinematic work has explicitly documented practical non-identifiability under insufficient excitation.
- **Remaining limitation:** “Minimum” is usually task/controller-specific, not a guarantee for internal NMS state or clinical decision. Few studies test sensor subsets under placement shift, dropout and cross-session/patient change with posterior uncertainty and independent ground truth.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **High when narrowed.** The current chronic-stroke dense IMU and mocap assets support nested sensor ablation and locked-session evaluation. Without EMG/pressure/force/ultrasound, the claim must remain movement-state or downstream-function specific.
- **Next pilot test:** Evaluate nested sensor sets under session-level splits, sensor rotation/dropout and paretic/non-paretic stratification. Use two endpoints: an external reference (mocap or measured sensor) and a downstream clinical/functional decision such as gait-event timing or asymmetry. Require calibrated uncertainty and compare against a simple measured-sensor baseline.
- **Would change verdict:** A multimodal patient study with formal identifiability and decision-preservation criteria across sessions would make the broad gap substantially closed.

## G08 — Patient-grounded Embodied-AI benchmark alignment

- **Candidate gap:** Can MyoSuite/MS-Human-style tasks be paired with synchronized patient data and standardized sim-to-real metrics?
- **Falsifiable form:** The gap would be false if an open benchmark jointly supplied patient sensor/biomechanics data, a bound muscle-driven simulator, calibration protocol, device/task definition and locked sim-to-real metrics.
- **Supporting evidence:** The core Embodied-AI benchmarks are reproducible but generic; patient NMS studies use small, heterogeneous pipelines and rarely expose an ML-ready environment.
- **Counter-evidence searched:** MyoSuite/MyoChallenge clinical data, AddBiomechanics, patient OpenSim datasets, sim-to-real benchmark, MyoAssist and assistive-device task suites.
- **Closest existing work:** [AddBiomechanics](https://addbiomechanics.org/download_data.html) provides large physically processed motion, force and inverse-dynamics data; [MyoAssist 0.1](https://doi.org/10.1109/ICORR66766.2025.11063089) adds amputee/prosthesis environments; [MyoAssist 1.0](https://doi.org/10.64898/2026.08.25.746839) standardizes 15 assistive-device simulations and shared evaluation. Its documentation still lists a curated real/simulated motion library as planned rather than a synchronized patient benchmark.
- **Remaining limitation:** Data platforms and simulation platforms are converging, but patient binding, clinical metadata, calibration targets, sensor noise and locked sim-to-real outcome metrics are not delivered together.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Medium–high as benchmark engineering; medium as scientific novelty.** A data adapter and baseline suite are feasible, but physics validation is limited if the source dataset lacks GRF, EMG or device interaction forces.
- **Next pilot test:** Convert one locked stroke gait subset to a versioned OpenSim/MyoAssist-compatible representation, define calibration/test splits and three discrepancy metrics (kinematics, external mechanics where available, downstream task). Release one generic and one patient-conditioned baseline. Stop if missing physical signals make the simulator unidentifiable rather than merely imperfect.
- **Would change verdict:** A public benchmark satisfying patient data + bound simulator + locked metrics would change this to `not-a-gap`.

## G09 — Demographic and morphological validity

- **Candidate gap:** How do sex, age, pathology, device fit and underrepresented anatomy affect personalization error and failure?
- **Falsifiable form:** The broad gap would be false if models and datasets already quantified these axes with subgroup-specific external validation and showed where generic scaling/personalization fails.
- **Supporting evidence:** Many core papers use small healthy samples or one pathology and do not report subgroup calibration/failure. Generic adult anatomy and muscle-force parameters remain common.
- **Counter-evidence searched:** sex-specific knee/FE modeling, age/sex PCSA, pediatric scaling, statistical shape models, clinical scaling validation and demographic bias.
- **Closest existing work:** A [2026 review](https://doi.org/10.1080/10255842.2026.2656284) documents sex-neutral knee modeling and proposes sex-aware geometry/material/strength strategies; [Dalman et al. (2022)](https://doi.org/10.1016/j.jbiomech.2022.111170) tested adult-to-pediatric shoulder scaling against measured strength; a [333-child shape-model study](https://doi.org/10.1016/j.jbiomech.2024.112211) predicts pediatric lower-limb geometry from sparse landmarks; a [2024 age/sex PCSA review](https://arxiv.org/abs/2411.00071) shows uniform force scaling misses demographic muscle-distribution differences.
- **Remaining limitation:** Individual morphology components are being addressed, but cross-population failure rates for a complete sensor→model→decision pipeline, especially in stroke/SCI and device fit, remain poorly characterized.
- **Verdict:** `partially-addressed`.
- **Feasibility:** **Low as the main project with the current small clinical cohort.** It needs diverse samples and reliable demographic/severity/device-fit metadata. It is feasible as a prespecified audit axis, not as a universal equity claim.
- **Next pilot test:** Before training, define available demographic/pathology strata and test calibration residuals, uncertainty coverage and downstream errors hierarchically. Report where sample size makes inference impossible. Do not infer sex/age fairness from balanced average error.
- **Would change verdict:** A representative multi-site benchmark with subgroup-calibrated NMS outcomes and documented failure modes would close the broad gap.

## G10 — Governance, ownership and auditability

- **Candidate gap:** Who owns a longitudinal twin, how are updates audited, and how should clinicians/users receive uncertainty and intervention rationale?
- **Falsifiable form:** As an NMS technical gap, it would be false if general medical digital-twin governance already supplies reusable requirements for consent, ownership, versioning, audit, explanation and accountability.
- **Supporting evidence:** The NMS core literature rarely implements these mechanisms, and long-lived personalized data amplify privacy and accountability concerns.
- **Counter-evidence searched:** healthcare/HDT governance, ethics, ownership, auditability, explainability, regulatory oversight, consent and clinician-facing uncertainty.
- **Closest existing work:** A [2026 healthcare HDT review](https://pmc.ncbi.nlm.nih.gov/articles/PMC13328380/) proposes a four-tier governance framework covering data governance, model development, clinical deployment and regulatory oversight; the [Saxby–Pizzolato NMS framework](https://doi.org/10.1123/jab.2023-0114) already includes curate, maintain, synchronize, error logging and user-interface functions; general HDT roadmaps address privacy, security, cost and ethics.
- **Remaining limitation:** NMS-specific implementation examples are sparse, especially audit trails for model/parameter updates and clinician presentation of uncertainty. However, this is primarily governance/HCI/regulatory implementation rather than a neuromusculoskeletal scientific novelty claim.
- **Verdict:** `out-of-scope` for the current core technical PhD direction.
- **Feasibility:** **Low without ethics, clinical-informatics and HCI collaborators.** It remains mandatory system design work.
- **Next pilot test:** Produce a threat model, data/model lineage schema, versioned update log and clinician-facing uncertainty mock-up for any prototype. Treat this as responsible-research infrastructure unless the thesis explicitly becomes interdisciplinary governance/HCI research.
- **Would change verdict:** A deliberate shift of thesis scope toward clinical HCI, regulation or data governance would bring the candidate back in scope, but would not make it an NMS mechanism gap.

---

## Priority recommendation

### Advance now

**G07 + G01 + G05, narrowly combined:** determine which realistic sensor subset preserves a specific stroke-gait state/decision across sessions, quantify calibrated uncertainty, and abstain safely under dropout or distribution shift.

This is feasible with the current sparse-to-dense wearable work, but the contribution must be stated as **sensor-to-state reliability and failure-aware decision preservation**, not “a complete digital twin” and not “using fewer IMUs.” Add EMG, pressure or another modality only if it increases observability of a specified neural/mechanical state.

### Build as the PhD expansion

**G03 + G04:** bind the reliable state estimator to a patient-conditioned neuromechanical simulator/policy and test an unseen intervention or context. This requires richer ground truth and preferably a robotics/clinical collaborator.

### Keep as the long-term thesis vision

**G02:** two-timescale adaptation first; do not promise neural drive, fatigue, plasticity and tissue remodeling in one initial system.

### Do not use as primary novelty claims

- G06 is too broad and contradicted by controlled clinical evidence.
- G09 should be a validation/audit requirement unless a sufficiently diverse cohort is secured.
- G10 is a deployment responsibility, not the present NMS scientific gap.
