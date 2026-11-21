# Release checklist (to be done by the author — nothing here has been executed)

Status of this folder: **prepared for review; not pushed, not tagged, not released, not archived.**

## A. Before pushing (author decisions)
- [ ] Final paper title and journal are decided; update the README title line (currently notes the title is not final).
- [x] Research-history additions (PROVENANCE A2, B2) approved by the author on 2026-11-20 (wording to be re-read before release).
- [ ] Approve the final research-history wording in `README.md` ("Research-history disclosure") and `docs/PROVENANCE.md`.
- [ ] Decide whether to relabel Mishima/Kim entries in `data/literature_anchors.json` (already done in this folder:
      Mishima = assumed critical-point location; Kim = apparent κT maximum; Holten & Anisimov = candidate critical point).
- [ ] Decide the version number (this folder is the v1.1.2 candidate; `CITATION.cff` still refers to the published v1.1.1).
- [x] `reconstruction_attempt/` (failed reconstruction) is kept OUTSIDE this repository on purpose; decide whether it should ever be published.
- [ ] If the original optimization scripts/logs are found, add them under `docs/` or `scripts/` and revise `docs/PROVENANCE.md`.

## B. Checks already run on this folder (Python 3.13.18; see `results/`)
- [x] `python src/verify_model.py --out-dir results` — TMD RMS 0.6359 K; max literature difference 0.3579 K; density RMS 1.227 %; Cp RMS 7.971 %.
- [x] `python validation/run_all.py` — checks A–E.
- [x] `python tests/test_regression.py` — 58/58 items; exact agreement (relative difference 0) with the 2026-10-01 results.
- [x] `python scripts/check_reproducibility.py` — numbers reproduced (tolerance 1e-9 relative).
- [x] `python scripts/make_figure1.py` — Figure 1 computed directly from the model (1 MPa grid): vector PDF, 600-dpi PNG, data CSV; Table 5 check max difference 0.038 K.
- [x] Re-run in clean virtual environments with Python 3.11.18 and 3.13.18 (all checks identical; figure CSV identical).
- [ ] Re-run from a fresh `git clone` after push (not possible before push).

## C. Push / tag / release (only after approval)
1. `git add -A && git commit -m "v1.1.2: validation scripts, provenance documentation, figure script"` in a local clone of the repository.
2. `git push origin main`; then create tag `v1.1.2` and a GitHub release (this triggers a Zenodo archive if the integration is enabled).
3. Do not overwrite or delete v1.1.1.

## D. After release (update everywhere)
- [ ] `CITATION.cff`: `version` and `doi`.
- [ ] Manuscript: Data availability / reference [dataset] entry (version, DOI), and mention `scripts/make_figure1.py` if desired.
- [ ] Cover letter: repository sentence.
