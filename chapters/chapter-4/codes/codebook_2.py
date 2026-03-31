# Source: Simulation/chapter-4/codebook.md -- Block 2


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ====================================================================
# 0. Analytical Validation Tool (BSM Model)
# ====================================================================

def black_scholes_call(S, K, T, r, sigma):
    """Calculates the analytical European Call price using the BSM formula."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# ====================================================================
# 1. Setup Functions (from Project 1)
# ====================================================================

def generate_gbm_path(S0, r, sigma, T, N, Z_sequence=None):
    """
    Generates a single asset price path. Can accept a sequence of Z_sequence 
    for use in Variance Reduction Techniques (VRTs).
    """
    dt = T / N
    drift = (r - 0.5 * sigma**2) * dt
    vol_factor = sigma * np.sqrt(dt)
    
    # Use provided Z_sequence or generate a new one
    if Z_sequence is None:
        Z = np.random.standard_normal(N)
    else:
        Z = Z_sequence
    
    path = np.zeros(N + 1)
    path[0] = S0
    
    for k in range(N):
        path[k+1] = path[k] * np.exp(drift + vol_factor * Z[k])
        
    return path

# ====================================================================
# 2. Simulation Parameters & Monte Carlo Pricing
# ====================================================================

# --- Pricing Parameters (Same as Project 1) ---
S0 = 100.0   # Initial asset price
K = 100.0    # Strike price
r = 0.05     # Risk-free interest rate
sigma = 0.20 # Volatility
T = 1.0      # Time to maturity
N = 252      # Number of time steps
M = 100000   # Number of paths (increased for better accuracy)

# Calculate BSM analytical price for validation
BSM_PRICE = black_scholes_call(S0, K, T, r, sigma)
DISCOUNT_FACTOR = np.exp(-r * T)

# --- Monte Carlo Simulation ---
terminal_prices = np.zeros(M)
payoffs = np.zeros(M)

for m in range(M):
    path = generate_gbm_path(S0, r, sigma, T, N)
    S_T = path[-1]
    
    # Payoff for European Call: max(S_T - K, 0)
    payoffs[m] = np.maximum(S_T - K, 0)
    
# Calculate Monte Carlo statistics
MC_PAYOFF_MEAN = np.mean(payoffs)
MC_PRICE = DISCOUNT_FACTOR * MC_PAYOFF_MEAN
MC_PAYOFF_STDEV = np.std(payoffs)

# Standard Error of the Mean (SEM)
MC_STANDARD_ERROR = DISCOUNT_FACTOR * (MC_PAYOFF_STDEV / np.sqrt(M))

# ====================================================================
# 3. Visualization and Comparison
# ====================================================================

# Plot 1: Payoff Distribution and BSM Price
fig, ax = plt.subplots(figsize=(8, 5))

# Filter for non-zero payoffs to make the histogram readable
non_zero_payoffs = payoffs[payoffs > 0]

ax.hist(non_zero_payoffs, bins=50, density=True, color='lightcoral', alpha=0.7, label='Simulated Payoffs ($h_m > 0$)')
ax.axvline(MC_PAYOFF_MEAN, color='blue', linestyle='-', linewidth=2, label=f'Mean Payoff $\\mathbb{{E}}[h_m]$: {MC_PAYOFF_MEAN:.4f}')

ax.set_title(f'Distribution of Call Option Payoffs ($M={M}$ Paths)')
ax.set_xlabel('Payoff $h(S_T)$')
ax.set_ylabel('Density')
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()

# --- Comparison Summary ---
print("\n--- Monte Carlo Pricing vs. BSM Analytical Price ---")
print(f"Analytical BSM Price:      {BSM_PRICE:.5f}")
print(f"Monte Carlo Price (V_hat): {MC_PRICE:.5f}")
print("------------------------------------------------")
print(f"Difference (MC - BSM):     {MC_PRICE - BSM_PRICE:.5f}")
print(f"Standard Error (SEM):    \u00B1 {MC_STANDARD_ERROR:.5f}")
print(f"Validation: |Difference| < 3 * SEM? {np.abs(MC_PRICE - BSM_PRICE) < 3 * MC_STANDARD_ERROR}")
