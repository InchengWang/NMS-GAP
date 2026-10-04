# PhD Research Proposal

## Title

**Toward Decision-Validated Human Neuromusculoskeletal Digital Twins: UWB Motion Capture for Embodied Rehabilitation Interaction**

**中文题目：面向具身康复交互的 UWB 动作捕捉与决策验证型人体神经肌骨数字孪生**

Prepared for doctoral research in **Mingming Zhang's group, Southern University of Science and Technology**. Evidence checked on **2026-10-04**.

## Proposal status and scope

This plan applies the [nms-digital-twin-phd-proposal skill](https://github.com/InchengWang/nms-digital-twin-skills/blob/main/nms-digital-twin-phd-proposal/SKILL.md), including its proposal structure and experiment-design checklist. It advances bounded residuals of the repository's validated **G07/G01, G05 and G04**, rather than carrying the older multi-timescale claim into a different sensing technology.

**UWB ranging/localization is the principal motion-sensing tool.** The working assumption is a wearable tag–anchor platform compatible with the group's UI-MoCap line [R02]. This is a hardware assumption to verify, not a statement that raw timestamps, channel impulse responses or tag-to-tag ranging are currently accessible. Radar-based, contactless UWB sensing is a different measurement problem and is outside this draft.

The perception benchmark covers functional whole-body movement; the mechanistic and interaction studies converge on **one trunk–upper-limb subsystem during seated reaching**. This task is selected for tractable external-force measurement and bounded physical interaction, and is consistent with the group's upper-limb control work [R18]. Its selection remains an advisor-facing design choice. Whole-body muscle identification and simultaneous upper/lower-limb robot development are not graduation requirements.

EMG is included when a neural–muscular claim requires it; instrumented interaction force is included when dynamics require it. IMU is an **optional supplementary modality and comparator**, never the organizing research question. Optical motion capture provides a laboratory reference, not a required deployment input.

The inherited gap verdicts and this UWB-specific counter-evidence check are documented in [GAP_VALIDATION_AND_NEAREST_WORK.md](GAP_VALIDATION_AND_NEAREST_WORK.md). The relevant verdict is **partially-addressed**, with UWB-specific mechanisms still subject to pilot falsification. No claim of global priority, complete physiological observability, clinical efficacy or a fully validated digital twin is made.

## 1. Background and motivation

Motion capture is useful to rehabilitation only if the measured movement supports a valid judgment about the person and an appropriate subsequent action. A spatially plausible avatar can conceal errors in anatomical angles, movement compensation, inferred joint moments or the timing of assistance. Conversely, reproducing joint motion does not identify the neural or muscular strategy that produced it.

UWB offers a direct spatial measurement channel. Its scientific value here is the opportunity to examine which human–environment and inter-segment relationships are constrained by measured distances, which are filled in by learned motion priors, and how that distinction affects a model used for interaction. UWB-specific problems include body shadowing, multipath, weak geometric configurations, asynchronous measurements and tag reattachment. Their effects must be measured rather than assumed to vanish because the signal is radio-based.

A human NMS representation adds a different layer: EMG-informed excitation and activation dynamics connect movement to muscular output, while external forces constrain net mechanics. Existing motion-to-biomechanics and real-time neuromechanical systems already establish this general bridge [R11], [R12]. The thesis therefore asks whether a **UWB observation model with diagnosed ambiguity** can support a reliable, person-bound representation and improve decisions under realistic changes.

The intended embodied-intelligence loop is: the agent maintains a belief about a human–device state, predicts consequences of a bounded action, acts on the physical interaction and updates from the resulting observations. A neural network producing an avatar is an enabling perception component; the action–response loop supplies the interaction contribution.

## 2. State of the art

| Research family | Nearest prior work and established capability | Boundary relevant to this proposal |
|---|---|---|
| UWB-only joint measurement | Qi et al. already estimated flexion/extension from wearable inter-segment ranging [R01]. | Measuring a hinge angle with UWB is established; the question must concern ambiguity, task validity or downstream consequences. |
| Lab-aligned sensing hardware | UI-MoCap supports UWB positioning and IMU data transport [R02]. | A new positioning/filtering demonstration alone would overlap the group's established platform. |
| Upper-limb hybrid motion estimation | Shi et al. combine IMU and UWB with complementary/Kalman filtering for upper-limb movement [R20]. | Upper-limb UWB fusion already exists; it is an optional-modality baseline, not the thesis identity. |
| Sparse full-body reconstruction | UIP and GIP combine ranging with inertial observations, including multi-person tracking [R03], [R05]. | Sparse sensing and spatial interaction reconstruction are existing capabilities. |
| Uncertainty-aware motion fusion | UMotion incorporates pose and sensor uncertainty with body-specific constraints [R04]. | Uncertainty, shape conditioning and a feedback estimator are not sufficient novelty by themselves. |
| Explicit ranging geometry | Ultra Diffusion Poser models sensor layout and distance consistency [R06]. | Adding geometric constraints or diffusion guidance is already addressed. |
| Pure-distance full-body motion | WiP reconstructs motion from pairwise distances [R07]. | “UWB without IMU” is not a defensible first-of-kind claim; its accessed version and publication-status limit must be retained. |
| UWB-to-robot interaction | Range-only posture recognition has already generated mobile/aerial robot commands [R08]. | UWB-based HRI exists; the proposed test must go beyond gesture-to-command mapping. |
| UWB network adaptation | Dynamic reference-anchor selection and a two-layer network architecture address localization/scalability [R09], [R10]. | Adaptive anchor choice and global/local ranging separation are implementation baselines, not claimed inventions. |
| Neuromechanical modeling | RGBD upper-limb modeling, CEINMS-RT and the NMSM Pipeline support sensing-to-model, real-time control and personalization [R11], [R12], [R14]. | Replacing their kinematic input with UWB does not establish a scientific contribution. |
| Reduced post-stroke arm modeling | Asghari et al. developed a planar NMS arm model in post-stroke participants [R21]. | A reduced patient arm model is established; locked predictions and measurement-to-decision effects need separate evidence. |
| Uncertainty-to-assistance | An NMS-informed Bayesian model has already supplied torque confidence bounds to an exoskeleton [R13]. | Confidence-based assistance exists; the residual concerns calibrated action consequences during identifiable sensor/model failures. |
| Muscle-driven embodied control | MyoSuite provides contact-rich muscle control; simulation-trained assistance and recent personalized FES have physical precedents [R15], [R16], [R17]. | Neither simulated physiology nor model-to-device transfer is absent from the literature. |
| Subject-specific rehabilitation interaction | Miao et al. adapt upper-limb compliance using interaction force and personal workspace [R18]. | Personal workspace and adaptive compliance must be strong practical baselines. |

**Current status affecting interpretation.** The Nature 2024 assistance paper carries a **2026-07-27 Editor's Note about availability of supporting data and code** [R16]. It remains relevant prior work, but its reported benefits are not used as reproducibility evidence or numerical design targets. WiP is inspected as arXiv v1; authors report a TOG publication/acceptance, but a publisher version and DOI were not independently verified [R07]. These are distinct status issues.

## 3. Validated research gap

### 3.1 Traceability to the existing gap validation

| Inherited dossier | Original verdict | Residual retained here | UWB-specific refinement |
|---|---|---|---|
| G07 + G01: actionable multimodal observability and identifiable personalization | Partially-addressed | An endpoint-specific observation set with explicit uncertainty and independent validation. | Determine which task-relevant anatomical states ranging actually constrains after reattachment and geometric/visibility changes. |
| G01 + G04: person-specific state validity and unseen-condition prediction | Partially-addressed | Validate a small person-bound model outside calibration before refitting. | Propagate correlated UWB errors into one measurable NMS endpoint and a locked load/assistance response. |
| G05: uncertainty, sensor failure and closed-loop decisions | Partially-addressed | Connect diagnosed sensing/model failures to evaluated action, attenuation or fallback. | Compare posterior-aware decisions with ordinary uncertainty wrappers and deterministic faults at matched sensing and computational budgets. |

The broad G02 multi-timescale fatigue/rehabilitation claim is **not** inherited as established novelty. This project first distinguishes session calibration changes from human changes; longer-term physiological interpretation is an optional later hypothesis. G06 is not used to claim that personalized biomechanical interventions lack clinical benefit.

### 3.2 Bounded gap statement

The targeted nearest-work check found substantial solutions for UWB reconstruction, uncertainty fusion, geometric constraints, radio-network adaptation, upper-limb fusion and posture-based robot commands [R01], [R02], [R03], [R04], [R05], [R06], [R07], [R08], [R09], [R10], [R20]. It also found mature NMS, reduced post-stroke arm and assistance components [R11], [R12], [R13], [R14], [R15], [R16], [R17], [R18], [R21].

The selected residual is **the experimentally assessed relationship between task-specific UWB observability, independently evaluated neural–mechanical estimates and downstream physical interaction decisions across sessions**. A missing all-in-one system is not, by itself, evidence of scientific novelty. Each Aim must show an identifiable mechanism, a decision-relevant boundary or a falsifiable benefit beyond component integration.

This is a targeted counter-evidence assessment, not a systematic proof that no prior paper meets these criteria. The UWB-specific verdict remains **partially-addressed**; untested superiority and physiological explanations are hypotheses.

## 4. Central research question

**Which task-relevant human states are reliably recoverable from a UWB-centered observation set, and does explicitly representing their uncertainty improve person-specific NMS prediction and bounded rehabilitation interaction compared with strong motion-only, point-estimate and deterministic-fallback baselines?**

## 5. Central hypothesis

A task-specific estimator that separates **measurement-constrained geometry, learned motion priors, session calibration and EMG-informed mechanics** will support more reliable cross-session decisions than an otherwise comparable pipeline that treats reconstructed motion as exact.

This hypothesis has three separately falsifiable components:

1. **H1 — Sensing:** observability-aware UWB configuration and calibration produce better calibrated task-state estimates or identify unusable states more reliably than fixed configurations and strong ranging-based reconstruction methods at matched resources.
2. **H2 — Modeling:** propagating UWB and attachment uncertainty into a small personalized NMS model improves locked future-session/condition prediction or avoids confident errors relative to plug-in point estimates and calibrated black-box predictors.
3. **H3 — Interaction:** the validated state belief reduces defined action errors or constraint violations without unacceptable task-performance loss relative to motion-only assistance, point-state assistance and deterministic failure rules.

Failure of H2 means the task does not warrant the proposed NMS complexity. Failure of H3 means the representation has not demonstrated a control benefit. Neither failure can be repaired by relabeling an avatar as a twin.

## 6. Specific Aim 1 — Establish the task-specific observability and failure boundaries of UWB motion capture

**Question and construct.** Which UWB measurements constrain the selected joint/task states, and when does a plausible reconstruction depend predominantly on a population motion prior? Primary states are elbow flexion and hand-to-target position in the interaction task; trunk compensation and functional whole-body motion are additional validation states.

**Nearest-work boundary.** This Aim builds on joint ranging [R01], UWB hardware [R02], uncertainty fusion [R04], explicit geometry [R06], pure-distance reconstruction [R07] and existing upper-limb hybrid estimation [R20]. Its proposed contribution is a tested boundary between measured geometry and inferred movement under defined deployment changes, not a new claim for UWB pose estimation.

### Tasks

| Task | Method and evidence to produce | Prior-work anchor |
|---|---|---|
| A1.1 — Reproduce the measurement and pose baselines | Characterize static/dynamic range or TDoA errors, reproduce the available tag-localization pipeline, and benchmark UWB-only and optional-fusion reconstruction. | UI-MoCap, UIP, UMotion and WiP [R02], [R03], [R04], [R07]. |
| A1.2 — Diagnose observability before optimizing a network | Analyze measurement Jacobians/range-graph geometry for the selected subsystem; test rank loss, mirror/twist ambiguity and sensitivity using a rig and controlled human poses. Compare configurations at equal airtime. | UWB joint-angle measurement and geometry-aware reconstruction [R01], [R06]; adaptive network methods are comparators [R09], [R10]. |
| A1.3 — Validate uncertainty after reattachment and environmental change | Lock a later session and a changed anchor/room condition; compare empirical interval coverage and error–abstention curves against calibrated baseline wrappers. Include real body shadowing and safely staged link blockage. | UMotion and WiP [R04], [R07]. |

**Model.** Use a causal, articulated factor-graph/state-space estimator with anatomical constraints, uncertain tag attachment and a learned residual/prior only where justified. Begin with robust classical localization plus constrained inverse kinematics. Introduce one learned model family after the geometric baseline works. Constrained angle priors must not be mistaken for measurements.

**Data.** A mechanical articulated rig with encoder angles isolates geometry and timing effects. Public UIP-DB/GIP-DB support motion-baseline checks only. A new pilot uses approximately 6–8 healthy volunteers, with independent reattachment over 2–3 visits. The main planning envelope is 20–24 healthy adults and, if clinical access permits, 12–16 stroke participants with repeated sessions. These are resource estimates; confirmatory sample size follows pilot-based design simulation.

The functional motion battery includes reaching, trunk rotation, sit-to-stand, turning and short transfers. The mechanistic endpoint is concentrated on the reaching subsystem. Stroke movements are recorded as real impairments; simulated impairment is not a substitute for patient evidence.

**Baselines.** Robust multilateration/TDoA localization plus constrained IK; UWB-only sequence regression; WiP; matching-input UIP/UMotion/UDP; fixed versus available dynamic anchor reference; optical-reference reconstruction. GIP is a contextual/multi-person comparator only if that task is included. All sensor requirements are disclosed.

**Evaluation.** Primary: participant-level held-out-session CRPS for elbow angle, accompanied by interval coverage, interval width and task-defined usable-data coverage. Secondary: hand-position error, trunk-state error, anatomical joint error, absolute translation error where anchored, tail error, capture-to-output latency and tag/airtime burden. Report aligned pose errors separately from errors in the physical coordinate frame; alignment cannot hide spatial errors relevant to a robot.

**Expected contribution and failure value.** An endpoint-specific account of what ranging can and cannot support, with an empirically validated configuration/calibration rule. If a state is unobservable or too noisy, publish the ambiguity and minimum additional information needed, then restrict Aims 2–3 to the usable state. This is more informative than an unsupported full-body physiological claim.

**Feasibility.** High for rig/public-data work; medium for repeated clinical capture. Progression requires real timestamps, stable anatomical calibration and task-adequate precision/latency, not merely good avatar appearance.

## 7. Specific Aim 2 — Test whether a UWB-centered person model supports reliable neural–mechanical prediction

**Question and construct.** Does uncertainty in motion and attachment materially change an externally evaluable NMS estimate or prediction? Can a small session-updated model distinguish calibration effects from human performance changes?

**Nearest-work boundary.** Motion-to-musculoskeletal analysis, real-time EMG modeling, treatment personalization and reduced post-stroke arm models already exist [R11], [R12], [R14], [R21]. A new sensing input or planar patient model is not the contribution. This Aim tests the propagation of a diagnosed spatial ambiguity into a named mechanical endpoint and whether limited updating improves prediction.

### Tasks

| Task | Method and evidence to produce | Prior-work anchor |
|---|---|---|
| A2.1 — Bind a reduced arm model to the participant | Fit only a small practically identifiable parameter set using UWB kinematics, measured EMG and known interaction force; retain a generic scaled model as a comparator. | RGBD biomechanics, CEINMS-RT and planar post-stroke modeling [R11], [R12], [R21]. |
| A2.2 — Propagate measurement and parameter ambiguity | Compare plug-in mean kinematics with joint posterior samples, retaining shared-anchor and cross-time correlations; perform prior-sensitivity and parameter-compensation analyses. | UMotion for sensing uncertainty and NMS-BNN for torque uncertainty [R04], [R13]. |
| A2.3 — Lock a later session and an unseen load/assistance level | Compare a frozen model, brief session calibration, model updating and black-box prediction before revealing the evaluation condition. Separate attachment/electrode changes from human latent changes. | NMSM prediction/personalization and physical model-to-device transfer [R14], [R17]. |

**Model.** Start with a planar elbow/shoulder or elbow-dominant subsystem, adding trunk degrees of freedom only when observable. A Hill-type/activation-dynamics core maps measured excitation proxies and muscle–tendon geometry into net joint moment. Use OpenSim/CEINMS-compatible components rather than rebuilding a full simulator. Population muscle parameters are fixed unless calibration data and sensitivity analysis justify individual estimation.

Session nuisance terms include tag-to-segment offsets, synchronization error and EMG scale. They have reference tasks and explicit priors. Session-updated calibration must not be interpreted as recovery, fatigue or motor learning without independent evidence.

**Data and reference.** Collect synchronized UWB, targeted flexor/extensor EMG, optical segment tracking and instrumented handle/robot forces. Include elbow-focused isometric dynamometer measurements where feasible and dynamic reaching under known external load. The primary reference for dynamic net moment is optical kinematics plus independently recorded external forces and stated inertial assumptions; it is not a direct measure of each muscle's force.

One repeatable load contrast is selected during the pilot, then one previously unseen level is held out. Reference EMG channels used only for evaluation must be excluded from fitting; fitted EMG cannot simultaneously be presented as independent physiological validation.

**Baselines.** Generic scaled model; one-time personal model; brief calibration-only update; UWB mean-state model; UWB uncertainty propagated through the same model; optical-reference kinematics with the same EMG/model; a probabilistically calibrated data-driven force/moment predictor; the same models with optional IMU supplementation. Hold EMG channels, force availability and calibration duration constant when comparing the effect of UWB processing.

**Evaluation.** Primary: participant-level predictive CRPS for the selected net-moment endpoint in a locked future session/load. Secondary: MAE/RMSE, coverage and width, systematic bias, change-prediction error, sensor-versus-model variance, parameter stability and held-out-channel EMG agreement where available. Internal muscle force and tissue load are reported as model-dependent estimates unless independently validated.

**Expected contribution and failure value.** Identify when spatial uncertainty actually changes a neural–mechanical conclusion, and whether a small updated person model improves transport to later observations. If uncertainty propagation has no useful effect, or geometry dominates all errors, retain a simpler kinematic/force model. If parameters compensate for one another, report equivalence classes instead of asserting a unique physiological state.

**Feasibility.** Medium: EMG and external-force synchronization are required. This Aim cannot be completed from the existing IMU-only dataset. Upper-limb model support in the chosen framework must be checked; software availability alone does not establish a validated arm implementation.

## 8. Specific Aim 3 — Evaluate decision value in bounded embodied human–robot interaction

**Question and construct.** Does the additional human-state belief improve a physical action when motion/measurement conditions change, or is a simpler controller sufficient?

**Nearest-work boundary.** Posture-to-robot commands, personal-workspace compliance and uncertainty-informed assistance already exist [R08], [R13], [R18]. Muscle-driven simulation and physical model transfer also have precedents [R15], [R16], [R17]. The residual test concerns **action consequences attributable to the human-state representation**, not the existence of UWB HRI or an adaptive robot.

### Tasks

| Task | Method and evidence to produce | Prior-work anchor |
|---|---|---|
| A3.1 — Compare what information the controller needs | Use the same bounded admittance/AAN controller with motion-only, point NMS and probabilistic NMS information. In simulation/replay, compare a reduced muscle-driven human with simpler force-response dynamics. | MyoSuite and personal compliance control [R15], [R18]. |
| A3.2 — Test uncertainty-to-action rules against ordinary fallbacks | Evaluate continue, attenuate and transition to a validated low-assistance mode under observed and replayed measurement faults, at matched delay/burden. | Range-only HRI and NMS-BNN assistance [R08], [R13]. |
| A3.3 — Validate the physical action–response loop | Conduct a short randomized within-participant comparison after bench/HIL gates; predict the response to a bounded assistance change before applying it. Track human motion, voluntary output and interaction force separately. | CEINMS-RT, NMSM and personalized FES transfer [R12], [R14], [R17]. |

**Controller and embodiment.** The main controller is one constrained admittance/assist-as-needed design. A probabilistic state informs bounded assistance gain or target adaptation; a low-level robot controller and independent limits retain control of the device. A small learned human-response model may support prediction. A new RL algorithm is not required, and unrestricted online exploration is excluded from physical studies.

The agent must evaluate how an action alters the next observation and task performance. Its output is not merely a posture class. Patient-specific NMS complexity is retained only if its information improves a predeclared control endpoint.

**Experiment.** First use replay and a hardware-in-the-loop rig to compare faults without exposing people to induced risky commands. Healthy-user reaching follows only if the device interface, geometry and conservative fallback are verified. An exploratory stroke study is conditional on clinical access and the same gates. Deliberate fault injection remains in replay/HIL; normal-use sensor degradation can be logged in supervised human sessions.

Use reversible, short assistance contrasts in counterbalanced order, with standardized probe tasks and empirically adequate rest/reset. If adaptation carries over, analyze first exposure or redesign; longer-term retention requires a separate study.

**Baselines.** Encoder/force-based conservative control; UWB motion-only control; point-state NMS control; posterior-state control; deterministic quality/dropout rules; calibrated baseline uncertainty wrapper; independent reference-state controller in replay. The encoder/force comparator is essential to show whether UWB adds information beyond the robot's existing measurements.

**Evaluation.** Primary decision endpoint: independently labeled constraint violations among continued decision opportunities, assessed jointly with a prespecified task-performance non-inferiority margin. Report intervention/attenuation burden, completion/hand error, interaction-force peaks, action divergence from the reference decision and observed response-prediction error. Human voluntary net output and EMG/co-contraction are descriptive physiological endpoints, not direct recovery or neural-engagement truth.

**Expected contribution and failure value.** Evidence that a specified sensed/model state changes an action in a beneficial way, or evidence that the task is adequately served by simpler information. A pose or NMS accuracy improvement without action benefit does not establish H3. A HIL-only result is a system-validation result, not patient rehabilitation efficacy.

**Feasibility.** Medium for replay/HIL, conditional for human robotics. A planned 12–16-person healthy crossover is a resource envelope, not a claim of adequate power or rare-event safety. Patient feasibility is optional and separately designed.

## 9. Methodology and experiment plan

### 9.1 UWB measurement model and capability check

Let p_i(q, theta, o_i) be tag i's predicted spatial position from joint state q, anthropometry theta and attachment offset o_i.

For hardware offering direct two-way ranging, use a range factor:

```text
r_i,a(t) = ||p_i(t) - anchor_a|| + range_bias_i,a(t) + noise_i,a(t)
r_i,j(t) = ||p_i(t) - p_j(t)|| + range_bias_i,j(t) + noise_i,j(t)
```

For TDoA hardware, model the measured difference rather than inventing independent ranges:

```text
c * delta_t_i,(a,b)(t)
    = ||p_i(t) - anchor_a|| - ||p_i(t) - anchor_b||
      + synchronization_bias_(a,b)(t) + noise_i,(a,b)(t)
```

Timing conventions and residual clock/antenna terms are determined from the real firmware/protocol. Shared reference anchors induce correlated errors. Anchor positions and their calibration uncertainty are included. Link-specific acquisition times are retained; a rolling ranging cycle is not assumed to be an instantaneous full-body frame.

If only vendor positions are exposed, characterize their empirical error and correlation and use a position observation model. In that case, no claim about raw-radio inference or direct range-level calibration is permitted. CIR/first-path information and inter-tag links are optional capabilities to verify.

Range-only geometry has rigid-motion/reflection ambiguities without a physical reference. A tag on a segment does not uniquely observe axial twist. These are measurement-model properties, not limitations solved automatically by a neural network. The primary interaction setup uses calibrated room/device anchors and anatomical joint constraints; anchor-free reconstruction is a secondary comparator. Multiple tags or an optional orientation source are added only where the observability analysis justifies them.

### 9.2 Sensor roles and evidence limits

| Modality | Role during the thesis | Interpretation limit |
|---|---|---|
| UWB tags and anchors | Principal operational spatial sensing; configuration and quality are research variables. | Distances/positions do not directly observe muscle excitation or unique joint rotations. |
| Targeted sEMG | Operational neural–muscular input in Aims 2–3; a smaller separate reference set if justified. | Excitation proxy; amplitude does not directly measure motor-neuron drive, voluntary participation or muscle force. |
| Instrumented handle, load cell, dynamometer and robot encoders | Known external interaction, torque calibration and independent device feedback. | Encoder kinematics do not observe every human joint or trunk compensation. |
| Optical motion capture | Laboratory kinematic reference and anatomical calibration checks. | Skin/segment modeling errors remain; it is not a perfect anatomical truth. |
| Optional IMU | Ablation, comparison or a justified disambiguating observation. | Its inclusion must be named in every result; UWB-only and fused results remain distinct. |
| Optional ultrasound/imaging | Only if one otherwise essential parameter remains unidentifiable. | Not required by default, and no tissue-safety claim without validation. |

### 9.3 Reduced NMS model and update policy

For the instrumented subsystem, use:

```text
M(q) * q_ddot + C(q,q_dot) + G(q)
    = tau_human + J(q)^T * force_robot + other_known_external_terms
tau_human = moment_arms(q) * muscle_forces(activation, length, velocity, theta)
```

Unmeasured support/contact forces invalidate a naive inverse-dynamics estimate. Begin with a controlled seated task in which external loads are known; do not export this dynamics claim to sit-to-stand without measuring foot/chair/support forces.

Geometry/body parameters are calibrated initially; attachment and EMG nuisance terms may update at session start using a fixed brief reference protocol. Human-response parameters update only from data reserved for that purpose. State estimation is causal at runtime. Offline smoothing is available for reference analysis and must be separately labeled.

Use posterior samples or an ensemble with empirically calibrated output intervals. Compare with a simpler residual/calibration wrapper. Uncertainty should include measurement noise, attachment ambiguity, parameter ambiguity and model discrepancy to the extent estimable; no decomposition is declared identifiable merely because it has separate software variables.

### 9.4 Staged experiments

| Stage | Independent information and change | Main purpose |
|---|---|---|
| E0: mechanical rig | Encoder angles, surveyed geometry; different anchor layouts, tag offsets and acquisition timing. | Distinguish geometric ambiguity from algorithmic failure without human physiology. |
| E1: motion benchmark | Repeated UWB/optical capture; reattachment, task shifts, body shadowing and room/anchor changes. | Test H1 and calibrate endpoint-specific uncertainty. |
| E2: neural–mechanical study | Targeted EMG, measured external loads, repeated reference tasks, held-out load/session. | Test H2 and the value of selective model updating. |
| E3: replay and HIL | Recorded/simulated faults with independently recorded reference state and force/position constraints. | Determine whether the belief changes action errors; qualify physical-study gates. |
| E4: supervised short interaction | Locked controller parameters and randomized assistance order; fresh response measurements. | Test H3 in a real action–response loop; feasibility rather than durable recovery. |

Public motion datasets bootstrap sensing software, not patient NMS truth. Existing stroke IMU/mocap work can support synchronization, split and perturbation infrastructure, but is not represented as a UWB dataset.

### 9.5 Locked validation and reproducibility

Use grouped development and test sets with independent people for population generalization, and chronological held-out sessions for personalized generalization. Fit scalers, sensor selection, body priors, nuisance models, interval calibration and action thresholds using training/development data only. Remove source-dataset overlap in pretrained synthetic-motion evaluation.

Models requiring different placements are compared on compatible configurations, with equalized optional inputs and explicit resource accounting. Full-body public results and the reduced interaction subsystem are separate benchmark tracks. Report original-code runs versus reimplementations; inaccessible baseline software is not silently replaced with a weak namesake.

Archive protocol/firmware versions, anchor geometry, raw measurements where consent permits, coordinate transforms, time offsets, calibration provenance, train/test manifests, reference uncertainty and exclusion reasons. Release deidentified data only with appropriate consent; publish executable benchmark adapters even if clinical raw data cannot be shared.

## 10. Baselines and ablation design

| Layer | Required comparison | What it tests |
|---|---|---|
| Measurement | Fixed reference/localization versus available dynamic reference; same radio budget [R02], [R09]. | Established networking versus the task-specific configuration decision. |
| Perception | Classical localization + IK; UWB-only regression/WiP; compatible UIP, UMotion and UDP [R03], [R04], [R06], [R07]; classical upper-limb fusion only in the optional IMU track [R20]. | Geometry, motion prior and uncertainty benefits. |
| Sensor ablation | UWB-only; UWB + targeted EMG for NMS; optional IMU; reference optical kinematics with the same EMG/force. | Information added by each modality without conflating sensor and model changes. |
| Personalization | Generic; one-time personalized; session nuisance-only update; small model update. | Whether physiological model updating is actually needed. |
| Uncertainty | Plug-in means; propagated joint uncertainty; black-box predictive distribution; calibration-only wrapper [R04], [R13]. | Whether uncertainty adds value beyond ordinary recalibration. |
| Control | Existing encoder/force control; motion-only; point NMS; posterior NMS; deterministic fallback [R18]. | Whether the proposed representation changes action outcomes. |
| Offline reference | Same control law with reference kinematics/force in replay. | Cost of sensing errors; this is a reference controller, not a biological oracle. |

Core comparisons hold EMG channels, force access, architecture capacity, calibration time and compute budget constant wherever possible. Report Pareto fronts for error, abstention, latency, wearing burden and airtime instead of declaring a universal minimum sensor count.

## 11. Metrics and success criteria

| Aim | Primary endpoint | Essential companion measures |
|---|---|---|
| Aim 1 | Held-out-session CRPS of elbow angle, aggregated per participant. | Angle MAE/95th-percentile absolute error; hand-position error in cm; 50/80/90% interval coverage and width; usable-data fraction; latency and configuration burden. |
| Aim 2 | Held-out-session/load CRPS of the selected net joint moment in Nm. | Bias, MAE/RMSE; predictive coverage/width; parameter compensation; change-prediction accuracy; held-out EMG agreement only where independent. |
| Aim 3 | Constraint-violation risk among continued actions, with task-performance non-inferiority. | Hazard-event miss rate, attenuation/fallback burden, reach completion/error, peak interaction force, human output and physical response-prediction error. |

For replay/HIL decision opportunity t, define h_t = 1 when an independently evaluated proposed action violates a **prespecified physical constraint** (for example force, workspace or speed), and c_t = 1 when the proposed decision is to continue.

```text
hazard-event miss rate = count(h_t=1 and c_t=1) / count(h_t=1)
risk among continued actions = count(h_t=1 and c_t=1) / count(c_t=1)
```

Handle zero denominators explicitly. Evaluate shadow decisions using the reference model/measurement with a documented uncertainty margin; these are evaluated action constraints, not observed tissue injury. Physical-study violations use measured outcomes and are reported separately.

An OOD flag, NLOS label, high uncertainty or disagreement between models is **not** a hazard label. Lower measured force due to constant abstention is not useful control. Establish action-risk and performance tradeoffs together.

Set accuracy tolerances, action constraints and the task non-inferiority margin after the pilot **and before the independent main test**. Derive them from the task/control margin and reference repeatability, not borrowed avatar accuracy or unverified clinical thresholds. Success requires practical usefulness plus a confidence interval supporting the primary comparison. No invented percentage improvement is promised.

## 12. Statistical analysis

1. **Unit of inference.** The participant is the main unit; trials and frames are repeated observations. Compute session/task summaries before group comparisons or use hierarchical models with participant and session effects. More samples per trajectory do not replace more participants.

2. **Predeclared contrasts.** Select the strongest compatible baseline during development, then lock one principal comparison per Aim. Primary effects are paired differences in CRPS for Aims 1–2 and the risk/performance contrast for Aim 3. Other architecture and sensor ablations are secondary.

3. **Sample-size design.** Estimate between-person variance, within-person correlation, expected dropout and plausible effects from the pilot. Use simulation-based precision/power analysis for each main contrast, including the planned multiplicity rule; ordinary superiority targets use two-sided alpha 0.05 and task non-inferiority uses a one-sided 0.025 test or equivalent confidence bound before multiplicity adjustment. Report effect assumptions and interval widths. The cohort envelopes above are recruitment planning figures, not completed power calculations. If recruitment cannot support a clinical inference, retain feasibility/precision endpoints.

4. **Models and intervals.** Use mixed-effects models for method, session, task/load, radio condition and control order, with participant random effects; apply suitable transformations or robust alternatives for skewed errors. Use participant-cluster bootstrap intervals, preserving sessions/trials within participants. For event risk, use clustered binomial models or participant-level event summaries; account for repeated opportunities rather than treating every frame as independent.

5. **Calibration.** Assess coverage and proper scoring rules on held-out participants/sessions/conditions, including interval width and subgroup uncertainty. Use a separate development calibration split. Conformal wrappers are baselines, not guarantees under arbitrary distribution shift. Reference measurement noise contributes to an empirical coverage assessment and is reported.

6. **Multiple comparisons.** Aim 3 requires both the risk comparison and task-performance non-inferiority; preregister it as an intersection-union claim, with an Aim-level p-value determined by its weaker component on the prespecified testing scale. Apply Holm adjustment across the three Aim-level primary claims when making a joint confirmatory claim; report component confidence bounds and raw/adjusted p-values. Label the broader ablation/subgroup analyses exploratory, with effect sizes rather than selective significance claims.

7. **Control interpretation.** Counterbalance reversible assistance order and model order/period effects. Task-performance non-inferiority requires the prespecified confidence bound to lie within the chosen margin. If practice or adaptation cannot be reset, crossover conclusions are limited and a first-exposure or parallel design is used. A short crossover cannot establish durable recovery.

8. **Missingness and failure.** Treat failed capture, dropout and fallback as outcomes as well as missingness. Report attempted and analyzable participants/sessions, prespecified exclusions and sensitivity to informative missingness. Do not remove the hardest NLOS or patient conditions to improve mean accuracy.

9. **Scope of inference.** Report healthy and patient results separately. Severity/body-size audits are descriptive unless powered. Few or zero violations do not establish clinical safety; give event denominators and uncertainty bounds. Causal language is limited to randomized bounded assistance contrasts, not observational sensor/model correlations.

## 13. Expected contributions

| Contribution | Evidence needed | Nearest-work boundary |
|---|---|---|
| Scientific: task-specific spatial/physiological information boundaries | Controlled ambiguity tests and independent repeated-session references; cases where comparable poses yield different or non-identifiable mechanics. | Goes beyond reconstruction scores in [R01], [R04], [R06], [R07]; does not claim ranging uniquely recovers physiology. |
| Methodological: uncertainty carried from ranging into a measurable person-model endpoint | Controlled decomposition/ablation and locked moment/response prediction beyond a calibration-only baseline. | Builds on [R04], [R11], [R12], [R13], [R14], [R21]; a sensor substitution or reduced patient model alone is insufficient. |
| Interaction: state information with verified action consequences | The same controller improves the declared risk/performance comparison; encoder/force and deterministic-fallback controls remain competitive baselines. | Narrows established HRI/adaptive assistance in [R08], [R13], [R18]. |
| Dataset/benchmark: a traceable sensing–model–decision evaluation track | Synchronized UWB, calibration, reference kinematics, selected EMG/force and repeated-session/fault manifests. | Complements existing UIP/GIP benchmarks [R03], [R05]; benchmark creation alone is an engineering contribution. |
| Translational feasibility | Supervised short interaction and usability/burden outcomes if gates pass. | Extends one task/context; does not claim a general treatment benefit or superiority to existing personalized intervention. |

These are expected, conditional outcomes. A thesis can retain value through explicit negative results about observability or unnecessary model complexity.

## 14. Risks and alternatives

| Risk | Early signal / kill test | Alternative preserving scientific value |
|---|---|---|
| Short segment baselines and body shadowing make UWB too imprecise. | Pilot fails task-defined angle/position and latency budgets across reattachment, even with reasonable placement. | Redesign tag/anchor geometry; restrict to an observable planar state or gross compensation; quantify the optional IMU/encoder information needed. Do not promise unrestricted UWB-only full-body kinematics. |
| Raw range/TDoA data or inter-tag links are unavailable. | Firmware/API exposes only positions, or ranging schedules cannot support required timing. | Use characterized position observations; keep unsupported raw-radio and peer-ranging claims out. Report hardware capability limits. |
| A learned prior conceals geometric ambiguity. | Accurate familiar motions but confident failures on controlled ambiguous or atypical movements. | Multi-hypothesis estimates, conservative constraints and explicit abstention; reduce claimed state dimensionality. |
| NMS parameters compensate or EMG calibration dominates. | Prior-sensitive parameters, unstable gains or no locked prediction gain over a calibrated black box. | Fix nuisance/physiology parameters, use a reduced EMG-informed moment model, and publish identifiability limits. |
| UWB uncertainty does not change downstream decisions. | Posterior controller adds no benefit at matched task performance/burden; encoder/force baseline is sufficient. | Focus the thesis on observable whole-body compensation/assessment and the circumstances where extra sensing is unnecessary. Keep control as a negative decision-value result. |
| Sensor quality and true human change are confounded. | Apparent subject-state change follows reattachment or electrode placement and disappears with reference calibration. | Treat it as measurement drift; use nuisance-only updates and stop interpreting it as fatigue/recovery. |
| Robot or clinical access is delayed. | Required interface, reference force or approved recruitment is unavailable by the planned checkpoint. | Complete rig, offline predictive and HIL studies; use healthy repeated sessions. No patient efficacy claim. |
| Physical-studies gates fail. | Required precision, fallback transitions or constraints are not demonstrated on bench/HIL. | Keep the model advisory/offline and evaluate shadow decisions; do not command assistance from an unqualified estimator. |

Re-search nearest work before each publication. A paper that closes a residual changes the contribution to replication, external validation or a different measurable limitation; it does not justify ignoring the counter-evidence.

## 15. Timeline

Use a **36-month research plan from the confirmed doctoral start date**; program dates and graduation requirements must be aligned with the supervisor. Pre-entry work can begin before enrollment. A shorter schedule keeps clinical robotics conditional rather than compressing an unsupported trial.

| Period | Work and decision gate | Deliverable |
|---|---|---|
| Pre-entry / months 1–2 | Inventory hardware/raw interfaces, reproduce basic localization, define coordinates and task/model scope. | Capability sheet, nearest-work update and endpoint specification. |
| Months 3–6 | Rig experiment, healthy repeated-session pilot, protocol/ethics preparation and main design simulation. | A1 go/no-go; calibrated baseline and finalized sample-size plan. |
| Months 6–12 | Main perception collection; fixed versus selected configuration; locked sessions/rooms; public-baseline reproduction. | Paper 1: UWB task observability and failure boundaries. |
| Months 10–20 | Instrumented EMG/force tasks, reduced model and nuisance/parameter analyses. | Validated reference pipeline; A2 identifiability and precision gate. |
| Months 18–25 | Locked future-session/load prediction and uncertainty/complexity ablations. | Paper 2: decision-relevant NMS uncertainty or its limits. |
| Months 22–29 | Replay/HIL control comparisons and conservative fallback verification. | A3 hardware go/no-go; sensor–state–action benchmark. |
| Months 27–32 | Supervised healthy interaction; optional patient feasibility only if recruitment and previous gates permit. | Paper 3: physical interaction value or a well-supported negative result. |
| Months 32–36 | External checks, integrated evaluation, journal revisions and dissertation. | Thesis and qualified person-model/system release. |

**First 90 days.** Confirm whether the platform exposes TDoA, TWR, positions, peer links and quality diagnostics; quantify dynamic timing/error rather than reading an IMU transmission rate as localization rate; reproduce one classical UWB baseline and one compatible strong motion baseline; select an anatomical subsystem and force reference; run the rig ambiguity test; draft participant protocols; freeze the pilot decision rules.

Potential outlets follow the demonstrated contribution: **TNSRE/JBHI** for sensing tied to biomechanical/clinical validity, **TBME/TNSRE** for mechanistic estimation, and **TRO/RA-L/TMRB/ICRA** for a substantive physical interaction/control result. These are fit hypotheses, not promised acceptances; a simple sensor replacement would not meet the intended contribution level.

## 16. Fit to background and target laboratories

### Fit to the researcher's background

The engineering-mechanics background and prior Kalman-filtering/semi-recursive musculoskeletal dynamics work support articulated observation models, uncertainty propagation and inverse-dynamics scrutiny. The current chronic-stroke sparse-sensing work contributes experience with patient heterogeneity, repeated-session splits, missing observations and downstream evaluation.

The doctoral transition is to radio measurement physics, anatomical observability, EMG-informed reduced modeling and physical interaction. Existing biRNN/TCN/SHRED experience helps implement comparators; it does not determine the architecture or make IMU reconstruction the thesis. Existing gait data support pipeline development only where their measurements actually support the question.

Training priorities are UWB protocol/antenna/timing behavior, practical identifiability, EMG acquisition, OpenSim/CEINMS-compatible modeling, measured external forces and human–robot control. A full-body generative model and a new robot-learning algorithm are optional extensions after these foundations work.

### Fit to Mingming Zhang's SUSTech group

The official profile identifies rehabilitation robotics, physical human–robot systems and a UWB/IMU platform [R19]; UI-MoCap and subject-specific upper-limb compliance provide concrete methodological anchors [R02], [R18]. This makes the group a coherent home for a sensing-to-interaction thesis.

The proposed division is: UWB capability/configuration work with the sensing line; controlled human-state experiments with an NMS/biomechanics collaborator; and one bounded robot task with the group's interaction/control line. Existing publications establish topical fit, **not guaranteed access** to a particular robot, dynamometer, optical system, EMG setup or patient cohort. Confirm those resources during the first checkpoint.

| Laboratory/research line | Role in this plan | Evidence and boundary |
|---|---|---|
| **Mingming Zhang / SUSTech** | Primary doctoral setting: UWB platform, physical interaction and rehabilitation task design. | UI-MoCap, compliance control and official research scope [R02], [R18], [R19]. |
| **Hayashibe / Tohoku** | Continuity in neural engineering, mechanics and existing patient-data methods. | The researcher's established training context; no new equipment or exchange availability assumed. |
| **Durandau–Sartori neuromechanics** | Potential methodological collaboration for EMG-informed real-time model/control validation. | CEINMS-RT and MyoSuite [R12], [R15]; institutional collaboration is not presumed. |
| **Pizzolato–Lloyd personalization** | Potential advice on parameter identification, reference uncertainty and individualized mechanics. | Participation in CEINMS-RT [R12]; task-specific expertise/access must be confirmed. |

## 17. Claim gates for “digital twin” and “embodied intelligence”

A UWB-driven avatar supports a **motion-capture** claim. A continuously updated personalized kinematic representation supports a **person-bound motion model** claim. A digital-twin claim in this thesis additionally requires persistent individual binding, identified update provenance, independently evaluated neural–mechanical outputs and locked later-condition/response validation.

A controller driven by that representation supports an **embodied interaction** claim only when its actions affect a measured physical human–device loop. Simulation and HIL claims remain labeled separately. Neither EMG amplitude increase, high task reward, narrow posterior intervals nor a plausible full-body animation proves physiological truth, safe tissue loading or durable recovery.

**Core graduation logic:** determine what UWB can measure; determine what that information supports in a person model; then determine whether the supported information improves an action. The strongest result may include finding that some states or model components are unnecessary.

## References

[R01]–[R21] link directly to primary or author/institutional sources. Full titles, publication status, access depth, novelty boundaries and the counter-evidence search record are in [GAP_VALIDATION_AND_NEAREST_WORK.md](GAP_VALIDATION_AND_NEAREST_WORK.md).

[R01]: https://pubmed.ncbi.nlm.nih.gov/24403428/
[R02]: https://pubmed.ncbi.nlm.nih.gov/38408007/
[R03]: https://siplab.org/projects/UltraInertialPoser
[R04]: https://arxiv.org/html/2505.09393v1
[R05]: https://siplab.org/projects/GroupInertialPoser
[R06]: https://siplab.org/projects/UltraDiffusionPoser
[R07]: https://arxiv.org/html/2601.19519v1
[R08]: https://tiers.utu.fi/publications/
[R09]: https://ieeexplore.ieee.org/document/11420874
[R10]: https://www.mdpi.com/1424-8220/26/18/5738
[R11]: https://pubmed.ncbi.nlm.nih.gov/39579665/
[R12]: https://research.utwente.nl/en/publications/ceinms-rt-an-open-source-framework-for-the-continuous-neuro-mecha-2/
[R13]: https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1254088/full
[R14]: https://link.springer.com/article/10.1186/s12984-025-01629-5
[R15]: https://proceedings.mlr.press/v168/caggiano22a.html
[R16]: https://www.nature.com/articles/s41586-024-07382-4
[R17]: https://link.springer.com/article/10.1186/s12984-026-02136-x
[R18]: https://www.sciencedirect.com/science/article/abs/pii/S092188901930898X
[R19]: https://www.sustech.edu.cn/en/faculties/zhangmingming.html
[R20]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10422251/
[R21]: https://pubmed.ncbi.nlm.nih.gov/30056607/
