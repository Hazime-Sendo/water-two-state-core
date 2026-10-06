# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
#
# Extended two-state (LDL/HDL) free-energy landscape model of liquid water's
# density, isothermal compressibility, isobaric heat capacity, and sound
# speed anomalies across 0-100 MPa. See the accompanying manuscript and
# verify_model.py for the physical model definition, parameter provenance,
# and numerical verification against IAPWS-95 and independent literature
# estimates of the structural-fluctuation (Widom-line) maximum.

import numpy as np

R = 8.314
Tref = 273.15
T0 = 273.15

A1, A2, P1, P2 = 7.8542e-07, 1.1821e-06, 38.4215, 118.5630
w1, w2 = 20.0, 40.0
Vm_LDL0 = 1.0/0.930
Vm_HDL0 = 1.0/1.054

# Final stability-constrained joint-fit parameters (established earlier in this project)
dH0, dS0, dCp0, DV0 = -6731.97, -33.2262, 600.521, 23.3507
aL, aH = -1.06576e-04, 3.14402e-04
kT_LDL, kT2_LDL = 7.53251e-04, 1.20121e-06
kT_HDL, kT2_HDL = -8.27783e-05, 1.99779e-07

def deltaV(P):
    f1 = 1/(1+np.exp((P-P1)/w1)); f2 = 1/(1+np.exp((P-P2)/w2))
    return DV0 - A1*f1 - A2*f2

def deltaG(T, P):
    dH = dH0 + dCp0*(T-Tref)
    dS = dS0 + dCp0*np.log(T/Tref)
    return dH - T*dS + P*deltaV(P)

def x_fraction(T, P):
    dG = deltaG(T, P)
    return 1/(1+np.exp(np.clip(dG/(R*T), -700, 700)))

def Vm_LDL(T,P): return Vm_LDL0*(1+aL*(T-T0))*(1-kT_LDL*P+kT2_LDL*P**2)
def Vm_HDL(T,P): return Vm_HDL0*(1+aH*(T-T0))*(1-kT_HDL*P+kT2_HDL*P**2)

def rho(T,P):
    x = x_fraction(T,P)
    return 1/(x*Vm_LDL(T,P)+(1-x)*Vm_HDL(T,P))

def Cp_LDL(T): return 5.0 + 0.01*(T-273.15)
def Cp_HDL(T): return 4.0 + 0.005*(T-273.15)
dH_LDL_val, dH_HDL_val = -200.0, -100.0

def Cp(T,P):
    x = x_fraction(T,P)
    Cp_mix = x*Cp_LDL(T) + (1-x)*Cp_HDL(T)
    eps=1e-2
    dx_dT = (x_fraction(T+eps,P)-x_fraction(T-eps,P))/(2*eps)
    return Cp_mix + (dH_LDL_val-dH_HDL_val)*dx_dT

def kappa_T(T,P):
    eps=1e-2
    V = lambda PP: 1/rho(T,PP)
    return -((V(P+eps)-V(P-eps))/(2*eps))/V(P)

def alpha(T,P):
    eps=1e-2
    V = lambda TT: 1/rho(TT,P)
    return (V(T+eps)-V(T-eps))/(2*eps)/V(T)

def kappa_S(T,P):
    kT=kappa_T(T,P); Cpv=Cp(T,P); a=alpha(T,P); rv=rho(T,P)
    return kT - T*a**2/(rv*Cpv)

def sound_speed(T,P):
    rv=rho(T,P); kS=kappa_S(T,P)
    return 1/np.sqrt(rv*kS) if kS>0 else np.nan

if __name__ == "__main__":
    print("module loaded OK")
