# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
"""Regression test (no pytest needed): python tests/test_regression.py  (exit 0 = pass).
Runs validation check D and asserts the deterministic key numbers."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validation"))
import check_D_regression as D
import check_A_logistic_terms as A

def main():
    r = D.run(); bad = [x for x in r["results"] if not x["pass"]]
    for x in bad: print("FAIL", x)
    a = A.run()
    if a["max_abs_extremum_diff_K"] > 0.01:
        print("FAIL: A1=A2=0 shifted an extremum by", a["max_abs_extremum_diff_K"]); bad.append(a)
    # legacy check: results of the 2026-10-01 verification (found in the project files) must be reproduced exactly
    import json
    root = Path(__file__).resolve().parent.parent
    old = json.load(open(root / "data" / "legacy_2026-10-01_verification_results.json"))
    new = json.load(open(root / "results" / "verification_results.json"))
    def flat(o, p=""):
        if isinstance(o, dict):
            for k, v in o.items(): yield from flat(v, p + k + ".")
        elif isinstance(o, list):
            for i, v in enumerate(o): yield from flat(v, p + str(i) + ".")
        else: yield p, o
    N = dict(flat(new)); worst = max(abs(v - N[k]) / max(abs(v), 1e-300) for k, v in flat(old))
    print("legacy 2026-10-01 results vs committed results: max relative diff %.2e" % worst)
    if worst > 1e-9: bad.append("legacy mismatch")
    print("regression: %d/%d passed" % (r["n_pass"], r["n"]))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
