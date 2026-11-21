# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
"""Regenerate Figure 1 (four anomaly lines vs pressure) as vector PDF + 600-dpi PNG + CSV of the plotted data.

All curves are computed directly from src/model_final.py (no image digitizing, no reading of any earlier figure)
on the pressure grid 0.1, 1, 2, ..., 100 MPa (101 points). Extrema are located with the validation/common.py
finders: grid scan with 0.05 K step followed by 3-point parabolic refinement; search windows: TMD 235-300 K,
kappa_T max 185-260 K, Cp max 185-260 K, sound-speed minimum (max of rho*kappa_S) 180-260 K. The script also compares
the 20 extrema of manuscript Table 5 (0.1 K precision) with the recomputed values and prints the maximum difference. The three markers are literature reference temperatures (Table 4 of the manuscript): they are
comparison values, not independent validation data, and the Mishima point is an assumed critical-point location.
Requires matplotlib (optional dependency; not needed for the validation checks).
Usage: python scripts/make_figure1.py [output_dir]   (default: results/figures)
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "validation"))
import numpy as np
from common import load_model, tmd, kT_peak, cp_peak, c_min

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42   # embed TrueType fonts
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "DejaVu Sans"
import matplotlib.pyplot as plt


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    m = load_model()
    P = np.array([0.1] + list(range(1, 101)), dtype=float)
    cur = {"TMD": [tmd(m, p) for p in P], "kT": [kT_peak(m, p) for p in P],
           "Cp": [cp_peak(m, p) for p in P], "c": [c_min(m, p) for p in P]}
    with open(out / "figure1_data.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["P_MPa", "TMD_K", "kappaT_max_K", "Cp_max_K", "sound_speed_min_K"])
        for i, p in enumerate(P):
            w.writerow([p] + ["%.3f" % cur[k][i] for k in ("TMD", "kT", "Cp", "c")])
    # Table 5 of the manuscript (printed to 0.1 K): P -> (TMD, kappa_T max, Cp max, sound-speed min)
    table5 = {0.1: (275.9, 224.4, 228.2, 206.7), 25: (271.6, 219.9, 225.1, 204.1), 50: (266.2, 215.4, 222.1, 201.5),
              75: (259.8, 211.0, 219.1, 198.8), 100: (252.7, 206.4, 216.2, 196.0)}
    worst = 0.0
    for pp, vals in table5.items():
        i = int(np.argmin(abs(P - pp)))
        for k, v in zip(("TMD", "kT", "Cp", "c"), vals):
            worst = max(worst, abs(cur[k][i] - v))
    print("Table 5 check: max |recomputed - printed| = %.3f K over 20 extrema (printed precision 0.1 K -> expect <= 0.05)" % worst)
    assert worst <= 0.05 + 1e-9, "Table 5 mismatch"
    fig, ax = plt.subplots(figsize=(6.0, 5.2))
    ax.plot(P, cur["TMD"], color="#6a1b9a", ls="-", lw=1.8, label="Density maximum (TMD)")
    ax.plot(P, cur["kT"], color="#1f77b4", ls="--", lw=1.8, label=r"$\kappa_T$ maximum")
    ax.plot(P, cur["Cp"], color="#d62728", ls="-.", lw=1.8, label=r"$C_p$ maximum")
    ax.plot(P, cur["c"], color="#2ca02c", ls=":", lw=2.2, label="Sound-speed minimum")
    ax.plot([0.1], [229.0], "o", color="k", ms=6, ls="none", label="Kim et al. (2017), apparent max.")
    ax.plot([13], [227.0], "s", color="k", ms=6, ls="none", label="Holten & Anisimov (2012), candidate CP")
    ax.plot([50], [223.0], "^", mfc="white", mec="k", mew=1.4, ms=7, ls="none", label="Mishima (2010), assumed CP")
    ax.set_xlabel("Pressure (MPa)", fontsize=11)
    ax.set_ylabel("Temperature (K)", fontsize=11)
    ax.set_xlim(-3, 103)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(out / "figure1_anomaly_lines.pdf")
    fig.savefig(out / "figure1_anomaly_lines.png", dpi=600)
    print("wrote", out)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "results" / "figures")
