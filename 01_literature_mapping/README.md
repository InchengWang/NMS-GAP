# NMS-GAP — Human Neuromusculoskeletal Digital Twin / Embodied AI Literature Map

First-pass evidence map for human neuromusculoskeletal digital twins and embodied intelligence, with emphasis on:

- neural control;
- musculoskeletal and multiscale modeling;
- subject-/patient-specific modeling;
- wearable and field sensing;
- rehabilitation;
- assistive robotics.

IMU is treated as one wearable movement-sensing modality rather than the center of the map.

## Deliverables

- [`TAXONOMY.md`](TAXONOMY.md): operational digital-twin maturity ladder and multidimensional NMS taxonomy.
- [`SEARCH_PROTOCOL.md`](SEARCH_PROTOCOL.md): query families, inclusion/exclusion criteria, verification rules, and first-pass limitations.
- [`data/literature_matrix.csv`](data/literature_matrix.csv): 60-paper machine-readable seed matrix.
- [`NMS_literature_map_first_pass.xlsx`](NMS_literature_map_first_pass.xlsx): filterable workbook with summary, literature matrix, and codebook.
- [`CLUSTERS_AND_GAPS.md`](CLUSTERS_AND_GAPS.md): major research clusters, researcher lineages, venue coverage, and uncovered space.

## Central conclusion

The literature currently consists of several strong but incompletely connected layers. Personalized biomechanics is strongest at internal-load and treatment simulation; neural-interface work is strongest at EMG/motor-unit-to-NMS mapping; Embodied AI is strongest at scalable muscle-driven control; and wearable/robotics work is strongest at real-time observability and assistance. The most defensible near-term research program is to connect these layers rather than label any one layer a complete digital twin.

In this first-pass matrix, most original papers are coded as `twin_enabling`, not as complete digital twins. The most mature patient-facing closed loops are real-time NMS-driven prosthesis/exoskeleton interfaces; the most scalable Embodied AI systems remain simulation-only; and longitudinal multi-timescale patient twins remain largely uncovered.

## Priority researcher lineages

- **Durandau–Sartori–Farina:** motor-unit/EMG-driven NMS estimation and real-time wearable-robot control.
- **Pizzolato–Lloyd–Saxby–Diamond:** CEINMS, multiscale personalization, tissue loading, and the explicit NMS digital-twin clinical framework.
- **Fregly/Shourijeh:** model personalization and counterfactual treatment optimization.
- **Yanan Sui:** high-dimensional musculoskeletal Embodied AI, dynamic synergies, full-body self models, and earlier rehabilitation robotics.
- **Delp/Collins:** musculoskeletal infrastructure, field observation, and real-world personalized assistance.

## Evidence status

This is a structured seed map with verified metadata and abstracts for most rows. It is **not yet** a PRISMA-complete systematic review. Search counts, deduplication, independent screening, full-text extraction, risk-of-bias assessment, and citation-network expansion are explicitly reserved for round two.

## Suggested reading order

1. Saxby et al. (2023) for the NMS digital-twin framework.
2. Pizzolato et al. (2015) and Durandau et al. (2018) for calibrated and real-time NMS modeling.
3. Sartori et al. (2017), Kapelner et al. (2020), and Jung et al. (2022) for neural-to-mechanical observability.
4. Durandau et al. (2019) and Sartori et al. (2018) for patient/prosthesis closed loops.
5. Hammond et al. (2025) and Pizzolato et al. (2020) for treatment prediction and multiscale personalization.
6. MyoSuite, MyoDex, DynSyn, MotorNet, and MS-Human-700 for the Embodied AI layer.
7. OpenSense, OpenCap, wearable ultrasound, and multimodal JBHI papers for field observability.

