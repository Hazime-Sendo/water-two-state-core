# Parameter provenance and research history (v1.1.2 final candidate)

Updated 2026-11-20: Sections A2 (supplementary-information record) and B2 (reconstruction attempt) added; no model, parameter or result changed.

This file separates (A) facts confirmed directly from project documents, (B) facts confirmed by calculation,
and (C) matters that cannot be established. Nothing in C is stated as fact elsewhere in this repository.

## A. Confirmed from documents
- The 2026-10-01 manuscript (10 pages), Sec. 3.3, states that the ten free parameters (dH0, dS0, dCp0, DV0, aL, aH,
  kT_LDL, kT2_LDL, kT_HDL, kT2_HDL) were obtained by a derivative-free (Nelder-Mead) **joint optimization against two
  targets**: the IAPWS-95 density-maximum line at 11 pressures (0.1-100 MPa) and the three literature
  structural-fluctuation points of `data/literature_anchors.json`, with a penalty for kappa_T < 0.
- The same manuscript's Abstract, Results, Discussion and Conclusion say that these three points were *not used in
  the fit* and that agreement is an "out-of-sample test". **The 2026-10-01 manuscript is internally contradictory.**
- `src/model_final.py` (identical, byte for byte, to the 2026-10 model file found in the project) carries the comment
  "Final stability-constrained joint-fit parameters (established earlier in this project)".
- The ten parameters were optimized with A1, A2, P1, P2 held fixed. The same four values appear in an earlier draft
  script in which DV0 = 2.4e-6 (a different scale; the logistic terms were not negligible there).

## A2. Procedure recorded in the 2026-10 supplementary information, Sec. S2 (a document record, not verified code)
Added 2026-11-20. The following is what the author's supplementary text of that period *says*. It was not found as
code, and no implementation of it has been confirmed; it is reproduced here only as a record.

| Stage | Recorded content |
|---|---|
| 1 | Sign correction of aL, aH (both initially negative; no density maximum) to positive values. |
| 2 | aL, aH, kT_LDL, kT2_LDL, kT_HDL, kT2_HDL fitted by `scipy.optimize.curve_fit` (trust-region reflective) to the IAPWS-95 density-maximum line at 11 pressures; dH0, dS0 fixed at -3759.33 J/mol and -14.9274 J/(mol K) from an earlier, separate density fit (see the note after the table). |
| 3 | dCp0 scanned by bisection (`brentq`) so that the max |dx/dT| falls at 229 K at 0.1 MPa; then DV0 scanned on a logarithmic grid (0.1-80) to match the 13 and 50 MPa literature points as well. |
| 4 | All ten parameters re-optimized jointly by Nelder-Mead (`scipy.optimize.minimize`, adaptive, maxiter = maxfev = 30000). Objective: sum of squared deviations over the 11 density-line points + 3 literature points weighted 3x + penalty sum(min(kappaT,0)^2) x 1e8 on a 17 x 11 grid (T 220-300 K, P 0-100 MPa). Gradient-based optimization was reported to stall because the objective is piecewise constant. Bounds listed for the bounded stage were not enforced in Stage 4 (the final aL and kT_HDL are outside them). |

The same text reports five randomized restarts (+/-50 %) that gave similar residuals but widely different values of aL,
aH and the kT_HDL / kT2_HDL pair (partial non-identifiability).
Consequences: (i) the three literature points are documented there as *part of the objective* (Stage 3 even fixes dCp0 by
the 229 K point), which is consistent with, and stronger than, the "not independent validation" wording used in this
repository; (ii) the Stage-2 values of dH0 and dS0 belong to the earlier, simpler model of 2026-09 (not the final model).

## B2. Reconstruction attempt of the Stage-4 objective (2026-11-20) -- not successful
An independent investigation record is kept **outside this repository** (`reconstruction_attempt/`, script, JSON results);
it is not part of the released code and must not be taken as the original optimization.
- Reconstructed objective J = sum_11 (TMD_model - TMD_IAPWS)^2 + 3 x sum_3 (T_Widom,model - T_lit)^2 + 1e8 x sum(min(kappaT,0)^2),
  with the repository's own conventions for the undocumented details: TMD and max|dx/dT| located by the 0.05 K / 0.01 K
  scan + parabolic refinement of `validation/common.py`; IAPWS-95 TMD at 0.101325, 10, 20, ..., 100 MPa; 17 x 11 kappaT grid.
