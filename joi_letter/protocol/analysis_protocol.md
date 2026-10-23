# Analysis protocol: from antenatal VE to infant population impact

## Question

Among infants younger than 3 months, how much does incidence fall if antenatal coverage rises from the observed 73.0% to 75%, 80% or 90%, given Walker’s window effectiveness?

## Reported contrast

The result in the letter is the screening identity. Walker estimates effectiveness as one minus the vaccination odds ratio. When population coverage is the exposure prevalence, that odds ratio equals the disease risk ratio exactly. Rarity explains why laboratory-confirmed infant cases are sparse; it is not the converting step. With coverage c equal to the fraction of infants whose mothers were vaccinated, and with the force of infection common to the arms, incidence in the age window is proportional to 1 − c × VE. The reduction from 73.0% to a national coverage target c1 is 1 − (1 − c1 × VE) / (1 − 0.730 × VE). Each target replaces the national mean. Derivations, the parameter ledger and Supplement Figure S1 are in `manuscript/joi_letter_supplement.md`.

The primary VE is 0.846 (95% CI 0.769–0.897), for infants younger than 3 months. The restricted estimate for onset before 2 months is 0.862 (95% CI 0.783–0.913). Walker’s hospitalisation estimate, 0.882 (0.810–0.927), and death estimate, 0.915 (0.754–0.971), are reported through the same identity. All four are taken from the target article. The hospitalisation and death rows are Walker’s published values. Gestational age is not reweighted: that article found no significant difference across gestational-age categories. The transfer slope, the protection duration, the relative-effect multiplier and the transmission level do not enter this expression.

## Design

Paired deterministic age-structured scenarios use the staged UK-labelled candidate configuration. The historical reconstructed state is held fixed within each scenario. Every Letter scenario replaces the candidate's stored annual phase with the declared UK annual prior before integration: seasonal amplitude 0.14 and seasonal phase day 300, the pre-COVID autumn peak. The candidate phase near day 134 follows the 2024 reporting surge and is not used. The 8-year cycle is not added. The fitted log-transmission path ends on 2024-12-31. From 2025-01-01 through 2035-12-31 every arm holds the declared baseline, log-multiplier −0.50, with reversion rho 0. The prospective policy window is 2027-01-01 to 2035-12-31. One weekly integrator stamp on 2036-01-01 falls outside that window and is excluded from the endpoint. The current arm is itself a prospective policy: antenatal uptake is the observed 2025–26 England annual estimate, 73.0%, mapped by clip(0.02 + 0.55 × uptake, 0, 0.75) to newborn birth exposure 0.4215. National coverage targets of 75%, 80% and 90% use maternal_coverage_min and map to 0.4325, 0.4600 and 0.5150. In the scenario files these arms are labelled floors. They replace the national mean. Maternal protection is 180 days in the prospective window only. The fitted history keeps its 90-day duration, so both mechanism arms share one arrival state. Walker anchoring is applied only in that prospective window. The integrated relative reduction is the diagnostic of that stack. It is not the reported population impact. Absolute sums from the run remain model units under the held transmission bound.

## Scenarios

1. Observed 73.0% baseline, legacy mapping.
2. National coverage targets of 75%, 80% and 90% on that same history and mapping. Scenario files label these arms as floors.
3. The same four arms with Walker anchoring in the prospective window only.
4. Timing sensitivity only if the input representation can be mapped to a documented receipt-time distribution.

The retired profile-history factorial is not part of this contrast. Profile runs kept an 8-year cycle that the recovered candidate does not have, so a history-by-mechanism interaction from those runs is not identified.

The 75/80/90% scenarios are programme targets, not achieved coverage forecasts. They do not include cost, workforce, access, or equity constraints unless those data are added explicitly.

## Maternal VE mapping

The published 0.846 estimate is the window-level risk ratio used in the reported contrast. Inside the transmission diagnostic it is not a direct model parameter. That diagnostic applies a maternal relative-effect multiplier of 0.75 before combining acquisition and conditional symptom protection. The legacy mapping uses raw maternal parameters 0.55 and 0.92, a composite of 0.817875. The Walker-anchored mapping retains raw acquisition protection 0.55 and derives raw conditional symptom protection 0.9838297872 so that the composite on the protected state equals 0.846. Entry is still clip(0.02 + 0.55 × uptake, 0, 0.75), and protection still wanes at 1/180 per day against a mean residence of 91.25 days. Those two factors keep the implied individual effectiveness near 30.2% (legacy) or 31.2% (composite set to 0.846). The components are a decomposition, not separately estimated effects. Hospitalisation and death indices use endpoint-specific conditional severity assumptions and are not treated as additional estimates of the same biological VE.

## Endpoints

Primary: cumulative symptomatic pertussis cases in the model's infant 0–2 month bin, mapped to the `<3 months` target only if the age-bin definition and boundary are exact. If the model bin is not exact, report the closest model-defined infant endpoint and label the mismatch.

Secondary: infant hospitalisations and deaths from the conditional severity cascade; these are not independently calibrated outcomes.

## Required checks

- Verify that maternal coverage is an uptake input and not the newborn protected fraction.
- Verify that the source article's VE is not double-counted with an existing maternal relative-effect parameter.
- Verify age-boundary mapping, calendar dates, and scenario pairing.
- Verify absolute and relative contrasts from the same starting state.
- Confirm no individual-level CPRD data are represented as available.
- Run a smoke test before the full scenario grid.
- Preserve all scenario configuration hashes and software versions.

## Interpretation boundary

The analysis estimates conditional population impact under the model and staged inputs. It does not re-estimate VE, establish causal effects of the English programme, or validate a national 2027–2035 forecast.
