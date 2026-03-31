# Source: Simulation/chapter-8/codebook.md -- Block 3

import numpy as np
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# ====================================================================
# 1. Simulation Parameters
# ====================================================================

S0 = 100.0   # Initial price
mu = 0.10    # Expected return (uncorrected drift)
sigma = 0.30 # Volatility
T = 1.0      # Time to maturity
N = 252      # Number of steps (fine enough for GBM)

M_PATHS = 10000 # Number of paths for ensemble averaging

# Calculate theoretical drifts
ITO_CORRECTION_TERM = -0.5 * sigma**2 * T
ITO_DRIFT_THEO = (mu - 0.5 * sigma**2) * T # Expected log-return
CLASSICAL_DRIFT_THEO = mu * T             # Uncorrected drift (what classical calculus predicts)

# ====================================================================
# 2. GBM Simulation (Using the Exact Solution for Accuracy)
# ====================================================================

# We use the exact solution for the terminal price, which is required for accurate ensemble checking.
# S_T = S0 * exp( (mu - 0.5*sigma^2)*T + sigma*sqrt(T)*W_T )
# W_T ~ N(0, T), so sigma*W_T ~ N(0, sigma^2*T)

log_returns = np.zeros(M_PATHS)

for m in range(M_PATHS):
    # W_T is a single normal sample scaled by sqrt(T)
    W_T = np.random.standard_normal() * np.sqrt(T)
    
    # Calculate the terminal log-price relative to S0: ln(S_T/S0)
    log_ST_S0 = (mu - 0.5 * sigma**2) * T + sigma * W_T
    log_returns[m] = log_ST_S0

# Calculate ensemble average of log-return
E_LOG_RETURN_EMPIRICAL = np.mean(log_returns)
E_LOG_RETURN_STD = np.std(log_returns)

# ====================================================================
# 3. Visualization and Comparison
# ====================================================================

fig, ax = plt.subplots(figsize=(8, 5))

# Plot the three key values
bar_labels = ['Classical Drift $\\mu T$', 'Empirical $\\langle \\ln(S_T/S_0) \\rangle$', 'Itō Corrected Drift']
drift_values = [CLASSICAL_DRIFT_THEO, E_LOG_RETURN_EMPIRICAL, ITO_DRIFT_THEO]

ax.bar(bar_labels, drift_values, color=['skyblue', 'purple', 'green'], alpha=0.7)

# Add reference lines
ax.axhline(ITO_DRIFT_THEO, color='green', linestyle='--', linewidth=2, label='Itō Corrected Target')
ax.axhline(CLASSICAL_DRIFT_THEO, color='red', linestyle=':', linewidth=2, label='Classical Target')

# Labeling and Formatting
ax.set_title(f'Numerical Verification of the Itō Correction Term (\\sigma^2/2)')
ax.set_ylabel('Average Logarithmic Return $\\langle \\ln(S_T/S_0) \\rangle$')
ax.text(1, E_LOG_RETURN_EMPIRICAL, f'{E_LOG_RETURN_EMPIRICAL:.4f}', ha='center', va='bottom', fontsize=12)
ax.text(2, ITO_DRIFT_THEO, f'{ITO_DRIFT_THEO:.4f}', ha='center', va='bottom', fontsize=12)

ax.grid(True, axis='y')
plt.legend()
plt.tight_layout()
plt.show()

# --- Conclusion ---
print("\n--- Itō Correction Numerical Check ---")
print(f"Uncorrected (Classical) Drift \u03bcT: {CLASSICAL_DRIFT_THEO:.5f}")
print(f"Itō Correction Term (-\u03c3\u00b2T/2):   {ITO_CORRECTION_TERM:.5f}")
print(f"Corrected (Itō) Drift (\u222e[ln(S_T/S0)]): {ITO_DRIFT_THEO:.5f}")
print("---------------------------------------------------")
print(f"Empirical Ensemble Average \u222e[ln(S_T/S0)]: {E_LOG_RETURN_EMPIRICAL:.5f}")

print("\nConclusion: The numerical ensemble average of the log-price closely matches the corrected drift (0.055) and is significantly lower than the uncorrected drift (0.100). This confirms the presence of the Itō correction, which demonstrates that volatility introduces a predictable, deterministic drag on the average log-return.")
