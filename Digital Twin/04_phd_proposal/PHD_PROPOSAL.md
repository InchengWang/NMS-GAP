# PhD Research Proposal

## Title

**Toward an Uncertainty-Aware Longitudinal Human Neuromusculoskeletal Digital Twin: Observable State Estimation, Two-Timescale Adaptation, and Safe Rehabilitation Decisions**

## Proposal status and scope

This is an advisor-facing research plan derived from the preceding literature map, core-paper critiques, and counter-evidence gap validation. It deliberately uses **toward**: the work will only be called a longitudinal neuromusculoskeletal (NMS) digital twin if the integrated system satisfies the claim gate in [`NOVELTY_AND_NEAREST_WORK.md`](NOVELTY_AND_NEAREST_WORK.md).

The clinical use case is chronic post-stroke gait rehabilitation and wearable robotic assistance, because it provides meaningful asymmetry, impairment, fatigue, adaptation and device-interaction questions. The scientific target is broader than gait-event detection or inertial-sensor reconstruction. IMUs are one possible kinematic source; EMG, plantar pressure, laboratory kinetics and targeted anatomical or muscle-state measurements are included only when they make a prespecified NMS state or decision observable.

---

## 1. Background and motivation

Human rehabilitation and assistive robotics must act on a system whose internal state is only partially observable. The same joint motion can arise from different neural recruitment, muscle weakness, co-contraction, tendon mechanics or compensatory strategies. A model calibrated once in a laboratory can therefore fit motion or joint moment while remaining wrong about the internal state that matters for treatment or assistance.

A useful human NMS digital twin should do more than reproduce movement. It should:

1. bind a neural–muscle–skeletal model to a specific person;
2. update that model from repeated physical observations;
3. express what is and is not identifiable from the available sensors;
4. predict a held-out future state, context or intervention response;
5. propagate uncertainty into feedback, assistance or abstention;
6. remain valid as fatigue and rehabilitation adaptation change the person.

The literature already supplies many of these components. The unresolved research problem is whether they can be joined and validated without hiding non-identifiability, simulator mismatch or longitudinal change behind average prediction accuracy.

---

## 2. State of the art

### 2.1 Neuromusculoskeletal modeling

OpenSim/CEINMS-style models link kinematics, external forces, EMG-derived excitation, muscle–tendon dynamics and joint mechanics. Hybrid NMS methods can infer unmeasured muscle excitation while preserving measured EMG, and real-time EMG-driven models can extrapolate to tasks or degrees of freedom not used in calibration. Their main limitation for digital-twin use is that matching net joint moments does not uniquely validate individual muscle force, tissue load or physiological parameters.

### 2.2 Sensor-to-state estimation

OpenSense and OpenCap make wearable or low-cost motion estimation scalable; EMG exposes neural drive; pressure sensing constrains foot–ground interaction; ultrasound and medical imaging can constrain muscle or anatomy when justified. Sparse-sensing studies show that fewer channels may reproduce a selected output, but they rarely establish formal identifiability of the internal state required for a downstream decision across patients and sessions.

### 2.3 Subject-specific personalization and uncertainty

Sequential Bayesian self-calibration, rapid continuous calibration and NMS-informed Bayesian neural networks already demonstrate online updating or uncertainty estimation. The residual issue is their combination: a multi-joint patient model whose practically identifiable states remain calibrated on unseen sessions and whose uncertainty separates sensor noise, parameter ambiguity and model mismatch.

### 2.4 Predictive simulation and intervention planning

The NMSM Pipeline integrates subject-specific joints, muscle–tendon properties, neural control and treatment optimization, while SimCP and multiscale models support patient-specific counterfactuals. A randomized gait-retraining trial has already shown that personalized biomechanical decisions can improve patient outcomes. Consequently, this proposal does **not** claim that model-guided intervention or clinical benefit is absent. It tests the narrower question of whether a synchronized NMS posterior predicts a particular patient's response outside calibration before the model is refitted.

