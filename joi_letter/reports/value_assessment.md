# Value assessment

Status: **reported contrast is the screening identity. The transmission run is a mechanism diagnostic. Absolute counts are not a UK burden estimate.**

Derivations, the parameter ledger and Supplement Figure S1 are in `manuscript/joi_letter_supplement.md`. The supplement does not re-integrate the model.

The reported baseline is the observed 2025–26 England annual antenatal uptake, 73.0%. Incidence in the age window is proportional to 1 − c × VE. The primary VE is Walker’s estimate for infants younger than 3 months, 0.846 (95% CI 0.769–0.897). The restricted onset-before-2-months estimate is 0.862 (95% CI 0.783–0.913). No transfer slope, duration, relative-effect multiplier or transmission level enters.

| Window | VE | 75% floor | 80% floor | 90% floor |
|---|---:|---:|---:|---:|
| Younger than 3 months | 0.846 | 4.4245% | 15.4856% | 37.6079% |
| Same, VE 0.769 | 0.769 | 3.5064% | 12.2723% | 29.8042% |
| Same, VE 0.897 | 0.897 | 5.1971% | 18.1900% | 44.1757% |
| Onset before 2 months | 0.862 | 4.6502% | 16.2756% | 39.5264% |

The letter rounds population reductions to one decimal. It quotes disease at 4.4%, 15.5% and 37.6% (29.8–44.2% at 90%), hospitalisation at 90% as 42.1% (33.7–48.7%) and death at 90% as 46.8% (28.5–56.7%). The onset-before-2-months row stays in the table. Along the observed path, 58.6% to 73.0% is 24.2% of cases, 26.3% of hospitalisations and 28.4% of deaths, and 65.6% to 73.0% is 14.1%, 15.5% and 16.9%. Those path reductions treat the recorded rise as uptake. UKHSA Note 1 says the September 2024 Record a Vaccination service may account for part of the recent recorded increase. At 73.0%, direct protection has removed 61.8% of the zero-coverage incidence, and the uncovered 27% of infants account for 70.6% of cases, 75.8% of hospitalisations and 81.3% of deaths. At 90% those shares of remaining cases are 41.9% uncovered and 58.1% breakthrough. March 2026 is a monthly cross-section set against the 2025–26 annual national mean: median 76.4%; 20 of 42 below 75%; eight below 70%; 16 at or above 80%. Birmingham and Solihull, 54.4%, to the national 73.0% is 29.2% of cases, 31.5% of hospitalisations and 33.9% of deaths; to 90% it is 55.8%, 60.4% and 64.9%. Dorset, 85.1%, to 90% is 14.8% of cases. Incidence at 54.4% is 1.93 times incidence at 85.1%. The 90% screening reduction is 6.4 times the legacy integrated reduction, quoted as 5.9% against 37.6%. The letter also cites Walker’s 2024 laboratory-confirmed total (14,879 cases, 11 infant deaths), the study counts (188, 143, 31), the matched-coverage gaps (London 47.9% versus 70.5%; black women 41.4% versus white women 69.7%), Amirthalingam 2014 (91%, 84–95%, on 82 infants), Amirthalingam 2016 (death effectiveness 95%, 79–100%), Tessier 2021 on the 20–32 week window, Farrington 1993 for the screening identity, Byrne 2018 for coverage inequality, and Choi and colleagues’ 2026 account of the wave. Held-out counts 1,746 (2023) and 29,317 (2024) are the England-and-Wales weekly statutory-notification series, not that laboratory-confirmed total and not the England NOIDs annual series (1,557 and 19,218).

The transmission diagnostic is unchanged. Birth exposure is clip(0.02 + 0.55 × uptake, 0, 0.75): 0.4215, 0.4325, 0.4600 and 0.5150. From 2025-01-01 the log-transmission multiplier is held at −0.50. The annual term is amplitude 0.14 and phase day 300. The 8-year cycle is not used. Maternal protection is 180 days in the prospective window and 90 days on the fitted history. Walker anchoring is prospective only. The endpoint is `infant_0_2m`, summed across strains, for calendar dates from 2027-01-01 through 2035-12-31. The integrator’s 2036-01-01 weekly stamp is excluded.

Primary 0–2-month symptomatic cases:

| Mechanism | 73.0% baseline | 75% floor | 80% floor | 90% floor |
|---|---:|---:|---:|---:|
| Legacy mapping | 24.328442 | 24.158739 (0.6975%; 0.169703 averted) | 23.734918 (2.4396%; 0.593524 averted) | 22.889135 (5.9161%; 1.439307 averted) |
| Walker-anchored | 23.986082 | 23.807721 (0.7436%; 0.178361 averted) | 23.362287 (2.6007%; 0.623795 averted) | 22.473417 (6.3064%; 1.512665 averted) |

