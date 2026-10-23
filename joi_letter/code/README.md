# Code boundary

The production transmission model remains in the parent repository and is not copied or modified by this project. Local scripts will call it through explicit read-only paths or, where needed, use a frozen copy created by `scripts/00_stage_inputs.py`.

Any local model adapter must:

- expose the exact maternal VE and coverage parameters;
- write a machine-readable configuration and hash;
- emit a scenario-level result table;
- fail if the `<3 months` endpoint is not exactly represented; and
- distinguish smoke-test, diagnostic, and publication outputs.
