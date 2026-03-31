# Source: Simulation/chapter-10/codebook.md -- Block 2

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# ====================================================================
# 1. Integration Core (RK4 Solver)
# ====================================================================

# Reusing hh_derivatives, steady_state_value, V_REST, etc., from Project 1

def rk4_step(func, S, I_ext, dt):
    """Performs one RK4 time step for the state vector S = [V, m, h, n]."""
    k1 = func(S, I_ext)
    k2 = func(S + 0.5 * dt * k1, I_ext)
    k3 = func(S + 0.5 * dt * k2, I_ext)
    k4 = func(S + dt * k3, I_ext)
    return S + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

def run_hh_simulation(I_ext_pulse, t_final, dt, S_init):
    """Runs a full HH simulation for a given constant stimulus I_ext_pulse."""
    steps = int(t_final / dt)
    S = S_init.copy()
    Vm_history = np.zeros(steps)
    
    for i in range(steps):
        # The current is only applied for the first 1 ms
        I_current = I_ext_pulse if i * dt <= 1.0 else 0.0
        
        S = rk4_step(hh_derivatives, S, I_current, dt)
        Vm_history[i] = S[0]
        
    return np.max(Vm_history)

# ====================================================================
# 2. Threshold Sweep Simulation
# ====================================================================

# Initial Conditions (from Project 1)
V0 = -65.0 
m0 = steady_state_value(alpha_m(V0), beta_m(V0))
h0 = steady_state_value(alpha_h(V0), beta_h(V0))
n0 = steady_state_value(alpha_n(V0), beta_n(V0))
S_INIT = np.array([V0, m0, h0, n0])

# --- Simulation Parameters ---
DT = 0.01      # ms
T_FINAL = 10.0 # ms (long enough for the spike to finish)

# Current range to test
I_EXT_MIN = 5.0
I_EXT_MAX = 8.0
I_EXT_STEP = 0.2
I_ext_values = np.arange(I_EXT_MIN, I_EXT_MAX + I_EXT_STEP, I_EXT_STEP)

# Storage
Vmax_history = []

print(f"Testing threshold current range from {I_EXT_MIN} to {I_EXT_MAX} \u03bcA/cm\u00b2...")

for I_ext in I_ext_values:
    V_max = run_hh_simulation(I_ext, T_FINAL, DT, S_INIT)
    Vmax_history.append(V_max)

# ====================================================================
# 3. Visualization and Analysis
# ====================================================================

plt.figure(figsize=(8, 5))

# Plot Vmax vs. Iext
plt.plot(I_ext_values, Vmax_history, 'o-', color='darkred', lw=2)

# Labeling and Formatting
plt.title('All-or-Nothing Response: Threshold Current $I_{\\text{crit}}$')
plt.xlabel('Stimulus Current $I_{\\text{ext}}$ ($\mu\\text{A/cm}^2$)')
plt.ylabel('Maximum Voltage Reached $V_{\\max}$ (mV)')
plt.grid(True, which='both', linestyle=':')

# Annotate the threshold jump point (approximate)
threshold_index = np.argmax(np.diff(Vmax_history))
I_crit_approx = I_ext_values[threshold_index] + I_EXT_STEP / 2
plt.axvline(I_crit_approx, color='red', linestyle='--', label=f'$I_{{crit}} \\approx {I_crit_approx:.1f}$')
plt.legend()

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- Threshold Analysis Summary ---")
print(f"Calculated Critical Current (Approx): {I_crit_approx:.2f} \u03bcA/cm\u00b2")
print("\nConclusion: The plot demonstrates the all-or-nothing response: below the critical threshold current, the maximum voltage remains near the resting potential. Once the threshold is crossed, the maximum voltage immediately jumps to the full spike amplitude, confirming the non-linear, regenerative nature of the action potential.")
