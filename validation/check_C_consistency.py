# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
"""Check C: thermodynamic consistency between DeltaG and the separately specified
pure-structure volumes / heat capacities.
 (1) (dG/dP)_T [J mol^-1 MPa^-1 = cm^3/mol] vs M (V_LDL - V_HDL)  [V in cm^3/g]
 (2) dCp0 [J mol^-1 K^-1] vs M (Cp_LDL - Cp_HDL) [model Cp units treated as J g^-1 K^-1]
 (3) DeltaH(T) vs M (H_LDL - H_HDL) with the model's constant -100 [internal units]
A thermodynamically self-consistent two-state model would give ratios of ~1.
Evaluation only."""
import numpy as np
from common import *

def run():
    m = load_model()
    T, P = np.meshgrid(np.linspace(230, 300, 71), np.linspace(0, 100, 101))
    h = 1e-3
    dGdP = (m.deltaG(T, P + h) - m.deltaG(T, P - h)) / (2 * h)
    MdV = M_H2O * (m.Vm_LDL(T, P) - m.Vm_HDL(T, P))
    diff, ratio = dGdP - MdV, dGdP / MdV
    out = {"dGdP_vs_M_dV": {
        "dGdP_range": [float(dGdP.min()), float(dGdP.max())],
        "MdV_range": [float(MdV.min()), float(MdV.max())],
        "diff_range": [float(diff.min()), float(diff.max())],
        "ratio_min": float(np.min(np.abs(ratio))), "ratio_max": float(np.max(np.abs(ratio))),
        "ratio_median": float(np.median(np.abs(ratio))), "sign_agreement_fraction": float(np.mean(np.sign(dGdP) == np.sign(MdV))),
        "note": "units cm^3/mol; V_LDL-V_HDL is negative (LDL larger volume => MdV>0 means V_LDL>V_HDL)"}}
    Ts = np.linspace(230, 300, 8)
    dCp_pure = M_H2O * (m.Cp_LDL(Ts) - m.Cp_HDL(Ts))
    out["dCp"] = {"dCp0_J_per_mol_K": float(m.dCp0), "M*(Cp_LDL-Cp_HDL)_at_T": dict(zip(map(str, Ts.round(1)), dCp_pure.tolist())),
                  "ratio_range": [float(m.dCp0 / dCp_pure.max()), float(m.dCp0 / dCp_pure.min())]}
    dH_per_g = (m.dH0 + m.dCp0 * (Ts - m.Tref)) / M_H2O
    out["dH"] = {"deltaH_over_M_at_T": dict(zip(map(str, Ts.round(1)), dH_per_g.tolist())),
                 "model_H_LDL_minus_H_HDL": float(m.dH_LDL_val - m.dH_HDL_val),
                 "ratio_abs": dict(zip(map(str, Ts.round(1)), np.abs(dH_per_g / (m.dH_LDL_val - m.dH_HDL_val)).tolist()))}
    out["verdict"] = "NOT self-consistent (phenomenological model)" if out["dGdP_vs_M_dV"]["ratio_min"] > 2 else "check ratios"
    return out

if __name__ == "__main__":
    r = run(); save("check_C.json", r); a = r["dGdP_vs_M_dV"]
    print("C: dG/dP range %.2f..%.2f cm3/mol ; M(VL-VH) %.2f..%.2f ; |ratio| %.1f..%.1f (median %.1f)" %
          (*a["dGdP_range"], *a["MdV_range"], a["ratio_min"], a["ratio_max"], a["ratio_median"]))
    print("C: dCp0 = %.1f J/mol/K; ratio to M(Cp_LDL-Cp_HDL): %.1f..%.1f" % (r["dCp"]["dCp0_J_per_mol_K"], *r["dCp"]["ratio_range"]))
    print("C: verdict:", r["verdict"])
