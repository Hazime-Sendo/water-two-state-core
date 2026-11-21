# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
"""Check A: effect of the two logistic terms in DeltaV(P) (A1, A2).
Compares current parameters with A1 = A2 = 0: extremum temperatures of the four
anomaly lines, DeltaV(P), and DeltaG(T,P). Evaluation only; no refit."""
import numpy as np
from common import *

def run():
    base, zero = load_model(), load_model(A1=0.0, A2=0.0)
    out = {"extrema_K": {}, "grid_step_K": 0.05}
    for name, fn in (("TMD", tmd), ("kT_peak", kT_peak), ("Cp_peak", cp_peak), ("c_min", c_min)):
        rows = []
        for P in PRESSURES_FIVE:
            a, b = fn(base, P), fn(zero, P)
            rows.append({"P_MPa": P, "current": a, "A1=A2=0": b, "diff_K": b - a})
        out["extrema_K"][name] = rows
    out["max_abs_extremum_diff_K"] = max(abs(r["diff_K"]) for v in out["extrema_K"].values() for r in v)
    P = np.linspace(0, 100, 101)
    dv0, dv = zero.deltaV(P), base.deltaV(P)
    out["deltaV_cm3_per_mol"] = {"DV0": float(base.DV0), "max_abs_diff": float(np.max(np.abs(dv0 - dv))),
                                 "max_rel_diff": float(np.max(np.abs(dv0 - dv) / dv0)),
                                 "value_at_0": float(dv[0]), "value_at_100": float(dv[-1])}
    T, PP = np.meshgrid(np.linspace(230, 300, 71), np.linspace(0, 100, 101))
    dG = base.deltaG(T, PP) - zero.deltaG(T, PP)
    out["deltaG_J_per_mol"] = {"max_abs_diff": float(np.max(np.abs(dG))),
                               "max_rel_diff": float(np.max(np.abs(dG) / np.abs(base.deltaG(T, PP)).clip(1e-12)))}
    return out

if __name__ == "__main__":
    r = run(); save("check_A.json", r)
    print("A: max |extremum shift| with A1=A2=0 : %.4f K (grid 0.05 K)" % r["max_abs_extremum_diff_K"])
    d = r["deltaV_cm3_per_mol"]; print("A: DeltaV(P) max abs diff %.3e cm3/mol (rel %.2e); DeltaG max abs diff %.3e J/mol" %
          (d["max_abs_diff"], d["max_rel_diff"], r["deltaG_J_per_mol"]["max_abs_diff"]))
