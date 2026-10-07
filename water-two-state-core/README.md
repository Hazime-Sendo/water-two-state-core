# water-two-state-core

Verification code for the extended two-state (LDL/HDL) free-energy landscape
model of liquid water's thermodynamic anomalies, accompanying:

> Hazime Sendo (independent researcher), *Thermodynamic Determination of
> Water's Anomalies Across 0–100 MPa via a Two-State Free Energy Landscape*,
> submitted to *The Journal of Chemical Physics*. ORCID: 0009-0007-3285-0308.

Every number quoted in the manuscript is computed by the script here from the
model definition — nothing is copied from the manuscript by hand.

## Layout

| Path | Contents |
|---|---|
| `src/model_final.py` | The model: ΔG(T,P), two-state fraction x(T,P), molar volumes, and derived ρ, κT, Cp, κS, sound speed. |
| `src/verify_model.py` | Verification script (seven checks, below). |
| `data/literature_anchors.json` | The three independent literature Widom-line anchors (Kim 2017; Holten & Anisimov 2012; Mishima 2010) with references. |
| `scripts/run_verification.sh` | Regenerates `results/verification_results.json` and `results/verification_stdout.txt`. |
| `scripts/check_reproducibility.py` | Re-runs everything from scratch, compares to the committed JSON, writes `results/reproducibility_log.txt`. |
| `results/` | Committed outputs of the most recent run. |
| `requirements.txt` | Pinned dependencies (numpy, scipy, iapws). |
| `LICENSE` | Apache License 2.0. |

IAPWS-95 reference values are generated on the fly with the `iapws` package;
no reference data file is needed.

## Run it

Python 3.11 or newer.

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
2. **Widom-line anchors** (max of |dx/dT|) vs three out-of-sample literature estimates — max deviation **0.36 K** (quote as "within 0.4 K").
3. **Stability** — κT > 0 on 187 grid points (220–300 K, 0–100 MPa); Cp > 0 on 231 points (200–300 K); no negative values.
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
- The Holten & Anisimov (2012) *Sci. Rep.* anchor (≈227 K, 13 MPa) must not be confused with Holten, Bertrand, Anisimov & Sengers, *J. Chem. Phys.* (2014; arXiv:1111.5587), which reports different critical-point estimates.
- Individual fitted parameters are only partly identifiable; the transferable results are the predicted anomaly temperatures.

## Citation

Please cite the paper above and, once released, the Zenodo archive of this repository.

## License

Apache License 2.0 — see `LICENSE`. Copyright 2026 Hazime Sendo.
