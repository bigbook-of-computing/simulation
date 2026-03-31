# Source: Simulation/chapter-9/codebook.md -- Block 3

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D # Required for 3D plotting

# ====================================================================
# 1. BSM Analytical Formula
# ====================================================================

def black_scholes_call(S, K, tau, r, sigma):
    """Calculates BSM Call price for time to maturity tau."""
    if tau <= 0:
        return np.maximum(S - K, 0)
    
    # Ensure tau is not zero for calculations
    tau_safe = np.maximum(tau, 1e-10) 
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * tau_safe) / (sigma * np.sqrt(tau_safe))
    d2 = d1 - sigma * np.sqrt(tau_safe)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * tau_safe) * norm.cdf(d2)
    return call_price

# ====================================================================
# 2. Data Grid Setup
# ====================================================================

# --- Parameters ---
K = 100.0
r = 0.05
sigma = 0.20
T_MAX = 1.0 # Max time to maturity

# Create the grid for the 3D plot
S_mesh = np.linspace(50, 150, 50)  # Stock Price range
Tau_mesh = np.linspace(1e-10, T_MAX, 50) # Time to Maturity range (avoiding exactly 0)

S_grid, Tau_grid = np.meshgrid(S_mesh, Tau_mesh)

# Calculate the Option Price Z-axis (C) for every point in the grid
C_grid = black_scholes_call(S_grid, K, Tau_grid, r, sigma)

# ====================================================================
# 3. Visualization (3D Surface Plot)
# ====================================================================

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surface = ax.plot_surface(S_grid, Tau_grid, C_grid, cmap='viridis', edgecolor='none')

# Labeling and Formatting
ax.set_title('Black–Scholes PDE Solution Surface $C(S, \\tau)$')
ax.set_xlabel('Stock Price S')
ax.set_ylabel('Time to Maturity $\\tau$ (Years)')
ax.set_zlabel('Option Price C')

# Add a color bar
fig.colorbar(surface, shrink=0.5, aspect=5, label='Option Price')

# Set view angle for better visualization
ax.view_init(elev=20, azim=-120)

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- Analysis of the Black–Scholes Price Surface ---")
print("The 3D surface plot represents the solution C(S, \u03c4) to the BSM PDE.")
print("\nKey features observed:")
print("1. Boundary Condition: At \u03c4 \u2248 0 (Maturity), the surface approaches the payoff max(S - K, 0).")
print("2. Convexity: The curvature (\u0393) is highest when S \u2248 K and \u03c4 is small.")
print("3. Time Value: The price is always positive before maturity (\u03c4 > 0), even when S < K, due to the time value of money and volatility.")
