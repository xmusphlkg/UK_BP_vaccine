# UK antenatal pertussis vaccination: replication materials

This repository holds the **public replication materials** for a Letter to the
Editor submitted to the *Journal of Infection*, in response to

> Walker JL, Ribeiro S, Litt D, et al. Antenatal pertussis vaccine effectiveness
> in England remains high post COVID-19. *J Infect*. 2026;93:106836.
> doi:10.1016/j.jinf.2026.106836

Working title of the Letter: **“From antenatal pertussis vaccine effectiveness to
infant population impact.”**

The project question is:

> Does high antenatal vaccine effectiveness translate into low infant population
> burden when coverage is incomplete, delayed, or unequally distributed?

The analysis connects Walker and colleagues’ published effectiveness estimates to
observed English antenatal coverage and to an age-structured transmission model
of this project’s own construction. It does **not** re-estimate individual-level
vaccine effectiveness. The CPRD pregnancy records and the case-level linkage data
of the target article were not available to this project and are not reproduced
here.

## Headline result

The reported population contrast is Farrington’s **screening identity**. When
population coverage is the exposure prevalence, the odds ratio estimated by that
method equals the disease risk ratio, so incidence in the age window scales with
`1 − c × VE`. The baseline is the observed 2025–26 England annual antenatal
uptake, **73.0%** (UKHSA). With Walker’s primary estimate for infants younger
than 3 months, **VE = 0.846 (95% CI 0.769–0.897)**, the reduction in infant cases
relative to that baseline is

| National coverage target | Cases, <3 months | 95% CI range |
|---|---:|---:|
| 75% | 4.42% | 3.51–5.20% |
| 80% | 15.49% | 12.27–18.19% |
| 90% | 37.61% | 29.80–44.18% |

The Letter rounds these to 4.4%, 15.5% and 37.6%. Restricted to onset before
2 months (VE 0.862), the 90% target gives 39.53%. Through the same identity, the
90% target reduces hospitalisations by 42.1% and deaths by 46.8% using Walker’s
published estimates for those endpoints.

The age-structured transmission run is a **mechanism diagnostic**, not the
reported population impact. Its birth-entry slope (0.02 + 0.55 × uptake), its
180-day maternal-protection clock and its decomposed composite leave implied
individual effectiveness near **30.2%** (31.2% when the composite is anchored to
0.846), which yields reductions of 0.70%, 2.44% and 5.92% at the same targets.
The 6.4-fold gap between 37.6% and 5.9% is the point of the comparison. Absolute
counts from that run are uncalibrated model units, not a UK burden estimate.

Full derivations, parameter ledger and the source of every number quoted above
are in [`joi_letter/reports/value_assessment.md`](joi_letter/reports/value_assessment.md),
[`joi_letter/protocol/analysis_protocol.md`](joi_letter/protocol/analysis_protocol.md)
and [`joi_letter/reports/validation_report.md`](joi_letter/reports/validation_report.md).

## Repository map

```
UK_BP_vaccine/
├── README.md                  this file
├── LICENSE                    MIT (code); data licences noted below
├── CITATION.cff               how to cite these materials
├── requirements.txt           Python packages used by the released scripts
├── RELEASE_MANIFEST.md        every released file with its SHA-256
└── joi_letter/
    ├── README.md              project overview, status and reproducibility steps
    ├── Makefile               convenience targets for the local checks
    ├── PROJECT_STATUS.md      task ledger for the working project
    ├── protocol/              analysis protocol (design, endpoints, checks, limits)
    ├── config/                machine-readable study configuration
    ├── code/                  protocol validator and the reported-number verifier
    ├── references/            factual record of the estimates taken from the target article
    ├── data/
    │   ├── raw/               staged inputs (UKHSA workbook, surveillance extracts, model config)
    │   ├── metadata/          provenance: hashes, source list, surveillance manifest
    │   └── derived/           tidy inputs behind every figure panel and result table
    ├── outputs/
    │   ├── figures/           the three display items (PNG, PDF, SVG)
    │   ├── tables/            monthly UKHSA coverage summary
    │   └── model_runs/        run summaries and metadata behind the diagnostic figures
    ├── reports/               input audit, validation report, value assessment
    └── scripts/               numbered pipeline, oldest to newest
```

## What is reproducible here

Everything below runs with the Python packages in `requirements.txt`
(plus R ≥ 4.2 with `ggplot2`, `patchwork`, `dplyr`, `readr`, `tidyr`, `scales`,
`grid` and `ragg` for the display figures).

**Tier 1 — self-contained, no external code needed.**

```bash
python3 joi_letter/code/validate_protocol.py               # checks the study configuration
python3 joi_letter/code/verify_reported_numbers.py         # recomputes every reported contrast
python3 joi_letter/scripts/04_extract_ukhsa_coverage.py    # rebuilds the coverage inputs from the workbook
python3 joi_letter/scripts/17_make_supplement_schematic.py # closed-form supplement figure + assertions
python3 joi_letter/scripts/14_audit_coverage_and_factorial.py
```

