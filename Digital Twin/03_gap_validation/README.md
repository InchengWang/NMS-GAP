# NMS Digital-Twin Gap Validation

Counter-evidence-based validation of the ten candidate gaps listed in the first literature map. The review follows the repository skill `nms-digital-twin-gap-validation`: every claim is made falsifiable, searched with synonyms and adjacent terminology, compared against its nearest work, and passed through novelty, contribution and feasibility gates.

## Files

- [`GAP_VALIDATION_REPORT.md`](GAP_VALIDATION_REPORT.md): ten complete gap dossiers and the final priority recommendation.
- [`COUNTER_EVIDENCE_LOG.md`](COUNTER_EVIDENCE_LOG.md): search date, sources, counter-queries, inspected nearest work and unresolved search areas.
- [`data/gap_validation_matrix.csv`](data/gap_validation_matrix.csv): machine-readable verdicts, feasibility and pilot tests.

## Verdict distribution

| Verdict | Count | Candidate IDs |
|---|---:|---|
| `confirmed-open` | 1 | G02 |
| `partially-addressed` | 7 | G01, G03, G04, G05, G07, G08, G09 |
| `not-a-gap` | 1 | G06 |
| `speculative-opportunity` | 0 | — |
| `out-of-scope` | 1 | G10 |

## Practical conclusion

For the current chronic-stroke wearable/mocap research base, the best near-term pilot is not a full digital twin. It is a narrower test of **which sensor subset preserves a decision-relevant state under session change, with calibrated uncertainty and a safe failure rule**. That pilot combines G01, G05 and G07 without pretending that movement reconstruction alone is a complete NMS twin.