### 2.5 Assistive robotics and Embodied AI

Durandau–Sartori neuromechanical interfaces, adaptive model-based exosuits and recent simulation-to-hardware policies demonstrate meaningful closed loops. MyoSuite, MyoDex and MyoAssist provide reusable muscle-driven control environments. However, healthy-device deployment, patient-conditioned simulation, uncertainty-aware control and physiological safety are usually demonstrated in different systems. A simulator or policy alone is not a patient twin.

### 2.6 Longitudinal validation

MyoSuite represents fatigue and pathology perturbations; real-time personalized multiscale modeling estimates tissue strain; longitudinal EMG studies observe training adaptation. The preceding gap validation found no patient-bound NMS system that jointly identifies and externally validates fast within-session fatigue and slow across-week adaptation. This is the only broad candidate judged `confirmed-open`, but the tractable thesis restricts it to two timescales rather than promising neural drive, motor learning and tissue remodeling simultaneously.

---

## 3. Validated research gap

### Core scientific gap

**G02 — `confirmed-open`, narrowed:** current studies do not jointly identify, synchronize and validate a fast fatigue state and a slower rehabilitation-adaptation state in the same patient-bound NMS model, nor show that separating those states improves locked future-session prediction.

### Enabling residual gaps

- **G07 + G01 — `partially-addressed`:** no broad novelty is claimed for sparse sensing or Bayesian calibration. The residual question is whether a task-appropriate multimodal subset preserves a specified NMS state or decision across sessions with calibrated posterior uncertainty and diagnosed practical identifiability.
- **G05 — `partially-addressed`:** robust controllers and uncertainty-bound assistance already exist. The residual question is how sensing/model uncertainty, dropout and physiological constraints jointly trigger action, abstention or fallback in a patient-conditioned NMS loop.
- **G03 + G04 — `partially-addressed`:** patient-informed policies and treatment simulations exist. The residual question is whether conditioning on an identified patient posterior improves held-out response without exploiting simulator error, and whether a prediction is locked before observing the intervention condition.

### Non-gap and scope boundaries

G06 is not used as novelty because controlled clinical benefit from personalized biomechanical intervention already exists. G09 is a prespecified validity audit rather than the main claim. G10 is responsible system design but outside the central NMS mechanism contribution.

---

## 4. Central research question

**Can a patient-bound hybrid NMS model, updated from decision-relevant multimodal sensing, maintain calibrated state estimates across days, distinguish fast fatigue from slower rehabilitation adaptation, and use that uncertainty to improve or safely withhold a rehabilitation-assistance decision under unseen conditions?**

---

## 5. Central hypothesis

A hierarchical hybrid state-space model that combines an EMG-informed mechanistic NMS core, population-level priors, patient-specific parameters and separate fast/slow latent states will provide better calibrated predictions on locked future sessions than (i) a generic model, (ii) a one-time personalized model, (iii) independent session-by-session recalibration and (iv) a purely data-driven sequence model. If its posterior is used as a safety contract, it will reduce false-safe decisions during sensor loss or distribution shift without unacceptable loss of functional performance.

The hypothesis is falsified if the two latent timescales are not practically distinguishable, if apparent personalization is unstable across sessions, if uncertainty is not calibrated on held-out data, or if uncertainty gating does not improve safety relative to simpler baselines.

---

## 6. Specific aims

## Specific Aim 1 — Identify a decision-sufficient multimodal observation set and calibrate an uncertainty-aware patient NMS state

### Question

Which sensing combination is sufficient to estimate a prespecified neural–mechanical gait state and preserve a rehabilitation/device decision across sessions, and which parameters remain non-identifiable?

### Method

Develop a hybrid sequential estimator around an OpenSim/CEINMS-compatible lower-limb model. Separate:

- slowly varying anatomical and muscle–tendon parameters;
- session-level calibration terms such as electrode gain and sensor alignment;
- stride-level states including neural drive, activation, joint mechanics and selected load variables;
- sensor and model-form uncertainty.

