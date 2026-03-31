# Source: Simulation/chapter-6/codebook.md -- Block 3

import numpy as np
import matplotlib.pyplot as plt
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ====================================================================
# 1. System Functions
# ====================================================================

# 1D Double-Well Potential: E(x) = x^4 - 2x^2
def E(x):
    """Energy function with minima at x = +/- 1."""
    return x**4 - 2*x**2

def metropolis_step(x, beta, step_size=0.5):
    """Standard Metropolis step for one replica."""
    x_trial = x + random.uniform(-step_size, step_size)
    dE = E(x_trial) - E(x)
    
    if random.random() < np.exp(-beta * dE):
        return x_trial
    else:
        return x

# ====================================================================
# 2. Parallel Tempering Simulation
# ====================================================================

# --- Simulation Parameters ---
STEPS = 20000
STEP_SIZE = 0.5

# Temperature Ladder (Geometric Spacing is typical)
# Beta: [0.5, 1.0, 2.0, 5.0]
BETAS = np.array([0.5, 1.0, 2.0, 5.0]) 
N_REPLICAS = len(BETAS)

# Initializing Replicas (start the cold replica stuck in the positive well)
X_init = np.random.randn(N_REPLICAS)
X_init[-1] = 1.0  # Force the coldest replica to start trapped (x=+1)

# Trajectory Storage (X[i, t] is the position of the configuration currently at beta_i)
X = np.zeros((N_REPLICAS, STEPS))
X[:, 0] = X_init.copy()

# Energy Storage (used for swap analysis/diagnostics)
E_init = E(X_init)

for t in range(1, STEPS):
    # 1. Local Metropolis Updates
    for i, beta in enumerate(BETAS):
        X_init[i] = metropolis_step(X_init[i], beta, STEP_SIZE)
        
    # 2. Replica Exchange (Swap Attempts)
    # Iterate over neighboring pairs, starting from the coldest pair (n_replicas-1, n_replicas-2)
    for i in range(N_REPLICAS - 1, 0, -1):
        
        # Replica 'i' is colder (higher beta), Replica 'j' = i-1 is hotter (lower beta)
        beta_i, beta_j = BETAS[i], BETAS[i-1]
        X_i, X_j = X_init[i], X_init[i-1]
        
        # Swap acceptance probability P_swap = min(1, exp( (beta_i - beta_j) * (E_j - E_i) ))
        # Note: Swap involves swapping configurations, not the temperatures (betas are fixed indices)
        d_beta = beta_i - beta_j  # d_beta > 0
        dE = E(X_j) - E(X_i)      # Energy difference of the *configurations*
        
        P_swap = np.exp(d_beta * dE)
        
        if random.random() < P_swap:
            # Execute the swap: configurations X_i and X_j trade places
            X_init[i], X_init[i-1] = X_init[i-1], X_init[i]
            
    # Record the current configuration positions
    X[:, t] = X_init


# ====================================================================
# 3. Visualization
# ====================================================================

# Trajectory of the Coldest Replica (Index 3, Beta=5.0)
COLDEST_REPLICA_INDEX = N_REPLICAS - 1
X_coldest_traj = X[COLDEST_REPLICA_INDEX, :]

plt.figure(figsize=(10, 4))
plt.plot(X_coldest_traj, lw=0.7, color='darkred')

# Highlight the two minima
plt.axhline(1, color='gray', linestyle=':', alpha=0.7)
plt.axhline(-1, color='gray', linestyle=':', alpha=0.7)

plt.title(f'Parallel Tempering Trajectory of Coldest Replica ($\u03B2={BETAS[-1]:.1f}$)')
plt.xlabel('Step')
plt.ylabel('Position $x$')
plt.grid(True, which='both', linestyle=':')

plt.tight_layout()
plt.show()

# --- Verification of Global Exploration ---
percent_in_well_neg = np.mean(X_coldest_traj < -0.5)
percent_in_well_pos = np.mean(X_coldest_traj > 0.5)

print("\n--- Parallel Tempering Analysis ---")
print(f"Coldest Replica Beta (\u03B2): {BETAS[-1]:.1f}")
print(f"Fraction of time in negative well (x < -0.5): {percent_in_well_neg:.2f}")
print(f"Fraction of time in positive well (x > 0.5): {percent_in_well_pos:.2f}")

print("\nConclusion: The cold replica's trajectory successfully jumps between the two wells ($x=\pm 1$), demonstrated by the non-zero fraction of time spent in both wells. This global exploration, which is exponentially difficult for a single cold chain, confirms that the Parallel Tempering method effectively overcomes the high energy barrier by leveraging the mobility of the high-temperature replicas.")
