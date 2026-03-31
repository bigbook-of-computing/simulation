# Source: Simulation/chapter-10/codebook.md -- Block 3

import numpy as np
import matplotlib.pyplot as plt

# ====================================================================
# 1. Full HH Simulation Run (Spiking Parameters)
# ====================================================================

# --- Simulation Setup ---
DT = 0.01  # ms
T_TOTAL = 50.0  # ms
I_EXT_MAG = 10.0 # Suprathreshold current
STIM_START, STIM_END = 10.0, 11.0 # 1 ms pulse

# I_ext function (Stimulus pulse)
def I_ext(t):
    return I_EXT_MAG if STIM_START <= t <= STIM_END else 0.0

# Initial State (from Project 2)
V0 = -65.0
m0 = steady_state_value(alpha_m(V0), beta_m(V0))
h0 = steady_state_value(alpha_h(V0), beta_h(V0))
n0 = steady_state_value(alpha_n(V0), beta_n(V0))
S_INIT = np.array([V0, m0, h0, n0])

# State storage setup
steps = int(T_TOTAL / DT)
time = np.arange(0, T_TOTAL, DT)
Vm, m, h, n = np.zeros(steps), np.zeros(steps), np.zeros(steps), np.zeros(steps)
Vm[0], m[0], h[0], n[0] = S_INIT

S = S_INIT.copy()
for i in range(1, steps):
    S = rk4_step(hh_derivatives, S, I_ext(time[i-1]), DT)
    Vm[i], m[i], h[i], n[i] = S

# ====================================================================
# 2. Current Calculation (Post-Simulation)
# ====================================================================

# Calculate Conductances and Currents from the state traces
GNA = GNA_BAR * m**3 * h
GK = GK_BAR * n**4

INa = GNA * (Vm - ENA)
IK = GK * (Vm - EK)
IL = GL * (Vm - EL)

# ====================================================================
# 3. Visualization
# ====================================================================

fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot 1: Voltage Trace
ax[0].plot(time, Vm, color='darkred', lw=2)
ax[0].set_title('Hodgkin–Huxley Voltage Trace ($V_m$)')
ax[0].set_ylabel('Voltage ($V_m$, mV)')
ax[0].grid(True)
ax[0].axvline(STIM_START, color='gray', linestyle=':', label='$I_{\\text{ext}}$ pulse')

# Plot 2: Ionic Currents
ax[1].plot(time, INa, label='$I_{\\text{Na}}$ (Inward)', color='dodgerblue', lw=2)
ax[1].plot(time, IK, label='$I_{\\text{K}}$ (Outward)', color='orange', lw=2)
ax[1].plot(time, IL, label='$I_L$ (Leak)', color='gray', lw=1, linestyle='--')
ax[1].axhline(0, color='k', linestyle='-')

ax[1].set_title('Ionic Currents During the Action Potential')
ax[1].set_xlabel('Time (ms)')
ax[1].set_ylabel('Current Density ($\mu\\text{A/cm}^2$)')
ax[1].set_ylim(-300, 100) # Set fixed axis for clarity
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
max_INa = np.min(INa)
max_IK = np.max(IK)
INa_peak_time = time[np.argmin(INa)]
IK_peak_time = time[np.argmax(IK)]

print("\n--- Ionic Current Dynamics Analysis ---")
print(f"I_Na Peak (Inward): {max_INa:.2f} \u03bcA/cm\u00b2 at t={INa_peak_time:.2f} ms")
print(f"I_K Peak (Outward): {max_IK:.2f} \u03bcA/cm\u00b2 at t={IK_peak_time:.2f} ms")
print(f"Conclusion: The negative I_Na current peaks first, driving the voltage spike, while the positive I_K current peaks later, driving repolarization. This difference in kinetic timing is the deterministic cause of the action potential's waveform.")
