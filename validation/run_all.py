# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
"""Run checks A-E, write results/validation/*.json and validation_log.txt. Exit 1 if check D fails."""
import sys, io, contextlib, datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_A_logistic_terms as A, check_B_expansion_sign as B, check_C_consistency as C, check_D_regression as D, check_E_scope as E
from common import environment, save, OUT

def main():
    log = ["water-two-state-core validation log", "UTC: %s" % datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), "env: %s" % environment(), ""]
    ok = True
    for name, mod in (("A", A), ("B", B), ("C", C), ("D", D), ("E", E)):
        r = mod.run(); save("check_%s.json" % name, r)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            pass
        if name == "A": log.append("A: max |extremum shift| A1=A2=0: %.4f K; DeltaV max abs diff %.3e cm3/mol (rel %.1e); DeltaG max abs diff %.3e J/mol" % (r["max_abs_extremum_diff_K"], r["deltaV_cm3_per_mol"]["max_abs_diff"], r["deltaV_cm3_per_mol"]["max_rel_diff"], r["deltaG_J_per_mol"]["max_abs_diff"]))
        if name == "B":
            for k, v in r["variants"].items(): log.append("B: %-13s TMD(0.1MPa)=%.2f K RMS=%.3f K" % (k, v["TMD_K"][0], v["RMS_vs_IAPWS95_K"]))
        if name == "C": a = r["dGdP_vs_M_dV"]; log.append("C: dG/dP %.2f..%.2f vs M(VL-VH) %.2f..%.2f cm3/mol; |ratio| %.1f..%.1f; dCp0 ratio %.1f..%.1f; %s" % (*a["dGdP_range"], *a["MdV_range"], a["ratio_min"], a["ratio_max"], *r["dCp"]["ratio_range"], r["verdict"]))
        if name == "D":
            log.append("D: %d/%d regression items passed" % (r["n_pass"], r["n"])); ok = r["n_pass"] == r["n"]
            log += ["D: FAIL %s" % x for x in r["results"] if not x["pass"]]
        if name == "E": log.append("E: %d pts; kT<=0 %d; Cp<=0 %d; kS<=0 %d (P %s, T %s)" % (r["n_points"], r["n_kT_nonpositive"], r["n_Cp_nonpositive"], r["n_kS_nonpositive"], r["kS_nonpositive_P_range_MPa"], r["kS_nonpositive_T_range_K"]))
    log.append("OVERALL: " + ("PASS (regression)" if ok else "FAIL"))
    (OUT / "validation_log.txt").write_text("\n".join(log) + "\n"); print("\n".join(log)); return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
