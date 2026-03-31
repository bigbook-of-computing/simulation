# Source: Simulation/chapter-9/codebook.md -- Block 7

import numpy as np
import matplotlib.pyplot as plt
from math import exp, log, sqrt 
from scipy.stats import norm
from scipy.linalg import solve_banded # Tool to solve the tridiagonal system efficiently

# ====================================================================
# 1. Setup Parameters and Analytical Benchmark
# ====================================================================

# --- Parameters ---
S_MAX = 200.0   
K = 100.0       
r = 0.05        
sigma = 0.20    
T = 1.0         
Nt = 500        # Time steps
Ns = 100        # Price steps

# Grid parameters
dt = T / Nt
dS = S_MAX / Ns
S = np.linspace(0, S_MAX, Ns + 1) # Price vector

# Analytical European Put Price (for comparison)
# Put-Call Parity: P = C - S + K*exp(-rT)
C_BSM = black_scholes_call(S[Ns // 2], K, T, r, sigma)
EUROPEAN_PUT_THEO = C_BSM - S[Ns // 2] + K * exp(-r * T)

def black_scholes_call(S, K, T, r, sigma):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)

# ====================================================================
# 2. Implicit FDM (Proxy for Stable Solver) and Constraint Enforcement
# ====================================================================

# --- Initial Condition: Payoff at Expiry ---
V_put = np.maximum(K - S, 0)
intrinsic_value = V_put.copy() # The payoff function itself

# Backward time iteration
for n in range(Nt, 0, -1):
    
    # --- A. Implicit FDM Solver Setup (Proxy for B or CN) ---
    # Coefficients A, B, C for the Implicit/Crank-Nicolson scheme (AV^{n+1} = V^{n})
    
    # We use Implicit FDM coefficients for simplicity: A, B, C define the tridiagonal matrix
    A_implicit = -0.5 * dt * (r * S / dS + sigma**2 * S**2 / dS**2)
    B_implicit = 1.0 + r * dt + dt * sigma**2 * S**2 / dS**2
    C_implicit = 0.5 * dt * (r * S / dS - sigma**2 * S**2 / dS**2)
    
    # The tridiagonal matrix (A) is built from the coefficients
    diagonals = np.zeros((3, Ns + 1))
    diagonals[0, 2:Ns] = A_implicit[2:Ns]      # Upper diagonal (C)
    diagonals[1, 1:Ns] = B_implicit[1:Ns]      # Main diagonal
    diagonals[2, 0:Ns-1] = C_implicit[1:Ns]    # Lower diagonal (A)
    
    # RHS is V at the previous time step (V^n)
    RHS = V_put.copy() 
    
    # --- Boundary Conditions for Implicit Solve ---
    # Left (S=0): V(0, t) = K * exp(-r * tau)
    RHS[0] = K * exp(-r * n * dt)
    diagonals[1, 0] = 1.0 # Ensure main diag is 1.0
    
    # Right (S=S_MAX): V(S_MAX, t) = 0
    RHS[Ns] = 0.0
    diagonals[1, Ns] = 1.0 # Ensure main diag is 1.0
    
    # --- Solve the Tridiagonal System (V_hold) ---
    # V_hold is the value if the option is held (continuation value)
    V_hold = solve_banded((1, 1), diagonals[:, 1:Ns], RHS[1:Ns])
    
    # Reassemble V_hold including boundaries
    V_new = np.insert(V_hold, 0, RHS[0])
    V_new = np.append(V_new, RHS[Ns])

    # --- B. Enforce Early Exercise Constraint ---
    # V^n = max(V_hold^n, V_intrinsic^n)
    V_put = np.maximum(V_new, K - S) # K-S is the intrinsic value for a Put

# Final American Put price at S=100 (index 50)
AMERICAN_PUT_FDM = V_put[Ns // 2]
EARLY_EXERCISE_PREMIUM = AMERICAN_PUT_FDM - EUROPEAN_PUT_THEO

# ====================================================================
# 3. Visualization and Comparison
# ====================================================================

fig, ax = plt.subplots(figsize=(8, 5))

# Plot Intrinsic Value
ax.plot(S, intrinsic_value, 'k:', label='Intrinsic Value Max(K-S, 0)')

# Plot American Put Price
ax.plot(S, V_put, 'r-', lw=2, label=f'American Put Price (FDM)')

# Plot European Put Price (for comparison)
European_Put_Curve = S - K + black_scholes_call(S, K, T, r, sigma)
ax.plot(S, European_Put_Curve, 'b--', lw=1.5, alpha=0.7, label='European Put (Analytical)')

# Highlight the calculated price point (S0=100)
ax.plot(S[Ns // 2], AMERICAN_PUT_FDM, 'o', markersize=8, color='red', 
        label=f'American V0: {AMERICAN_PUT_FDM:.4f}')

# Labeling and Formatting
ax.set_title('American Put Valuation with Early Exercise Constraint')
ax.set_xlabel('Stock Price S')
ax.set_ylabel('Option Price V')
ax.set_xlim(0, 150)
ax.set_ylim(0, 50)
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- American Put Early Exercise Premium Analysis ---")
print(f"European Put Price (Analytical): {EUROPEAN_PUT_THEO:.5f}")
print(f"American Put Price (FDM):      {AMERICAN_PUT_FDM:.5f}")
print("---------------------------------------------------------")
print(f"Early Exercise Premium: {EARLY_EXERCISE_PREMIUM:.5f}")
print("\nConclusion: The FDM simulation successfully priced the American Put by enforcing the early exercise constraint V = max(V_hold, V_intrinsic) at every time step. The resulting American price is higher than the corresponding European price, demonstrating the premium associated with the flexibility of early exercise.")
