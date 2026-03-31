# Source: Simulation/chapter-9/codebook.md -- Block 4

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ====================================================================
# 1. BSM Analytical Formula Implementation
# ====================================================================

# BSM parameters (held constant)
K = 100.0
T = 1.0
r = 0.05

def calculate_d1_d2(S, K, T, r, sigma):
    """Calculates d1 and d2 BSM parameters."""
    tau = T  # Time to maturity
    if tau <= 0:
        return np.nan, np.nan
    
    # Ensure tau is not zero for calculations
    tau_safe = np.maximum(tau, 1e-10) 
    sqrt_tau = np.sqrt(tau_safe)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * tau_safe) / (sigma * sqrt_tau)
    d2 = d1 - sigma * sqrt_tau
    return d1, d2

def black_scholes_call(S, K, T, r, sigma):
    """Calculates the analytical European Call price."""
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def calculate_vega(S, K, T, r, sigma):
    """Calculates Option Vega (sensitivity to volatility)."""
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    tau_safe = np.maximum(T, 1e-10)
    
    # Vega = S * sqrt(T) * N'(d1)
    vega = S * np.sqrt(tau_safe) * norm.pdf(d1)
    return vega

# ====================================================================
# 2. Scenarios and Calculation
# ====================================================================

S0 = 100.0

# --- Scenario A: Low Volatility (Sigma=0.10) ---
SIGMA_A = 0.10
PRICE_A = black_scholes_call(S0, K, T, r, SIGMA_A)
VEGA_A = calculate_vega(S0, K, T, r, SIGMA_A)

# --- Scenario B: High Volatility (Sigma=0.50) ---
SIGMA_B = 0.50
PRICE_B = black_scholes_call(S0, K, T, r, SIGMA_B)
VEGA_B = calculate_vega(S0, K, T, r, SIGMA_B)

# ====================================================================
# 3. Visualization and Summary
# ====================================================================

# Plot the Option Price vs. Volatility
sigma_range = np.linspace(0.05, 0.55, 100)
C_vs_sigma = black_scholes_call(S0, K, T, r, sigma_range)

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(sigma_range, C_vs_sigma, lw=2, color='darkred')

# Highlight the two scenario points
ax.plot(SIGMA_A, PRICE_A, 'o', markersize=8, color='blue', label=f'Low $\sigma$ Price: {PRICE_A:.4f}')
ax.plot(SIGMA_B, PRICE_B, 's', markersize=8, color='green', label=f'High $\sigma$ Price: {PRICE_B:.4f}')

# Labeling and Formatting
ax.set_title('Option Price Increase with Volatility (Vega)')
ax.set_xlabel('Volatility ($\u03C3$)')
ax.set_ylabel('Call Option Price $C$')
ax.grid(True, which='both', linestyle=':')
ax.legend()

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- Volatility Scenarios and Vega Analysis ---")
print(f"Strike K={K}, Time T={T}, Rate r={r}")
print("-------------------------------------------------------")
print(f"| Scenario | Volatility (\u03c3) | Price (V) | Vega (\u2202V/\u2202\u03c3) |")
print("| :--- | :--- | :--- | :--- |")
print(f"| Low \u03c3 | {SIGMA_A:.2f} | {PRICE_A:.4f} | {VEGA_A:.4f} |")
print(f"| High \u03c3 | {SIGMA_B:.2f} | {PRICE_B:.4f} | {VEGA_B:.4f} |")
print("-------------------------------------------------------")

print("\nConclusion: The option price increases significantly from {PRICE_A:.4f} to {PRICE_B:.4f} as volatility rises. This confirms that **volatility always adds value to an option** (Vega > 0), reflecting the increased probability of extreme outcomes necessary for the option to finish in-the-money.")
