# Validation report

Status: **conditional exploratory outputs available; validation gate not passed**.

Completed checks:

- staged-input hashes match `data/metadata/staged_input_manifest.json`;
- all required UK inputs are present;
- maternal VE is mapped once inside each transmission arm;
- the reported population contrast does not use that arm: it applies Walker’s window VE directly, because the arm’s entry slope, 180-day clock and decomposed composite imply about 30% individual effectiveness;
- the primary endpoint is the exact modelled `infant_0_2m` age bin;
- paired scenarios share a common reconstructed starting state;
- scenario outputs are finite, non-negative and monotone across the 75%, 80% and 90% targets;
- the applied prospective coverage was audited: the current arm is the observed 73.0% uptake and maps to birth exposure 0.4215, and the 75%, 80% and 90% floors map to 0.4325, 0.4600 and 0.5150;
- both mechanism arms hold log-transmission at −0.50 from 2025-01-01, use a 180-day prospective duration against a 90-day fitted history, and pass the 2029–2035 stability gate (max/min about 1.16) with strictly decreasing 0–2-month totals;
- the 0–2-month ledger for 2027–2035 is `data/derived/joi_factorial_absolute.csv`, and the coverage audit is `data/derived/joi_coverage_trajectory_audit.csv`;
- output ledgers retain scenario, endpoint, absolute cases, comparator cases, absolute difference, relative reduction, run metadata and input hashes;
- no output is described as a validated national forecast.

Validation boundary:

- the recovered candidate state reconstruction was rejected by the parent calibration acceptance gate;
- independent rolling-origin held-out sMAPE was 1.892164 in 2023 and 1.293582 in 2024 on the validation score's 0–2 scale;
- the resulting estimates are suitable for paired sensitivity comparisons and mechanism cross-checks, not point epidemic forecasting.
