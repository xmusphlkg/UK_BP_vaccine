# Release manifest

Every file in this repository with its byte size and SHA-256 digest.
Regenerate with

```bash
find . -path ./.git -prune -o -type f -print | grep -v RELEASE_MANIFEST.md | sort | xargs sha256sum
```

Files deliberately not released are listed in `README.md` under
“What is deliberately not released”.

83 files, 3,991,033 bytes.

| File | Bytes | SHA-256 |
|---|---:|---|
| `.gitignore` | 196 | `7d0e216ff84af50aad2fb7045e45018387a67a68586a46a89cf89627dd5cd570` |
| `CITATION.cff` | 1,760 | `1316dd625bd0df617957768b2b04036740d591121f44698b14f7e21737e32301` |
| `LICENSE` | 1,378 | `2e239ea07ff559814552a7ccdd0bee0e413c33e4d0587415575f7dc968b30066` |
| `README.md` | 10,609 | `f09f04d71080273794d9b5dc4b1056dda9aff725dc0a6ee3e92b8f9dfb2fde35` |
| `joi_letter/Makefile` | 366 | `5a31d35473b42e4c2e11001837ef4a51a3a4af30fefb10858a065df53ff43fb8` |
| `joi_letter/PROJECT_STATUS.md` | 2,437 | `3de481ca9388118b1c7fa9830ec68cf31f3be2f068e83b898169253a21badf6b` |
| `joi_letter/README.md` | 7,344 | `010c0677f9490b675d84b60231a183ca6f6ab5d50eae28344b355549ef04f6f3` |
| `joi_letter/code/README.md` | 575 | `7dfa198596124e3d6fa03c0a0e2f47cbf91e9ca53f84a8a03fdf832b939b7b36` |
| `joi_letter/code/validate_protocol.py` | 877 | `74bd9591af521ccf9111bfba247d985e5c4f73720bc8b3f93da2647a2218774d` |
| `joi_letter/code/verify_reported_numbers.py` | 10,256 | `88de2728fa2814fb66b25c19fd201f53a68f56d175b6ba8f99968a7329dfdf2b` |
| `joi_letter/config/letter_config.yaml` | 600 | `4ad5ce25d55f65f63f1f57828e59f0ea14d16424da42958e2d713f28d8c87abd` |
| `joi_letter/data/derived/joi_coverage_panel_data.csv` | 93,895 | `5c04bc5e3a2a53b3b701855340ec38ea1b7e1400f8cab13200af9f334dee2a38` |
| `joi_letter/data/derived/joi_coverage_trajectory_audit.csv` | 1,403 | `4e1d9f66299e995fc0c486c81956338815f50373dab0fcb8dfe37c3e56010b76` |
| `joi_letter/data/derived/joi_factorial_absolute.csv` | 2,152 | `1e0e55ee8962be6bd722423f52ef8f3700aa5963ddec285b2e0f30a827349d27` |
| `joi_letter/data/derived/joi_figure_panel_data.csv` | 1,864 | `dcff80912d37419e8dfa3485e317e315bdfa5634797fc820dad64f60bed9f80c` |
| `joi_letter/data/derived/joi_infant_under3_summary.csv` | 1,907 | `2aa76fee1fa163a34aefa6b778bb0c2e38cebe27f67accc9bcb15dda91dd8bdc` |
| `joi_letter/data/derived/joi_mechanism_grid.csv` | 318,813 | `f0ec2d50fc36a76bdeb27059f01b1771cf2a3134111f4eb6c1d33938a4477d69` |
| `joi_letter/data/derived/joi_reduction_readings.csv` | 504 | `13911d5cc5b46133e2e54d7bd234f0706378d4e1d3c79c95f8871562d1aad0fe` |
| `joi_letter/data/derived/joi_scenario_timeseries.csv` | 506,516 | `c6e5e80998d14785494d6a0750c6e611b9b5d18355221148545c2b016c5d8d64` |
| `joi_letter/data/derived/joi_seasonal_profile.csv` | 726 | `2d58f753f09534590836fc463007f9aeb71cfcf11cb263cff5774d10bff58ee1` |
| `joi_letter/data/derived/joi_validation_panel_data.csv` | 12,779 | `d48faebfa86f15a340eb0c32354b36d35e0cde966f1e8f763343b7f01baed9e7` |
| `joi_letter/data/derived/joi_validation_seasonal_profile.csv` | 1,741 | `09e32e9f8cb560a8a75ee01f296578eed49992db482914f01de63d4863115c16` |
| `joi_letter/data/derived/joi_validation_timeseries.csv` | 13,409 | `890b874141b4d2826ff42b19a2e81f63ec89e43ecb83d77635e21b015b3b3354` |
| `joi_letter/data/derived/ukhsa_coverage_annual.csv` | 126 | `cd2c5f0d8b9e8fc4be3c570b411989aec8df8ac4b770af4001081cccb04434cb` |
| `joi_letter/data/derived/ukhsa_coverage_icb_long.csv` | 77,889 | `e2ff2db753cf2d9822697b5f2e6fc40a3547e6b9c1b3d84577aabb6b19bb3f39` |
| `joi_letter/data/derived/ukhsa_coverage_national_monthly.csv` | 1,493 | `5fd5949df80fecdff52f6cca0b6890052ab228db1b9d934db897ca1b5c23e738` |
| `joi_letter/data/metadata/external_sources.md` | 1,199 | `8478648c5573c746395629c0141fa81d0b5005970356c8ee350c629bc0db1901` |
| `joi_letter/data/metadata/staged_input_manifest.json` | 3,339 | `7339c2b4d4814ffe7d6b673a287974ea48fefc081798814592a1ed65d63914c0` |
| `joi_letter/data/metadata/uk_scope_provenance.json` | 10,370 | `bc39cb1399cf9e3817ea9070bb9a6ce720948d05ce133e5f9b44c16b97c37371` |
| `joi_letter/data/metadata/validated_surveillance_source_manifest.csv` | 23,331 | `2b3e1c5399d4160b17a178035ef9099eea9dca6f43ba319ff9e55c1aabdd55e4` |
| `joi_letter/data/raw/README.md` | 3,051 | `c8eeeee364a1310f776f04e8cc413838b798441fe7a74938c78e90ad7da69d93` |
| `joi_letter/data/raw/country_profile_inputs.csv` | 9,219 | `e323c2c4f026e1229c168093893aa7f71fd8a66ac0686684c3e562ba2601ed0b` |
| `joi_letter/data/raw/england_infant_deaths.csv` | 8,320 | `89cc06459eee2f7ae9b9cc246e5b8fc7188bdaaf9afca804c0162ef3ea52a85e` |
| `joi_letter/data/raw/england_notifications_age.csv` | 103,299 | `a5738ff6acbae46784f5b040fe97e8dd265fc3daaa501e1e210752514b742dbb` |
| `joi_letter/data/raw/england_notifications_annual.csv` | 10,528 | `ef06ce166f6a5b03563d5f9207ce69dfff3f11cf9e25735ead79472c62eb4212` |
| `joi_letter/data/raw/england_population_model_age.csv` | 70,503 | `72d0356777e223c283efcf26557e5482e28b45ba3b3e210a2aab804b6b643c5d` |
| `joi_letter/data/raw/maternal_coverage_processed.csv` | 7,571 | `98be10681b2e9a22e819691e3199169f90c0abe848a950610263151b9fa44dcf` |
| `joi_letter/data/raw/uk_candidate_config.yaml` | 171,258 | `8dca16c6422a25a348257b113e89979a000ed465046b301586268f6dcd9d82e7` |
| `joi_letter/data/raw/uk_notifications.csv` | 334,319 | `bec6cfedb4a8058d4802f0204aeef8795c3bdf75aead8adaadd2ebc25c02a698` |
| `joi_letter/data/raw/ukhsa_prenatal_coverage_q1_2024.xlsx` | 55,875 | `d4851862de5fa418450c3946ddfd344332f1ec6109a50e172b08d7937f020438` |
| `joi_letter/data/raw/ukhsa_prenatal_coverage_q4_2026.xlsx` | 162,232 | `5278b6b42bbf37460b7530623a0c1be43f445f8f7bb60c7f4689ec87866d0380` |
| `joi_letter/outputs/figures/joi_maternal_coverage_impact_figure1.pdf` | 49,508 | `aaa1dfb5a59f80f077257b73c3955931f2214393726a3d39841da87e3f556470` |
| `joi_letter/outputs/figures/joi_maternal_coverage_impact_figure1.png` | 252,418 | `8a224b795e3b0e422acec1a0f3d830f0ada847393b4dbc26e195bf0073a07348` |
| `joi_letter/outputs/figures/joi_maternal_coverage_impact_figure2.pdf` | 50,419 | `c3e10d41584b43ae2011e0f537b525a960a4d7fc0f291c33a3375b87e9d3758a` |
| `joi_letter/outputs/figures/joi_maternal_coverage_impact_figure2.png` | 297,680 | `78cc6130ffe41221beca05b44922bbde12f7151b169278f5c780af2f1f7ed006` |
| `joi_letter/outputs/figures/joi_supplement_schematic.pdf` | 40,306 | `bb423258ef9cbdd4c7cf1028bc0d4ebe7d83839f76495c8e1d5d2efcc4ca82ea` |
| `joi_letter/outputs/figures/joi_supplement_schematic.png` | 901,922 | `4f6accf57bbd8a7eb52708e812e350c6ea14c5afb72d6f88484f64ef1bb2527b` |
| `joi_letter/outputs/figures/vector/joi_maternal_coverage_impact_figure1.svg` | 60,084 | `b20f29ee6c6ba68dc4a9893551134238c9d682b85b5f0c21cabfb5886863f18d` |
| `joi_letter/outputs/figures/vector/joi_maternal_coverage_impact_figure2.svg` | 51,779 | `956e75346a5c32d58f97f5a84b2423fd3f368f75b0ed612a8783cc47aa3d9ce8` |
| `joi_letter/outputs/figures/vector/joi_supplement_schematic.svg` | 64,493 | `ac0b8dbf2e566cebe6a907e9202bd0ab57718ed0f5ab795da413879838ea7dc0` |
| `joi_letter/outputs/model_runs/observed_baseline_legacy/metadata.json` | 1,708 | `865ee72dd8c3bc3dd137e44f6c96fc35ec8a07c05fcd9f48a7318b5d929df76e` |
| `joi_letter/outputs/model_runs/observed_baseline_legacy/summary.csv` | 22,024 | `f8d941c01693c318d7239d6cb07c0f36b3be691c20e6d6ee8e2d5d6adcba7d0b` |
| `joi_letter/outputs/model_runs/observed_baseline_walker/metadata.json` | 1,710 | `313faa2e3bc909d6c87e3436fb0f39c823cb4f9606a7c11740224843cf2819d5` |
| `joi_letter/outputs/model_runs/observed_baseline_walker/summary.csv` | 22,029 | `bf04dd0730b962abdfb1b2287cfd37edf502f67cda4112f5a270cc9458d2df9b` |
| `joi_letter/outputs/tables/ukhsa_coverage_monthly_summary.csv` | 1,137 | `ce9bdf6657901d6c81c11f4e852b2bab926799f1b47c681d8b4c5ca03854d37d` |
| `joi_letter/protocol/analysis_protocol.md` | 6,448 | `d31a27f92f1cd8b8cf990463d6ce7449fbc188ec917c038d2377e34470ab804d` |
| `joi_letter/references/joi_article.md` | 1,097 | `29b9e9ca6a61970147ffe7f73764c3eae72ef35a20a01e357c461f6d867baca3` |
| `joi_letter/reports/input_audit.json` | 63 | `1033ce1947cfce38d0a04a148a2279f5d8aa74b841f8037127e69e35ab234998` |
| `joi_letter/reports/protocol_validation.json` | 101 | `7642d9d6f3f3e6b5875282eb07c56ee513bea5f3f6eb38dfcd2f51d0d7ba2434` |
| `joi_letter/reports/scenario_runner_status.json` | 96 | `6ed7e0a9f132a50ac03e13ae0a50ea5faf6f0e464704dd6cf4b2561baf6a16d4` |
| `joi_letter/reports/validation_report.md` | 1,930 | `a0aba5bb1cadd338c7cc0a69869d8b2655b2ca003652502c744a90bc231a9159` |
| `joi_letter/reports/value_assessment.md` | 9,097 | `9d9e2673e0d130a580974dd8358b7e18e74930ccee90b22476896b1312a2ef39` |
| `joi_letter/scripts/00_stage_inputs.py` | 2,279 | `b290d7af3bd7a1e1e9b6facbf91050c4a767048fcac5c0abd7e7914cb8fa78a7` |
| `joi_letter/scripts/01_audit_inputs.py` | 1,027 | `83c99def18b38f6faeab9e52eceaa5b0e62087effe681465842d93268b58bdc3` |
| `joi_letter/scripts/02_run_scenarios.py` | 1,012 | `5958fd9c5c11f58fa8945040c8f4a73e743eeba24e31f58ec26f496f4a7769c9` |
| `joi_letter/scripts/03_build_letter_outputs.py` | 403 | `a1ac506c0fc156243d614e52b33c405d87e43cf354d1cec0fc7e9f6722256a3b` |
| `joi_letter/scripts/04_extract_ukhsa_coverage.py` | 3,186 | `3415cc8e0f99e7a00a9e9704b01cb3b970dedc16001e365baf5e2568887042f0` |
| `joi_letter/scripts/05_word_count.py` | 615 | `68bac16000e1f3d32cae577c56bbdf7dfc9b8e779adcd908ee13170272caa7bd` |
| `joi_letter/scripts/06_run_model_scenarios.py` | 5,848 | `96abc02ff2d1f7690b5934b5b8153c3069986db3bd395938c6a77ef03bda5f74` |
| `joi_letter/scripts/07_assess_results.py` | 2,820 | `8d6f42d2e58834c522125d37d828047a47f51832dbe3e4515fa15304c9e14de5` |
| `joi_letter/scripts/08_run_recovered_candidate.py` | 6,667 | `15ef4f5dd8bcc7f3171c9de2038ed7e7e745e8aa4cf5b1b9f7d22468d83a9c42` |
| `joi_letter/scripts/09_make_figure_ggplot.R` | 25,087 | `5dc54a6d78ea46e84495d581e4a5b025d379a54c5fc289bf4e8dd22e9bd5e910` |
| `joi_letter/scripts/10_prepare_infant_under3_summary.py` | 3,599 | `8af19e36212c808800590aa0a7b8afc643cf5adf240d1086798a4f8b62755aae` |
| `joi_letter/scripts/11_make_two_figures_ggplot.R` | 518 | `56b781e7fda0c391ff9c3ddae4b1894922455c33a732e5847eba94f9058f8d2d` |
| `joi_letter/scripts/12_prepare_figure_ledgers.py` | 5,903 | `d99171967f6ca3a90bdea368f9ed14d782b9dcaa631148c993dcc3b92d6280db` |
| `joi_letter/scripts/13_run_recovered_candidate_walker.py` | 8,107 | `8bb2a2590b0880e4ffd7493762ecd0159824e27f064aed57d58bf4b0584e2aca` |
| `joi_letter/scripts/14_audit_coverage_and_factorial.py` | 4,228 | `e6af11bb737d6bffc2f30e93b56e5ab7013b302f7443680978c8f94c43116b3e` |
| `joi_letter/scripts/15_reforecast_structural_validation.py` | 5,942 | `a93da737ef57f45f1fdc740d5fd2ff01714ae08bfcf1b5e787920bd5028b0f84` |
| `joi_letter/scripts/16_run_observed_baseline.py` | 11,780 | `b44d8dee5950ede1e36dc6d12b11ec5898001b38ab6380d47cd13473c7f04180` |
| `joi_letter/scripts/17_make_supplement_schematic.py` | 12,801 | `793111f12de61aa63958a8402c37a8e28230360d167b8c99af59ee523d9ee961` |
| `joi_letter/scripts/figure_style.R` | 4,472 | `79a6e13fe33d68c171f2caf936e81df41deb060094e69fcca51bff3e783e2c8f` |
| `joi_letter/scripts/uk_structural_seasonality.py` | 2,191 | `a4e34282a3da45292f701b84e5dac8e18ff9f0683f2b4f6a80cbb2cd7050c358` |
| `requirements.txt` | 470 | `0ae71688697b1046f65fb448e417353aaf71bcb19c3bf59deafe93fb43d47899` |
