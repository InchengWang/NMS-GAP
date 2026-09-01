# Cross-Paper Critical Synthesis

## Executive judgment

The 49 core papers do **not** contain a complete longitudinal human neuromusculoskeletal digital twin. They contain five strong but only partially connected assets:

1. neural-drive observation through EMG, HD-EMG decomposition and intramuscular EMG;
2. subject-/patient-specific muscle–tendon, joint and tissue models;
3. counterfactual simulations for load and treatment planning;
4. scalable muscle-driven Embodied AI simulators and control priors;
5. online personalization and robot/prosthesis intervention loops.

The central gap is therefore an integration-and-validation gap: a system must infer a person's NMS state, quantify uncertainty, predict a meaningful unseen outcome, update over time, and safely change an intervention.

## Classification result

| Research layer | Strongest real contribution | Why it is not yet a full twin |
|---|---|---|
| Sensing | OpenSense/OpenCap scale kinematics; ultrasound and neural interfaces expose otherwise hidden state. | Most stop at motion/intent estimation and do not prove that added sensing identifies muscle/tissue state or improves decisions. |
| Modeling | CEINMS/OpenSim and neural-to-mechanical models provide mechanistic state and load estimates. | Internal muscle/contact/tissue states often lack direct ground truth; parameter compensation and identifiability remain weakly handled. |
| Personalization | MRI/ultrasound calibration, wrapping geometry, continuous calibration and patient-specific FE improve individual binding. | Most are single-session `L1`; anatomy/parameter personalization is not longitudinal state synchronization. |
| Prediction | NMSM Pipeline and multiscale treatment simulations ask clinically meaningful counterfactuals. | Validation commonly uses hypothetical/small cases or model-derived endpoints rather than prospective treatment outcomes. |
| Embodied AI | MyoSuite, MotorNet, MyoDex, DynSyn and MS-Human-700 make high-dimensional control tractable. | They are generic `L0` simulators/policies; realism, high actuator count or “self model” language does not bind them to a patient. |
| Assistance | Durandau/Sartori model-based control and rapid online exoskeleton adaptation implement real intervention loops. | Cohorts are small, sessions short, physiological state incomplete and uncertainty/longitudinal adaptation rarely validated. |

## Closest work to a real NMS digital twin

“Closest” here means architectural proximity, not clinical readiness.

| Paper | Why it is close | Remaining decisive gap |
|---|---|---|
| ROB001 Durandau et al. (2019) | Residual EMG → subject-specific NMS estimate → real-time exoskeleton command, including paresis patients. | Only 3 patients, heterogeneous devices, short laboratory feasibility, no longitudinal/uncertainty layer. |
| ROB002 Sartori et al. (2018) | Real-time personalized NMS mapping supports simultaneous prosthesis control. | Control decoding rather than complete patient state; limited evidence for daily multi-session function. |
| ROB003 Lotti et al. (2020) | Adaptive biomechanical model is embedded in a soft exosuit control loop. | Mainly engineering demonstration; patient and clinical outcome validation absent. |
| ROB011 Kang et al. (2025) | Fast online human–exoskeleton adaptation, prediction and actuation; preliminary stroke result. | Clinical evidence is a single-patient pilot; no mechanistic longitudinal state or calibrated uncertainty. |
| NMS014 Pizzolato et al. (2020) | Real-time sensing drives a personalized FE surrogate and local Achilles strain estimate with smartphone feedback. | Single subject, offline initial calibration and no human-in-the-loop intervention validation. |
| NMS015 Hambly et al. (2025) | Continuous NMS calibration reaches offline-level fit rapidly, moving personalization into the session. | Joint-moment fit does not establish correct internal states; longitudinal clinical stability is untested. |
| NMS018 Li et al. (2024) | Sparse MRI personalizes a lower-limb model used to control an exoskeleton. | Four volunteers, indirect force validation and no patient/longitudinal test. |

NMS011 (Hammond et al., 2025) is the strongest open predictive-treatment substrate: it makes a patient-specific post-stroke counterfactual executable and reproducible. Its evidence is still a single hypothetical use case rather than prospective proof that the selected treatment improves a patient's outcome.

## Papers that should not be called digital twins

- A generic OpenSim/MuJoCo model or muscle-driven RL policy is `L0`, even if anatomically detailed.
- A one-time personalized model is `L1`, not a synchronized twin.
- A wearable estimator or dashboard is at most a `L2` shadow unless it updates a decision-relevant model.
- A controller optimized from metabolic cost may be `L4` closed-loop personalization while still not being an NMS twin, because it lacks neural–muscle–skeletal state.
- A framework can describe `L4–L5` without itself constituting an implemented twin.

## Cross-cutting evidence weaknesses

1. **Internal-state ground truth:** muscle force, contact force and tissue strain are often evaluated through joint moments or literature ranges generated by related model assumptions.
2. **Identifiability:** good torque/kinematic fit can arise from compensating neural, muscle and geometry parameters.
3. **Calibration–prediction separation:** many evaluations test the same task family used for calibration rather than unseen intervention/context.
4. **Clinical endpoint gap:** controller accuracy and simulation plausibility are frequently presented without prospective functional, pain, safety or recovery outcomes.
5. **Longitudinal gap:** electrode placement, fatigue, motor learning, plasticity, tissue remodeling and disease progression are rarely modeled together across sessions.
6. **Uncertainty gap:** few systems propagate sensor, parameter and model-form uncertainty into intervention decisions.
7. **Population gap:** patient studies are often single cases or very small heterogeneous cohorts; sex, age, severity and context generalization are inconsistent.
8. **Reproducibility gap:** modeling platforms are often open, while patient data, calibrated models, real-time controller stacks and hardware specifications are not jointly available.

## PhD-relevant research program

The highest-value thesis is not “an IMU digital twin” or another generic muscle-driven agent. It is an uncertainty-aware bridge:

> multimodal wearable/clinical observation → patient-specific neural–muscle–skeletal state → validated counterfactual → safe adaptive rehabilitation/assistance.

A defensible staged program would be:

1. identify the minimal multimodal signals that make clinically relevant NMS states observable;
2. calibrate a mechanistic or hybrid model with explicit parameter posterior/identifiability analysis;
3. separate calibration tasks from prediction tests and validate an unseen load, movement or intervention response;
4. close the loop with feedback/robot assistance under safety constraints;
5. test cross-day recalibration, fatigue and motor-learning adaptation in a patient cohort;
6. report whether the twin changes a clinical/device decision and whether that change improves an external outcome.

This program directly connects the Durandau–Sartori neural/control lineage, the Pizzolato–Lloyd personalization/multiscale lineage, and the Sui/Embodied-AI control lineage while preserving the distinction between a useful simulator and a patient twin.