Use Bayesian state-space inference or a differentiable mechanistic surrogate, with population priors and patient-specific posterior updating. Select sensor subsets by posterior contraction or expected information gain for a **named endpoint**, not by reconstruction accuracy alone.

Candidate measurements are targeted lower-limb EMG, plantar pressure, a minimal kinematic source (IMU or multiview video), and a laboratory reference subset with motion capture and force plates. Ultrasound or imaging is optional and used only to constrain a parameter that remains non-identifiable without it.

### Data

1. **Retrospective pilot:** existing chronic-stroke dense-IMU/mocap sessions, used only to test locked-session evaluation, sensor perturbations and movement-state decision preservation.
2. **Main repeated-session cohort:** target 30 enrolled chronic-stroke participants to obtain approximately 24 completers, with the final sample determined by simulation-based power analysis after the pilot. Record multiple walking conditions and repeated sessions. A reference laboratory session contains mocap and force plates; deployable sessions use the selected wearable subset.
3. **Optional public data:** AddBiomechanics/OpenCap-compatible datasets for software validation, never as a substitute for patient binding.

### Feasibility

The retrospective pilot is immediately feasible with the existing stroke data and does not require new sensing claims. The full internal-state study is **medium feasibility** because it requires synchronized EMG and external-force reference data; the design therefore starts with a small prespecified state vector and adds ultrasound or imaging only after an identifiability analysis shows that it is necessary. The target cohort is provisional until ethics, recruitment rate and simulation-based power are confirmed.

### Baselines

- generic scaled OpenSim model;
- one-time personalized CEINMS/OpenSim model;
- sequential Bayesian self-calibration following the Bueno–Montano line;
- rapid continuous calibration following the Hambly line;
- purely data-driven biRNN/TCN/Transformer estimator;
- full-sensor oracle and fixed sparse-sensor configurations;
- measured-sensor downstream baseline for the user's existing gait-event task.

### Evaluation

- external kinematics/kinetics error and, where measurable, EMG/activation or load agreement;
- held-out-session log predictive density, negative log likelihood, CRPS and MAE/RMSE;
- empirical coverage and width of 50%, 80% and 90% posterior intervals;
- profile likelihood, posterior correlation, effective rank and parameter stability;
- decision preservation relative to the reference-sensor decision;
- robustness to realistic rotation, drift, channel dropout and task shift;
- paretic/non-paretic and prespecified severity-stratum audit.

### Expected contribution

A falsifiable account of which NMS states and decisions are observable from which deployable measurements, plus a calibrated online personalization method. The contribution is not “fewer IMUs”; it is decision-specific observability with explicit failure bounds.

### Failure interpretation

If internal NMS states cannot be identified, the thesis will report the equivalence classes or parameters that remain ambiguous and restrict subsequent aims to externally validated states. This negative result is scientifically useful and prevents a false digital-twin claim.

---

## Specific Aim 2 — Separate fast fatigue from slow rehabilitation adaptation in a longitudinal patient twin

### Question

Does explicitly modeling a fast within-session state and a slow across-week state improve future-session prediction, and can the two states be independently anchored to external measurements?

### Method

Extend Aim 1 to a hierarchical two-timescale state-space model:

- **fast state:** fatigue/recovery updated within bouts or strides, constrained by neural drive, torque/force capacity, EMG spectral or amplitude changes and recovery periods;
- **slow state:** cross-session adaptation updated over days or weeks, constrained by strength, functional performance, habitual gait and stable changes in coordination or muscle–tendon parameters.

Compare mechanistic fatigue dynamics, a learned state transition constrained by physiology, and a hybrid residual formulation. Cross-timescale coupling is included only if identifiable. Tissue remodeling is not claimed unless an independently measured tissue endpoint and adequate follow-up become available.

### Data

