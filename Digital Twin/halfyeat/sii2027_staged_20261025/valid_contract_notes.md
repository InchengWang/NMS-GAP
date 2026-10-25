# Separate VALID target preparation contract

This is preparation for one frozen five-arm development diagnostic. It is not permission to train on VALID, choose checkpoints by VALID, search a lag or axes, or claim patient-excluded generalization. The producer has not been run on real dynamic VALID data.

`build_valid_targets.py --metadata-check` reads five existing JSON inventories only. The current inventories contain exactly 12 VALID parents and 7,238 full original frames, without crop. P6/hemi060204 has no S5 accelerometer file; P17/hemi170103 has no S5 gyroscope file. The other 70 of 72 parent/modality combinations are available according to the frozen inventory. Availability is not yet a numerical interpolation audit.

The existing full query endpoints equal the accepted matching record's `source_walk_epoch_bounds_ms` for all 12 parents. Their original episode/run context margins are at least 12.9 seconds. This establishes a metadata basis for retaining minimal adjacent native interpolation rows just outside the query interval, instead of changing the analysis support. It does not establish that those rows are inside the exact walking interval. At real export each endpoint flank must obey the same already fixed interpolation gap allowance as its source: native 25.1 ms and point 0.0251 s. It must remain within both the original native episode and run and must not enter a different role's walking interval. Point row times are mapped to the same native epoch using the fixed candidate offset for this check. The manifest explicitly reports the external row indices, clock values and before/after context distances. Only the immediate nearest interpolation bracket is allowed; the allowance does not authorize selecting more distant rows.

Before the analysis contract was frozen and before any real VALID dynamic values or performance were read, the root amended the initial 10 ms endpoint-only threshold to the source's already declared maximum interpolation gap. The basis is the existing clock inventory's known timestamp jitter up to 11 ms, which is incompatible with an endpoint-only 10 ms rule despite satisfying the fixed 25.1 ms interpolation policy. This is a consistency amendment using source clock metadata, with no VALID error or performance information. The old 16-check receipt (`valid_synthetic_preflight.json`) and metadata report (`valid_metadata_preflight.json`) retain their original producer SHA and historical 10 ms policy; the new source-bound checks are `valid_synthetic_preflight_v2.json` and `valid_metadata_preflight_v2.json`. The current real numerical endpoint gate remains unpassed. Any bracket gap/context violation is fatal: the producer must not silently remove frames, change the lag, search axes, convert a present modality to missing, or exclude a trial.

## Export authorization

`valid_export_authorization.template.json` is deliberately invalid until the root separately freezes it as `valid_export_authorization.json`. The status must become `authorized_once_VALID_development_diagnostic`; the allowed list must remain all 12 sorted VALID parents; expected frames must remain 7,238 and support must remain `full_original_no_crop`.

The authorization binds the VALID producer SHA, the unchanged TRAIN helper SHA, three prerequisite files (TRAIN independent target audit, TRAIN training audit, and the pre-VALID analysis contract), and five distinct final-epoch-50 checkpoint paths/SHAs for direct, auxiliary_only, latent_bottleneck, strict_staged and residual_staged. All four prerequisite assertions must be true. These assertions are signed by the root through the frozen authorization file, and are not inferred from unspecified audit JSON field names. The exporter checks each bound artifact's exact SHA before it hashes or loads a VALID source. Prerequisite/checkpoint paths must be inside the study root and cannot be CSV or NPZ files. The analysis contract need not refer back to the authorization, avoiding a hash-reference loop. The output data contract records the authorization file SHA. A second identical export can validate existing immutable files; this does not authorize another analysis or a new model selection round.

## NPZ schema

The filename is `{subject}__{trial}_staged_VALID.npz`. Model-facing arrays use the same names, shapes and units as TRAIN; VALID preserves all original frames.

| Field | Shape / dtype | Meaning |
|---|---|---|
| x | N×12 float32 | Exact original S1/S2 native measured six-axis input, unchanged |
| y | N×6 float32 | Exact original angle target, unchanged |
| sensor_target | N×18 float32 | S3, S4, S5; each ACC xyz in m/s² then GYRO xyz in rad/s |
| sensor_mask | N×18 bool | Available modalities true; only frozen inventory absence permits false |
| positions | N×24 float32 | Eight optical joint/foot landmark xyz positions, bilateral-hip midpoint subtracted, mm→m |
| time / input_epoch_ms / optic_absolute_time | N, original dtype | Exact original time arrays; audit metadata, not model inputs |
| source_frame_indices | N int64 | `arange(N)`; no crop |
| sensor_source_left_indices / sensor_source_right_indices | N×6 int64 | Source data-row indices, zero based after header; missing modality −1 |
| sensor_interp_alpha | N×6 float64 | Linear interpolation fraction; missing modality zero |
| point_source_left_indices / point_source_right_indices | N int64 | Optical point source row indices |
| point_interp_alpha | N float64 | Point interpolation fraction |
| subject / parent_id / split / contract_sha256 / provenance_json | Scalar Unicode | Identity, VALID role, independent data contract and source/context receipts |

The position frame remains the inherited pelvis engineering axes. These are skeletal landmark proxies, not physical hardware sensor centers or clinical JCS coordinates. Position interpolation and centering use float64 followed by one float32 cast. Existing x/y and query clocks are not recalculated from auxiliary labels. The auxiliary arrays are diagnostic targets, never deployment inputs.

## Manifest schema and exposure accounting

`contract.json` binds the independent authorization, metadata, source plan for all 12 parents, code/helper SHAs, query policy, coordinate/units/missingness definitions and endpoint context rule. Both contract and manifest explicitly expose `analysis_contract_sha256`, equal to the separately authorized `prerequisites.VALID_analysis_contract.sha256`, for the evaluation gate. `manifest.json` is emitted only for the complete 12-parent / 7,238-frame release. A `--parent` subset emits a `partial_manifest_{selectionSHA16}.json` and cannot claim completeness. The final schema binding is additionally checked in `valid_synthetic_preflight_v3.json`; all prior receipts remain preserved.

Top-level manifest fields include version/status, complete_release, contract/producer/helper/authorization SHAs, requested_VALID_parents, roles `{TRAIN:0, VALID:12, TEST:0}`, frames, crop=null, target seconds, unique source count, native/point numeric row counts, external adjacent-row counts, fixed context limit and containment assertions, scaler/model fit counts zero, and pending independent-audit readiness. Each parent row records artifact SHA, full frame count, availability, supervised seconds/channel-frames, source NPZ SHA and array SHAs. `source_value_read_receipts` records the source identity, VALID owners, all clock rows scanned, exact selected row indices, selected-token and decoded-row SHAs, unit factor, and per-parent endpoint support. `run_receipts/run_{SHA20}.json` records the immutable invocation/access log separately.

Native raw files are shared with TRAIN/TEST intervals. Mechanical full-file SHA checks before and after decoding read every byte; both CSV passes read rows as strings, and the clock pass parses all timestamps. Only the union of authorized VALID interpolation bracket rows has signal numbers converted. This must never be described as zero TRAIN/TEST source-byte exposure. No TRAIN or TEST dynamic NPZ arrays are loaded by this producer.

## Remaining numerical gates

Before any diagnostic, real export must verify each original NPZ/source SHA and exact x/y/clocks, complete coverage and strictly monotonic clocks, no extrapolation, native/point bracket gaps ≤25.1 ms, finite selected values, all endpoint context constraints, fixed units and masks, and immutable output consistency. An independent audit must then compare all exported arrays, masks, source brackets and position proxies. The metadata-only and synthetic reports do not pass these real-data gates.
