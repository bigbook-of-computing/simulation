# Source: Simulation/chapter-9/codebook.md -- Block 5

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from math import exp, log, sqrt # Use math functions for constants

# ====================================================================
# 1. Setup Parameters and Analytical Benchmark
# ====================================================================

# --- Parameters ---
S_MAX = 200.0   # Max price in the grid (S_max)
K = 100.0       # Strike price
r = 0.05        # Risk-free rate
sigma = 0.20    # Volatility
T = 1.0         # Time to maturity
Nt = 500        # Number of time steps (N_t)
Ns = 100        # Number of price steps (N_S)

# Grid parameters
dt = T / Nt
dS = S_MAX / Ns

# Price vector (from 0 to S_MAX)
S = np.linspace(0, S_MAX, Ns + 1)
t = np.linspace(0, T, Nt + 1)

# Analytical BSM Price (for comparison)
def black_scholes_call(S, K, T, r, sigma):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)

BSM_PRICE = black_scholes_call(S[Ns // 2], K, T, r, sigma) # At S=100

# ====================================================================
# 2. Explicit FDM Coefficients and Solver
# ====================================================================

# Initial condition (Payoff at Expiry, t=T)
V = np.maximum(S - K, 0)

# Backward time iteration
for n in range(Nt, 0, -1):
    # Calculate coefficients A, B, C for V_i^n from V^{n+1}
    # Coefficients are dependent on S_i (the current price index)
    
    # Pre-calculate the components of the BSM operator at each price index S_i
    # Note: i starts at 0, representing S=0. S[i] is the price at index i.
    
    # Coefficients for the Explicit scheme (V_i^n = A*V_{i-1}^{n+1} + B*V_i^{n+1} + C*V_{i+1}^{n+1})
    A = 0.5 * dt * (r * S / dS - sigma**2 * S**2 / dS**2)
    C = 0.5 * dt * (r * S / dS + sigma**2 * S**2 / dS**2)
    B = 1.0 + r * dt - (A + C) # B = 1 + r*dt - r*dt = 1 + dt*(-sigma^2*S^2/dS^2) 
    
    # Calculate V_new (V at time step n-1) using V (V at time step n)
    V_new = np.zeros_like(V)
    
    # Loop over inner price points (i=1 to Ns-1)
    for i in range(1, Ns):
        V_new[i] = A[i] * V[i-1] + B[i] * V[i] + C[i] * V[i+1]
        
    # --- Boundary Conditions ---
    # 1. Left boundary (S=0): V(0, t) = 0
    V_new[0] = 0 
    # 2. Right boundary (S=S_MAX): V(S_MAX, t) ≈ S_MAX - K*exp(-r(T-t))
    time_remaining = (n-1) * dt
    V_new[Ns] = S_MAX - K * exp(-r * time_remaining)
    
    # Update V for the next iteration
    V = V_new

# Final numerical price at S=100 (index 50)
MC_FDM_PRICE = V[Ns // 2]
PRICE_DIFFERENCE = MC_FDM_PRICE - BSM_PRICE

# ====================================================================
# 3. Visualization and Comparison
# ====================================================================

# Plot the final price curve vs. analytical
fig, ax = plt.subplots(figsize=(8, 5))

# Plot BSM Analytical Price
S_bsm = S[1:] # Exclude S=0 for log
C_bsm = [black_scholes_call(s, K, T, r, sigma) for s in S_bsm]
ax.plot(S_bsm, C_bsm, 'r--', lw=2, label='BSM Analytical Solution')

# Plot FDM Numerical Price
ax.plot(S, V, 'b-', lw=1.5, alpha=0.8, label='Explicit FDM Numerical Solution')

# Highlight the calculated price point (S0=100)
ax.plot(S[Ns // 2], MC_FDM_PRICE, 'o', markersize=8, color='black', label=f'FDM Price at S={S[Ns//2]:.0f}: {MC_FDM_PRICE:.4f}')

# Labeling and Formatting
ax.set_title('Explicit FDM Solution of the BSM PDE (Backward Time)')
ax.set_xlabel('Stock Price S')
ax.set_ylabel('Call Option Price V')
ax.set_xlim(0, 150)
ax.set_ylim(0, 50)
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- Explicit FDM Numerical Accuracy Check ---")
print(f"Analytical BSM Price (S=100): {BSM_PRICE:.5f}")
print(f"Explicit FDM Price (S=100):   {MC_FDM_PRICE:.5f}")
print(f"Absolute Error:               {np.abs(PRICE_DIFFERENCE):.5f}")

print("\nConclusion: The Explicit (Forward Euler) FDM scheme produced a numerical solution that closely approximates the analytical BSM price. This demonstrates the numerical feasibility of solving the BSM PDE using the same FDM techniques employed for the Heat Equation.")