Use a repeated-measures subset of the Aim 1 cohort during a six-week rehabilitation or gait-training period, conditional on clinical partnership and ethics approval. Proposed time points are baseline, weeks 2, 4 and 6, plus retention. Each visit contains controlled walking bouts, a standardized fatigue/recovery protocol and external anchors such as dynamometry, walking speed/endurance, clinical motor score and targeted EMG features. Ultrasound-derived architecture or tendon measures are secondary and only added when feasible.

### Feasibility

This Aim is **medium feasibility with a rehabilitation partner and low feasibility without one**. It deliberately estimates two timescales rather than neural drive, motor learning and tissue remodeling together. Data collection can begin after the Aim 1 protocol is stable, and the primary analysis remains valid if imaging is unavailable because dynamometry, functional measures and EMG provide independent anchors for the narrowed fatigue/adaptation states.

### Baselines

- static personalized model;
- independent per-session recalibration;
- single latent-state model;
- uncoupled fast and slow models;
- purely recurrent sequence model with matched parameter count;
- oracle model using all reference measurements.

### Evaluation

- locked next-session log predictive density and prediction error;
- prediction of within-session performance decline and recovery;
- association and change sensitivity against prespecified external fatigue and rehabilitation anchors;
- posterior separation of fast and slow states, including cross-correlation and contraction;
- ablation of cross-timescale coupling;
- calibration before, during and after the intervention period;
- subgroup and missing-visit sensitivity analyses.

### Expected contribution

An implemented and externally tested two-timescale synchronization mechanism for a patient NMS model. The advancement is relative to studies that model fatigue, tissue load or longitudinal adaptation separately.

### Failure interpretation

If fast and slow states compensate for one another or do not improve future-session prediction, the integrated claim is rejected. The fallback is a simpler change-point or hierarchical covariate model that quantifies when longitudinal recalibration is necessary and when a static model remains sufficient.

---

## Specific Aim 3 — Test whether posterior uncertainty enables safe held-out rehabilitation or assistance decisions

### Question

Can a patient-conditioned NMS posterior improve a locked prediction or assistance decision under an unseen context while reducing false-safe actions during sensor failure and model mismatch?

### Method

Proceed through gated stages:

1. **Offline counterfactual test:** calibrate on one set of speed, support or device conditions; lock predictions for a held-out condition before refitting.
2. **Patient-conditioned simulation:** bind the Aim 1–2 posterior to an OpenSim/Moco, MyoSuite or MyoAssist-compatible environment. Compare model-predictive control and policy learning, and explicitly search for simulator exploitation through physiology and model-mismatch stress tests.
3. **Safety layer:** convert posterior uncertainty, out-of-distribution score and physiological constraints into continue, attenuate, abstain or fallback actions.
4. **Hardware feasibility, only after gates:** perform a small supervised study with an available rehabilitation robot or wearable device. This stage tests feasibility and safety, not clinical efficacy.

The initial decision may be assistance magnitude, assistance timing, support-device recommendation or task difficulty. It must be chosen before analysis and tied to an external functional or biomechanical endpoint.

### Data

- locked held-out conditions from the repeated-session cohort;
- simulated rollouts with sampled patient posterior, fatigue state, sensor faults and model mismatch;
- if safety gates pass, a target 8–12 participant supervised hardware feasibility study, with a separate protocol and stopping rules.

### Feasibility

Offline held-out prediction and posterior-sampled simulation are **high feasibility** using the Aim 1–2 data and open NMS environments. Patient hardware work is **medium to low feasibility** and is not required for the thesis to succeed: it proceeds only if a compatible device, supervisory controls, ethics approval and the preregistered simulation safety gates are all available.

### Baselines

- generic and one-time personalized NMS controllers;
- robust MPC without calibrated NMS posterior;
- NMS-informed confidence-bound assistance following Zhang et al.;
- experiment-free simulation-trained assistance;
- patient-informed policy using coarse pathology parameters rather than a posterior;
- no-assistance or fixed assist-as-needed condition where ethically and practically appropriate.

### Evaluation

