# Human Neuromusculoskeletal Embodied-AI Critique Protocol

**Version:** first Embodied-AI-centered re-assessment, 2026-09-01  
**Scope:** all 49 records marked `priority=core` in [`../../01_literature_mapping/data/literature_matrix.csv`](../../01_literature_mapping/data/literature_matrix.csv).

## Purpose

This pass asks what each paper actually contributes to **human neuromusculoskeletal (NMS) Embodied AI**. It follows the repository skill `nms-digital-twin-paper-critique`, but replaces the original digital-twin-centered decision with an embodied-intelligence test:

> Does the work connect a human-relevant neural–muscle–skeletal body, sensing or state estimation, action selection, and environment or device interaction—and how strongly is that loop grounded in a specific human or rehabilitation setting?

The checked Problem, Method, Data, Evaluation, Findings, Limitations and Reproducibility evidence is inherited from the earlier full-text/methods-results critique. The interpretation, primary type and PhD relevance are re-coded here.

## Required paper-card fields

Every card contains:

1. Problem
2. Method
3. Data
4. Evaluation
5. Findings
6. Embodied AI Assessment
7. Limitations
8. Reproducibility
9. PhD Relevance

The Embodied AI Assessment explicitly examines human NMS modeling, embodied intelligence, sensorimotor control, human–robot interaction, assistive control, rehabilitation relevance and subject-specific validation.

## Primary type rule

Each paper receives one primary label. Secondary tags preserve overlap.

| Primary type | Deciding criterion |
|---|---|
| `sensing` | Its main contribution is observing neural, muscular, movement or interaction state; the action loop is absent or secondary. |
| `modeling` | Its main contribution is a neural, muscle, skeletal, tissue or patient model; control or interaction is absent/secondary. |
| `control` | Its main contribution is action selection, online adaptation or optimization, with embodiment demonstrated at least virtually or physically. |
| `robotics` | Its main contribution is an evaluated physical human–robot/prosthesis/exoskeleton loop. |
| `rehabilitation` | Its main contribution is a rehabilitation state, intervention or outcome rather than a new sensing/model/control method. |
| `embodied_ai` | It directly studies an agent acting through a neural/musculoskeletal body in an environment, or provides a central benchmark/control framework for that problem. |
| `embodied_ai_related_weak` | It is a review, framework or adjacent paper whose empirical contribution does not implement a body–perception–action–environment loop. |

Being labeled `modeling`, `sensing`, `control` or `robotics` is not a quality judgment. It identifies what the paper actually advances.

## Embodiment evidence scale

| Level | Operational definition |
|---|---|
| `E0` | No implemented embodied agent; review, framework or conceptual contribution only. |
| `E1` | Body/sensing/model substrate exists, but no evaluated action–environment loop. |
| `E2` | Closed simulated or virtual sensorimotor loop; no validated physical human/device interaction. |
| `E3` | Physical human/device loop with real-time action, mainly healthy or short-session evidence. |
| `E4` | Patient-grounded, subject-specific physical adaptive loop with at least preliminary functional or physiological evaluation. |
| `E5` | Longitudinal clinical co-adaptation with explicit safety/uncertainty and meaningful rehabilitation outcomes. |

No paper in this 49-paper core set reaches `E5`.

## Interpretation rules

- A generic muscle-driven RL agent can be genuine simulated Embodied AI (`E2`) without being human-specific.
- A wearable sensor or offline decoder is not Embodied AI until its output participates in an evaluated action loop.
- A detailed NMS model is a body substrate, not an intelligent agent.
- Physical robot hardware is not sufficient if action is preset and human state does not affect control.
- Human-in-the-loop optimization is embodied control even without an explicit NMS state, but it should not be called NMS modeling.
- Weakness, fatigue or pathology parameters in simulation do not establish patient-specific validation.
- Technical accuracy does not imply rehabilitation value; functional, neural-engagement, safety or recovery outcomes must be checked separately.
- IMU is one possible observation modality. It has no privileged status over EMG, pressure, video, ultrasound, imaging or force measurement.

## Evidence levels

Evidence codes are retained from the earlier critique:

- `full_text_checked`
- `methods_results_checked`
- `methods_results_checked_via_full_text_secondary_copy`
- `abstract_and_methods_summary_checked`

The last category is explicitly weaker. Inaccessible details remain unresolved rather than being inferred.

## Scope limits

- This is a critical re-assessment of the existing core set, not a new exhaustive Embodied-AI literature search.
- The core set was originally selected for NMS digital-twin mapping, so pure robotics/Embodied-AI work outside that search may be underrepresented.
- Evidence should be re-extracted before meta-analysis, clinical claims or quantitative review.
- The classification describes each paper's primary contribution; it does not deny useful secondary relevance.

