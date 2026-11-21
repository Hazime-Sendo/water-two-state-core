# Validation scripts (v1.1.2-candidate)

Run: `python validation/run_all.py` (about 3 s; writes `results/validation/*.json` and `validation_log.txt`),
`python tests/test_regression.py` (exit 0 = pass).

| Check | Question | Result in this environment |
|---|---|---|
| A | Do the logistic terms (A1, A2) matter? | No: A1=A2=0 shifts no extremum (0.0000 K on a 0.05 K grid); DeltaV changes < 2e-6 cm^3/mol |
| B | Sign of aL, aH | Flipping or zeroing either degrades TMD RMS from 0.64 K to 2.6-35 K: signs are required |
| C | Thermodynamic consistency | NOT consistent: ratios 9-34 (volume), 29-43 (Cp) |
| D | Regression | 58/58 items agree (parameters, TMD RMS, 3 Widom values, 20 extrema, committed table) |
| E | Scope scan | kT, Cp > 0 everywhere scanned; kS <= 0 only at 100 MPa, T >= 278 K |

Check E (scope scan) is included in `run_all.py`. Figure 1 is generated directly from the model functions by `scripts/make_figure1.py` (1 MPa grid; extrema by 0.05 K
grid scan + parabolic refinement; search windows in `validation/common.py`). It reproduces the 20 extrema of manuscript
Table 5 to within 0.038 K (printing precision 0.1 K). As a one-time historical cross-check, an earlier raster version of
the figure had been compared by digitizing (max 0.23 K, pixel precision); the present figure does not use that image.

Environment: Python 3.13.18, numpy 2.4.4, scipy 1.17.1, iapws 1.5.5; no randomness.
Tolerances (check D): TMD RMS 0.005 K; Widom 0.03 K; extrema 0.06 K (expected values are quoted to 0.1 K);
committed table 0.1 K; parameters exact. Extremum finder: 0.05 K grid + parabolic refinement (does not
reuse `verify_model.py` helpers).
Limits: check D compares with numbers hard-coded from the manuscript and, in one clearly labelled step,
with `results/verification_results.json`; the figure PNG is not compared numerically.