- held-out response prediction and interval coverage before refitting;
- false-safe and false-abstain rates;
- time to detect drift/dropout and time to safe fallback;
- frequency and severity of physiological constraint violations;
- task performance, gait stability/symmetry and user effort;
- simulation-to-recorded or simulation-to-hardware discrepancy;
- for hardware feasibility: adverse events, protocol completion and predefined functional/biomechanical endpoints with confidence intervals.

### Expected contribution

Evidence for or against a practical uncertainty-to-action contract in a patient-conditioned NMS loop. Success would support an `L4` closed-loop prototype and, together with Aim 2, progress toward—not automatically prove—an `L5` longitudinal twin.

### Failure interpretation

If learned policies exploit simulator error, the project reverts to constrained model-predictive or rule-based decisions. If uncertainty is uncalibrated under shift, assistance remains advisory/offline. If safety gates fail, no patient hardware deployment occurs; the failure envelope and abstention requirements remain publishable outputs.

---

## 7. Integrated methodology

### 7.1 Twin state and update architecture

The proposed state is partitioned rather than represented by one opaque embedding:

\[
z_t = \{q_t, \dot q_t, a_t, f_t, \theta_{patient}, c_{session}, h_{fast,t}, h_{slow,k}\},
\]

where \(q_t\) and \(\dot q_t\) are movement states, \(a_t\) is muscle activation/neural-drive state, \(f_t\) represents selected force/load variables, \(\theta_{patient}\) contains stable patient parameters, \(c_{session}\) captures session-specific nuisance calibration, and \(h_{fast,t}\) and \(h_{slow,k}\) represent within-session fatigue and cross-session adaptation. Only components supported by the data will be estimated.

The measurement model maps EMG, plantar pressure and kinematic observations to this state. The transition model combines NMS mechanics with learned residuals. Uncertainty is decomposed where possible into measurement, parameter and residual/model-form components. Updates occur at stride level for fast states and session level for slow states.

### 7.2 Calibration and validation separation

- split by participant and session before windowing;
- lock at least one task/context and one future session from calibration;
- prohibit post-outcome refitting for counterfactual evaluation;
- tune models only within training participants/sessions;
- report personalized, population-prior and unseen-subject performance separately;
- version every patient model and retain the sensor/model update log.

### 7.3 Sensor selection principle

Sensor inclusion is determined by incremental information about the target state or decision. IMU reconstruction is allowed as a missing-data component, but reconstructed channels are never treated as independent ground truth. A modality is retained only if it improves posterior contraction, calibration, external-state validation or decision performance after accounting for burden.

### 7.4 Reproducibility

Release, subject to consent and governance constraints:

- preprocessing and synchronization code;
- model definitions, priors and calibration scripts;
- session-level split manifests;
- sensor-failure generators and preregistered stress tests;
- de-identified or derived benchmark data where permitted;
- container/environment specifications and trained baseline weights;
- a model card describing supported population, failure modes and claim level.

---

## 8. Baseline hierarchy

| Layer | Required baselines | Purpose |
|---|---|---|
| Sensing | measured reference; full deployable set; nested sensor subsets; user's biRNN/TCN reconstruction | Separate observation loss from downstream model value. |
| NMS model | generic scaled model; one-time CEINMS/OpenSim personalization; per-session recalibration | Test whether longitudinal updating adds value beyond standard personalization. |
| Probabilistic inference | sequential Bayesian calibration; deterministic estimator; deep ensemble/BNN alternative | Test posterior calibration and distinguish method benefit from model capacity. |
| Timescale | static, single-state, uncoupled two-state, coupled two-state | Test whether a multi-timescale representation is necessary and identifiable. |
| Prediction | pure data-driven model; mechanistic model; hybrid residual model | Test whether mechanics improves extrapolation rather than only fit. |
| Decision/control | fixed assistance; robust MPC; confidence-bound controller; generic policy; coarse patient-parameter policy | Isolate the value of a calibrated patient posterior and safety gate. |

---

## 9. Metrics and statistical analysis

### 9.1 Primary outcomes

