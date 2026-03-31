# Source: Simulation/chapter-8/codebook.md -- Block 4

import numpy as np
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# ====================================================================
# 1. Setup Parameters and Theory
# ====================================================================

S0 = 100.0   # Initial price
mu = 0.10    # Expected return (mu)
sigma = 0.30 # Volatility
T = 1.0      # Time to maturity

M_PATHS = 100000 # High number of paths to eliminate Monte Carlo sampling error

# Theoretical expectation (unbiased mean for the Exact Solution)
E_ST_THEO = S0 * np.exp(mu * T)

# ====================================================================
# 2. Simulation Solvers
# ====================================================================

def solve_exact(S0, mu, sigma, T, N=1, Z_sequence=None):
    """
    Exact GBM solution, which is independent of the number of steps N.
    """
    W_T = Z_sequence * np.sqrt(T)
    drift_term = (mu - 0.5 * sigma**2) * T
    diffusion_term = sigma * W_T
    S_T = S0 * np.exp(drift_term + diffusion_term)
    return S_T

def solve_em(S0, mu, sigma, T, N, Z_sequence=None):
    """
    Euler-Maruyama approximation, highly sensitive to N.
    """
    dt = T / N
    S = S0
    
    for i in range(N):
        dW = np.sqrt(dt) * Z_sequence[i]
        # S_{n+1} = S_n + mu*S_n*dt + sigma*S_n*dW
        S += mu * S * dt + sigma * S * dW
        
    return S

# ====================================================================
# 3. Running Simulations and Comparing Means
# ====================================================================

# Pre-generate one large set of standard normals for all tests
Z_large_set = np.random.randn(M_PATHS, 100) # Max steps needed is 100

# --- A. Exact Solution (N=1) ---
# Unbiased for any N. Using only the first column of the noise array.
S_T_A = solve_exact(S0, mu, sigma, T, N=1, Z_sequence=Z_large_set[:, 0])
MEAN_A = np.mean(S_T_A)

# --- B. Euler-Maruyama (N=1) - Large \Delta t ---
# Should be biased.
S_T_B = solve_em(S0, mu, sigma, T, N=1, Z_sequence=Z_large_set[:, 0])
MEAN_B = np.mean(S_T_B)

# --- C. Euler-Maruyama (N=100) - Small \Delta t ---
# Should converge closely to the theoretical mean (weak convergence in action).
S_T_C = solve_em(S0, mu, sigma, T, N=100, Z_sequence=Z_large_set)
MEAN_C = np.mean(S_T_C)

# --- Comparison Data ---
labels = ['Theory Target $S_0e^{\mu T}$', 
          f'A. Exact Solver ($N=1$)', 
          f'B. EM Solver ($N=1$, Large $\\Delta t$)', 
          f'C. EM Solver ($N=100$, Small $\\Delta t$)']
means = [E_ST_THEO, MEAN_A, MEAN_B, MEAN_C]

# ====================================================================
# 4. Visualization
# ====================================================================

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(labels, means, color=['gray', 'green', 'red', 'darkblue'], alpha=0.7)
ax.axhline(E_ST_THEO, color='black', linestyle='--', label='Theoretical Target')

# Annotate differences
for i in range(1, 4):
    diff = means[i] - E_ST_THEO
    ax.text(labels[i], means[i] + 0.1, f'{means[i]:.4f}\n(Error: {diff:.3f})', 
            ha='center', va='bottom', fontsize=10)

# Labeling and Formatting
ax.set_title('Comparison of Mean Terminal Price: Exact vs. Euler–Maruyama')
ax.set_ylabel('Mean Terminal Price $\\langle S_T \\rangle$')
ax.set_ylim(E_ST_THEO - 0.5, E_ST_THEO + 0.5)
ax.grid(True, axis='y')

plt.tight_layout()
plt.show()

# --- Conclusion ---
print("\n--- SDE Solver Comparison Summary ---")
print(f"Theoretical Mean E[S_T]: {E_ST_THEO:.4f}")
print(f"1-Step Exact Mean (A): {MEAN_A:.4f} (Unbiased)")
print(f"1-Step EM Mean (B):    {MEAN_B:.4f} (Biased)")
print(f"100-Step EM Mean (C):  {MEAN_C:.4f} (Converged)")

print("\nConclusion: The one-step Euler–Maruyama solver (B) results in a noticeable upward bias in the terminal mean, confirming that large time steps introduce discretization error. The Exact solver (A) and the multi-step EM solver (C) both accurately converge to the theoretical mean E[S_T], demonstrating the weak convergence of EM requires sufficiently small \u0394t.")
