# First-Pass Search Protocol

## 1. Review question

How is the human neuromusculoskeletal system being modeled, individualized, observed, predicted, and acted upon as a digital twin or embodied agent for neural control, rehabilitation, and assistive robotics?

This is a **first-round evidence map**, not yet a PRISMA-complete systematic review. The goal is high-recall discovery of research clusters and bridges, followed by a traceable seed matrix.

## 2. Scope and cutoff

- Search cutoff: **2026-09-01**.
- Main publication window: **2015–2026**.
- Seminal pre-2015 papers retained when they define EMG-driven NMS modeling or hybrid neural-control methods.
- Language: English.
- Species: human; high-fidelity human models; animal work only if directly necessary to validate a human NMS mechanism (none prioritized in this pass).
- IMU is searched under wearable sensing, not used as a central concept.

## 3. Concept blocks

```text
A. System
(neuromusculoskeletal OR neuro-musculo-skeletal OR neuromechanical
 OR "musculoskeletal model*" OR "muscle-driven model*")

B. Individual binding / twin behavior
("digital twin*" OR "human digital twin*" OR subject-specific
 OR patient-specific OR personali?ed OR calibration OR adaptive
 OR "real-time" OR online OR longitudinal OR predictive)

C. Neural and sensing
("neural control" OR "motor unit*" OR "muscle synerg*" OR EMG
 OR electromyogra* OR ultrasound OR optomyogra* OR wearable*
 OR inertial OR IMU OR vision OR pressure OR imaging)

D. Action/use
(rehabilitation OR neurorehabilitation OR prosthe* OR exoskeleton
 OR "assistive robot*" OR FES OR "functional electrical stimulation"
 OR "treatment planning" OR feedback OR "human-in-the-loop")

E. Embodied learning
("embodied AI" OR "embodied intelligence" OR reinforcement learning
 OR imitation learning OR "world model*" OR "differentiable biomechan*"
 OR MyoSuite OR MyoSim OR MotorNet)
```

## 4. Reproducible query families

### PubMed / biomedical databases

```text
((neuromusculoskeletal[Title/Abstract] OR neuromechanical[Title/Abstract]
  OR "musculoskeletal model"[Title/Abstract])
 AND
 ("digital twin"[Title/Abstract] OR subject-specific[Title/Abstract]
  OR patient-specific[Title/Abstract] OR personalized[Title/Abstract]
  OR personalised[Title/Abstract] OR "real-time"[Title/Abstract]
  OR online[Title/Abstract] OR adaptive[Title/Abstract])
 AND
 (human*[Title/Abstract] OR patient*[Title/Abstract]))
```

```text
((EMG[Title/Abstract] OR electromyography[Title/Abstract]
  OR "motor unit"[Title/Abstract] OR "muscle synergy"[Title/Abstract])
 AND (musculoskeletal[Title/Abstract] OR neuromechanical[Title/Abstract])
 AND (rehabilitation[Title/Abstract] OR prosthesis[Title/Abstract]
  OR exoskeleton[Title/Abstract] OR "assistive robot"[Title/Abstract]))
```

```text
((wearable*[Title/Abstract] OR ultrasound[Title/Abstract]
  OR optomyography[Title/Abstract] OR IMU[Title/Abstract]
  OR inertial[Title/Abstract] OR markerless[Title/Abstract])
 AND (musculoskeletal[Title/Abstract] OR joint-load*[Title/Abstract]
  OR muscle-force*[Title/Abstract])
 AND (real-time[Title/Abstract] OR monitoring[Title/Abstract]
  OR rehabilitation[Title/Abstract] OR control[Title/Abstract]))
```

### Scopus / Web of Science style

```text
TITLE-ABS-KEY(
  (neuromusculoskeletal OR neuromechanical OR "musculoskeletal model*")
  AND ("digital twin*" OR subject-specific OR patient-specific
       OR personali?ed OR adaptive OR "real-time" OR online)
  AND ("neural control" OR EMG OR "motor unit*" OR wearable*
       OR rehabilitation OR prosthe* OR exoskeleton OR "assistive robot*")
)
AND PUBYEAR > 2014 AND PUBYEAR < 2027
```

