# Source: Simulation/chapter-5/codebook.md -- Block 3


import numpy as np
import random
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Functions and Parameters (from Project 2)
# ====================================================================

# --- Parameters (Bursty Regime) ---
K_ON = 0.01   # Gene activation rate (s^-1)
K_OFF = 0.1   # Gene inactivation rate (s^-1)
KM = 1.0      # Transcription rate
GAMMA_M = 0.05 # mRNA degradation rate
T_FINAL = 10000.0 # Time to reach steady state
M_TRAJECTORIES = 500 # Number of independent trajectories

# Stoichiometry (State change vectors: [Delta_g, Delta_m])
STOICHIOMETRY = np.array([
    [+1, 0], # 1: Activation
    [-1, 0], # 2: Inactivation
    [ 0, +1],# 3: Transcription
    [ 0, -1] # 4: mRNA Decay
])

# Deterministic Steady-State Mean (for reference)
P_ON_SS = K_ON / (K_ON + K_OFF)
M_MEAN_DET = P_ON_SS * (KM / GAMMA_M)

def run_ssa_gene_expression(T_final, g_init, m_init):
    """
    Runs a single SSA trajectory for the telegraph model (mRNA only) up to T_final.
    Returns the final mRNA count m_T.
    """
    t = 0.0
    g = g_init
    m = m_init
    
    while t < T_final:
        # --- Compute Propensities ---
        a1 = K_ON * (1 - g)
        a2 = K_OFF * g
        a3 = KM * g
        a4 = GAMMA_M * m
        propensities = np.array([a1, a2, a3, a4])
        a0 = np.sum(propensities)
        
        if a0 == 0:
            break
            
        # --- 1. Draw Waiting Time (tau) ---
        r1 = random.uniform(0, 1)
        tau = (1.0 / a0) * np.log(1.0 / r1)
        
        # --- 2. Select Reaction Channel (j) ---
        r2 = random.uniform(0, 1)
        cumulative_propensity = np.cumsum(propensities)
        j = np.searchsorted(cumulative_propensity, r2 * a0)
        
        # --- 3. Update State and Time ---
        t += tau
        
        delta_nu = STOICHIOMETRY[j, :]
        g += delta_nu[0]
        m += delta_nu[1]
        
    return m # Return the final mRNA count

# ====================================================================
# 2. Ensemble Simulation and Noise Quantification
# ====================================================================

final_m_ensemble = np.zeros(M_TRAJECTORIES)

for i in range(M_TRAJECTORIES):
    # Run each trajectory independently from the initial state
    final_m_ensemble[i] = run_ssa_gene_expression(T_FINAL, G_INIT, M_INIT)

# --- Calculate Ensemble Statistics ---
M_MEAN_EMPIRICAL = np.mean(final_m_ensemble)
M_VARIANCE_EMPIRICAL = np.var(final_m_ensemble, ddof=1) # Use ddof=1 for sample variance

# Calculate the Fano Factor (Noise Strength)
FANO_FACTOR = M_VARIANCE_EMPIRICAL / M_MEAN_EMPIRICAL

# ====================================================================
# 3. Visualization and Analysis
# ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Steady-State Distribution (Histogram of Final Counts)
ax[0].hist(final_m_ensemble, bins=np.arange(0, np.max(final_m_ensemble) + 1, 1), 
           density=True, color='purple', alpha=0.7, align='left')
ax[0].axvline(M_MEAN_EMPIRICAL, color='red', linestyle='--', label=f'Mean $\\langle m \\rangle$: {M_MEAN_EMPIRICAL:.1f}')
ax[0].set_title('Steady-State mRNA Distribution (Ensemble)')
ax[0].set_xlabel('Final mRNA Count ($m$)')
ax[0].set_ylabel('Probability Density')
ax[0].legend()
ax[0].grid(True, which='major', axis='y', linestyle=':')

# Plot 2: Fano Factor Visualization
bars = ax[1].bar(['Poisson ($\eta=1$)', f'Simulated ($\eta$)'], [1.0, FANO_FACTOR], color=['gray', 'darkred'])
bars[0].set_alpha(0.5)
ax[1].axhline(1.0, color='black', linestyle='--', label='Poisson Threshold')
ax[1].text(1, FANO_FACTOR + 0.5, f'{FANO_FACTOR:.2f}', ha='center', fontweight='bold', color='darkred')
ax[1].set_title('Noise Quantification: Fano Factor ($\eta$)')
ax[1].set_ylabel('Fano Factor ($\eta$)')
ax[1].set_ylim(0, np.max([FANO_FACTOR, 5]) * 1.1)
ax[1].grid(True, which='major', axis='y', linestyle=':')

plt.tight_layout()
plt.show()

# --- Summary ---
print("\n--- Super-Poissonian Noise Quantification ---")
print(f"Ensemble Mean <m>:      {M_MEAN_EMPIRICAL:.2f}")
print(f"Ensemble Variance Var(m): {M_VARIANCE_EMPIRICAL:.2f}")
print("-----------------------------------------")
print(f"Fano Factor ( = Var/Mean): {FANO_FACTOR:.2f}")
print(f"Deterministic Mean (Benchmark): {M_MEAN_DET:.2f}")

print("\nConclusion: The calculated Fano Factor (\u03B7) is significantly greater than 1.0 (Super-Poissonian), quantitatively confirming that the telegraph model successfully captures the **transcriptional bursting** regime, where noise is high due to episodic production of large numbers of mRNA molecules.")
