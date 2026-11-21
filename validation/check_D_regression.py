# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
"""Check D: regression of existing results. Expected values are the manuscript/report
numbers (hard-coded below, from the sixth-version manuscript). Model values are recomputed
here from model functions; the committed results/verification_results.json is read ONLY
for the final cross-comparison (labelled)."""
import json
import numpy as np
from common import *

EXPECT = {
  "params": dict(dH0=-6731.97, dS0=-33.2262, dCp0=600.521, DV0=23.3507, aL=-1.06576e-4, aH=3.14402e-4,
                 kT_LDL=7.53251e-4, kT2_LDL=1.20121e-6, kT_HDL=-8.27783e-5, kT2_HDL=1.99779e-7,
                 A1=7.8542e-7, A2=1.1821e-6, P1=38.4215, P2=118.5630),
  "TMD_RMS_K": 0.636,
  "widom_model_K": {0.1: 228.96, 13.0: 227.36, 50.0: 222.82},
  "lines": {"TMD": [275.9, 271.6, 266.2, 259.8, 252.7], "kT_peak": [224.4, 219.9, 215.4, 211.0, 206.4],
            "Cp_peak": [228.2, 225.1, 222.1, 219.1, 216.2], "c_min": [206.7, 204.1, 201.5, 198.8, 196.0]},
}
TOL = {"params": 0.0, "TMD_RMS_K": 0.005, "widom_K": 0.03, "line_K": 0.06, "json_K": 0.1}

def run(with_iapws=True):
    m = load_model(); res = []; chk = lambda n, ok, a, b: res.append({"item": n, "pass": bool(ok), "recomputed": a, "expected": b})
    for k, v in EXPECT["params"].items():
        chk("param " + k, getattr(m, k) == v, float(getattr(m, k)), v)
    if with_iapws:
        T = np.array([tmd(m, P) for P in PRESSURES_TMD]); ref = np.array([iapws_tmd(P) for P in PRESSURES_TMD])
        rms = float(np.sqrt(np.mean((T - ref) ** 2)))
        chk("TMD RMS (11 P, vs IAPWS-95)", abs(rms - EXPECT["TMD_RMS_K"]) <= TOL["TMD_RMS_K"], rms, EXPECT["TMD_RMS_K"])
    for P, e in EXPECT["widom_model_K"].items():
        w = widom_T(m, P); chk("Widom model value %.1f MPa" % P, abs(w - e) <= TOL["widom_K"], w, e)
    fns = {"TMD": tmd, "kT_peak": kT_peak, "Cp_peak": cp_peak, "c_min": c_min}; got = {}
    for n, fn in fns.items():
        for P, e in zip(PRESSURES_FIVE, EXPECT["lines"][n]):
            v = fn(m, P); got[(n, P)] = v
            chk("%s @ %.1f MPa" % (n, P), abs(v - e) <= TOL["line_K"], v, e)
    # labelled cross-comparison with the committed result table (the only read of results/)
    fl = json.load(open(ROOT / "results" / "verification_results.json"))["four_lines"]
    for row in fl:
        P = row[0]
        for n, v in zip(("TMD", "kT_peak", "Cp_peak", "c_min"), row[1:5]):
            chk("committed table %s @ %.1f" % (n, P), abs(got[(n, P)] - v) <= TOL["json_K"], got[(n, P)], v)
    return {"tolerances": TOL, "n": len(res), "n_pass": sum(r["pass"] for r in res), "results": res,
            "figure_data_note": "figure1_anomaly_lines.png is a raster image; its plotted curves are the same four-line quantities checked above (no separate numeric figure table exists)."}

if __name__ == "__main__":
    r = run(); save("check_D.json", r)
    for x in r["results"]:
        if not x["pass"]: print("D: FAIL", x)
    print("D: %d/%d regression items passed" % (r["n_pass"], r["n"]))