- **Aim 1:** held-out future-session log predictive density and 90% posterior-interval coverage error for prespecified NMS outputs; decision preservation under the selected deployable sensor set.
- **Aim 2:** difference in locked next-session predictive performance between the two-timescale and single-state models, with evidence that the two latent states are separately anchored and not merely compensating parameters.
- **Aim 3:** false-safe rate under prespecified dropout/distribution-shift scenarios, accompanied by functional/task performance and physiological constraint violations.

### 9.2 Secondary outcomes

Kinematic and kinetic MAE/RMSE, correlation where appropriate, CRPS, NLL, calibration slope/intercept, interval width, parameter posterior contraction, gait symmetry, walking speed/endurance, user effort and simulation-to-reality discrepancy.

### 9.3 Statistical plan

1. Define one primary endpoint and one primary baseline contrast per Aim before confirmatory analysis.
2. Estimate sample size by simulation using pilot-derived within-person variance, missingness and expected attrition; do not rely on a post-hoc observed-power calculation.
3. Use hierarchical mixed-effects or Bayesian hierarchical models with participant-level random intercepts and, where supported, random slopes; include session, condition, method and relevant pathology/severity covariates as prespecified fixed effects.
4. Use participant-level bootstrap confidence intervals for non-Gaussian error and safety metrics; never treat gait cycles as independent participants.
5. For posterior calibration, report empirical coverage with confidence intervals, calibration curves, CRPS and interval width together.
6. For method comparisons, use nested likelihood or information-criterion comparisons when models are compatible and paired participant-level permutation/bootstrap tests otherwise.
7. Correct secondary-family multiplicity with Holm's method or control the false-discovery rate; report effect sizes and uncertainty, not only p-values.
8. Handle missing visits with a model appropriate to the missingness mechanism and perform pattern-mixture or complete-case sensitivity analysis.
9. Audit paretic/non-paretic side, severity, age and sex only where sample size supports inference; otherwise report descriptive uncertainty rather than fairness claims.

Decision-preservation margins and physiological safety thresholds will be selected with clinical/robotics collaborators before the locked test. The proposal does not invent universal thresholds from the present literature map.

---

## 10. Expected contributions

### Scientific

- Evidence on whether fast fatigue and slower rehabilitation adaptation are distinguishable and predictively useful within one patient NMS model.
- A quantified boundary between observable and non-identifiable patient states under realistic sensing.

### Methodological

- A hierarchical hybrid inference framework that separates patient, session, fast and slow states and propagates posterior uncertainty.
- A decision-specific sensor-selection and uncertainty-to-action safety protocol.

### Dataset and benchmark

- A versioned repeated-session patient dataset or shareable derived benchmark with locked splits, sensor-failure scenarios and generic versus patient-conditioned baselines, subject to ethics and consent.

### Translational

- Preclinical or feasibility-level evidence about when a personalized model may change a rehabilitation/device decision and when it should abstain.

### Tool/system

- An OpenSim/CEINMS-compatible pipeline and optional MyoSuite/MyoAssist adapter with reproducible calibration, stress testing and model lineage.

These are expected outputs to be tested, not proven outcomes.

---

## 11. Risks, kill tests and alternatives