- **At the final parameters: J = 4.9375** (TMD term 4.4475, i.e. RMS 0.636 K; literature term 0.4900 incl. the 3x weight;
  penalty 0).
- Nelder-Mead (adaptive, variables scaled by |final value|, maxfev = 30000, six runs: one from the final parameters and
  five from seeded random starts within +/-50 %, seed 20261120): all runs reached **J = 0.30-0.42** (best 0.299), with
  parameters far from the final ones (maximum relative change between 3.7 and 148; e.g. dCp0 = 2254 J/(mol K), above the
  documented bound of 2000). A shorter 3000-evaluation test gave J = 0.34-0.45.
- Several conditions had to be supplied by this investigation because the source text does not give them (grids, extremum search, the units/scaling of the penalty, the treatment of the three TMD/Widom sub-searches, variable scaling, stopping tolerances); a different choice could change the numbers.
- Preliminary 3000-evaluation test (same setup): J = 0.34-0.45.
- Therefore the final parameters are **not a minimum of the reconstructed objective**, and the objective is strongly
  degenerate. The generation path of the final parameters (objective details, weights, stopping point, possible
  early termination or a different configuration) remains **unestablished, and the optimization could not be
  reproduced**. This does **not** show that the procedure recorded in 2026-10 was wrong: the reconstruction may differ from the original objective in undocumented details, and the original run may have been stopped, restarted or configured differently. It also does not affect the reported numbers, which are reproduced from the final parameter values.

## B. Confirmed by calculation (validation/, tests/)
- The current model reproduces the 2026-10-01 verification results exactly (max relative difference 0): TMD RMS
  0.6358631752997514 K; Widom max |diff| 0.35793817673561534 K; density RMS 1.2271517 %; Cp RMS 7.9710044 %;
  the four-line table (see `data/legacy_2026-10-01_verification_results.json`).
- With A1 = A2 = 0 no extremum moves (0.0000 K on a 0.05 K grid); the logistic terms are numerically inert.
- Evaluation-only sensitivity (no refit): +/-1 % changes of dCp0 move TMD RMS and the Widom errors in opposite
  directions, consistent with (but not proof of) both targets having shaped the parameters.

## C. Not established
- The actual objective function, weights, penalty form and search history *as implemented* (Sec. A2 gives only the
  text record, and B2 shows that the recorded objective does not reproduce the final parameters). **The original
  optimization scripts and logs are not available.**
- How A1, A2, P1, P2 were originally determined.
- Whether the model was ever optimized against the density line alone (Sec. A2 records a density-only Stage 2 for six
  parameters, but this is not verified).

## Consequence
The three literature points are **not** treated as independent validation data. They are mutually independent
sources, but they are not known to be independent of the model's development. The agreement with them (max 0.36 K)
is reported as simultaneous consistency with the density-maximum line. The optimization itself cannot be
reproduced; the reported numbers can be reproduced from the final parameter values.

## Literature reference check: Mishima (2010) 223 K / 50 MPa (checked 2026-11-19)
Checked against the author-hosted PDF of J. Chem. Phys. 133, 144503 (2010), as read by an automated text extraction
(page footers could not be read reliably, so page numbers are approximate). The value is an **assumed / roughly
suggested liquid-liquid critical-point location, not a measured value and not a Widom-line or kappa_T-maximum
location**: Abstract ("when the critical point is assumed to exist at ~50 MPa and ~223 K"), Sec. V "Location of LLCP"
(p. ~144503-5/6) and Sec. VI Conclusion ("roughly suggested to locate at ~50 MPa and ~223 K"). No numerical uncertainty
is given; Fig. 1 caption states that the theoretical line changes by 10 K and 20 MPa for the illustrated parameters.
Comparing the model's max|dx/dT| with this value is therefore a loose consistency comparison. The label
"compressibility extrapolation" in data/literature_anchors.json is imprecise (the paper uses volume data and a modified
Fuentevilla-Anisimov scaling equation); the author decides whether to relabel.
