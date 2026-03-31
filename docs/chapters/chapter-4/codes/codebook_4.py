# Source: Simulation/chapter-4/codebook.md -- Block 4


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ====================================================================
# 1. Setup and Core Path Generator (Modified for Asian Average)
# ====================================================================

# --- Pricing Parameters (Same as Project 2 & 3) ---
S0 = 100.0   # Initial asset price
K = 100.0    # Strike price
r = 0.05     # Risk-free interest rate
sigma = 0.20 # Volatility
T = 1.0      # Time to maturity
N = 252      # Number of time steps (daily observation frequency)
M = 100000   # Number of paths to simulate

dt = T / N  
DISCOUNT_FACTOR = np.exp(-r * T)
STEPS_COUNT = N + 1 # Number of observation points including S0

def generate_gbm_average(S0, r, sigma, T, N, Z_sequence):
    """
    Generates a single asset price path and returns the final arithmetic average 
    of all prices in the path.
    """
    dt = T / N
    drift = (r - 0.5 * sigma**2) * dt
    vol_factor = sigma * np.sqrt(dt)
    
    # Use provided Z_sequence (e.g., from Antithetic Variates)
    Z = Z_sequence
    
    current_S = S0
    sum_S = S0  # Initialize sum with the starting price S0
    
    for k in range(N):
        current_S *= np.exp(drift + vol_factor * Z[k])
        sum_S += current_S  # Accumulate the price
        
    # Calculate arithmetic average
    arithmetic_average = sum_S / STEPS_COUNT
        
    return arithmetic_average

# We use Antithetic Variates here as a standard practice to reduce variance
# We will run M_PAIRS pairs, totaling M paths.
M_PAIRS = M // 2 

# ====================================================================
# 2. Monte Carlo Simulation for Asian Call
# ====================================================================

# Storage for averaged payoffs
antithetic_payoff_averages = np.zeros(M_PAIRS)

for m in range(M_PAIRS):
    # 1. Generate one sequence of normal deviates
    Z_sequence = np.random.standard_normal(N)
    
    # 2. Path 1: Original Path (Z)
    S_avg_original = generate_gbm_average(S0, r, sigma, T, N, Z_sequence)
    h_original = np.maximum(S_avg_original - K, 0)
    
    # 3. Path 2: Antithetic Path (-Z)
    S_avg_antithetic = generate_gbm_average(S0, r, sigma, T, N, -Z_sequence)
    h_antithetic = np.maximum(S_avg_antithetic - K, 0)
    
    # 4. Store the average of the paired payoffs
    antithetic_payoff_averages[m] = (h_original + h_antithetic) / 2

# Calculate Monte Carlo statistics
MC_PAYOFF_MEAN_ASIAN = np.mean(antithetic_payoff_averages)
MC_PRICE_ASIAN = DISCOUNT_FACTOR * MC_PAYOFF_MEAN_ASIAN

# Standard Error of the Mean (SEM) using M_PAIRS effective trials
MC_STDEV_ASIAN = np.std(antithetic_payoff_averages)
MC_SEM_ASIAN = DISCOUNT_FACTOR * (MC_STDEV_ASIAN / np.sqrt(M_PAIRS))

# 95% Confidence Interval (z-score for 95% is approx 1.96)
CONFIDENCE_INTERVAL = MC_SEM_ASIAN * 1.96

# ====================================================================
# 3. Visualization and Analysis
# ====================================================================

# Plot 1: Payoff Distribution 
fig, ax = plt.subplots(figsize=(8, 5))

# Filter for non-zero payoffs 
non_zero_payoffs = antithetic_payoff_averages[antithetic_payoff_averages > 0]

ax.hist(non_zero_payoffs, bins=50, density=True, color='purple', alpha=0.7, 
        label='Simulated Payoffs ($h_m > 0$)')

ax.axvline(MC_PAYOFF_MEAN_ASIAN, color='red', linestyle='-', linewidth=2, 
           label=f'Mean Payoff $\\mathbb{{E}}[h_m]$: {MC_PAYOFF_MEAN_ASIAN:.4f}')

ax.set_title(f'Distribution of Arithmetic Asian Call Payoffs ($M={M}$ Paths)')
ax.set_xlabel('Average Payoff $h(\\bar{{S}})$')
ax.set_ylabel('Density')
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()

# --- Pricing Summary ---
print("\n--- Arithmetic Asian Call Option Price ---")
print(f"Option Type: Arithmetic-Average Asian Call (Path Dependent)")
print(f"Total Paths Simulated: {M} (50,000 Antithetic Pairs)")
print("-------------------------------------------------------")
print(f"Monte Carlo Price (V_hat): {MC_PRICE_ASIAN:.5f}")
print(f"Standard Error (SEM):    \u00B1 {MC_SEM_ASIAN:.5f}")
print(f"95% Confidence Interval: ({MC_PRICE_ASIAN - CONFIDENCE_INTERVAL:.5f}, {MC_PRICE_ASIAN + CONFIDENCE_INTERVAL:.5f})")

print("\nConclusion: Monte Carlo simulation successfully priced the analytically intractable Arithmetic Asian Call Option. The price is derived from averaging the path-dependent payoff function $h(\\bar{{S}})$ over 100,000 simulated risk-neutral paths, and the use of Antithetic Variates ensures a tight confidence interval on the final estimate.")
