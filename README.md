# water-two-state-core

Verification code for the extended two-state (LDL/HDL) free-energy landscape
model of liquid water's thermodynamic anomalies, accompanying:

> Hazime Sendo (independent researcher), *Four Anomaly Lines of Water Across
> 0–100 MPa from a Phenomenological Two-State Model* (manuscript in preparation;
> an earlier title appears in v1.1.1; the final title and journal are not yet decided). ORCID: 0009-0007-3285-0308.

Every number quoted in the manuscript is computed by the script here from the
model definition — nothing is copied from the manuscript by hand.

## Research-history disclosure (please read)

- The **original optimization scripts and logs for the ten fitted parameters were not found.** The optimization itself
  therefore cannot be reproduced; the reported numbers **can** be reproduced from the final parameter values in
  `src/model_final.py`.
- A 2026-10-01 manuscript records a joint optimization against the IAPWS-95 density-maximum line **and** the three
  literature reference temperatures, while other passages of the same manuscript say those points were not used. This is
  unresolved. The three literature values are therefore **not** presented as independent validation.
- The Mishima (2010) value (223 K, 50 MPa) is an **assumed liquid–liquid critical-point location**, not a measured Widom
  maximum. The Kim et al. (2017) value (229 K) is an apparent κT maximum inferred from the structure factor. The
  comparison with the model's max|∂x/∂T| is a loose consistency check between quantities of different definition.
- A 2026-10 supplementary text describes a four-stage procedure (documented, not verified as code); an attempt to reconstruct its objective did **not** reproduce the final parameters. The path that produced the final parameters therefore remains unestablished. Details and evidence: `docs/PROVENANCE.md` (Sections A2, B2).

## What the model reproduced / what it does not (yet) guarantee

**Reproduced (computed here):** the temperature of maximum density (RMS 0.636 K
vs IAPWS-95 over 0–100 MPa); the structural-fluctuation (|dx/dT|) maximum at three
literature points; and the temperatures of four anomaly lines (TMD, κT maximum,
Cp maximum, sound-speed minimum) at 0.1–100 MPa.

**Not guaranteed:** (i) full thermodynamic consistency derived from a single free
energy — the pure-structure volumes and heat capacities are specified separately
from ΔG and are not constrained to match its derivatives (`validation/check_C_consistency.py`);
(ii) absolute accuracy of all properties at high pressure (κT is only 0.01–0.1× the
IAPWS-95 value at 100 MPa; κS turns negative near 100 MPa at high T); (iii) that the
literature Widom points are independent of parameter selection — see `docs/PROVENANCE.md`.

## Layout

| Path | Contents |
|---|---|
| `src/model_final.py` | The model: ΔG(T,P), two-state fraction x(T,P), pure-structure specific volumes (cm³/g), and derived ρ, κT, Cp, κS, sound speed. ΔG and the pure-structure volume/heat-capacity functions are specified separately (see below). |
| `src/verify_model.py` | Verification script (seven checks, below). |
| `CITATION.cff`, `RELEASE_CHECKLIST.md` | Citation metadata; steps to be done by the author before any push/tag/release. |
| `data/literature_anchors.json` | The three literature Widom-line comparison points (Kim 2017; Holten & Anisimov 2012; Mishima 2010) with references. |
| `data/legacy_2026-10-01_verification_results.json` | Verification results of 2026-10-01 found in the project files; `tests/test_regression.py` requires exact agreement. |
| `scripts/run_verification.sh` | Regenerates `results/verification_results.json` and `results/verification_stdout.txt`. |
| `scripts/make_figure1.py` | Regenerates Figure 1 (vector PDF, 600-dpi PNG) and `figure1_data.csv` into `results/figures/` (needs matplotlib). |
| `scripts/check_reproducibility.py` | Re-runs everything from scratch, compares to the committed JSON, writes `results/reproducibility_log.txt`. |
| `validation/` | Independent checks A–E, recomputed from the model functions (they do not read `results/`): A logistic terms, B expansion-coefficient signs, C thermodynamic consistency, D regression (58 items), E stability/scope scan. |
| `tests/` | Regression test (`python tests/test_regression.py`). |
| `docs/` | `PROVENANCE.md` (research history), `SCOPE.md`, `VALIDATION.md`. |
| `results/` | Committed outputs of the most recent run. |
| `requirements.txt` | Pinned dependencies (numpy, scipy, iapws). |
| `LICENSE` | Apache License 2.0. |

IAPWS-95 reference values are generated on the fly with the `iapws` package;
no reference data file is needed.

## Run it

### Quick start (no programming experience needed)