### IEEE Xplore / robotics and biomedical engineering

```text
("All Metadata":neuromusculoskeletal OR "All Metadata":"musculoskeletal model")
AND ("All Metadata":personalized OR "All Metadata":"patient-specific"
     OR "All Metadata":"real-time" OR "All Metadata":adaptive)
AND ("All Metadata":exoskeleton OR "All Metadata":prosthesis
     OR "All Metadata":rehabilitation OR "All Metadata":wearable)
```

Run venue filters separately for:

- IEEE TNSRE, TBME, JBHI, TRO, TMRB and Journal of Neural Engineering.
- Journal of NeuroEngineering and Rehabilitation, Journal of Biomechanics, Scientific Reports.
- ICRA, IROS, NeurIPS, CoRL, ICML, L4DC and RSS.

### ML/robotics proceedings

```text
(musculoskeletal OR neuromuscular OR muscle-driven)
AND (control OR reinforcement learning OR imitation OR policy
     OR synergy OR embodied OR prosthetic OR exoskeleton)
```

Search the proceedings sites directly because `digital twin` is rarely used by the Embodied AI papers.

### Author and lineage queries

```text
(Durandau OR Sartori) AND (EMG-driven OR neuromusculoskeletal)
AND (real-time OR exoskeleton OR prosthesis)
```

```text
(Pizzolato OR Lloyd OR Diamond OR Saxby) AND
(personalized OR multiscale OR CEINMS OR digital twin OR rehabilitation)
```

```text
("Yanan Sui" OR "Yannan Sui") AND
(musculoskeletal OR embodied OR rehabilitation OR exoskeleton)
```

The verified researcher spelling in the mapped publications is **Yanan Sui**.

## 5. Inclusion criteria

Include if at least one condition in each row is satisfied:

| Dimension | Inclusion condition |
|---|---|
| System | Explicit neural–muscle–skeletal chain; muscle-driven musculoskeletal model; or tissue model receiving NMS loading |
| Individual/action relevance | Subject/patient personalization, real-time synchronization, treatment prediction, wearable observability, rehabilitation feedback, or assistive-device control |
| Evidence type | Peer-reviewed original research, high-value review/framework, or strategically important open benchmark/software paper |
| Validation | Human data, patient data, validated simulation, or open benchmark with physiological models |
| Time | 2015–2026, plus named seminal precursors |

## 6. Exclusion criteria

Exclude from the core matrix when the paper is:

- An industrial/manufacturing digital twin with no human NMS link.
- Pure activity recognition, gait-event detection, pose reconstruction, or IMU classification with no internal mechanics, neural state, treatment, or assistive-control bridge.
- Pure medical imaging segmentation with no mechanical/treatment model.
- A generic robot-controller paper that does not model, estimate, or adapt to human biological state.
- A static avatar/dashboard described as a twin without synchronization or predictive/actionable content.
- Purely animal or cell/tissue work without a direct bridge to human NMS modeling.
- A duplicate, retracted item, non-English paper, commentary without technical content, or inaccessible record lacking sufficient metadata.

Borderline sensing and controller papers can be kept as `adjacent` when they expose an important bridge or missing layer.

## 7. Screening and verification fields

- `metadata_verified`: title, authors/year/venue/identifier checked.
- `metadata_and_abstract_verified`: abstract inspected and classification based on reported methods/results.
- `full_text_sections_verified`: relevant methods/results or systematic-review sections inspected.
- `preprint_metadata_verified`: retained as a watch item; do not mix with peer-reviewed evidence.

## 8. Current search limits

This pass used public scholarly pages, PubMed/publisher metadata, proceedings sites, and researcher/institution publication pages. It did not yet perform:

1. Database-export deduplication with exact hit counts.
2. Independent dual screening.
3. Full-text extraction for every row.
4. Backward/forward citation snowballing for every core paper.
5. Risk-of-bias or model-credibility scoring.

These items define round two rather than hidden assumptions in round one.

