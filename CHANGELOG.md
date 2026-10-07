# Changelog

## v1.1.0 (2026-10-07)
- Added check 7: absolute κT vs IAPWS-95 (`results/verification_results.json`, key `kappaT_abs`).
- README: clarified that the κS boundary is a model boundary (about 25 K above the model density maximum at 100 MPa) and documented the κT limitation.
- No change to the model (`src/model_final.py`) or to any v1.0.0 result.

## v1.0.0 (2026-10-06)
- Initial release: model, verification script (checks 1-6), literature anchors, reproducibility check.
