# Source: Simulation/chapter-1/codebook.md -- Block 3

import numpy as np
import random
import matplotlib.pyplot as plt

# ====================================================================
# 1. MCMC Setup (Re-run well-mixed case from Project 2)
# ====================================================================

# Potential and Target PDF (re-defined for completeness)
def potential_V(x):
    return x**4 - 2*x**2 + 1

def target_pdf(x, beta):
    return np.exp(-beta * potential_V(x))

def metropolis_accept(P_old, P_new):
    if P_old == 0:
        return True
    return random.uniform(0, 1) <= min(1.0, P_new / P_old)

# MCMC Parameters
TOTAL_STEPS = 100000
BETA = 1.0  # High T, well-mixed case
BURN_IN = 5000
DELTA_RANGE = 0.5

# Run the simulation
def run_metropolis_simulation(beta, total_steps, delta_range):
    current_x = -1.0
    positions = np.zeros(total_steps)
    current_P = target_pdf(current_x, beta)

    for t in range(total_steps):
        delta = random.uniform(-delta_range, delta_range)
        proposed_x = current_x + delta
        proposed_P = target_pdf(proposed_x, beta)

        if metropolis_accept(current_P, proposed_P):
            current_x = proposed_x
            current_P = proposed_P

        positions[t] = current_x

    return positions

# Get the well-mixed chain after burn-in
full_chain = run_metropolis_simulation(BETA, TOTAL_STEPS, DELTA_RANGE)
chain = full_chain[BURN_IN:]
N_samples = len(chain)
N_total = TOTAL_STEPS

# ====================================================================
# 2. Autocorrelation and ESS Calculation
# ====================================================================

def autocorr_func(x, lag):
    """Calculates the Autocorrelation Function C(tau) for a given lag."""
    N = len(x)
    mean_x = np.mean(x)
    var_x = np.var(x)

    if var_x == 0:
        return 1.0 if lag == 0 else 0.0

    cov = np.sum((x[:N - lag] - mean_x) * (x[lag:] - mean_x)) / (N - lag)
    return cov / var_x

def estimate_tau_int(x, max_lag_limit=500):
    """Estimates the integrated autocorrelation time from C(tau)."""
    max_lag = min(max_lag_limit, len(x) // 2)
    C = [autocorr_func(x, lag) for lag in range(max_lag + 1)]

    tau_int = 0.5
    for c_tau in C[1:]:
        if c_tau < 0.0:
            break
        if c_tau < 0.05:
            tau_int += c_tau * 2
            break
        tau_int += c_tau

    ess_denom = 1.0
    for c_tau in C[1:]:
        if c_tau < 0.05:
            ess_denom += 2 * c_tau
            break
        ess_denom += 2 * c_tau

    final_tau_int = 0.5 if ess_denom <= 1.0 else (ess_denom - 1.0) / 2.0
    C_plot = [autocorr_func(x, lag) for lag in range(max_lag + 1)]

    return final_tau_int, C_plot

# Compute tau_int and ACF
tau_int, C_plot = estimate_tau_int(chain)

# Calculate ESS
ESS = N_samples / (1.0 + 2.0 * tau_int)

# ====================================================================
# 3. Visualization and Analysis
# ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 4))

# Plot 1: Autocorrelation Function
ax[0].plot(C_plot, marker='o', markersize=3, linestyle='-', linewidth=1)
ax[0].axhline(0, color='gray', linestyle='--')
ax[0].axvline(tau_int, color='red', linestyle='--', label=f'$\\tau_{{\\text{{int}}}} \\approx {tau_int:.2f}$')
ax[0].set_title('Autocorrelation Function $C(\\tau)$ of $x_t$')
ax[0].set_xlabel('Time Lag $\\tau$ (steps)')
ax[0].set_ylabel('Autocorrelation $C(\\tau)$')
ax[0].set_xlim(0, 50)
ax[0].legend()
ax[0].grid(True, which='both', linestyle=':')

# Plot 2: ESS Bar Chart
ax[1].bar(['Total Samples ($N$)', 'Effective Samples (ESS)'], [N_samples, ESS], color=['darkblue', 'teal'])
ax[1].set_title('MCMC Sampling Efficiency')
ax[1].set_ylabel('Sample Count')
ax[1].text(0, N_samples * 0.9, f'{N_total} total steps', ha='center', color='white', fontweight='bold')
ax[1].text(1, ESS * 0.8, f'ESS $\\approx {ESS:.0f}$', ha='center', color='white', fontweight='bold')

plt.tight_layout()
plt.show()

# Final Analysis
print("\n--- Efficiency Analysis Summary ---")
print(f"Total Correlated Samples (N): {N_samples}")
print(f"Integrated Autocorrelation Time (tau_int): {tau_int:.2f} steps")
print(f"Effective Sample Size (ESS): {ESS:.0f}")
print(f"Efficiency Factor (ESS/N): {ESS/N_samples:.2f}")

print("\nConclusion: The MCMC chain, though well-mixed, generates correlated samples, evidenced by the non-zero autocorrelation at $\\tau > 0$. The integrated autocorrelation time $\\tau_{\\text{int}}$ indicates that roughly 4 to 5 steps are needed for samples to become statistically independent. Consequently, the Effective Sample Size (ESS) is significantly less than the total number of collected samples $N$, confirming the inherent correlation in sequential MCMC sampling.")
