# Source: Simulation/chapter-5/codebook.md -- Block 1


import numpy as np
import random
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Parameters and Initial State
# ====================================================================

# Define Reaction Rate Constants (k_1, k_2)
K1 = 1.0  # Rate for A -> B (Production)
K2 = 0.1  # Rate for B -> 0 (Decay)

# Initial Molecule Counts (State Vector x = [NA, NB])
NA_INIT = 10
NB_INIT = 0

# Define Stoichiometry Vectors (Delta_nu_j)
# Reaction 1 (A -> B): Delta_nu_1 = [-1, +1]
# Reaction 2 (B -> 0): Delta_nu_2 = [ 0, -1]
STOICHIOMETRY = np.array([
    [-1, +1],
    [ 0, -1]
])

# ====================================================================
# 2. The Gillespie SSA Core Step (The Engine)
# ====================================================================

def gillespie_step(NA, NB, K1, K2):
    """
    Performs one step of the Direct Gillespie Stochastic Simulation Algorithm.
    
    Returns: (tau, j, next_NA, next_NB)
    """
    
    # --- 1. Compute Propensities ---
    a1 = K1 * NA  # Propensity for Reaction 1 (A -> B)
    a2 = K2 * NB  # Propensity for Reaction 2 (B -> 0)
    
    # Propensity array and total propensity a_0
    propensities = np.array([a1, a2])
    a0 = np.sum(propensities)
    
    # Check for steady state (no more reactions possible)
    if a0 == 0:
        return np.inf, 0, NA, NB

    # --- 2. Draw Waiting Time (tau) ---
    r1 = random.uniform(0, 1)
    # tau = (1 / a0) * ln(1 / r1)
    tau = (1.0 / a0) * np.log(1.0 / r1)
    
    # --- 3. Select Reaction Channel (j) ---
    r2 = random.uniform(0, 1)
    
    # Cumulative sum rule: find smallest j such that sum(a_k) >= r2 * a0
    # The selected channel index (0 or 1)
    j = 0
    if r2 * a0 >= a1:
        j = 1 # Reaction 2 fires
        
    # --- 4. Update State ---
    # Apply the stoichiometry vector for the chosen reaction j
    delta_nu = STOICHIOMETRY[j, :]
    next_NA = NA + delta_nu[0]
    next_NB = NB + delta_nu[1]
    
    # Reaction index starts from 1 for output clarity
    return tau, j + 1, next_NA, next_NB

# ====================================================================
# 3. Trajectory Run and Verification
# ====================================================================

# Simulation Parameters
MAX_STEPS = 50 

# Trajectory Storage
trajectory = []
current_time = 0.0
NA = NA_INIT
NB = NB_INIT

for step in range(MAX_STEPS):
    # Perform one Gillespie step
    tau, reaction_j, next_NA, next_NB = gillespie_step(NA, NB, K1, K2)
    
    if tau == np.inf:
        break
        
    # Update time and state
    current_time += tau
    NA = next_NA
    NB = next_NB
    
    # Record the new state and event
    trajectory.append({
        'Step': step + 1,
        'Time': current_time,
        'Reaction': reaction_j,
        'NA': NA,
        'NB': NB,
        'a0': K1 * (NA + (STOICHIOMETRY[0, 0] if reaction_j==1 else 0)) + K2 * (NB + (STOICHIOMETRY[1, 1] if reaction_j==2 else 0)),
        'Prob_j1': (K1 * NA) / (K1 * NA + K2 * NB) if (K1 * NA + K2 * NB) > 0 else 0
    })

# Convert to DataFrame for clean display and print
import pandas as pd
df = pd.DataFrame(trajectory)
df_display = df[['Step', 'Time', 'Reaction', 'NA', 'NB']]

# --- Verification ---
print("--- Gillespie SSA Trajectory Verification (First 15 Steps) ---")
print(df_display.head(15).to_markdown(index=False))

print("\nVerification of Initial Propensity Weighting:")
# Initial State: NA=10, NB=0. Propensities: a1 = 10, a2 = 0. a0 = 10.
# P(j=1) = a1/a0 = 10/10 = 1.0. 
print(f"Initial Rates: K1={K1}, K2={K2}")
print(f"Initial State: NA={NA_INIT}, NB={NB_INIT}")
print(f"Initial Propensities: a1={K1*NA_INIT}, a2={K2*NB_INIT}. Total a0={K1*NA_INIT + K2*NB_INIT}")
print("Expected initial reaction: Reaction 1 (A -> B) with P=1.0. Time advance should be rapid (mean tau=1/10=0.1).")

# --- Visualization (Time Series of Molecule Counts) ---
plt.figure(figsize=(10, 4))
plt.step(df['Time'], df['NA'], where='post', label='Molecule A ($N_A$)', color='blue')
plt.step(df['Time'], df['NB'], where='post', label='Molecule B ($N_B$)', color='red')
plt.title('Gillespie Trajectory: $A \\to B$ and $B \\to \\emptyset$')
plt.xlabel('Time (t)')
plt.ylabel('Molecule Count')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()

print("\nConclusion: The core SSA step successfully simulates the discrete molecular events. Initially, only Reaction 1 (A -> B) occurs, causing $N_A$ to decrease and $N_B$ to increase. As $N_B$ grows, the propensity for Reaction 2 (B -> 0) increases, and the simulation time advances stochastically based on the total propensity.")
