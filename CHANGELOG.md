# Changelog

## v1.1.2-candidate (unreleased, local only)
- Docs/comments only: README title, "specific volumes (cm^3/g)", model-construction note, "reproduced / not guaranteed" section; removed "independent"/"out-of-sample" wording for the Widom points; code comments in `model_final.py` and `verify_model.py` corrected (AST of executable code unchanged; only string literals/comments differ).
- 2026-11-20: `docs/PROVENANCE.md` extended (A2: four-stage procedure recorded in the 2026-10 supplementary text; B2: failed reconstruction of its objective, J = 4.94 at the final parameters vs 0.30-0.42 for free minimization); README research-history paragraph; Figure 1 now computed on a 1 MPa grid with an automatic Table 5 check. No model, parameter or numerical result changed.
- Added `validation/` (checks A-E), `tests/test_regression.py`, `docs/` (PROVENANCE, SCOPE, VALIDATION), `results/validation/`.
- Research history: documented the 2026-10-01 manuscript/code/results (joint-optimization statement, internal contradiction); added `data/legacy_2026-10-01_verification_results.json` and an exact-agreement test.
- `verify_model.py` text: "a few percent for Cp" replaced by the measured values (about 1.2 % density, 8.0 % Cp).
- Model equations, parameters and `results/verification_results.json` unchanged (bit-identical on rerun).

## v1.1.1 (2026-11-14)
- Wording only: removed the references to a "submission agent" from the docstring and printed text of `src/verify_model.py` and from `results/verification_stdout.txt`.
- No change to the model or to any numerical result (reproducibility check: 97 values matched).

## v1.1.0 (2026-10-07)
- Added check 7: absolute κT vs IAPWS-95 (`results/verification_results.json`, key `kappaT_abs`).
- README: clarified that the κS boundary is a model boundary (about 25 K above the model density maximum at 100 MPa) and documented the κT limitation.
- No change to the model (`src/model_final.py`) or to any v1.0.0 result.

## v1.0.0 (2026-10-06)
- Initial release: model, verification script (checks 1-6), literature anchors, reproducibility check.