The letter quotes the legacy integrals as 0.7%, 2.4% and 5.9%, and the Walker-anchored 90% integral as 6.3%. The unrounded ledger is 0.6975%, 2.4396% and 5.9161% (legacy) and 0.7436%, 2.6007% and 6.3064% (Walker composite on the protected state). The 90% gap between those two integrals is 0.3903 percentage points. These are not the reported population impact. The simulation is this project’s observed-baseline run, not a reimplementation of Choi and colleagues.

The current-arm annual totals for 2029–2035 run from 2.537 to 2.947 (legacy) and from 2.501 to 2.906 (Walker). The max/min ratios are 1.161 and 1.162. Both arms are strictly decreasing across 73% → 75% → 80% → 90%. In 2030–2035 every weekly peak falls in December. The within-year index peaks at 1.139 in December and troughs at 0.886 in June (ratio 1.285).

### Why the integral is about 6%

Mean residence in `infant_0_2m` is 0.25 × 365 = 91.25 days, so the aging rate is 1/91.25 per day. Waning is 1/180 per day. The equilibrium fraction of protected entrants’ person-time still in the protected state is φ = 180/271.25 = 0.66359447. Legacy composite v = 1 − (1 − 0.75 × 0.55)(1 − 0.75 × 0.92) = 0.817875. A vaccinated mother maps to entry 0.57 and an unvaccinated mother to entry 0.02. Individual effectiveness is

1 − [1 − 0.57 φ v] / [1 − 0.02 φ v] = 0.30178129 (30.2%).

With v set to 0.846 the same expression is 0.31227676 (31.2%). Population reduction on the diluted exposure, 1 − [1 − e1 φ v] / [1 − e0 φ v] with e0 = 0.4215, is 0.774%, 2.709% and 6.580% (legacy) and 0.809%, 2.831% and 6.876% (v = 0.846). The legacy integral at 90% is 5.916%. The 0.66 percentage-point residual is not assigned to a further mechanism.

Both-strain infection-weighted maternal-origin shares in the legacy run, horizon 2027-01-01 to 2035-12-31, are 0.184192, 0.189573, 0.203185 and 0.231106. The susceptibility-weighted equilibrium, with protected susceptibility 1 − 0.75 × 0.55 = 0.5875, gives 0.185759, 0.191258, 0.205171 and 0.233728. The dose-1 origin share is 0 in every arm. Case sums across strains match the ledger: current 24.328442.

### Parameter basis

| Quantity | In the reported contrast | Basis |
|---|---|---|
| Uptake 73.0%, and the path 58.6%, 65.6%, ICB 54.4–85.1% | Yes | UKHSA prenatal coverage, 2025–26 annual and March 2026 |
| Targets 75%, 80%, 90% | Yes, as uniform national means | Scenario files label the same arms as floors. Not fitted coverages |
| VE 0.846 (0.769–0.897) | Yes, primary | Walker, infants younger than 3 months, screening method |
| VE 0.862 (0.783–0.913) | Yes, restricted window | Walker, onset before 2 months |
| Odds ratio read as a risk ratio | Yes | Exact when population coverage is the exposure prevalence. Rarity explains sparse laboratory-confirmed cases; it is not the converting step |
| No gestational-age weight | Yes | Walker found no significant difference by gestational-age category |
| Slope 0.55, intercept 0.02, cap 0.75 | No | `config/model_settings.yaml`: reduced-form proxy, not a measured transfer probability. The cap does not bind on these uptakes |
| Relative-effect multiplier 0.75 | No | Fixed in the submitted intervention, not estimated from clinical data |
| Raw VE_sus 0.55 and VE_sym 0.92 | No | A disease-effectiveness estimate reused as an infection component, with a hospitalisation prior stacked on top. Not two identified effects |
| Prospective duration 180 days | No | Mode of the triangular intervention prior 90/180/270. Not an antibody half-life |
| PT-IgG half-life 29.4 days (27.3–31.7) | Not inserted | Healy et al., Vaccine 2020. No concentration equals protection, and Walker’s VE already averages the window |
| Log-multiplier −0.50 | No | Declared forecast stabiliser in `config/country_profiles.yaml`. Scales counts; absent from the screening ratio |
| Amplitude 0.14, phase day 300 | Timing only | Declared pre-COVID structural prior. Common to both arms of the ratio. December index 1.14 is descriptive |
| Bin width 0.25 years | Diagnostic only | Model demography. Names the compartment 0–2 months and sets the 91.25-day residence used above |

The absolute sums, about 24 model cases over nine years, are not England’s infant burden. The candidate status is `state_reconstruction_rejected`, reporting in the candidate is saturated, and −0.50 is the declared forecast prior rather than a value fitted to 2025–2035. The held-out structural reforecast is unchanged: 1,066 predicted versus 1,746 reported in 2023, and 7,719 versus 29,317 in 2024, with the prediction rising into December while 2024 peaked in May. Those folds were not refit, and the phase was not moved to May.

The retired 58.56% baseline and the history-by-cycle factorial are not results of this contrast. Do not cite 18,810 cases, reductions of 9.53%, 11.17% or 14.43%, or an interaction of +0.46 percentage points.
