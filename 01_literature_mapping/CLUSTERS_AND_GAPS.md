# Main Research Clusters and Uncovered Space

## Executive synthesis

The field is not one coherent "human NMS digital twin" literature. It is a set of partially connected programs:

1. personalized biomechanics and treatment simulation;
2. neural decoding and EMG-/motor-unit-driven NMS models;
3. scalable musculoskeletal Embodied AI;
4. wearable/field observability;
5. rehabilitation and assistive robot control;
6. tissue-scale and longitudinal health prediction.

Most mapped studies are **twin-enabling L1–L2 components**. Some reach L3 predictive behavior or L4 closed-loop assistance. No seed paper in this first pass convincingly demonstrates an uncertainty-aware, longitudinal L5 neuromusculoskeletal twin that jointly updates neural control, muscle/tendon, joint/tissue, and device interaction in real-world patients.

## Cluster 1 — Personalized NMS models and calibration

**Core lineages:** Pizzolato–Lloyd–Saxby–Diamond; Fregly/Shourijeh; Besier; OpenSim/CEINMS.

**What is mature**

- EMG-driven and EMG-informed models map neural surrogates to muscle forces and joint moments.
- Subject-specific anatomy, wrapping surfaces, muscle strength, electromechanical delay, and synergies can materially change internal-load estimates.
- Open-source infrastructure is improving: OpenSim, CEINMS, nmsBuilder, and the NMSM Pipeline.
- Whole-body-to-tissue pipelines can estimate cartilage/tendon mechanics and support treatment hypotheses.

**What is not mature**

- Parameter identifiability remains weak: different parameter sets can fit the same external moment.
- Calibration is often task-specific and validated on the same or closely related tasks.
- Patient-specific geometry is expensive; learned surrogates need strong out-of-distribution checks.
- Predictive treatment studies usually stop before prospective clinical outcome validation.

## Cluster 2 — Neural control and NMS mapping

**Core lineages:** Sartori–Farina–Durandau; motor-unit/HD-EMG interfaces; synergy and predictive neuromechanics.

**What is mature**

- Surface/intramuscular EMG and motor-unit discharge can drive mechanistic estimates of muscle force, joint moment, and movement.
- Physiological model constraints can make prosthetic commands more plausible and robust.
- Muscle synergies and low-dimensional representations reduce actuation complexity.

**What is not mature**

- Sparse muscle coverage and changing EMG conditions still create observability gaps.
- Neural plasticity, fatigue, spasticity, and day-to-day changes are rarely modeled together.
- A low-dimensional controller can be efficient without necessarily corresponding to biological neural organization.
- Few studies carry uncertainty from neural decoding through muscle/tissue predictions.

## Cluster 3 — Musculoskeletal Embodied AI

**Core platforms/methods:** MyoSim, MyoSuite, MyoDex, MotorNet, Latent Exploration, DynSyn, MS-Human-700, MyoChallenge.

**What is mature**

- Physiological simulators now support contact-rich, high-dimensional control and assistive-device models.
- Curriculum, latent exploration, task priors, and dynamic synergies greatly improve learning efficiency.
- Shared benchmarks create a common interface between robotics, ML, biomechanics, and neuroscience.

**What is not mature**

- Most policies control a generic simulated body, not a synchronized person.
- Sim-to-real transfer to patients is largely unproven.
- Reward functions and training data can produce capable but physiologically non-identifiable solutions.
- Benchmarks rarely evaluate calibration burden, sensor dropout, disease progression, clinical safety, or long-term co-adaptation.

**Interpretation:** Embodied AI provides the policy and scalable simulation layer; it does not become a patient digital twin until individual binding, updating, validation, and action are demonstrated.

## Cluster 4 — Wearable and field observability

**Representative modalities:** EMG/HD-EMG, intramuscular EMG, ultrasound, optomyography, deformation/force myography, IMU, pressure, smartphone video.

**What is mature**

- OpenSense and OpenCap extend kinematic/dynamic analysis beyond conventional laboratories.
- Muscle-oriented modalities can reveal intent or deep-muscle morphology not captured by kinematics alone.
- Multimodal IMU–EMG models can estimate joint moments in constrained tasks.

**What is not mature**

- Most systems estimate an output but do not assess whether the full latent NMS state is observable.
- Calibration drift, electrode/probe shift, missing sensors, and domain change are inconsistently tested.
- Tissue and neural state are rarely synchronized at compatible timescales.
- Many wearable papers remain black-box estimators with no counterfactual or causal model.

## Cluster 5 — Rehabilitation and assistive robotics

**Core lineages:** Durandau–Sartori real-time NMS control; Pizzolato model-based neuroprostheses; Collins/Delp human-in-the-loop personalization; Yanan Sui's rehabilitation and Embodied AI work.

**What is mature**

