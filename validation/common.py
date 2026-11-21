# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
"""Shared helpers for the v1.1.2-candidate independent validation scripts.

Design rules: (1) everything is recomputed from the functions in src/model_final.py;
(2) no result table in results/ is read (except in the explicit regression comparison
of check D, which is labelled as such); (3) no randomness; (4) no fitting/optimisation
of model parameters -- only evaluation and 1-D extremum location on a fixed grid.
"""
import importlib.util
import json
import platform
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "model_final.py"
OUT = ROOT / "results" / "validation"
M_H2O = 18.015  # g/mol, used only to convert specific volume (cm^3/g) to molar (cm^3/mol)
PRESSURES_FIVE = [0.1, 25.0, 50.0, 75.0, 100.0]
PRESSURES_TMD = [0.101325] + [10.0 * k for k in range(1, 11)]


def load_model(**overrides):
    """Load a fresh, private copy of src/model_final.py and override module constants.
    Functions look up module globals at call time, so overrides take effect."""
    spec = importlib.util.spec_from_file_location("model_copy_%d" % id(overrides), SRC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for k, v in overrides.items():
        if not hasattr(m, k):
            raise AttributeError(k)
        setattr(m, k, v)
    return m


def refine_extremum(f, lo, hi, step=0.05, mode="max"):
    """Grid scan (step K) + 3-point parabolic refinement. Vectorised f(T) -> array."""
    T = np.arange(lo, hi + step / 2, step)
    v = np.asarray(f(T), dtype=float)
    v = np.where(np.isfinite(v), v, -np.inf if mode == "max" else np.inf)
    i = int(np.argmax(v) if mode == "max" else np.argmin(v))
    if 0 < i < len(T) - 1:
        y0, y1, y2 = v[i - 1], v[i], v[i + 1]
        den = y0 - 2 * y1 + y2
        if den != 0 and np.isfinite(den):
            return float(T[i] + 0.5 * step * (y0 - y2) / den)
    return float(T[i])


def tmd(m, P):
    return refine_extremum(lambda T: m.rho(T, P), 235.0, 300.0, 0.05, "max")


def kT_peak(m, P):
    return refine_extremum(lambda T: m.kappa_T(T, P), 185.0, 260.0, 0.05, "max")


def cp_peak(m, P):
    return refine_extremum(lambda T: m.Cp(T, P), 185.0, 260.0, 0.05, "max")


def c_min(m, P):
    # c = 1/sqrt(rho*kS): minimum c <=> maximum rho*kS (kS>0 there)
    return refine_extremum(lambda T: m.rho(T, P) * m.kappa_S(T, P), 180.0, 260.0, 0.05, "max")


def widom_T(m, P):
    T = np.arange(200.0, 250.0, 0.01)
    d = np.abs(np.gradient(m.x_fraction(T, P), T))
    return refine_extremum(lambda t: np.interp(t, T, d), 200.5, 249.5, 0.01, "max")


def iapws_tmd(P):
    from iapws import IAPWS95
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda T: -IAPWS95(T=T, P=P).rho, bounds=(240, 285),
                        method="bounded", options={"xatol": 1e-6})
    return float(r.x)


def environment():
    import numpy, scipy
    env = {"python": platform.python_version(), "platform": platform.platform(),
           "numpy": numpy.__version__, "scipy": scipy.__version__,
           "randomness": "none (deterministic grid evaluation)"}
    try:
        import iapws
        env["iapws"] = iapws.__version__ if hasattr(iapws, "__version__") else "installed"
    except Exception:
        env["iapws"] = "not installed"
    return env


def save(name, obj):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, indent=2, default=float))