| Risk | Early warning | Kill test | Alternative with scientific value |
|---|---|---|---|
| Internal states are not identifiable | Broad/posterior correlations, unstable personalized parameters, good torque fit but inconsistent muscle state | Locked-session posterior fails to contract or parameters reverse across sessions without physiological explanation | Restrict claims to observable state/decision; publish identifiability boundary and required measurement set. |
| Multimodal burden is clinically impractical | Marginal information gain from extra sensors is small | A modality does not improve calibration or decision within a prespecified burden-adjusted margin | Remove it; use a deployable set and retain richer sensing only for periodic recalibration. |
| Fast and slow states compensate | Latent states are highly correlated and external anchors disagree | Two-state model does not improve future-session prediction over one-state baseline | Use hierarchical change-point/covariate model; quantify recalibration frequency instead of claiming physiological separation. |
| Slow adaptation cohort is delayed or underpowered | Recruitment/retention misses staged milestones | Prespecified feasibility threshold is missed before Year 2 midpoint | Use dense repeated measurements in a smaller cohort for mechanistic analysis; seek multi-site/clinical dataset for external validation. |
| Counterfactual prediction fails outside calibration | Good in-distribution fit but poor locked-condition coverage | Hybrid model does not outperform generic/data-driven baseline on the locked response | Reframe as failure-envelope discovery; identify where models cannot support intervention selection. |
| Policy exploits simulator | High reward with non-physiological forces/activation or poor recorded-data agreement | Constraint-violation or sim-to-real discrepancy exceeds predefined bound | Replace RL with constrained MPC or offline decision support; do not deploy policy. |
| Uncertainty does not support safe gating | High-confidence errors during dropout/shift | False-safe rate is not lower than simpler robust/fallback baseline | Use conformal/OOD wrapper or deterministic fault detection; keep model advisory. |
| Hardware/clinical study is unsafe or inaccessible | Safety review, ethics or device access is delayed | Offline gates or supervisory safety review fail | Stop at validated offline counterfactual and hardware-in-the-loop simulation; no patient deployment claim. |

---

## 12. Timeline and publication plan

The plan assumes a 36-month doctorate and uses overlapping data/software work. Hardware and longitudinal expansion remain gated.

| Period | Work package | Milestone / publication target |
|---|---|---|
| Months 1–3 | Re-search nearest work; finalize outcomes, ethics and data governance; reproduce generic/one-time baselines | Registered analysis plan; reproducible baseline repository |
| Months 4–8 | Existing stroke-data pilot; session-locked splits; sensor perturbation and uncertainty calibration | Pilot go/no-go for Aim 1; conference/workshop methods result if warranted |
| Months 7–14 | Repeated-session cohort launch; Aim 1 hybrid estimator and sensor-information analysis | Paper 1: observable state, identifiability and calibrated personalization |
| Months 12–22 | Complete main Aim 1 data; collect rehabilitation/fatigue longitudinal subset; develop two-timescale model | Aim 2 identifiability gate; dataset/benchmark release where permitted |
| Months 20–28 | Locked future-session validation and external anchors for Aim 2 | Paper 2: two-timescale longitudinal synchronization or its falsification |
| Months 24–31 | Held-out counterfactual, patient-conditioned simulation, uncertainty-gated decisions | Paper 3: safe predictive/assistive decision study |
| Months 29–33 | Optional supervised hardware feasibility after all gates | Feasibility report; no clinical-efficacy claim |
| Months 32–36 | External validation, integration, thesis and journal revisions | Thesis; integrated model/system paper if evidence supports it |

If a 30-month completion is mandatory, omit the patient hardware stage and treat Aim 3 as locked-condition prediction plus hardware-in-the-loop simulation. The full 36-month version is more defensible.

---

## 13. Fit to the researcher's background

The existing work on personalized sparse-to-dense IMU reconstruction in chronic stroke provides four useful foundations:

- patient-specific versus population/fine-tuned model comparison;
- session-level evaluation and chronic-stroke heterogeneity;
- sensor loss, placement rotation and reconstruction robustness;
- downstream gait-event validation rather than signal similarity alone.

These capabilities enter Aim 1 as a rapid pilot for missing-observation handling and safe failure detection. They do **not** define the thesis. The necessary doctoral expansion is from reconstructed movement signals to multimodal neural–mechanical state, explicit identifiability, posterior calibration, longitudinal physiology and decision validation. Existing biRNN/SHRED/TCN models serve as data-driven baselines, not as the proposed digital twin.

---

## 14. Fit to target research lines and laboratories

