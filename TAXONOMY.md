# Human Neuromusculoskeletal Digital Twin / Embodied AI Taxonomy

**Version:** first-pass map, 2026-09-01  
**Scope:** human neuromusculoskeletal (NMS) systems, with digital twin and Embodied AI treated as overlapping but non-equivalent research programs.

## 1. Operational boundary

This map does **not** treat every musculoskeletal simulation, wearable estimator, or virtual human as a digital twin. A paper is coded along a maturity ladder so that the term remains falsifiable.

| Level | Operational label | Minimum requirement | Typical examples | Not sufficient on its own |
|---|---|---|---|---|
| L0 | Generic simulator | A reusable human/animal model with no individual binding | Generic OpenSim/MuJoCo model; population-average policy | Anatomical realism alone |
| L1 | Subject-specific digital model | Individual parameters are instantiated, but updates are offline | MRI-derived geometry; calibrated EMG-driven model | Anthropometric scaling alone when clinically important parameters remain generic |
| L2 | Digital shadow | The physical person updates the model one-way, episodically or continuously | Wearable-to-model state estimation; online joint-load inference | Streaming a sensor dashboard without a mechanistic or predictive state model |
| L3 | Predictive twin | L2 plus validated counterfactual/predictive capability for unseen conditions | Treatment optimization; internal tissue-load prediction under alternative actions | Retrospective fit to the same task |
| L4 | Closed-loop twin | Digital state or prediction changes feedback, stimulation, robot assistance, or therapy | NMS-model-driven exoskeleton/prosthesis control | A generic controller that merely shares the same device |
| L5 | Longitudinal adaptive twin | L4 plus multi-timescale adaptation (motor learning, fatigue, plasticity, tissue remodeling/disease progression) with uncertainty-aware updates | Target state for the field | A short-session online calibration without longitudinal physiology |

The matrix column `dt_status` records the authors' framing and our evidence-aware classification:

- `explicit_digital_twin`: the paper explicitly uses and substantively implements or defines the term.
- `twin_enabling`: a required component or partial architecture, but not a full twin.
- `simulation_only`: a closed simulated perception-action loop without a synchronized physical person.
- `review`: synthesis/framework without a new implemented twin.

## 2. System taxonomy

### A. Physical scope

1. **Neural control:** cortical/spinal/motor-unit drive, muscle synergies, reflex/feedback policies, motor learning.
2. **Muscle-tendon:** activation and contraction dynamics, fatigue, force-length-velocity behavior, tendon mechanics.
3. **Skeleton and joints:** kinematics, joint moments, contact forces, ligament mechanics.
4. **Tissue and pathology:** cartilage, tendon, bone, muscle morphology, degeneration, remodeling.
5. **Human-device-environment:** prosthesis, exoskeleton, FES, rehabilitation robot, contact-rich tasks and terrain.

### B. Observability / sensing

| Layer | Representative modalities | What it observes | Main failure modes |
|---|---|---|---|
| Neural surrogate | surface EMG, HD-EMG decomposition, intramuscular EMG, EEG/BCI | excitation, motor-unit discharge, intent | electrode shift, crosstalk, nonstationarity, incomplete muscle coverage |
| Muscle state | ultrasound, optomyography, force/deformation myography, mechanomyography | morphology, contraction, deep-muscle state | coupling pressure, placement, depth/field-of-view, device bulk |
| Movement state | optical/markerless video, IMUs, encoders | pose, segment orientation, velocity | occlusion, drift, calibration, soft-tissue artifact |
| External mechanics | force plates, pressure insoles, interaction torque, load cells | ground/device interaction | limited coverage, shoe/device dependence, lab confinement |
| Anatomy/tissue | MRI, CT, ultrasound imaging | geometry, material proxies, pathology | cost, static snapshots, segmentation and registration error |
| Context/outcome | clinical scores, pain, fatigue, metabolic cost, task/environment | goals and utility | sparse labels, subjective bias, delayed outcomes |

**IMU rule:** IMU is one member of the movement-state layer. It is not used as the organizing center of this map.

### C. Model family

1. **Physics-based multibody NMS:** inverse/forward dynamics, Hill-type muscle-tendon units, EMG-driven or EMG-informed neural control.
2. **Finite-element / multiscale:** joint and tissue stress/strain coupled to whole-body loads.
3. **Neural-control models:** motor-unit pools, reflex/CPG structures, synergies, optimal feedback control.
4. **Hybrid physics–learning:** learned observation/state models, parameter inference, differentiable NMS, residual/surrogate models.
5. **Embodied policy/world model:** reinforcement learning, imitation, curriculum learning, latent/synergy action spaces.
6. **Treatment/control layer:** predictive optimization, model predictive control, human-in-the-loop optimization, safe/adaptive robot control.

### D. Personalization

Personalization should be coded by **what changes**, not by whether the paper uses the word "personalized":

- `P0 population`: no individual binding.
- `P1 anthropometric`: mass, height, segment length, coarse scaling.
- `P2 anatomical`: joint axes/centers, muscle paths, bone/tissue geometry.
- `P3 physiological`: maximum force, tendon slack length, activation/contraction dynamics, electromechanical delay.
- `P4 neural`: EMG mapping, motor-unit behavior, synergies, impairment-specific residual control.
- `P5 task/context`: environment, device, fatigue, speed, load, disease state.
- `P6 online/longitudinal`: parameters or latent states update during/over sessions with uncertainty tracking.

### E. Coupling and action

- **Offline reconstruction:** batch fitting or retrospective estimation.
- **Episodic synchronization:** calibration at session boundaries or after a data block.
- **Continuous one-way synchronization:** streaming physical-to-digital state update.
- **Feedback:** model outputs inform a patient, clinician, or user.
- **Assistive control:** model output commands a prosthesis, exoskeleton, FES, or robot.
- **Closed-loop co-adaptation:** human and controller both change; safety and stability are evaluated.

### F. Validation ladder

1. Numerical verification / software tests.
2. In-silico benchmark.
3. Healthy-participant laboratory validation.
4. Patient feasibility / small clinical cohort.
5. Prospective clinical decision or device study.
6. Comparative trial / randomized evaluation.
7. Longitudinal real-world outcome and model-updating validation.

## 3. Embodied AI versus digital twin

Embodied AI emphasizes learning and control through a body–environment loop. A digital twin emphasizes binding to a **particular physical person**, synchronization, prediction, and an actionable lifecycle. MyoSuite, MyoDex, DynSyn, MotorNet, and MS-Human-700 are therefore mapped as powerful `simulation_only` or twin-enabling substrates unless they are connected to an identified human and validated across updates.

The most important research bridge is:

> scalable embodied policies + patient-specific NMS state estimation + uncertainty-aware online calibration + safe human/device feedback.

## 4. Recommended coding additions for round two

- Maturity level `L0–L5` assigned after full-text reading.
- Personalization vector `P0–P6` rather than a single yes/no field.
- Validation cohort size, pathology, sex/age reporting, and out-of-distribution test.
- Model update rate, latency, sensor dropout handling, and calibration burden.
- Uncertainty type: aleatoric, epistemic, parameter posterior, confidence calibration.
- Availability of code, model, data, and real-time implementation.

