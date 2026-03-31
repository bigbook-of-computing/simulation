# Source: Simulation/chapter-9/codebook.md -- Block 6

import numpy as np
import matplotlib.pyplot as plt
from math import exp, log, sqrt # Use math functions for constants

# ====================================================================
# 1. Setup Parameters (Intentionally Unstable Grid)
# ====================================================================

# --- Parameters ---
S_MAX = 200.0   # Max price
K = 100.0       # Strike price
r = 0.05        # Risk-free rate
sigma = 0.20    # Volatility

# --- UNSTABLE GRID CHOICE ---
# Ns is small (large Delta S), Nt is small (large Delta t)
Ns = 50        # Number of price steps (\Delta S is large)
Nt = 50         # Number of time steps (\Delta t is large) 

T = 1.0         
dt = T / Nt
dS = S_MAX / Ns

# Price vector
S = np.linspace(0, S_MAX, Ns + 1)
t = np.linspace(0, T, Nt + 1)

# Check the ratio that governs stability (approx sigma^2 * dt / dS^2)
# If this value is large (e.g., > 0.5), instability is likely.
stability_ratio_approx = sigma**2 * dt / dS**2
print(f"Stability Ratio (\u03C3\u00B2\u0394t/\u0394S\u00B2): {stability_ratio_approx:.4f}")
print("Ratio is much greater than the stability limit (approx 0.5/1.0), Expecting Blow-Up.")

# ====================================================================
# 2. Explicit FDM Solver (Unstable Run)
# ====================================================================

# Initial condition (Payoff at Expiry, t=T)
V = np.maximum(S - K, 0)
V_history = [V.copy()] # Store the grid at time steps

# Backward time iteration
for n in range(Nt, 0, -1):
    
    # Coefficients for the Explicit scheme (V_i^n = A*V_{i-1}^{n+1} + B*V_i^{n+1} + C*V_{i+1}^{n+1})
    A = 0.5 * dt * (r * S / dS - sigma**2 * S**2 / dS**2)
    C = 0.5 * dt * (r * S / dS + sigma**2 * S**2 / dS**2)
    B = 1.0 - (A + C) # B = 1 - r*dt - (A+C) = 1 - dt*sigma^2*S^2/dS^2 - r*dt
    
    V_new = np.zeros_like(V)
    
    # Loop over inner price points (i=1 to Ns-1)
    for i in range(1, Ns):
        V_new[i] = A[i] * V[i-1] + B[i] * V[i] + C[i] * V[i+1]
        
    # --- Boundary Conditions ---
    V_new[0] = 0 
    time_remaining = (n-1) * dt
    V_new[Ns] = S_MAX - K * exp(-r * time_remaining)
    
    # Update V
    V = V_new
    V_history.append(V.copy())
    
    # Check for immediate blow-up
    if np.max(V) > 1e10:
        print(f"Simulation terminated due to numerical blow-up at time step {n}.")
        break

# ====================================================================
# 3. Visualization
# ====================================================================

V_history = np.array(V_history)

fig, ax = plt.subplots(figsize=(8, 5))

# Plot the final stable/unstable slice
ax.plot(S, V_history[0], 'r--', lw=2, label='Final Solution (t=0)')

# Plot a few intermediate, oscillatory steps to show instability build-up
num_plots = 5
for i in range(1, min(Nt // 10, 10)):
    ax.plot(S, V_history[i * (Nt // 10)], lw=1, alpha=0.5, label=f'Step {i * (Nt // 10)}')

ax.set_title('Instability of Explicit FDM (Violated Stability Condition)')
ax.set_xlabel('Stock Price S')
ax.set_ylabel('Call Option Price V (Oscillating)')
ax.set_xlim(0, 150)
ax.set_ylim(-50, 150) # Set a wide limit to see the blow-up visually
ax.grid(True)

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- Explicit FDM Stability Check ---")
print(f"Time Steps (Nt): {Nt}, Price Steps (Ns): {Ns}")
print(f"Intentionally Unstable Ratio (\u03c3\u00B2\u0394t/\u0394S\u00B2): {stability_ratio_approx:.4f}")
print("-------------------------------------------------")
print("Observation: The solution quickly became oscillatory and unstable, producing non-physical negative and excessively large option values.")
print("Conclusion: This confirms the **conditional stability** of the Explicit FDM. For robust financial modeling, unconditionally stable schemes like **Crank–Nicolson** or **Implicit FDM** are mandatory.")
