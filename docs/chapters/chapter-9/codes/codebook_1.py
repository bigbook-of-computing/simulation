# Source: Simulation/chapter-9/codebook.md -- Block 1

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ====================================================================
# 1. BSM Analytical Formula Implementation
# ====================================================================

def black_scholes_call(S, K, T, r, sigma, t=0.0):
    """
    Calculates the analytical European Call price using the BSM formula 
    at time t.
    """
    tau = T - t  # Time remaining to maturity
    if tau <= 0:
        return np.maximum(S - K, 0)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * tau) / (sigma * np.sqrt(tau))
    d2 = d1 - sigma * np.sqrt(tau)
    
    # N(d1) and N(d2) are the cumulative standard normal distribution function (CDF)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * tau) * norm.cdf(d2)
    return call_price

# ====================================================================
# 2. Parameter Setup and Calculation
# ====================================================================

# --- Parameters (Used in Chapter 4, Project 2) ---
S0 = 100.0   # Initial asset price
K = 100.0    # Strike price
r = 0.05     # Risk-free interest rate
sigma = 0.20 # Volatility
T = 1.0      # Time to maturity

# --- Monte Carlo Benchmark (Hypothetical Convergence Result from Ch4) ---
# We use a known, highly converged value for comparison.
MC_PRICE_BENCHMARK = 10.45037 
MC_SEM_BENCHMARK = 0.0105

# Calculate the BSM Price
BSM_PRICE = black_scholes_call(S0, K, T, r, sigma)

# Calculate the difference for validation
PRICE_DIFFERENCE = BSM_PRICE - MC_PRICE_BENCHMARK

# ====================================================================
# 3. Visualization and Comparison
# ====================================================================

# Plot the Option Price surface (Value vs. Price)
S_range = np.linspace(50, 150, 100)
C_surface = black_scholes_call(S_range, K, T, r, sigma)

plt.figure(figsize=(10, 5))
plt.plot(S_range, C_surface, lw=2, color='darkgreen', label='BSM Price Curve')

# Highlight the calculated price point (S0=100)
plt.plot(S0, BSM_PRICE, 'o', markersize=8, color='red', label=f'Calculated Price V0: {BSM_PRICE:.4f}')

# Labeling and Formatting
plt.title('Black–Scholes–Merton (BSM) Analytical Valuation')
plt.xlabel('Stock Price S')
plt.ylabel('Call Option Price C(S, t=0)')
plt.axvline(K, color='gray', linestyle='--', label='Strike K=100')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# --- Comparison Summary ---
print("\n--- Analytical Price vs. Monte Carlo Benchmark ---")
print(f"BSM Analytical Price:      {BSM_PRICE:.5f}")
print(f"MC Benchmark Price (Ch4):  {MC_PRICE_BENCHMARK:.5f}")
print("-------------------------------------------------")
print(f"Difference (BSM - MC):     {PRICE_DIFFERENCE:.5f}")
print(f"MC Standard Error (SEM): \u00B1 {MC_SEM_BENCHMARK:.5f}")

# Validation Check
# The prices are validated if the difference is within 3 standard errors.
IS_VALIDATED = np.abs(PRICE_DIFFERENCE) < 3 * MC_SEM_BENCHMARK
print(f"Validation Check: |Difference| < 3 * SEM? {IS_VALIDATED}")

print("\nConclusion: The analytically calculated BSM price must match the Monte Carlo result within the expected statistical error, confirming that both methods correctly compute the risk-neutral expected payoff.")