- Patient-specific EMG-driven models can support voluntary exoskeleton control after stroke/SCI.
- Model-based prosthesis and exosuit interfaces can operate online across tasks and loads.
- Human-in-the-loop and opportunistic adaptation can produce meaningful real-world assistance even without an explicit NMS model.

**What is not mature**

- Small feasibility cohorts dominate; clinical recovery is not the same as short-term control accuracy.
- Safe co-adaptation and stability across weeks/months are under-evaluated.
- Device benefit, neural engagement, tissue loading, fatigue, and patient preference are seldom optimized jointly.
- Closed-loop stimulation/robot control rarely incorporates predictive tissue damage or neuroplastic adaptation.

## Researcher map

| Researcher/lineage | Distinctive contribution in this map | Current bridge to target theme | Main missing link |
|---|---|---|---|
| Guillaume Durandau | Real-time EMG-driven NMS; patient exoskeleton control; MyoSim/MyoSuite | Strong L2–L4 human–robot synchronization | Larger longitudinal patient studies and uncertainty-aware adaptation |
| Massimo Sartori | Neural-to-musculoskeletal mapping; model-based bionics; scalable simulation | Strongest continuum from motor neurons to wearable robots | Clinical translation at scale and multi-timescale physiology |
| Claudio Pizzolato | CEINMS; multiscale personalized modeling; NMS digital-twin framework | Strong L1–L3 patient/tissue modeling and clinical vision | Continuous closed-loop sensing/control and prospective outcome trials |
| David Lloyd / Laura Diamond / David Saxby | Personalized loading, calibration, clinical biomechanics | High-quality internal-mechanics and pathology layer | Real-time deployment and closed-loop treatment |
| Benjamin Fregly / NMSM Pipeline | Patient-specific treatment optimization | Explicit counterfactual planning toward L3 | Prospective clinical verification and automated personalization |
| Yanan Sui | Musculoskeletal Embodied AI, synergies, full-body self model; earlier SCI rehab | High-dimensional policy and benchmark layer | Patient-specific sensing, sim-to-real, clinical closed loop |
| Delp / Collins line | OpenSim/OpenCap and real-world exoskeleton personalization | Field sensing and effective online adaptation | Explicit neural/muscle/tissue state in the optimization loop |

## Venue coverage interpretation

- **Well represented:** TNSRE, TBME, Scientific Reports, JNER, Journal of Biomechanics.
- **Relevant but terminology differs:** TRO papers emphasize online exoskeleton personalization; their biological model may be implicit.
- **JBHI:** strong on wearable state/kinetics estimation and emerging imaging-oriented digital twins; fewer papers close the neural–muscle–skeleton loop.
- **NeurIPS/ICML/L4DC/ICRA:** strong on scalable muscle-driven control and benchmarks, usually simulation-only.
- **CoRL:** no clear main-track patient-specific NMS digital-twin anchor was identified in round one; related work appears in workshops or other ML/robotics venues.

## Highest-priority uncovered questions

1. **Online identifiability:** Which neural, muscle, tendon, and joint parameters can be updated from realistic wearable sensor sets, and with what posterior uncertainty?
2. **Multi-timescale adaptation:** How should milliseconds-scale neural drive, minutes-scale fatigue, weeks-scale motor learning, and months-scale tissue remodeling coexist in one twin?
3. **Patient-specific Embodied AI:** Can a learned policy be conditioned on a calibrated patient NMS model and safely adapt without exploiting simulator error?
4. **Causal treatment prediction:** Can the twin predict an individual's response to altered assistance, FES, surgery, or training outside the calibration distribution?
5. **Closed-loop safety:** How are prediction uncertainty, sensor dropout, and physiological constraints converted into safe robot/stimulation actions?
6. **Clinical endpoints:** Do model-guided decisions improve function, pain, participation, or recovery—not only torque/angle prediction?
7. **Real-world observability:** What is the minimal multimodal sensing set (not necessarily minimal IMUs) that preserves clinically actionable NMS state?
8. **Benchmark alignment:** Can MyoSuite/MS-Human-style tasks be paired with synchronized patient datasets and standardized sim-to-real metrics?
9. **Equity and morphology:** How do sex, age, pathology, assistive-device fit, and underrepresented anatomy affect personalization and failure?
10. **Governance:** Who owns the longitudinal twin, how are updates audited, and how are clinicians/users shown uncertainty and intervention rationale?

## Round-two expansion queue

- Backward/forward citation chasing from the 25 highest-priority core papers.
- Full-text maturity coding `L0–L5` and personalization vector `P0–P6`.
- Dedicated review of neural plasticity, spasticity, fatigue, and FES models.
- Dedicated review of tissue adaptation/remodeling and multiscale uncertainty.
- Dedicated CoRL/TRO/JBHI search to locate terminology-mismatched bridges.
- Clinical-trial registry and prospective-study search.
- Code/data availability and real-time latency audit.
- Citation-network and co-authorship map after deduplication.

