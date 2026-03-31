# Source: Simulation/chapter-8/codebook.md -- Block 1

import numpy as np
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# ====================================================================
# 1. Simulation Parameters
# ====================================================================

T = 1.0     # Total time (T) for the process (e.g., 1 year)
N = 10000   # Number of time steps (N)
DT = T / N  # Time step size (Delta t)

M_PATHS = 10000  # Number of independent paths to run for ensemble verification

# Theoretical expectation for verification
E_WT_THEO = 0.0  # Mean of the Wiener Process at any time T is 0
VAR_WT_THEO = T  # Variance of the Wiener Process at time T is T

# ====================================================================
# 2. Simulation and Verification
# ====================================================================

terminal_W = np.zeros(M_PATHS)

# Calculate the constant scaling factor for the random increment
dW_scale = np.sqrt(DT)

for m in range(M_PATHS):
    # 1. Generate N independent standard normal variates
    Z_sequence = np.random.standard_normal(N)
    
    # 2. Calculate the Wiener increments: dW = sqrt(dt) * Z
    dW_sequence = dW_scale * Z_sequence
    
    # 3. Calculate the Wiener path: W_t = cumulative sum(dW)
    W_path = np.cumsum(dW_sequence)
    
    # Record the terminal value W_T
    terminal_W[m] = W_path[-1]

# --- Calculate Empirical Statistics ---
E_WT_EMPIRICAL = np.mean(terminal_W)
VAR_WT_EMPIRICAL = np.var(terminal_W, ddof=1) # Use ddof=1 for sample variance

# ====================================================================
# 3. Visualization and Analysis
# ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Ensemble Distribution (Histogram)
ax[0].hist(terminal_W, bins=50, density=True, color='purple', alpha=0.7, 
           label='Simulated $W_T$')
ax[0].axvline(E_WT_THEO, color='red', linestyle='--', 
             label='Theoretical Mean $\\mathbb{E}[W_T] = 0$')

# Labeling and Formatting
ax[0].set_title(f'Ensemble Distribution of Terminal $W_T$ ($T={T}$)')
ax[0].set_xlabel('Terminal Value $W_T$')
ax[0].set_ylabel('Density')
ax[0].legend()
ax[0].grid(True)

# Plot 2: Variance Check (Illustrating the squared term)
check_data = [VAR_WT_THEO, VAR_WT_EMPIRICAL]
ax[1].bar(['Theoretical Var($W_T$)=T', f'Empirical Var($W_T$): {VAR_WT_EMPIRICAL:.4f}'], 
         check_data, color=['gray', 'purple'])
ax[1].axhline(VAR_WT_THEO, color='red', linestyle='--', label='Target Variance')

# Labeling and Formatting
ax[1].set_title('Verification of Variance Scaling')
ax[1].set_ylabel('Variance')
ax[1].grid(True, axis='y')

plt.tight_layout()
plt.show()

# --- Verification Summary ---
print("\n--- Wiener Process Verification Summary ---")
print(f"Time Step (\u0394t): {DT:.4e}")
print(f"Total Paths (M): {M_PATHS}")
print("-----------------------------------------")
print(f"Theoretical Mean \u222e[W_T]: {E_WT_THEO:.4f}")
print(f"Empirical Mean \u222e[W_T]:   {E_WT_EMPIRICAL:.4f}")
print(f"Difference (Mean):       {np.abs(E_WT_EMPIRICAL - E_WT_THEO):.4e}")
print("-----------------------------------------")
print(f"Theoretical Variance Var[W_T]: {VAR_WT_THEO:.4f}")
print(f"Empirical Variance Var[W_T]:   {VAR_WT_EMPIRICAL:.4f}")
print(f"Difference (Variance):         {np.abs(VAR_WT_EMPIRICAL - VAR_WT_THEO):.4e}")

print("\nConclusion: The simulation successfully generated the Wiener Process. The ensemble of terminal values confirms the two defining properties: the mean is zero, and the variance is equal to the total time T (1.0), which provides the fundamental noise input for SDE solvers.")
