# Source: Simulation/chapter-10/codebook.md -- Block 1

import numpy as np
import random
from math import exp, log, sqrt

# ====================================================================
# 1. System Constants (Squid Giant Axon)
# ====================================================================

# Membrane parameters
CM = 1.0  # Membrane capacitance (uF/cm^2)

# Maximum conductances (mS/cm^2)
GNA_BAR = 120.0  # Sodium
GK_BAR = 36.0    # Potassium
GL = 0.3         # Leak

# Reversal potentials (mV)
ENA = 50.0  # Sodium
EK = -77.0  # Potassium
EL = -54.4  # Leak

V_REST = -65.0  # Approximate resting potential (mV)

# ====================================================================
# 2. Voltage-Dependent Rate Constants (alpha_x and beta_x)
# ====================================================================

def alpha_m(V):
    """Na+ activation rate constant."""
    return 0.1 * (25 - V) / (np.exp((25 - V) / 10) - 1)

def beta_m(V):
    """Na+ deactivation rate constant."""
    return 4 * np.exp(-V / 18)

def alpha_h(V):
    """Na+ inactivation rate constant."""
    return 0.07 * np.exp(-V / 20)

def beta_h(V):
    """Na+ deinactivation rate constant."""
    return 1 / (np.exp((30 - V) / 10) + 1)

def alpha_n(V):
    """K+ activation rate constant."""
    # Special handling for V=10 to avoid division by zero (L'Hopital's rule)
    if V == 10.0:
        return 0.1  # lim_{V->10} alpha_n(V) = 0.1
    return 0.01 * (10 - V) / (np.exp((10 - V) / 10) - 1)

def beta_n(V):
    """K+ deactivation rate constant."""
    return 0.125 * np.exp(-V / 80)

# ====================================================================
# 3. Full HH Derivative Function (The ODE System)
# ====================================================================

def hh_derivatives(S, I_ext):
    """
    Calculates the time derivatives (dV/dt, dm/dt, dh/dt, dn/dt)
    for the state vector S = [V, m, h, n].
    """
    V, m, h, n = S

    # Calculate voltage-dependent currents
    INa = GNA_BAR * m**3 * h * (V - ENA)
    IK = GK_BAR * n**4 * (V - EK)
    IL = GL * (V - EL)

    # Voltage derivative (Current Balance Equation)
    dVdt = (I_ext - (INa + IK + IL)) / CM

    # Gating variable derivatives (Kinetic ODEs)
    dmdt = alpha_m(V) * (1 - m) - beta_m(V) * m
    dhdt = alpha_h(V) * (1 - h) - beta_h(V) * h
    dndt = alpha_n(V) * (1 - n) - beta_n(V) * n

    return np.array([dVdt, dmdt, dhdt, dndt])

# ====================================================================
# 4. Compute Steady-State Initial Conditions (x_0)
# ====================================================================

def steady_state_value(alpha, beta):
    """Computes x_infinity = alpha / (alpha + beta)."""
    return alpha / (alpha + beta)

# Compute initial resting values at V_REST = -65.0 mV
m0 = steady_state_value(alpha_m(V_REST), beta_m(V_REST))
h0 = steady_state_value(alpha_h(V_REST), beta_h(V_REST))
n0 = steady_state_value(alpha_n(V_REST), beta_n(V_REST))

# Initial State Vector
S0_REST = np.array([V_REST, m0, h0, n0])

print("--- Hodgkin–Huxley Initial State Setup ---")
print(f"Resting Potential V_REST: {V_REST:.2f} mV")
print(f"Initial State m0 (Na Act): {m0:.4f}")
print(f"Initial State h0 (Na Inact): {h0:.4f}")
print(f"Initial State n0 (K Act): {n0:.4f}")
print(f"Initial State Vector S0: {S0_REST}")
