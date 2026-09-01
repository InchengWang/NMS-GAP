# Cross-Paper Synthesis: Human Neuromusculoskeletal Embodied AI

## Executive judgment

The 49-paper core set contains three mature but weakly connected research families:

1. physiologically grounded human NMS models with subject-specific calibration;
2. scalable muscle-driven simulated agents and control algorithms;
3. physical human–robot loops for prostheses, exosuits and exoskeletons.

No paper fully connects all three with longitudinal patient rehabilitation evidence. The central research opportunity is therefore not another generic muscle-driven RL benchmark and not another standalone wearable estimator. It is a **patient-grounded bridge from neural/NMS state to adaptive action, physical interaction and externally validated rehabilitation consequences**.

## Classification result

| Primary type | Count | What the group really contributes |
|---|---:|---|
| `modeling` | 17 | Physiological body models, personalization, identifiability, multiscale mechanics and treatment simulation. |
| `embodied_ai` | 12 | Simulated muscle-driven agents, action representations, motor priors, control benchmarks and one conceptual sensorimotor framework. |
| `robotics` | 6 | Physical prosthesis/exosuit/exoskeleton interaction and online assistance. |
| `sensing` | 5 | Neural, muscle, kinematic or morphological observation layers. |
| `embodied_ai_related_weak` | 5 | Reviews, roadmaps and frameworks without an implemented embodied agent. |
| `control` | 3 | Online personalization/optimization whose main novelty is action adaptation rather than the body model or hardware. |
| `rehabilitation` | 1 | Direct validation of a rehabilitation-relevant state/outcome without a new embodied controller. |

## Embodiment evidence

| Level | Count | Interpretation |
|---|---:|---|
| `E0` | 6 | Conceptual or review evidence only. |
| `E1` | 21 | Strong sensing/body-model substrate, but no evaluated action–environment loop. |
| `E2` | 14 | Simulated or virtual sensorimotor embodiment. |
| `E3` | 6 | Physical human/device loop, mainly short-session or non-patient evidence. |
| `E4` | 2 | Preliminary patient-grounded adaptive physical systems. |
| `E5` | 0 | No longitudinal, uncertainty-aware clinical co-adaptation system in the core set. |

## Strongest work by dimension

| Dimension | Strongest examples | Real contribution | Decisive limitation |
|---|---|---|---|
| Human NMS body model | Lloyd–Besier; CEINMS; Durandau 2018; Sartori et al. 2017 | Neural drive is linked to activation, muscle force and joint mechanics in interpretable, often personalized models. | Internal force/state truth and longitudinal identifiability remain limited. |
| Embodied-intelligence substrate | MotorNet; MyoSim; MyoSuite; MS-Human-700 | Enables policies to act through muscle-driven bodies and interact with tasks/devices at scale. | Generic simulation is not a human-bound model; simulator reward can hide physiological error. |
| Sensorimotor-control algorithm | Learn to Move; curriculum RL; latent exploration; DynSyn; MyoDex | Demonstrates locomotion/dexterity and reusable or adaptive control representations. | Almost entirely simulation-only; weak evidence for patient physiology or hardware transfer. |
| Human–robot interaction | Durandau 2019; Sartori 2018; Lotti 2020; Zhang 2017; Slade 2022; Kang 2025 | Closes real-time loops between human signals/outcomes and prosthesis or exoskeleton action. | Mechanistic NMS state, calibrated uncertainty and longitudinal patient evidence rarely coexist. |
| Assistive control | Durandau 2019; Zhang 2017; Slade 2022; Kang 2025 | Shows voluntary, outcome-optimized or rapidly individualized physical assistance. | Black-box objectives in some systems; small patient samples in mechanistic systems. |
| Rehabilitation relevance | NMSM Pipeline; Esrafilian 2022; Wang 2026; Cheng 2018; Kang 2025 | Introduces treatment counterfactuals, tissue consequences, neural engagement or patient feasibility. | Predicted benefit, acute physiology and durable recovery are often conflated. |
| Subject-specific validation | Akhundov 2022; Savage 2023; Diaz 2026; Durandau 2019; Wang 2026 | Tests anatomy/calibration or uses an identified person's model to change action. | Personalization may improve output fit without identifying true internal parameters. |

