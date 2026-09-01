# Core Paper Critique Protocol

**Version:** first critical-reading pass, 2026-09-01  
**Scope:** the 49 `priority=core` records in the first-pass NMS literature map.

## Purpose

This stage asks what each paper actually contributes to a **human neuromusculoskeletal digital twin**, rather than whether it uses adjacent vocabulary. It follows the repository skill `nms-digital-twin-paper-critique` and its critique rubric/paper-card template.

Every card separates author claims from this project's assessment and contains:

1. Problem
2. Method
3. Data
4. Evaluation
5. Findings
6. Digital Twin Assessment
7. Limitations
8. Reproducibility
9. PhD Relevance

The card also provides a one-sentence contribution, primary paper type and evidence level.

## Primary type decision

| Type | Deciding question |
|---|---|
| `sensing` | Does the main novelty improve observation of neural, muscle, movement, interaction or context state? |
| `modeling` | Does it primarily build or test a neural/muscle/skeletal/tissue or embodied dynamics model? |
| `personalization` | Does it identify or adapt parameters/states for a particular subject or patient? |
| `validation` | Is its main contribution an independent comparison, benchmark, clinical/functional evaluation or audit of claims? |
| `framework/review` | Does it synthesize or define the field without implementing the claimed system? |
| `near_true_twin` | Are person binding, state update, prediction and actionable feedback jointly implemented and empirically evaluated? |

A paper can have secondary types, but it receives one primary label in the machine-readable assessment. Sensor novelty is not twin novelty; IMU is not privileged over EMG, ultrasound, video, force/pressure or imaging.

## Digital-twin decision rule

The maturity scale is inherited from [`../01_literature_mapping/TAXONOMY.md`](../01_literature_mapping/TAXONOMY.md):

- `L0`: generic simulator; no individual binding.
- `L1`: offline subject-specific digital model.
- `L2`: episodic/continuous one-way digital shadow.
- `L3`: validated prediction/counterfactual for unseen conditions.
- `L4`: model/state/prediction changes feedback, stimulation, robot assistance or therapy.
- `L5`: longitudinal, multi-timescale, uncertainty-aware adaptive twin.

The following do **not** raise a paper above `L0–L1` by themselves: anatomical visual realism, muscle-driven simulation, an AI policy, a dashboard, the words “self model” or “digital twin,” retrospective fitting, or a generic human–robot loop.

To count as **near a true twin**, the implemented system must show most of:

1. a named/identified person's relevant NMS state or parameters;
2. repeated or online physical-to-digital updates;
3. a mechanistic or meaningfully constrained neural–muscle–skeletal link;
4. prediction/state estimation validated beyond the calibration signal;
5. an output that changes intervention, assistance or feedback;
6. explicit treatment of adaptation, safety or uncertainty.

No paper in this first core set satisfies all six or reaches `L5`.

## Evidence levels

| Evidence code | Meaning | Permitted claims |
|---|---|---|
| `full_text_checked` | Main text plus relevant methods/results/limitations were inspected. | Specific method, sample and result critique, within the paper's evidence. |
| `methods_results_checked` | Reliable methods/results records, author manuscript, repository or indexed full sections were inspected, but not every publisher page/appendix. | Specific checked claims; inaccessible details are not inferred. |
| `methods_results_checked_via_full_text_secondary_copy` | A complete or near-complete legitimate secondary-hosted copy was used. | Same caution as above, with provenance noted. |
| `abstract_and_methods_summary_checked` | Abstract plus reliable method/result summaries were available, but full text remained inaccessible. | Only directly supported claims; missing sample or limitation details are explicitly left unresolved. |

Where exact details could not be verified, the card says so. A technical accuracy result is never promoted to clinical value without a functional or clinical evaluation.

## Limitations and reproducibility

Limitations combine author-reported issues and clearly marked critical inference. Each card checks, where relevant: sample size and population; calibration/test leakage; internal-state ground truth; out-of-distribution conditions; longitudinal/real-world use; identifiability and uncertainty; sim-to-real; and intervention safety/clinical outcomes.

Reproducibility considers availability of code, data, model, environment, weights, hardware details and executable protocols—not only whether equations are described.

## Scope limits

- This is a structured critical-reading pass over the 49 core seed papers, not a risk-of-bias-complete systematic review.
- Some older or subscription-controlled papers were assessed from checked methods/results records or legitimate author copies; evidence is labeled rather than silently completed from abstracts.
- Values should be independently re-extracted before use in a meta-analysis, regulatory submission or clinical decision.