| Target research line | Strongest fit | Proposal adaptation | Needed complement |
|---|---|---|---|
| **Hayashibe line — neural engineering and rehabilitation robotics** | Aim 1 sensing/neural-state interface and Aim 3 robot feasibility; existing environment supports a fast start | Emphasize EMG-informed patient state, safe shared control and a realistic 30–36 month staged plan | Co-supervision in CEINMS/muscle–tendon identifiability and access to a longitudinal clinical cohort |
| **Durandau line — real-time neuromechanics and wearable robotics** | Aim 1 online personalization and Aim 3 uncertainty-gated exoskeleton control | Make EMG-driven real-time estimation and cross-session self-calibration the technical center | Longitudinal rehabilitation and tissue/multiscale collaborator for Aim 2 |
| **Sartori line — neural control, EMG-informed NMS and human–machine interfaces** | Aim 1 mechanistic neural–mechanical inference and Aim 3 physiological control | Strengthen motor-neuron/neural-drive constraints and multi-DOF real-time validation | Clinical longitudinal data and slower adaptation measurements |
| **Pizzolato–Lloyd line — CEINMS, personalization, multiscale modeling and treatment simulation** | Aim 2 longitudinal physiology and Aim 3 held-out counterfactual prediction | Emphasize identifiable patient parameters, tissue/load validation and treatment-response prediction | Real-time wearable robotics partner if a physical closed loop is required |
| **Yanan Sui / muscle-driven Embodied-AI line** | Aim 3 patient-conditioned policy, generalization and simulator-exploitation audit | Emphasize posterior-conditioned control priors and benchmark alignment | Strong NMS mechanistic, clinical and hardware co-supervision so the thesis does not collapse into generic simulation/RL |

The core proposal is most coherent with joint supervision spanning **real-time neuromechanics/robotics** and **patient-specific multiscale modeling**. In the current laboratory, a GP-Mech or similar exchange with a Durandau/Sartori/Pizzolato-aligned group would directly cover the largest methodological gap rather than merely adding prestige or a second dataset.

---

## 15. Nearest prior work anchoring the proposal

The proposal's novelty is bounded by the following closest precedents:

1. [Durandau, Farina & Sartori (2018)](https://doi.org/10.1109/TBME.2017.2704085): real-time EMG-driven multi-DOF NMS estimation.
2. [Durandau et al. (2019)](https://doi.org/10.1186/s12984-019-0559-z): patient neuromechanical control of wearable robots.
3. [Bueno & Montano (2017)](https://doi.org/10.1088/1741-2552/aa58f5): online sequential Bayesian NMS self-calibration.
4. [Zhang et al. (2023)](https://doi.org/10.3389/fnins.2023.1254088): NMS-informed uncertainty bounds in exoskeleton control.
5. [Rabbi et al. (2024)](https://doi.org/10.1007/s10237-024-01825-7): reduced EMG burden for NMS knee-contact-force estimation.
6. [Hambly et al. (2025)](https://doi.org/10.1109/ICORR66766.2025.11062981): rapid continuous NMS calibration.
7. [Pizzolato et al. (2020)](https://doi.org/10.3389/fbioe.2020.00878): personalized real-time multiscale Achilles strain estimation.
8. [MyoSuite](https://proceedings.mlr.press/v168/caggiano22a.html): muscle-driven control with fatigue/pathology perturbations.
9. [Hammond et al. (2025), NMSM Pipeline](https://doi.org/10.1186/s12984-025-01629-5): open patient-specific model personalization and treatment optimization.
10. [Luo et al. (2024)](https://doi.org/10.1038/s41586-024-07382-4): simulation-trained exoskeleton assistance transferred to healthy-user hardware.
11. [Ou et al. (2026)](https://doi.org/10.3390/healthcare14111523): pathology-informed assistance policies evaluated with stroke gait data.
12. [Uhlrich et al. (2025)](https://doi.org/10.1016/S2665-9913(25)00151-1): controlled clinical evidence for personalized gait retraining.

The exact residual claims and prohibited overstatements are recorded in [`NOVELTY_AND_NEAREST_WORK.md`](NOVELTY_AND_NEAREST_WORK.md).