## Papers closest to human NMS Embodied AI

### `E4`: strongest integrated evidence

- **ROB001 — Durandau et al. (2019):** residual neural drive → subject-specific NMS estimate → physical multi-joint exoskeleton action, including paresis participants. It is limited by three heterogeneous patients, short laboratory testing, no uncertainty and no recovery outcome.
- **ROB011 — Kang et al. (2025):** fast online human–exoskeleton adaptation and physical assistance with a preliminary stroke case. It is limited by a single patient result and lacks an explicit mechanistic neural–muscle–skeletal state.

These papers are complementary rather than interchangeable: ROB001 has stronger neuromechanical embodiment, while ROB011 has stronger rapid interaction adaptation.

### `E3`: important physical precedents

- **ROB002:** real-time NMS wrist–hand prosthesis control.
- **ROB003:** adaptive model-based soft-exosuit assistance.
- **ROB005:** human-in-the-loop metabolic optimization; strong embodiment but weak NMS representation.
- **ROB006:** real-world online exoskeleton personalization; strong deployment evidence but implicit physiology.
- **NMS018:** imaging-personalized body model changes robot therapy and is checked with EMG.
- **NMS015:** continuous differentiable NMS calibration coupled to exoskeleton control, with weaker accessible evidence in this critique pass.

## What should and should not be called Embodied AI

- **Yes, simulated Embodied AI:** a policy controlling a muscle-driven body in an environment, even if no real person is bound to it.
- **No, not an embodied agent:** an offline OpenSim/CEINMS model, sensor reconstruction system or clinical dashboard with no action loop.
- **Embodied control but not NMS modeling:** human-in-the-loop exoskeleton optimization that treats physiology as a black-box cost.
- **NMS modeling but not embodied intelligence:** accurate personalized muscle/tissue estimates that never change an action or feedback decision.
- **Closest to human NMS Embodied AI:** a real person's neural/mechanical state changes physical device action and the response is independently evaluated.

## Cross-cutting limitations

1. **Simulation-to-human gap:** the strongest AI algorithms are evaluated inside generic simulators.
2. **Model-to-action gap:** the strongest physiological models are mainly offline estimators or planners.
3. **Mechanism-to-deployment gap:** real-world exoskeleton optimization often works without an explicit NMS state.
4. **Patient evidence gap:** patient cohorts in closed-loop systems are usually single cases or very small.
5. **Longitudinal gap:** fatigue, learning, impairment change and device co-adaptation are seldom followed across days or weeks.
6. **Safety and uncertainty gap:** model/sensor uncertainty rarely defines a physical fallback or abstention action.
7. **Outcome gap:** reward, torque or kinematics are often reported without neural engagement, tissue safety, function or recovery.
8. **Subject-specific validity gap:** fitted parameters can compensate for one another; good control performance does not prove a correct internal body model.

## PhD implication

A defensible human NMS Embodied-AI program should connect, in stages:

1. a subject-specific neural–muscle–skeletal state with explicit identifiability and uncertainty;
2. a generic muscle-driven control prior or model-based controller;
3. patient-posterior conditioning and out-of-distribution/simulator-exploitation tests;
4. a physical rehabilitation or assistive interaction with a safe fallback;
5. longitudinal evaluation of function, neural engagement and biomechanical/tissue consequences.

The user's current sparse-to-dense IMU work is useful for missing-observation robustness and fault handling, but it should remain one sensing component. The PhD-level question is whether a patient-grounded NMS state changes embodied action safely and produces an externally validated consequence.

