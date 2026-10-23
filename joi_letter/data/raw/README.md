# Staged inputs

These files are read-only inputs for the Letter analysis. Each file’s source,
byte count and SHA-256 are recorded in `../metadata/staged_input_manifest.json`;
downloaded files are additionally listed with their download date and public URL
in `../metadata/external_sources.md`. Nothing here reproduces the Walker et al.
CPRD or case-linkage dataset, and no individual-level record is present.

## Licensing

`ukhsa_prenatal_coverage_q1_2024.xlsx` and `ukhsa_prenatal_coverage_q4_2026.xlsx`
are Crown-copyright UKHSA public-health tables redistributed under the Open
Government Licence v3. `scripts/04_extract_ukhsa_coverage.py` reads
the newer workbook and keeps the older one only as a fallback for a checkout that
has not refreshed the source.

The remaining inputs are aggregate surveillance, demographic and configuration
extracts staged from the authors’ parent modelling repository. Their upstream
paths are named in the manifest. No individual-level record and no privately
communicated array is present: the country profile inputs are WHO/UNICEF and
official-coverage aggregates, and the candidate configuration is a parameter
record of the kind the parent study already ships in its public bundle.

For publication, local absolute paths inside the staged configuration were
rewritten to the placeholder `<parent-repo-root>`. The recorded byte-level
SHA-256 of `uk_candidate_config.yaml` therefore differs from the digest embedded
in the run provenance; the content is unchanged apart from those path strings.

## Contents

| File | Role |
|---|---|
| `ukhsa_prenatal_coverage_q4_2026.xlsx` | Official England prenatal pertussis coverage by ICB, April 2023–March 2026. Source of the coverage path, the March 2026 cross-section and board-level gaps. |
| `ukhsa_prenatal_coverage_q1_2024.xlsx` | Earlier edition of the same table, January–March 2024. Retained as fallback. |
| `uk_candidate_config.yaml` | Staged age-structured model configuration used by the paired scenario runs. Content SHA-256 `e391da85…51`. Calibration status `state_reconstruction_rejected`. |
| `uk_notifications.csv` | Weekly notifications series used for structural validation and seasonal alignment. |
| `england_notifications_age.csv`, `england_notifications_annual.csv` | Age-resolved and annual England notification counts. |
| `england_infant_deaths.csv`, `england_population_model_age.csv` | Infant death counts and the population model by age. |
| `maternal_coverage_processed.csv`, `country_profile_inputs.csv` | Parent-project processed coverage series and country profile inputs. |

The annual UKHSA coverage estimates used in the reported contrast
(58.6% for 2023/24, 65.6% for 2024/25, 73.0% for 2025/26) come from the official
annual denominator and are transcribed into `../derived/ukhsa_coverage_annual.csv`
rather than reconstructed as an unweighted ICB average.

To restage these files from the authors’ parent repository, run
`scripts/00_stage_inputs.py`. It copies without modifying the parent and rewrites
the manifest.
