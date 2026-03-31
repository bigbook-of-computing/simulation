# Source: Simulation/chapter-5/codebook.md -- Block 2


import numpy as np
import random
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Parameters and Initial State
# ====================================================================

# Define Reaction Rate Constants (Bursty Regime)
K_ON = 0.01   # Gene activation rate (s^-1)
K_OFF = 0.1   # Gene inactivation rate (s^-1)
KM = 1.0      # Transcription rate (mRNA production rate when ON)
GAMMA_M = 0.05 # mRNA degradation rate (s^-1)

# Initial State
G_INIT = 0  # Gene state: 0=OFF, 1=ON
M_INIT = 0  # mRNA count

# Final Simulation Time
T_FINAL = 1000.0 # seconds

# Stoichiometry (State change vectors: [Delta_g, Delta_m])
STOICHIOMETRY = np.array([
    [+1, 0], # 1: Activation
    [-1, 0], # 2: Inactivation
    [ 0, +1],# 3: Transcription
    [ 0, -1] # 4: mRNA Decay
])

# Deterministic Steady-State Mean mRNA (for comparison)
# <m>_det = (k_on / (k_on + k_off)) * (k_m / gamma_m)
P_ON_SS = K_ON / (K_ON + K_OFF)
M_MEAN_DET = P_ON_SS * (KM / GAMMA_M)

# ====================================================================
# 2. The Gillespie SSA Simulation Loop
# ====================================================================

def run_ssa_gene_expression(T_final, g_init, m_init):
    """
    Runs a single SSA trajectory for the telegraph model (mRNA only).
    """
    time_points = [0.0]
    g_states = [g_init]
    m_counts = [m_init]
    
    t = 0.0
    g = g_init
    m = m_init
    
    while t < T_final:
        # --- Compute Propensities ---
        a1 = K_ON * (1 - g)  # OFF -> ON
        a2 = K_OFF * g       # ON -> OFF
        a3 = KM * g          # ON -> ON + m
        a4 = GAMMA_M * m     # m -> 0
        
        propensities = np.array([a1, a2, a3, a4])
        a0 = np.sum(propensities)
        
        if a0 == 0:
            t = T_final # Stop if no reactions are possible
            break
            
        # --- 1. Draw Waiting Time (tau) ---
        r1 = random.uniform(0, 1)
        tau = (1.0 / a0) * np.log(1.0 / r1)
        
        # --- 2. Select Reaction Channel (j) ---
        r2 = random.uniform(0, 1)
        cumulative_propensity = np.cumsum(propensities)
        
        # Find the smallest j such that cumulative_propensity[j] >= r2 * a0
        j = np.searchsorted(cumulative_propensity, r2 * a0)
        
        # --- 3. Update State and Time ---
        t += tau
        
        delta_nu = STOICHIOMETRY[j, :]
        g += delta_nu[0]
        m += delta_nu[1]
        
        # --- Record State ---
        time_points.append(t)
        g_states.append(g)
        m_counts.append(m)
        
    return np.array(time_points), np.array(m_counts)

# Run a single stochastic trajectory
time_ssa, m_ssa = run_ssa_gene_expression(T_FINAL, G_INIT, M_INIT)

# ====================================================================
# 3. Visualization
# ====================================================================

plt.figure(figsize=(10, 5))

# Plot the stochastic trajectory (discrete steps)
plt.step(time_ssa, m_ssa, where='post', label='Stochastic Trajectory $m(t)$', color='darkblue', linewidth=1.5, alpha=0.8)

# Plot the deterministic mean as a horizontal line
plt.axhline(M_MEAN_DET, color='red', linestyle='--', label=f'Deterministic Mean $\\langle m \\rangle_{{\\text{{det}}}}={M_MEAN_DET:.1f}$')

# Labeling and Formatting
plt.title('Gillespie Simulation of Transcriptional Bursting (mRNA only)')
plt.xlabel('Time (seconds)')
plt.ylabel('mRNA Copy Number ($m$)')
plt.ylim(bottom=0)
plt.legend()
plt.grid(True, which='both', linestyle=':', alpha=0.6)
plt.show()

# Display the image tag
print("")

# --- Summary ---
print("\n--- Simulation Summary ---")
print(f"Deterministic Mean <m>_det: {M_MEAN_DET:.2f}")
print(f"Burst Size Factor (k_m / gamma_m): {KM / GAMMA_M:.0f} mRNAs/burst")
print("\nObservation: The stochastic trajectory exhibits **transcriptional bursts**, where mRNA copy numbers spike rapidly during brief ON periods and then decay slowly during OFF periods. The mean of these fluctuations converges toward the smoother deterministic mean.")
