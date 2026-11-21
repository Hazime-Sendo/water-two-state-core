# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
"""Check E: scope of applicability. Distinguishes (1) extremum temperatures obtainable
over 0-100 MPa from (2) a thermodynamically stable EOS at all temperatures: scans
kappa_T, Cp, kappa_S positivity on T 180-400 K, P 0-100 MPa (2.5 MPa step)."""
import numpy as np
from common import *

def run():
    m = load_model(); Ts = np.arange(180.0, 400.0 + 1e-9, 1.0); Ps = np.arange(0.0, 100.0 + 1e-9, 2.5)
    T, P = np.meshgrid(Ts, Ps)
    kT, cp, kS = m.kappa_T(T, P), m.Cp(T, P), m.kappa_S(T, P)
    neg = kS <= 0
    return {"grid": "T 180-400 K step 1; P 0-100 MPa step 2.5", "n_points": int(T.size),
            "n_kT_nonpositive": int(np.sum(kT <= 0)), "n_Cp_nonpositive": int(np.sum(cp <= 0)),
            "n_kS_nonpositive": int(neg.sum()),
            "kS_nonpositive_P_range_MPa": [float(P[neg].min()), float(P[neg].max())] if neg.any() else None,
            "kS_nonpositive_T_range_K": [float(T[neg].min()), float(T[neg].max())] if neg.any() else None,
            "kS_min_positive_for_P_le_97.5": float(kS[Ps <= 97.5].min()),
            "interpretation": "Positivity of kT and Cp on this grid is a necessary-condition scan, not a proof of a stable "
                              "thermodynamically consistent EOS (see check C). kS<=0 occurs only near 100 MPa at high T."}

if __name__ == "__main__":
    r = run(); save("check_E.json", r)
    print("E: points %d | kT<=0: %d | Cp<=0: %d | kS<=0: %d (P %s, T %s)" % (r["n_points"], r["n_kT_nonpositive"], r["n_Cp_nonpositive"],
          r["n_kS_nonpositive"], r["kS_nonpositive_P_range_MPa"], r["kS_nonpositive_T_range_K"]))
