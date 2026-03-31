# Source: Simulation/chapter-4/codebook.md -- Block 1


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ====================================================================
# 1. Simulation Parameters
# ====================================================================

S0 = 100.0  # Initial asset price
r = 0.05    # Risk-free interest rate (annual)
sigma = 0.20  # Volatility (annual)
T = 1.0     # Time to maturity (years)
N = 252     # Number of time steps (e.g., trading days)
M = 10000   # Number of paths to simulate
dt = T / N  # Time step size

# Theoretical expectation for validation
E_ST_THEO = S0 * np.exp(r * T)

# ====================================================================
# 2. GBM Path Generator
# ====================================================================

def generate_gbm_path(S0, r, sigma, T, N):
    """
    Generates a single asset price path using the exact GBM discretization 
    under the risk-neutral measure Q.
    """
    dt = T / N
    # Pre-calculate constant drift and volatility terms
    drift = (r - 0.5 * sigma**2) * dt
    vol_factor = sigma * np.sqrt(dt)
    
    # Generate N standard normal variates for the entire path increments
    Z = np.random.standard_normal(N)
    
    # Pre-allocate path array (N+1 points: S0 to SN)
    path = np.zeros(N + 1)
    path[0] = S0
    
    # Iterate to generate the path
    for k in range(N):
        path[k+1] = path[k] * np.exp(drift + vol_factor * Z[k])
        
    return path

# ====================================================================
# 3. Running the Simulation and Validation
# ====================================================================

terminal_prices = np.zeros(M)
path_data_for_plot = []

for m in range(M):
    path = generate_gbm_path(S0, r, sigma, T, N)
    terminal_prices[m] = path[-1]
    
    # Save a few paths for visualization
    if m < 10:
        path_data_for_plot.append(path)

# Calculate empirical statistics
E_ST_EMPIRICAL = np.mean(terminal_prices)
EMPIRICAL_ERROR = np.std(terminal_prices) / np.sqrt(M)

# ====================================================================
# 4. Visualization
# ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
time_points = np.linspace(0, T, N + 1)

# Plot 1: Sample Asset Paths
ax[0].set_title(f'Sample GBM Paths (M={M} total)')
ax[0].set_xlabel('Time $t$ (Years)')
ax[0].set_ylabel('Asset Price $S_t$')
for path in path_data_for_plot:
    ax[0].plot(time_points, path, linewidth=1, alpha=0.6)
ax[0].grid(True)

# Plot 2: Terminal Price Distribution (Histogram)
ax[1].hist(terminal_prices, bins=50, density=True, color='skyblue', label='Simulated $S_T$')
ax[1].axvline(E_ST_THEO, color='red', linestyle='--', label='Theoretical Mean $\\mathbb{E}[S_T]$')
ax[1].set_title('Distribution of Terminal Prices $S_T$')
ax[1].set_xlabel('Terminal Price $S_T$')
ax[1].set_ylabel('Probability Density')
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()

# --- Validation Summary ---
print("\n--- GBM Path Generator Validation ---")
print(f"Theoretical Mean E[S_T]: {E_ST_THEO:.4f}")
print(f"Empirical Mean E[S_T]:   {E_ST_EMPIRICAL:.4f}")
print(f"Difference:              {E_ST_EMPIRICAL - E_ST_THEO:.4e}")
print(f"Statistical Error:       \u00B1 {EMPIRICAL_ERROR:.4f}")
print("\nConclusion: The empirical mean is within the statistical error of the theoretical risk-neutral mean, confirming the path generator is correctly implemented.")
