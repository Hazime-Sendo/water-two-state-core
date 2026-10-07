# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
"""Re-run the verification from scratch and compare against the committed
results/verification_results.json. Writes results/reproducibility_log.txt.

Usage:  python3 scripts/check_reproducibility.py
Exit code 0 = every number reproduced within tolerance; 1 = mismatch.
"""
import datetime
import json
import platform
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMITTED = ROOT / "results" / "verification_results.json"
LOG = ROOT / "results" / "reproducibility_log.txt"
RTOL = 1e-9  # deterministic code; allow only floating-point noise


def flatten(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, f"{prefix}{k}.")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f"{prefix}{i}.")
    else:
        yield prefix.rstrip("."), obj


def main():
    lines = []
    say = lambda s="": (lines.append(s), print(s))
    say("Reproducibility log -- water-two-state-core")
    say(f"Date (UTC) : {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S}")
    say(f"Python     : {platform.python_version()} on {platform.system()} {platform.machine()}")
    for pkg in ("numpy", "scipy", "iapws"):
        say(f"{pkg:<11}: {version(pkg)}")
    say()
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, str(ROOT / "src" / "verify_model.py"), "--out-dir", tmp],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        fresh = json.load(open(Path(tmp) / "verification_results.json"))
    ref = json.load(open(COMMITTED))
    f_fresh, f_ref = dict(flatten(fresh)), dict(flatten(ref))
    bad = 0
    for key in sorted(set(f_fresh) | set(f_ref)):
        a, b = f_fresh.get(key), f_ref.get(key)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            ok = abs(a - b) <= RTOL * max(1.0, abs(b))
        else:
            ok = a == b
        bad += not ok
        if not ok:
            say(f"MISMATCH {key}: fresh={a} committed={b}")
    say(f"Compared {len(f_ref)} values; mismatches: {bad}")
    say(f"tmd_rms_K            = {fresh['tmd_rms_K']:.3f} K")
    say(f"widom_max_abs_diff_K = {fresh['widom_max_abs_diff_K']:.2f} K")
    say("RESULT: " + ("REPRODUCED" if bad == 0 else "NOT REPRODUCED"))
    LOG.write_text("\n".join(lines) + "\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
