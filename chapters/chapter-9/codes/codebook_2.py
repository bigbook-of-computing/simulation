# Source: Simulation/chapter-9/codebook.md -- Block 2

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ====================================================================
# 1. BSM Greeks Implementation
# ====================================================================

# BSM parameters (held constant)
K = 100.0
T = 1.0
r = 0.05
sigma = 0.20

def calculate_d1(S, K, T, r, sigma):
    tau = T
    return (np.log(S / K) + (r + 0.5 * sigma**2) * tau) / (sigma * np.sqrt(tau))

def calculate_delta(S, K, T, r, sigma):
    """Calculates Delta: The first derivative (N(d1))."""
    d1 = calculate_d1(S, K, T, r, sigma)
    return norm.cdf(d1)

def calculate_gamma(S, K, T, r, sigma):
    """Calculates Gamma: The second derivative (N'(d1) / (S * sigma * sqrt(T)))."""
    d1 = calculate_d1(S, K, T, r, sigma)
    # N'(d1) is the standard normal PDF evaluated at d1
    N_prime_d1 = norm.pdf(d1) 
    
    gamma = N_prime_d1 / (S * sigma * np.sqrt(T))
    return gamma

# ====================================================================
# 2. Data Generation and Analysis
# ====================================================================

# Range of Stock Prices for plotting
S_range = np.linspace(50, 150, 200)

# Calculate Greeks across the range
Delta_values = calculate_delta(S_range, K, T, r, sigma)
Gamma_values = calculate_gamma(S_range, K, T, r, sigma)

# ====================================================================
# 3. Visualization
# ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Delta (Sensitivity to price change)
ax[0].plot(S_range, Delta_values, lw=2, color='blue')
ax[0].axvline(K, color='gray', linestyle='--', label='Strike K=100')
ax[0].axhline(0.5, color='black', linestyle=':', label='At-the-Money Delta')
ax[0].set_title('Delta ($\u0394$): The Hedging Ratio')
ax[0].set_xlabel('Stock Price S')
ax[0].set_ylabel('Delta ($\u0394$ = $\partial C / \partial S$)')
ax[0].set_ylim(0, 1)
ax[0].legend()
ax[0].grid(True)

# Plot 2: Gamma (Convexity and Re-hedging frequency)
ax[1].plot(S_range, Gamma_values, lw=2, color='red')
ax[1].axvline(K, color='gray', linestyle='--', label='Strike K=100')
ax[1].set_title('Gamma ($\u0393$): The Volatility of Delta')
ax[1].set_xlabel('Stock Price S')
ax[1].set_ylabel('Gamma ($\u0393$ = $\partial^2 C / \partial S^2$)')
ax[1].set_ylim(bottom=0)
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- Analysis of Option Greeks ---")
print(f"Delta is the slope of the option price curve; it ranges from 0 (Out-of-the-Money) to 1 (Deep In-the-Money).")
print(f"Gamma is the curvature of the option price; it peaks sharply at the strike price (S=K) where Delta changes fastest, requiring frequent re-hedging.")
