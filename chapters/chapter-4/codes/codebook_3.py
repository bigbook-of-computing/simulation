# Source: Simulation/chapter-4/codebook.md -- Block 3

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ====================================================================
# 1. Setup Functions
# ====================================================================

# Analytical BSM price (for benchmark)
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price


# GBM path generator (supports optional pre-generated normals)
def generate_gbm_path(S0, r, sigma, T, N, Z_sequence=None):
    """
    Generates a single asset price path using geometric Brownian motion.
    If Z_sequence is None, new random standard normal variates are generated.
    """
    dt = T / N
    drift = (r - 0.5 * sigma**2) * dt
    vol_factor = sigma * np.sqrt(dt)

    if Z_sequence is None:
        Z_sequence = np.random.standard_normal(N)

    path = np.zeros(N + 1)
    path[0] = S0

    for k in range(N):
        path[k + 1] = path[k] * np.exp(drift + vol_factor * Z_sequence[k])

    return path


# ====================================================================
# 2. Parameters
# ====================================================================

S0 = 100.0   # Initial asset price
K = 100.0    # Strike price
r = 0.05     # Risk-free interest rate
sigma = 0.20 # Volatility
T = 1.0      # Time to maturity (years)
N = 252      # Time steps
M_PAIRS = 50000  # Number of antithetic pairs (total 100,000 paths)

# Analytical BSM price and discount factor
BSM_PRICE = black_scholes_call(S0, K, T, r, sigma)
DISCOUNT_FACTOR = np.exp(-r * T)


# ====================================================================
# 3. Standard Monte Carlo (Independent Paths)
# ====================================================================

M_INDEPENDENT = M_PAIRS * 2  # 100,000 independent paths
independent_payoffs = np.zeros(M_INDEPENDENT)

for m in range(M_INDEPENDENT):
    S_T = generate_gbm_path(S0, r, sigma, T, N)[-1]
    independent_payoffs[m] = np.maximum(S_T - K, 0)

MC_STDEV_INDEPENDENT = np.std(independent_payoffs)
MC_SEM_INDEPENDENT = DISCOUNT_FACTOR * (MC_STDEV_INDEPENDENT / np.sqrt(M_INDEPENDENT))


# ====================================================================
# 4. Antithetic Variates Simulation
# ====================================================================

antithetic_payoff_averages = np.zeros(M_PAIRS)
payoffs_original = np.zeros(M_PAIRS)
payoffs_antithetic = np.zeros(M_PAIRS)

for m in range(M_PAIRS):
    # Generate a sequence of standard normal variates
    Z_sequence = np.random.standard_normal(N)
    
    # Path 1: original
    S_T_original = generate_gbm_path(S0, r, sigma, T, N, Z_sequence)[-1]
    h_original = np.maximum(S_T_original - K, 0)
    payoffs_original[m] = h_original
    
    # Path 2: antithetic
    S_T_antithetic = generate_gbm_path(S0, r, sigma, T, N, -Z_sequence)[-1]
    h_antithetic = np.maximum(S_T_antithetic - K, 0)
    payoffs_antithetic[m] = h_antithetic
    
    # Average the pair
    antithetic_payoff_averages[m] = (h_original + h_antithetic) / 2

# Antithetic Variates results
MC_PAYOFF_MEAN_AV = np.mean(antithetic_payoff_averages)
MC_PRICE_AV = DISCOUNT_FACTOR * MC_PAYOFF_MEAN_AV
MC_STDEV_AV = np.std(antithetic_payoff_averages)
MC_SEM_AV = DISCOUNT_FACTOR * (MC_STDEV_AV / np.sqrt(M_PAIRS))
correlation = np.corrcoef(payoffs_original, payoffs_antithetic)[0, 1]


# ====================================================================
# 5. Visualization and Comparison
# ====================================================================

fig, ax = plt.subplots(figsize=(8, 5))

labels = ['Standard MC (100k Trials)', 'Antithetic MC (50k Pairs)']
prices = [MC_PRICE_AV, MC_PRICE_AV]  # both plotted at same price for error comparison
errors = [MC_SEM_INDEPENDENT, MC_SEM_AV]

ax.errorbar(labels, prices, yerr=errors, fmt='o', capsize=5, linewidth=2, color='darkgreen')
ax.axhline(BSM_PRICE, color='red', linestyle='--', label='BSM Price')

ax.set_title('Variance Reduction: Standard Error Comparison (Total 100k Paths)')
ax.set_ylabel('Option Price Estimate ($V_0$)')
ax.set_ylim(BSM_PRICE - 0.2, BSM_PRICE + 0.2)
ax.legend()
ax.grid(True, linestyle=':')

plt.tight_layout()
plt.show()


# ====================================================================
# 6. Summary Output
# ====================================================================

print("\n--- Antithetic Variates (AV) Summary ---")
print(f"Total Paths Simulated: {M_PAIRS * 2:,} (50,000 pairs)")
print(f"Correlation between Payoffs (h, h~): {correlation:.4f}")
print("-------------------------------------------------------")
print(f"Standard MC SEM (100k independent trials): ± {MC_SEM_INDEPENDENT:.5f}")
print(f"AV MC SEM (50k effective trials):          ± {MC_SEM_AV:.5f}")
print(f"Variance Reduction Factor (1 - ρ²):        {1 - correlation**2:.4f}")

sem_ratio = MC_SEM_INDEPENDENT / MC_SEM_AV
print(f"SEM Reduction (SEM_Std / SEM_AV):          {sem_ratio:.2f}x")

print("\nConclusion: The Antithetic Variates technique successfully reduces the Standard Error of the Mean (SEM) while using only half as many independent random samples (50k pairs vs. 100k independent trials). The negative correlation between paired payoffs cancels variance, making the estimator more efficient.")
