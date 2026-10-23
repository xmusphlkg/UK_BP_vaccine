.PHONY: stage audit coverage under3 figure dry-run
stage:
	python3 scripts/00_stage_inputs.py
audit:
	python3 scripts/01_audit_inputs.py
coverage:
	python3 scripts/04_extract_ukhsa_coverage.py
under3:
	python3 scripts/10_prepare_infant_under3_summary.py
figure: under3
	Rscript scripts/09_make_figure_ggplot.R
dry-run:
	python3 scripts/02_run_scenarios.py --dry-run
