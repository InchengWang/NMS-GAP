# Backup slides and references

These pages are outside the 15-minute talk. [Return to the presentation](MIDTERM_DEFENSE_20261027_EN.md).

## A1 · Coordinates and label definitions

![Backup A1: Coordinates and label definitions](assets/defense_20261027/appendix_A1_coordinates.svg)

## A2 · Architecture, virtual-data and GEN5 results

![Backup A2: Architecture, virtual-data and GEN5 results](assets/defense_20261027/appendix_A2_ablations.svg)

## A3 · Cohorts and reference costs

![Backup A3: Cohorts and reference costs](assets/defense_20261027/appendix_A3_domains_costs.svg)

## A4 · Likely questions

![Backup A4: Likely questions](assets/defense_20261027/appendix_A4_questions.svg)

## Primary research references

- **R1.** Sánchez N, et al. Multi-Site Identification and Generalization of Clusters of Walking Behaviors in Individuals With Chronic Stroke and Neurotypical Controls. Neurorehabilitation and Neural Repair. 2023;37(11–12):810–822. DOI: 10.1177/15459683231212864. [Primary source](https://pubmed.ncbi.nlm.nih.gov/37975184/).
- **R2.** Kettlety SA, et al. Speed-dependent biomechanical changes vary across individual gait metrics post-stroke relative to neurotypical adults. Journal of NeuroEngineering and Rehabilitation. 2023;20:14. DOI: 10.1186/s12984-023-01139-2. [Primary source](https://link.springer.com/article/10.1186/s12984-023-01139-2).
- **R3.** Guo Y, et al. Physics-Informed Learning Framework for Lower Limb Kinematic Prediction With Sparse Sensors and Its Application in Chronic Stroke. IEEE TNSRE. 2025;33:2475–2486. DOI: 10.1109/TNSRE.2025.3581352. [Primary source](https://ieeexplore.ieee.org/document/11044411/).
- **R4.** Hur B, Baek S, Kang I, Kim D. Learning based lower limb joint kinematic estimation using open source IMU data. Scientific Reports. 2025;15:5287. DOI: 10.1038/s41598-025-89716-4. [Primary source](https://www.nature.com/articles/s41598-025-89716-4).

These studies motivate the questions; their participants and best errors are not added to our evaluation. No paper figures or full texts are reproduced. Ordinary fine-tuning and two-IMU prediction are prior work, not new algorithm claims.

## Project evidence

- **E1.** [Accepted stroke release and patient-specific baseline](SII2027_NATIVE_BASELINE_20261021_ZH.md).
- **E2.** [Ordered trial matching and marker recall](SII2027_MARKER_RECALL_20261021_ZH.md).
- **E3.** [Stroke GEN1 / GEN2 transfer and budget results](SII2027_GENERALIZATION_RESULTS_20261022_ZH.md).
- **E4.** [Frozen architecture and augmentation results](SII2027_ARCH_AUG_RESULTS_20261022_ZH.md).
- **E5.** [Accepted WMCG public-data experiment](SII2027_OPEN_EXTERNAL_VALIDATION_20261023_ZH.md).
- **E6.** [Accepted Dorschky optical two-knee experiment](SII2027_DORSCHKY_EXTERNAL_20261024_ZH.md).
- **E7.** [Three-level publication and research roadmap](MIDTERM_THEME_AND_PUBLICATION_ROADMAP_20261027_ZH.md).

The source experiment reports retain their original Chinese filenames and historical status. The presentation and spoken script are entirely English. Current stroke outputs are legacy pelvis-plane engineering angles; Dorschky outputs are signed heading-sagittal optical proxies. Raw IMU/marker samples, per-frame predictions, weights, and full papers are not included in this presentation package.
