# Midterm defense — 27 October 2026

**Generalizable and Personalized Motion Reconstruction in Stroke Patients Using Sparse IMUs**

**Yincheng Wang** · Supervisor: **Mitsuhiro Hayashibe** · **Tohoku University · Robotics**

The actual English visual presentation is now complete. **14 main slides, 14:30 speaking + 0:30 buffer; 4 backup slides outside the timed talk.** This replaces the earlier 13-page proposed outline; the additional space supports background and related work. The talk duration is a rehearsal target and still needs an aloud rehearsal.

- [Open the GitHub visual slide deck](MIDTERM_DEFENSE_20261027_EN.md).
- [Continuous English speaking script](MIDTERM_DEFENSE_20261027_SPEAKER_NOTES_EN.md).
- [Backup slides, questions and primary references](MIDTERM_DEFENSE_20261027_APPENDIX_EN.md).
- [Numerical evidence and source fingerprints](MIDTERM_DEFENSE_20261027_EVIDENCE.json).
- [Three-level research and publication goals](MIDTERM_THEME_AND_PUBLICATION_ROADMAP_20261027_ZH.md).

## Talk structure

| Slide | Topic | Time | Cumulative |
|---|---|---:|---:|
| 01 | Generalizable and Personalized Motion Reconstruction in Stroke Patients Using Sparse IMUs | 0:20 | 0:20 |
| 02 | Stroke gait requires both shared models and individual attention | 1:05 | 1:25 |
| 03 | Sparse wearable sensing trades measurement coverage for convenience | 0:55 | 2:20 |
| 04 | Sparse reconstruction and personalization already have strong precedents | 1:05 | 3:25 |
| 05 | Separate population transfer from the value of individual labels | 1:00 | 4:25 |
| 06 | Reliable pairing is a prerequisite for a meaningful learning result | 1:15 | 5:40 |
| 07 | Keep the network fixed and make the evaluation roles explicit | 1:15 | 6:55 |
| 08 | Verified inputs recover patient-specific motion beyond a constant baseline | 0:45 | 7:40 |
| 09 | Individual supervision matters; pretraining adds a modest further benefit | 1:20 | 9:00 |
| 10 | Personalization benefits depend on how much target reference is available | 1:15 | 10:15 |
| 11 | Public healthy cohorts provide technical replication across walking speeds | 1:15 | 11:30 |
| 12 | Direction augmentation reduces sensitivity, with a clean-error trade-off | 1:00 | 12:30 |
| 13 | The current contribution is an auditable study of personalization and its limits | 1:15 | 13:45 |
| 14 | From a complete exploratory study to stronger publication evidence | 0:45 | 14:30 |

## Core argument

Measured two-shank IMUs and reliable optical pairing support patient-specific reconstruction. Patient-excluded source models alone remain weak; limited target reference improves reconstruction, and pretrained weights add a modest benefit over a matched target-trained random-weight reference. Public healthy cohorts provide technical replication and reveal cross-speed and synthetic-orientation trade-offs.

Stroke is the core clinical development population; healthy data do not replace independent stroke validation. Dataset-specific engineering labels, budgets, scored supports and sample sizes remain separate. All results are existing accepted experiments; proposed optimization is shown only as future work. Architecture and experimental contracts remain frozen.

## Preserved history

- [Previous 13-page outline](MASTER_MIDTERM_OUTLINE_before_English_visual_deck_20261025_ZH.md).
- [Earlier November-date outline and historical updates](MASTER_MIDTERM_OUTLINE_before_20261025_ZH.md).
