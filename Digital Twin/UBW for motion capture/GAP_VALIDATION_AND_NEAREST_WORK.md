# Gap Validation and Nearest Prior Work

**Companion to [PHD_PROPOSAL.md](PHD_PROPOSAL.md). Evidence check: 2026-10-04.**

This record separates inherited gap validation, established prior capabilities and the smaller UWB-specific hypotheses that the proposed PhD would test. It does not upgrade an untested mechanism into a confirmed research result. The main plan uses UWB as the principal motion tool; IMU supplementation is optional and explicitly budgeted.

## 1. Provenance and validation standard

The source dossier is [Digital Twin gap validation](../03_gap_validation/GAP_VALIDATION_REPORT.md), its [gap matrix](../03_gap_validation/data/gap_validation_matrix.csv), the repository's [earlier PhD plan](../04_phd_proposal/PHD_PROPOSAL.md), and the [2026-10-01 literature update](../../01_literature_mapping/updates/2026-10-01.md). The earlier gap-validation cutoff was 2026-09-01; this companion adds a targeted primary-source counter-evidence check through 2026-10-04.

The plan follows the [nms-digital-twin-phd-proposal skill](https://github.com/InchengWang/nms-digital-twin-skills/blob/main/nms-digital-twin-phd-proposal/SKILL.md) and its proposal/experiment references. Every Aim has a construct, data, model, strong baseline, independently evaluable endpoint, feasibility gate and failure value.

**Meaning of “validated gap.”** A literature-assessed residual with an explicit verdict, not a proof of experimental novelty. The relevant inherited verdicts are partially-addressed. For this UWB proposal, absence of a paper containing every desired component is insufficient. The test must isolate a scientific or decision consequence beyond assembling those components.

### Inherited directions and the decision for this proposal

| ID / direction, summarized | Dossier verdict | Treatment in this proposal |
|---|---|---|
| G01: identifiability and posterior validity | Partially-addressed | Retain endpoint-specific geometric/parameter ambiguity and externally checked predictions. |
| G02: multiple time scales in fatigue/rehabilitation | Confirmed-open in the older broad dossier | Do not inherit this verdict as a UWB novelty claim. First distinguish measurement/calibration drift from human change. |
| G03: patient-specific embodied adaptation | Partially-addressed | Context for bounded interaction; not a commitment to a new general RL agent. |
| G04: locked unseen-condition response | Partially-addressed | Retain a held-out load/session and pre-action response prediction. |
| G05: uncertainty, failure and control | Partially-addressed | Retain independently evaluated action consequences and calibrated/simple fallback controls. |
| G06: general benefit of personalized intervention | Not-a-gap | Reject “personalization has no physical/clinical precedent.” |
| G07: minimum actionable multimodal observability | Partially-addressed | Primary entry point, narrowed to a task and observation budget, not a universal minimum sensor count. |
| G08: benchmarks | Secondary direction | Deliver an evaluation track only if it supports the scientific tests. |
| G09: morphology/generalization | Audit axis | Report relevant body/configuration variation without claiming powered subgroup effects. |
| G10: governance | Outside the selected core | Consent and provenance are study requirements, not the thesis novelty. |

The embodied-AI dossier's partially-addressed uncertainty-to-action direction is compatible with Aim 3. Its IMU-substitution direction does not justify making an IMU reconstruction project the core thesis.

## 2. UWB-specific residuals selected for testing

| Residual / Aim | Closest counter-evidence | What remains to test, without a priority claim | Verdict and falsification |
|---|---|---|---|
| U1 / Aim 1: task-specific observability and deployment failure | Joint ranging [R01], uncertainty fusion [R04], geometric diffusion guidance [R06], distance-only whole-body inference [R07], upper-limb fusion [R20]. | Which anatomical/physical-frame variables are constrained by actual radio observations under reattachment/NLOS/configuration changes, and whether estimated ambiguity predicts reference error. | **Partially-addressed.** A controlled rig may show that the chosen variable is not recoverable, or ordinary filtering/calibration may suffice. Restrict state/configuration accordingly. |
| U2 / Aim 2: diagnosed spatial uncertainty in a person-bound NMS endpoint | Sensing-to-upper-limb mechanics [R11], real-time EMG modeling [R12], torque uncertainty [R13], personalization tools [R14], planar post-stroke models [R21]. | Whether UWB uncertainty/attachment ambiguity materially changes locked net-moment or load-response prediction, beyond nuisance calibration and a calibrated black box. | **Partially-addressed.** No practical predictive effect, parameter compensation or calibration-only equivalence rules out the proposed stronger physiological claim. |
| U3 / Aim 3: incremental physical action value of the human-state belief | Range-only robot commands [R08], uncertainty-informed exoskeleton control [R13], real-time model control [R12], personalized compliance [R18]. | Whether the same bounded controller gains a prespecified risk/performance benefit from the posterior NMS information beyond encoder/force, motion-only, point NMS and ordinary fallback. | **Partially-addressed.** Matching performance with a simpler state/fallback means the complex representation is unnecessary for that task. HIL results alone cannot establish patient efficacy. |

These residuals are coupled but independently falsifiable. Aim 1 must identify a usable state before Aim 2 makes a mechanics claim. Aim 3 must demonstrate physical decision value; improved pose or moment accuracy alone is not enough.

## 3. Novelty claims that counter-evidence excludes

| Rejected broad claim | Nearest prior work | Allowed formulation |
|---|---|---|
| “First UWB joint-angle measurement.” | Qi et al. [R01]. | Evaluate anatomical/task validity under defined observation changes. |
| “First sparse IMU/UWB reconstruction or upper-limb fusion.” | UIP/GIP [R03], [R05]; Shi et al. [R20]. | Use these as compatible optional-fusion baselines. |
| “First uncertainty-aware UWB motion estimator.” | UMotion [R04]. | Test calibrated endpoint uncertainty and the resulting decision errors. |
| “First geometric constraints or sensor-layout recovery.” | Ultra Diffusion Poser [R06]. | Test what the known geometry genuinely identifies. |
| “First full-body motion capture from distances without IMU.” | WiP [R07]. | Benchmark a UWB-centered deployment without a priority claim. |
| “First adaptive reference anchor or global/local UWB design.” | Yang et al. [R09]; Müller et al. [R10]. | Compare established network designs at a matched radio budget. |
| “First UWB human–robot interaction.” | Salimi et al. [R08]. | Test measured physical assistance consequences beyond posture-to-command mapping. |
| “First real-time motion-to-NMS pipeline.” | Ceglia et al. [R11]; CEINMS-RT [R12]. | Isolate the effect of measurement ambiguity in an externally checked endpoint. |
| “First patient-specific or planar post-stroke arm model.” | NMSM Pipeline [R14]; Asghari et al. [R21]. | Test locked prediction and nuisance-versus-human-state identifiability. |
| “First uncertain neuromechanical state used for assistance.” | NMS-informed Bayesian control [R13]. | Compare calibrated decision risk at matched task utility against strong fallbacks. |
| “No muscle-driven embodied simulation or model-to-device precedent.” | MyoSuite [R15], Luo et al. [R16], personalized FES [R17]. | Use established components; qualify physical validation and reproducibility limits. |
| “UWB ranges uniquely reveal neural drive or individual muscle force.” | The proposal's measurement/model analysis, with relevant models [R11], [R12], [R21]. | Neural input requires an additional observation such as EMG; individual forces remain model-dependent without an independent reference. |
| “A unified UWB+NMS+robot system is automatically novel.” | All component families above. | Prove an observable mechanism, independent prediction or incremental action benefit. |

## 4. Nearest-work comparison by Aim

### Aim 1: measurement-constrained geometry versus inferred motion

The important comparators span UWB-only hinge estimation, pure-distance full-body reconstruction, sparse inertial/ranging reconstruction, explicit geometry and uncertainty-aware estimation [R01], [R03], [R04], [R06], [R07]. The new test uses anatomical and physical-frame references across deployment changes. A learned prior's plausible pose is not evidence of range-only observability.

Use classical localization/IK and a calibrated uncertainty wrapper as mandatory simple controls. Run named full-body methods only with compatible placements/inputs. Shi et al. are a direct upper-limb hybrid comparator in an optional IMU track [R20]; fusion results must not be relabeled UWB-only. Adaptive anchor and dense-network work narrow any radio-design novelty [R09], [R10].

### Aim 2: an independent mechanics endpoint rather than a latent-force score

RGBD upper-limb analysis and an existing post-stroke planar NMS arm model establish that sensing-driven and reduced patient models already exist [R11], [R21]. CEINMS-RT and NMSM supply modeling/control and personalization precedents [R12], [R14]. NMS uncertainty is also an established concept [R13].

The proposed test holds EMG and external-force information constant while varying UWB point/posterior input and update policy. A held-out net moment is externally evaluable under measured forces and explicit inverse-dynamics assumptions. Estimated individual muscle forces are not used as their own ground truth. A later load/session is locked before refitting; calibration shifts are not called recovery.

### Aim 3: physical response and action-risk tradeoffs

Range-only HRI already produces robot commands [R08]. Subject-specific upper-limb compliance and uncertainty-informed assistance are directly relevant controls [R18], [R13]. Physical neuromechanical control and model transfer have precedents [R12], [R16], [R17].

The incremental claim depends on an identical controller using different human-state information, evaluated jointly for independently defined action-constraint violations and task performance. Ordinary encoder/force control and deterministic/calibrated fallbacks may win. Fault replay/HIL, supervised human interaction and durable patient outcomes are different evidence levels.

## 5. Counter-evidence search record and access limitations

The check targeted the following topic families and their directly linked predecessor/citation records:

- UWB wearable joint angles; upper-limb IMU/UWB fusion; UI-MoCap.
- Sparse whole-body reconstruction: UIP, UMotion, GIP, Ultra Diffusion Poser; pairwise-distance WiP/Mocap Anywhere.
- Range-only posture recognition and robot interaction.
- TDoA reference selection, body shadowing and dense wearable network scalability.
- Upper-limb musculoskeletal sensing; EMG-driven real-time control; uncertainty-aware NMS assistance.
- Reduced post-stroke arm models; OpenSim personalization/prediction; muscle-driven simulation and physical model transfer.
- SUSTech faculty/group fit and the repository's newer literature-verification record.

**Inclusion standard.** Prior work is retained if it closes a proposed component claim or tests a closely related construct; full-text access is not required to recognize a clearly stated prior capability. However, absence of a feature from an abstract is not proof that the full paper lacks it. Specific negative assertions are limited to inspected methods, or expressed as “not established by the accessed evidence.”

**Sources.** Official publisher/proceedings records, author manuscripts/projects, PubMed/PMC bibliographic or author text, and university publication records. Search-index excerpts are identified below when direct full text was unavailable. Secondary reporting and DOI placeholders are not used as technical evidence. This is not an exhaustive systematic review, and no search-recall estimate is claimed.

### Status cautions carried into the plan

- **WiP [R07]:** the inspected version is arXiv v1. Author/institutional pages report a TOG publication/acceptance in 2026; the publisher version and DOI were not independently verified. A manuscript's placeholder DOI is omitted.
- **Luo et al. [R16]:** the current publisher record includes an Editor's Note dated 2026-07-27 concerning supporting data/code availability. This is not treated as a retraction. Reported benefit magnitudes do not set this proposal's power assumptions or success thresholds.
- **CEINMS-RT [R12]:** distinguish 2025 early-online and 2026 issue publication. Availability of a framework does not guarantee that the planned upper-limb instance is already validated.
- **Personalized FES [R17]:** accessed as a peer-reviewed accepted article; physical validation scope is limited, not durable recovery evidence. FES is a boundary reference rather than a new required thesis subsystem.
- **UI-MoCap [R02]:** IMU transport rate is not UWB localization rate. Actual ranging/timing/API availability is a pilot requirement.
- **September 2026 network paper [R10]:** use the primary publication month; an October video/index date is not the journal's original publication date.

**Update rule.** Re-run the nearest-work check before each submission. A closer paper can move the contribution toward external validation, replication or a different remaining limitation. It cannot be ignored to preserve the original novelty wording.

## 6. Reusable code/data entry points

| Prior work | Author-maintained resource | Intended use / constraint |
|---|---|---|
| UIP [R03] | [UltraInertialPoser](https://github.com/eth-siplab/UltraInertialPoser) | Sparse-fusion comparator/public data; inspect placement and license before use. |
| UMotion [R04] | [umotion](https://github.com/kk9six/umotion) | Uncertainty-aware comparator; verify compatible input and causal runtime. |
| GIP [R05] | [GroupInertialPoser](https://github.com/eth-siplab/GroupInertialPoser) | Multi-person comparator only when the protocol includes that task. |
| Ultra Diffusion Poser [R06] | [UltraDiffusionPoser](https://github.com/eth-siplab/UltraDiffusionPoser) | Geometric reconstruction comparator with explicit latency/compute accounting. |
| WiP [R07] | [Author project](https://ofir1080.github.io/wild-poser/) | Track accessed version and current code/data availability; do not assume a complete reusable radio stack. |

These links were located, not executed or licensed for the proposed new experiment. Baseline reproduction is a first-90-days milestone, not completed validation.

## 7. Full references and evidence depth

### R01

Qi, Y.; Soh, C. B.; Gunawan, E.; Low, K.-S.; Maskooki, A. **A Novel Approach to Joint Flexion/Extension Angles Measurement Based on Wearable UWB Radios.** IEEE JBHI 18(1):300–308; 2014. DOI: [10.1109/JBHI.2013.2253487](https://doi.org/10.1109/JBHI.2013.2253487). [Primary/author source](https://pubmed.ncbi.nlm.nih.gov/24403428/).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Indexed author abstract and bibliographic metadata.

### R02

Zhong, W.; Zhang, L.; Sun, Z.; Dong, M.; Zhang, M. **UI-MoCap: An Integrated UWB-IMU Circuit Enables 3D Positioning and Enhances IMU Data Transmission.** IEEE TNSRE 32:1034–1044; 2024. DOI: [10.1109/TNSRE.2024.3369647](https://doi.org/10.1109/TNSRE.2024.3369647). [Primary/author source](https://pubmed.ncbi.nlm.nih.gov/38408007/).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Indexed author abstract and bibliographic metadata; publisher record located.

### R03

Armani, R.; Qian, C.; Jiang, J.; Holz, C. **Ultra Inertial Poser: Scalable Motion Capture and Tracking from Sparse Inertial Sensors and Ultra-Wideband Ranging.** ACM SIGGRAPH 2024 Conference Papers, Article 51; 2024. DOI: [10.1145/3641519.3657465](https://doi.org/10.1145/3641519.3657465). [Primary/author source](https://siplab.org/projects/UltraInertialPoser).

- Publication status: Peer-reviewed conference.
- Evidence inspected: Author project, method and evaluation descriptions; code/data links.

### R04

Liu, H.; Ota, H.; Wei, X.; Hirao, Y.; Perusquía-Hernández, M.; Uchiyama, H.; Kiyokawa, K. **UMotion: Uncertainty-driven Human Motion Estimation from Inertial and Ultra-wideband Units.** CVPR 2025:7085–7094; 2025. [Primary/author source](https://arxiv.org/html/2505.09393v1).

- Publication status: Peer-reviewed conference; author manuscript inspected.
- Evidence inspected: Full-text methods, experiments and supplementary sections; official CVF conference metadata verified.

### R05

Xue, Y.; Jiang, J.; Armani, R.; Hollidt, D.; Liao, Y.-C.; Holz, C. **Group Inertial Poser: Multi-Person Pose and Global Translation from Sparse Inertial Sensors and Ultra-Wideband Ranging.** ICCV 2025:24910–24921; 2025. [Primary/author source](https://siplab.org/projects/GroupInertialPoser).

- Publication status: Peer-reviewed conference.
- Evidence inspected: Author project, method and evaluation descriptions; code/data links.

### R06

Hollidt, D.; Bendinelli, T.; Holz, C. **Ultra Diffusion Poser: Diffusion-Based Human Motion Tracking from Sparse Inertial Sensors and Ranging-based Between-sensor Distances.** CVPR 2026:7036–7046; 2026. [Primary/author source](https://siplab.org/projects/UltraDiffusionPoser).

- Publication status: Peer-reviewed conference.
- Evidence inspected: Author project and official CVF metadata; geometry and diffusion-guidance description.

### R07

Abramovich, O.; Shamir, A.; Aristidou, A. **Mocap Anywhere: Towards Pairwise-Distance based Motion Capture in the Wild (for the Wild).** arXiv:2601.19519v1; authors report TOG acceptance/publication in 2026; 2026. [Primary/author source](https://arxiv.org/html/2601.19519v1).

- Publication status: Accessed version is a preprint; publisher version/DOI not independently verified.
- Evidence inspected: Full-text methods, raw-UWB evaluation, limitations; author project and institutional publication listing.

### R08

Salimi, S.; Salimpour, S.; Peña Queralta, J.; Bessa, W. M.; Westerlund, T. **Benchmarking ML Approaches to UWB-Based Range-Only Posture Recognition for Human–Robot Interaction.** IEEE Sensors Journal; 2024 online / 2025 institutional issue listings. DOI: [10.1109/JSEN.2024.3493256](https://doi.org/10.1109/JSEN.2024.3493256). [Primary/author source](https://tiers.utu.fi/publications/).

- Publication status: Peer-reviewed journal; online and issue years distinguished.
- Evidence inspected: Author/institutional journal record and abstract; arXiv:2408.15717 abstract.

### R09

Yang, Y.; Zhang, L.; Xi, Z.; Sun, Y.; Chen, Q.; Zhang, M. **Dynamic Reference Anchor Selection for Enhanced TDoA-Based UWB Localization in Complex Scenarios.** IEEE Transactions on Wireless Communications; 2026. DOI: [10.1109/TWC.2026.3667604](https://doi.org/10.1109/TWC.2026.3667604). [Primary/author source](https://ieeexplore.ieee.org/document/11420874).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Indexed primary publisher title, abstract excerpt and DOI; complete text unavailable.

### R10

Müller, D.; Sonnberger, M.; Schmidt, J. F. **Two-Layer Ultra-Wideband Localization: Scalability for Dense Wearable Motion Capture.** Sensors 26(18):5738; 2026 September. DOI: [10.3390/s26185738](https://doi.org/10.3390/s26185738). [Primary/author source](https://www.mdpi.com/1424-8220/26/18/5738).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Indexed primary abstract and metadata; primary version notes; complete text blocked.

### R11

Ceglia, A.; Facon, K.; Begon, M.; Seoud, L. **Real-time, accurate, and open source upper-limb musculoskeletal analysis using a single RGBD camera — An exploratory hand-cycling study.** Computers in Biology and Medicine 184:109434; 2024 online / 2025 issue. DOI: [10.1016/j.compbiomed.2024.109434](https://doi.org/10.1016/j.compbiomed.2024.109434). [Primary/author source](https://pubmed.ncbi.nlm.nih.gov/39579665/).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Indexed author abstract and primary publisher metadata.

### R12

Sartori, M.; Refai, M. I.; Gaudio, L. A.; Cop, C. P.; Simonetti, D.; Damonte, F.; Hambly, M.; Lloyd, D. G.; Pizzolato, C.; Durandau, G. **CEINMS-RT: An Open-Source Framework for the Continuous Neuro-Mechanical Model-Based Control of Wearable Robots.** IEEE TMRB 8(1):405–417; 2025 online / 2026 issue. DOI: [10.1109/TMRB.2025.3643986](https://doi.org/10.1109/TMRB.2025.3643986). [Primary/author source](https://research.utwente.nl/en/publications/ceinms-rt-an-open-source-framework-for-the-continuous-neuro-mecha-2/).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Institutional journal record and author abstract; publication dates and final-version link.

### R13

Zhang, L.; Zhang, X.; Zhu, X.; Wang, R.; Gutierrez-Farewik, E. M. **Neuromusculoskeletal model-informed machine learning-based control of a knee exoskeleton with uncertainties quantification.** Frontiers in Neuroscience 17:1254088; 2023. DOI: [10.3389/fnins.2023.1254088](https://doi.org/10.3389/fnins.2023.1254088). [Primary/author source](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1254088/full).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Publisher full-text page; abstract and control framework.

### R14

Hammond, C. V. et al. **The Neuromusculoskeletal Modeling Pipeline: MATLAB-based model personalization and treatment optimization functionality for OpenSim.** JNER 22:112; 2025. DOI: [10.1186/s12984-025-01629-5](https://doi.org/10.1186/s12984-025-01629-5). [Primary/author source](https://link.springer.com/article/10.1186/s12984-025-01629-5).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Publisher full text; model-personalization tools and illustrative treatment example.

### R15

Caggiano, V.; Wang, H.; Durandau, G.; Sartori, M.; Kumar, V. **MyoSuite: A Contact-rich Simulation Suite for Musculoskeletal Motor Control.** L4DC, PMLR 168:492–507; 2022. [Primary/author source](https://proceedings.mlr.press/v168/caggiano22a.html).

- Publication status: Peer-reviewed conference.
- Evidence inspected: Official proceedings paper page and abstract.

### R16

Luo, S. et al. **Experiment-free exoskeleton assistance via learning in simulation.** Nature 630:353–359; 2024; Editor’s Note 2026-07-27. DOI: [10.1038/s41586-024-07382-4](https://doi.org/10.1038/s41586-024-07382-4). [Primary/author source](https://www.nature.com/articles/s41586-024-07382-4).

- Publication status: Peer-reviewed journal with Editor’s Note concerning data/code availability.
- Evidence inspected: Indexed primary publisher abstract, metadata and current Editor’s Note.

### R17

Coelho-Magalhães, T.; Azevedo-Coste, C.; Resende-Martins, H.; Bailly, F. **Personalized FES-cycling patterns via optimal control: from musculoskeletal simulation to experimental validation.** Journal of NeuroEngineering and Rehabilitation; 2026-09-04. DOI: [10.1186/s12984-026-02136-x](https://doi.org/10.1186/s12984-026-02136-x). [Primary/author source](https://link.springer.com/article/10.1186/s12984-026-02136-x).

- Publication status: Peer-reviewed accepted article; final version pending at access.
- Evidence inspected: Publisher accepted-article page, author abstract and experimental scope.

### R18

Miao, Q.; Peng, Y.; Liu, L.; McDaid, A.; Zhang, M. **Subject-specific compliance control of an upper-limb bilateral robotic system.** Robotics and Autonomous Systems 126:103478; 2020. DOI: [10.1016/j.robot.2020.103478](https://doi.org/10.1016/j.robot.2020.103478). [Primary/author source](https://www.sciencedirect.com/science/article/abs/pii/S092188901930898X).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Indexed primary publisher abstract and metadata.

### R19

Southern University of Science and Technology **ZHANG Mingming — Faculty profile.** Official SUSTech faculty page; Accessed 2026-10-04. [Primary/author source](https://www.sustech.edu.cn/en/faculties/zhangmingming.html).

- Publication status: Institutional resource; no device-access or recruitment guarantee.
- Evidence inspected: Official profile; research themes and UWB/IMU platform.

### R20

Shi, Y.; Zhang, Y.; Li, Z.; Yuan, S.; Zhu, S. **IMU/UWB Fusion Method Using a Complementary Filter and a Kalman Filter for Hybrid Upper Limb Motion Estimation.** Sensors 23(15):6700; 2023. DOI: [10.3390/s23156700](https://doi.org/10.3390/s23156700). [Primary/author source](https://pmc.ncbi.nlm.nih.gov/articles/PMC10422251/).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Publisher-author full text archived in PMC; methods and experiment design.

### R21

Asghari, M.; Behzadipour, S.; Taghizadeh, G. **A planar neuro-musculoskeletal arm model in post-stroke patients.** Biological Cybernetics 112(5):483–494; 2018. DOI: [10.1007/s00422-018-0773-y](https://doi.org/10.1007/s00422-018-0773-y). [Primary/author source](https://pubmed.ncbi.nlm.nih.gov/30056607/).

- Publication status: Peer-reviewed journal.
- Evidence inspected: Indexed author abstract and bibliographic metadata; full text not inspected.

## 8. Gate from gap to claim

Before promoting an expected contribution into a manuscript claim, record: the exact nearest comparator/version; equalized inputs and budgets; an independently measured target; a participant/session-separated test; the predeclared practical threshold; the uncertainty/effect interval; and the result of the Aim's falsification test. If any of these are missing, retain hypothesis or feasibility wording.

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