`verify_reported_numbers.py` re-derives the screening contrast from first
principles and asserts it against `data/derived/joi_reduction_readings.csv` and
`reports/value_assessment.md`; it also reconciles the age-structured diagnostic
against `data/derived/joi_factorial_absolute.csv`.
`17_make_supplement_schematic.py` aborts if any displayed closed form drifts from
the recorded ledger. Both fail closed, so a clean run is a numerical audit of the
released results.

**Tier 2 — needs the age-structured ODE engine of the parent project.**

Scripts `06`, `08`, `13`, `15` and `16` import `src_python` from the authors’
parent modelling repository (currently private) and are therefore **not** runnable
from this repository alone. Scripts `10` and `12` do not import the engine but read
the weekly grids it writes; those grids are regenerated rather than redistributed,
so they belong to this tier too. All of them are released so that the analysis is
fully specified and auditable, and their downstream products are released with
them, so every Tier 1 step above can be re-run and checked without that engine. Before
running `12_prepare_figure_ledgers.py`, set `JOI_VALIDATION_ROOT` to the parent
repository’s validation-fold directory; the script otherwise falls back to the
authors’ machine paths and will raise `FileNotFoundError`. The corresponding fold
results are already released in `data/derived/joi_validation_timeseries.csv` and
`data/derived/joi_validation_panel_data.csv`.

**Display figures.** The two Letter figures are composed in R from the released
ledgers. Run from inside `joi_letter/`, because the renderer resolves paths
relative to that directory:

```bash
cd joi_letter
Rscript scripts/09_make_figure_ggplot.R
```

Required R packages: `ggplot2`, `patchwork`, `dplyr`, `readr`, `tidyr`, `scales`,
`grid` (base R distribution) and `ragg` (PNG device). `svglite` is optional; when
installed it also writes the vector copies in `outputs/figures/vector/`.

## What is deliberately not released

- **The submitted manuscript text** (Letter draft, supplementary appendix and
  cover letter). Nothing from `manuscript/` is released; those files can be added
  after the editorial decision. Cross-references inside the released reports to
  `manuscript/joi_letter_supplement.md` therefore point to files that are not
  here. Supplement Figure S1 is still reproducible as
  `outputs/figures/joi_supplement_schematic.*` from
  `scripts/17_make_supplement_schematic.py`.
- **The target article PDF** (`PIIS0163445326001623.pdf`), which is Elsevier
  copyrighted and was used only as a reading source for published estimates. The
  estimates this analysis depends on are transcribed in
  [`joi_letter/references/joi_article.md`](joi_letter/references/joi_article.md).
- **The parent ODE engine** (`src_python`), until the parent study releases it.
- **Superseded artifacts** of the retired 58.56% baseline and the crossed
  history × mechanism factorial: the model units output by that run, its
  `outputs/tables/joi_model_scenario_summary.csv`, and the old-baseline
  `reports/value_assessment.json`.
  Do not cite those numbers: reductions of 9.53%, 11.17% and 14.43%, or an interaction
  of +0.46 percentage points, are **not** results of this contrast. `reports/value_assessment.md`
  marks the boundary.
- **Bulk simulation histories** (`outputs/model_runs/*/timeseries.parquet`, about
  25 MB). They are weekly grids that the parent engine regenerates; the display
  panels depend only on the released CSV ledgers in `data/derived/`.
- Local caches, logs and exploratory figure drafts.

## Interpretation boundary

Read `joi_letter/reports/validation_report.md` before quoting any number. The
recovered candidate’s state reconstruction was rejected by the parent calibration
acceptance gate; independent rolling-origin held-out sMAPE was 1.89 (2023) and
1.29 (2024) on that score’s 0–2 scale. Nothing here is a validated England or UK
national forecast, and the absolute simulated counts are model units. The
population contrast itself does not depend on those quantities, which is why it
is the reported result.

## Data provenance and licensing

- Code: MIT (see `LICENSE`).
- `joi_letter/data/raw/ukhsa_prenatal_coverage_*.xlsx` are Crown-copyright UKHSA
  public-health tables redistributed under the Open Government Licence v3, with
  sources and download dates recorded in
  [`joi_letter/data/metadata/external_sources.md`](joi_letter/data/metadata/external_sources.md).
- The remaining `data/raw/` inputs are aggregate, publicly sourced surveillance
  and demographic extracts staged from the parent project. Their source paths,
  byte counts and SHA-256 values are in
  [`joi_letter/data/metadata/staged_input_manifest.json`](joi_letter/data/metadata/staged_input_manifest.json),
  and the surveillance source register is
  `data/metadata/validated_surveillance_source_manifest.csv`.
- No individual-level record, no CPRD record and no case-linkage record is
  contained in this repository.

## Contact

Questions about these materials: open an issue on this repository.