1. Install Python 3.11 or newer from <https://www.python.org/downloads/> (the checks were run in clean virtual environments with Python 3.11.18 and 3.13.18; other versions have not been tested).
2. Download this folder and open a terminal in it (macOS/Linux: *Terminal*; Windows: *PowerShell*), e.g. `cd path/to/this/folder`.
3. Create an isolated environment and install the libraries:
   - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`
   - Windows PowerShell: `py -m venv .venv` then `.venv\Scripts\Activate.ps1`
   - then (all systems): `pip install -r requirements.txt`
4. Run the checks (about 10 s each):
   - `python src/verify_model.py --out-dir results` — prints the full report (Windows-friendly; the `.sh` wrapper does the same on macOS/Linux)
   - `python validation/run_all.py` — independent checks A–E; ends with `OVERALL: PASS (regression)`
   - `python tests/test_regression.py` — ends with `regression: 58/58 passed`
   - `python scripts/check_reproducibility.py` — ends with `RESULT: REPRODUCED`
5. Figure 1 (optional): `pip install matplotlib==3.11.2`, then `python scripts/make_figure1.py`. The figure is computed directly from the model functions (0.1, 1, 2, …, 100 MPa; extrema from a 0.05 K grid scan plus parabolic refinement), not traced from any image. It writes `results/figures/figure1_anomaly_lines.pdf` (vector), `.png` (600 dpi) and `figure1_data.csv`, and prints `Table 5 check: max |recomputed - printed| = 0.038 K` (the manuscript prints 0.1 K precision).

Expected key numbers: TMD RMS 0.636 K; maximum difference from the three literature reference temperatures 0.358 K;
density RMS 1.227 %; Cp RMS 7.971 % (absolute, vs IAPWS-95); 20 anomaly-line extrema as in `results/verification_stdout.txt`.
A `UserWarning: Using extrapolated values` from `iapws` is harmless.

### Command summary

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./scripts/run_verification.sh              # prints the full report, updates results/
python scripts/check_reproducibility.py    # exit code 0 = all numbers reproduced
```

`python src/verify_model.py --out-dir <dir>` writes the JSON elsewhere. A
harmless `UserWarning: Using extrapolated values` from `iapws` appears for
supercooled states; it is suppressed in the shell wrapper.

## What is checked

1. **TMD(P) vs IAPWS-95**, 0–100 MPa — RMS **0.636 K**.
2. **Widom-line anchors** (max of |dx/dT|) vs three literature estimates (not claimed to be independent of parameter selection; see `docs/PROVENANCE.md`) — max deviation **0.36 K** (quote as "within 0.4 K").
3. **Stability (limited grid)** — κT > 0 on 187 grid points (220–300 K, 0–100 MPa); Cp > 0 on 231 points (200–300 K); no negative values.
4. **Four anomaly lines** (TMD, κT peak, Cp peak, sound-speed minimum) at 0.1, 25, 50, 75, 100 MPa.
5. **Absolute magnitudes** of ρ and Cp vs IAPWS-95 — density RMS **1.23 %**, Cp RMS **7.97 %**. Note `rho()` is in g/cm³; multiply by 1000 for kg/m³.
6. **κS boundary ("anomaly death line")** — κS stays positive up to 97.5 MPa (min 1.5×10⁻⁷) and turns negative at 100 MPa for T ≳ 278 K, about 25 K above the model's density maximum at that pressure (252.7 K). This is a boundary of the model, not a property of water.
7. **κT absolute magnitude vs IAPWS-95** (added in v1.1.0) — the model κT is 0.8–0.9× the reference at 0.1 MPa, 0.4–0.5× at 50 MPa, and only 0.01–0.1× at 100 MPa.

The printed numbers are authoritative: if a manuscript draft disagrees, the draft is wrong.

## About the reproducibility check

`check_reproducibility.py` verifies that the code is deterministic and that
the committed `results/` match a fresh run in your environment (tolerance
1e-9 relative). It does not independently validate the physics; the
comparison against IAPWS-95 and the literature anchors in the report does.

## Known limitations

- `Cp_LDL(T)`, `Cp_HDL(T)` and the fluctuation amplitude are placeholder values chosen for the qualitative shape of the Cp anomaly, not fitted to IAPWS-95 absolute Cp (≈8 % RMS disagreement).
- Sound speed is in model-internal units; no absolute m/s comparison is made.
- `kappa_T_HDL`'s linear coefficient is negative. This makes the model κT too small at high pressure (check 7) and is the origin of the κS boundary in check 6. The transferable results are the predicted anomaly temperatures, not κT or κS magnitudes at high pressure.
- The Holten & Anisimov (2012) *Sci. Rep.* value (≈227 K, 13 MPa) must not be confused with Holten, Bertrand, Anisimov & Sengers, *Thermodynamics of supercooled water* (arXiv:1111.5587), which reports different critical-point estimates.
- Individual fitted parameters are only partly identifiable; the transferable results are the predicted anomaly temperatures.

## Citation

See `CITATION.cff`. Please cite the paper above (once published) and the Zenodo archive of this repository.

## License

Apache License 2.0 — see `LICENSE`. Copyright 2026 Hazime Sendo.
