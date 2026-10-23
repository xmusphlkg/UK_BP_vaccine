# Project status

Updated: 2026-10-22 (UTC)

## Current state

- [x] JOI article PDF archived locally.
- [x] JOI Letter requirements recorded in `reports/joi_requirements.md`.
- [x] Independent directory and provenance boundary created.
- [x] UK-labelled inputs staged with hashes.
- [x] Analysis protocol and manuscript scaffold created.
- [x] Implement a Walker-anchored maternal VE mapping for exploratory scenarios.
- [x] Implement and test the `<3 months` endpoint from the model's `infant_0_2m` age bin.
- [x] Run observed-profile and 75/80/90% maternal coverage scenarios under legacy and Walker-anchored VE settings.
- [x] Run the staged recovered UK candidate through the same paired scenarios, with calibration and hold-out status carried into metadata.
- [x] Replace the cycle-confounded factorial with the observed 73.0% baseline and the held −0.50 transmission bound (`scripts/16_run_observed_baseline.py`).
- [x] Refresh the coverage input to the UKHSA March 2026 workbook and preserve the 2023/24–2025/26 annual estimates.
- [ ] Add timing and subgroup analyses only if data support them.
- [x] Generate two publication figures and source-data ledgers with ggplot2 and patchwork.
- [x] Complete numerical monotonicity and output-integrity audit.
- [x] Render a caption-led two-figure ggplot2/patchwork set linking coverage recovery, the screening-method contrast, the stack’s implied individual effectiveness, the December seasonal term and the validation boundary.
- [x] Report the population contrast from Walker’s window VE and UKHSA coverage. The transmission run is the mechanism diagnostic of the uncited entry slope, 180-day clock and VE decomposition.
- [x] Write the supplement with the screening identity, the stack equilibrium, Supplement Figure S1 and the parameter ledger (`manuscript/joi_letter_supplement.md`).
- [ ] Complete UK-specific calibration and claim-source audit. The staged candidate is currently rejected by the parent state-reconstruction gate; independent-fold SMAPE is 1.89 (2023) and 1.29 (2024).
- [ ] Manually prepare any author-owned submission DOCX/PDF outside this automated directory.

## Scientific gate

No result may be described as a national forecast until an England-specific calibration, age-pattern check, and held-out validation pass. The current UK-labelled profile is a conditional scenario profile with a geographic scope mismatch documented in the parent project.
