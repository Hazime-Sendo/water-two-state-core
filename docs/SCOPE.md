# Scope of applicability

1. **What is computed:** temperatures of the density maximum, kappa_T maximum, Cp maximum and sound-speed
   minimum at 0.1-100 MPa, plus the |dx/dT| (structural-fluctuation) maximum.
2. **What is *not* established:** a thermodynamically stable, self-consistent equation of state at all
   temperatures in 0-100 MPa. Reasons: (a) DeltaG and the pure-structure volumes/heat capacities are
   specified separately and are not mutually consistent (validation/check_C_consistency.py:
   (dG/dP)_T is 9-34x M(V_LDL-V_HDL); dCp0 is ~29-43x the pure-structure Cp difference);
   (b) kappa_S <= 0 occurs at P = 100 MPa for T >= 278 K (23 of 9061 scanned points);
   (c) kappa_T at 100 MPa is only 0.01-0.1x the IAPWS-95 value.
3. Positivity of kappa_T and Cp on the scanned grid (T 180-400 K, P 0-100 MPa) is a necessary check only,
   not proof of stability or of thermodynamic consistency.
