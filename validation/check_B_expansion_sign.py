# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
"""Check B: sign of the pure-structure thermal-expansion coefficients aL, aH.
Lists TMD(P) for the current values and for sign-changed values (evaluation only)."""
import numpy as np
from common import *

VARIANTS = {"current": {}, "aL->-aL": {"aL": "neg"}, "aH->-aH": {"aH": "neg"},
            "both flipped": {"aL": "neg", "aH": "neg"}, "aL=aH=0": {"aL": 0.0, "aH": 0.0}}

def run(with_iapws=True):
    ref = np.array([iapws_tmd(P) for P in PRESSURES_TMD]) if with_iapws else None
    base = load_model()
    out = {"aL": float(base.aL), "aH": float(base.aH), "pressures_MPa": PRESSURES_TMD, "variants": {}}
    for name, spec in VARIANTS.items():
        ov = {k: (-getattr(base, k) if v == "neg" else v) for k, v in spec.items()}
        m = load_model(**ov)
        T = np.array([tmd(m, P) for P in PRESSURES_TMD])
        d = {"values": {k: float(getattr(m, k)) for k in ("aL", "aH")}, "TMD_K": T.tolist()}
        if ref is not None:
            d["RMS_vs_IAPWS95_K"] = float(np.sqrt(np.mean((T - ref) ** 2)))
        out["variants"][name] = d
    if ref is not None:
        out["IAPWS95_TMD_K"] = ref.tolist()
    return out

if __name__ == "__main__":
    r = run(); save("check_B.json", r)
    for k, v in r["variants"].items():
        print("B: %-13s aL=%+.3e aH=%+.3e  TMD(0.1MPa)=%.2f K  RMS=%.3f K" %
              (k, v["values"]["aL"], v["values"]["aH"], v["TMD_K"][0], v.get("RMS_vs_IAPWS95_K", float('nan'))))
