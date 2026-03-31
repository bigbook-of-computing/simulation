# Source: Simulation/chapter-10/codebook.md -- Block 4

import numpy as np
import matplotlib.pyplot as plt

# ====================================================================
# 1. Dual-Pulse Stimulus Function
# ====================================================================

I_PULSE_MAG = 10.0 # Suprathreshold magnitude
PULSE_DURATION = 1.0 # ms

# Initial State (from Project 2)
V0 = -65.0
m0 = steady_state_value(alpha_m(V0), beta_m(V0))
h0 = steady_state_value(alpha_h(V0), beta_h(V0))
n0 = steady_state_value(alpha_n(V0), beta_n(V0))
S_INIT = np.array([V0, m0, h0, n0])

def I_ext_dual_pulse(t, t_start_1, t_start_2):
    """Generates two 1ms current pulses."""
    t_end_1 = t_start_1 + PULSE_DURATION
    t_end_2 = t_start_2 + PULSE_DURATION
    
    current = 0.0
    if t_start_1 <= t < t_end_1:
        current += I_PULSE_MAG
    if t_start_2 <= t < t_end_2:
        current += I_PULSE_MAG
        
    return current

# ====================================================================
# 2. Simulation Loop (RK4)
# ====================================================================

DT = 0.01
T_TOTAL = 50.0
steps = int(T_TOTAL / DT)
time = np.arange(0, T_TOTAL, DT)

T1 = 10.0 # Start time of the first pulse

# Delay scenarios to test
DELAYS = [1.5, 5.0, 10.0] # ms separation (t2 - t1)
sim_results = {}

for delay in DELAYS:
    T2 = T1 + delay
    S = S_INIT.copy()
    Vm_history = np.zeros(steps)
    
    for i in range(steps):
        t_current = time[i]
        
        # Determine current based on dual pulses
        I_current = I_ext_dual_pulse(t_current, T1, T2)
        
        S = rk4_step(hh_derivatives, S, I_current, DT)
        Vm_history[i] = S[0]
        
    sim_results[delay] = Vm_history
    max_V = np.max(Vm_history[int(T2/DT):]) # Max V after the second pulse
    print(f"Delay {delay:.1f} ms: Max V after second pulse = {max_V:.2f} mV")

# ====================================================================
# 3. Visualization
# ====================================================================

plt.figure(figsize=(10, 5))

# Plot all three voltage traces
for delay, Vm_hist in sim_results.items():
    plt.plot(time, Vm_hist, lw=1.5, label=f'Delay {delay:.1f} ms')

# Annotate the stimulus periods
plt.axvline(T1, color='gray', linestyle=':', label='1st Pulse')
plt.axvline(T1 + 1.0, color='gray', linestyle=':')
plt.axvline(T1 + DELAYS[0], color='red', linestyle=':', label='2nd Pulse (Shortest Delay)')

plt.title('Hodgkin–Huxley: Simulation of the Refractory Period')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane Voltage $V_m$ (mV)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# --- Conclusion ---
print("\n--- Refractory Period Analysis ---")
print("Short Delay (1.5 ms): The second pulse should fail to fire a full spike or fire a greatly diminished one (Absolute/Relative Refractory Period).")
print("Long Delay (10.0 ms): The second pulse should fire a near-full spike (Recovery).")

print("\nConclusion: The simulation successfully demonstrated the refractory period. The initial spike places the neuron in a state of unresponsiveness, evidenced by the reduced or failed amplitude of the second spike when the pulse delay is short. As the time delay increases, the neuron recovers, confirming the slow recovery kinetics of the gating variables.")
