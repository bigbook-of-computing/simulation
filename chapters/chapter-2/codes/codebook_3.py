# Source: Simulation/chapter-2/codebook.md -- Block 3


import numpy as np
import matplotlib.pyplot as plt
import random

# ====================================================================
# 1. MCMC Setup (Re-run well-mixed case from Project 2)
# ====================================================================

# Potential and Metropolis Functions (J=1, H=0 assumed)
def get_neighbors(N, i, j):
    """PBC neighbor coordinates."""
    return [
        ((i + 1) % N, j), 
        ((i - 1 + N) % N, j), 
        (i, (j + 1) % N), 
        (i, (j - 1 + N) % N)  
    ]

def calculate_delta_E_local(lattice, i, j, J=1.0, H=0.0):
    """O(1) Delta E calculation for a single spin flip."""
    N = lattice.shape[0]
    spin_ij = lattice[i, j]
    sum_nn = 0
    for ni, nj in get_neighbors(N, i, j):
        sum_nn += lattice[ni, nj]
    
    delta_E = 2 * J * spin_ij * sum_nn 
    if H != 0.0:
        delta_E += 2 * H * spin_ij
        
    return delta_E

def attempt_flip(lattice, i, j, beta, J=1.0, H=0.0):
    """Metropolis acceptance rule."""
    delta_E = calculate_delta_E_local(lattice, i, j, J, H)
    
    if delta_E <= 0:
        acceptance_prob = 1.0
    else:
        acceptance_prob = np.exp(-beta * delta_E)
        
    if random.random() < acceptance_prob:
        lattice[i, j] *= -1
        return True
    return False

def calculate_total_energy(lattice, J=1.0, H=0.0):
    """
    Calculates the total energy E(sigma) for the whole lattice.
    Each bond is counted once.
    """
    N = lattice.shape[0]
    E = 0
    
    for i in range(N):
        for j in range(N):
            spin_ij = lattice[i, j]
            
            # Interaction Term: Only count Right and Down bonds to avoid double-counting
            # E_bond contribution: -J * sigma_i * sum(sigma_neighbors)
            E -= J * spin_ij * (lattice[(i + 1) % N, j] + lattice[i, (j + 1) % N])
            
            # External Field Term (often E_field = -H * M_total)
            E -= H * spin_ij
            
    return E

def run_simulation_and_measure(beta, N, J, H, eq_mcs, meas_mcs):
    """Runs MCMC and records observables."""
    current_lattice = np.ones((N, N), dtype=np.int8)

    # Thermalization (Burn-in)
    for eq_step in range(eq_mcs):
        run_sweep(current_lattice, beta, J, H)
        
    # Measurement Phase
    energies = []
    for meas_step in range(meas_mcs):
        run_sweep(current_lattice, beta, J, H)
        E = calculate_total_energy(current_lattice, J, H)
        energies.append(E)
        
    return np.array(energies)

def run_sweep(lattice, beta, J, H):
    """Performs one Monte Carlo Sweep (MCS)."""
    N = lattice.shape[0]
    total_spins = N * N
    
    for step in range(total_spins):
        i = random.randrange(N)
        j = random.randrange(N)
        attempt_flip(lattice, i, j, beta, J, H)

# --- Simulation Parameters ---
LATTICE_SIZE = 32
BETA = 1.0  # High T, well-mixed case
J_COUPLING = 1.0
H_FIELD = 0.0
EQUILIBRATION_MCS = 1000
MEASUREMENT_MCS = 20000 # Total steps for measurement

# Run simulation and get the energy time series
print(f"Running MCMC simulation for autocorrelation analysis (L={LATTICE_SIZE}, $\u03B2$={BETA})...")
energy_series = run_simulation_and_measure(
    BETA, LATTICE_SIZE, J_COUPLING, H_FIELD, EQUILIBRATION_MCS, MEASUREMENT_MCS
)
N_meas = len(energy_series)

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

    # Calculate covariance for lag tau: C(tau) = Cov(O_t, O_{t+tau}) / Var(O)
    cov = np.sum((x[:N - lag] - mean_x) * (x[lag:] - mean_x)) / (N - lag)
    return cov / var_x

def estimate_tau_int_and_acf(x, max_lag_limit=500):
    """Estimates the integrated autocorrelation time and computes ACF for plotting."""
    
    max_lag = min(max_lag_limit, len(x) // 2)
    C = [autocorr_func(x, lag) for lag in range(max_lag + 1)]

    # ESS Denominator (G) = 1 + 2 * sum(C(tau)) with a cutoff
    ess_denom = 1.0
    for c_tau in C[1:]:
        # Cutoff: Sum until C(tau) becomes negligible (e.g., < 0.05) or non-positive
        if c_tau < 0.05:
            ess_denom += 2 * c_tau
            break
        ess_denom += 2 * c_tau

    # Calculate integrated autocorrelation time: tau_int = (G - 1) / 2
    final_tau_int = 0.5 if ess_denom <= 1.0 else (ess_denom - 1.0) / 2.0

    return final_tau_int, C

# Compute tau_int and ACF
tau_int, C_plot = estimate_tau_int_and_acf(energy_series)

# Calculate ESS
ESS = N_meas / (1.0 + 2.0 * tau_int)

# ====================================================================
# 3. Visualization and Analysis
# ====================================================================

# Plot 1: Autocorrelation Function
fig, ax = plt.subplots(1, 2, figsize=(12, 4))

ax[0].plot(C_plot, marker='o', markersize=3, linestyle='-', linewidth=1)
ax[0].axhline(0, color='gray', linestyle='--')
ax[0].axvline(tau_int, color='red', linestyle='--', label=f'$\\tau_{{\\text{{int}}}} \\approx {tau_int:.2f}$')
ax[0].set_title('Autocorrelation Function $C_E(\\tau)$ for Energy')
ax[0].set_xlabel('Time Lag $\\tau$ (MCS)')
ax[0].set_ylabel('Autocorrelation $C(\\tau)$')
ax[0].set_xlim(0, 50)
ax[0].legend()
ax[0].grid(True, which='both', linestyle=':')

# Plot 2: ESS Bar Chart
ax[1].bar(['Total Samples ($N$)', 'Effective Samples (ESS)'], [N_meas, ESS], color=['darkblue', 'teal'])
ax[1].set_title('MCMC Sampling Efficiency (Energy)')
ax[1].set_ylabel('Sample Count')
ax[1].text(0, N_meas * 0.9, f'{MEASUREMENT_MCS} sweeps', ha='center', color='white', fontweight='bold')
ax[1].text(1, ESS * 0.8, f'ESS $\\approx {ESS:.0f}$', ha='center', color='white', fontweight='bold')

plt.tight_layout()
plt.show()

print(f"\n--- Efficiency Analysis Summary (Energy) ---")
print(f"Total Correlated Samples (N_meas): {N_meas}")
print(f"Integrated Autocorrelation Time (tau_int): {tau_int:.2f} MCS")
print(f"Effective Sample Size (ESS): {ESS:.0f}")
print(f"Efficiency Factor (ESS/N_meas): {ESS/N_meas:.2f}")

print(f"\nConclusion: The integrated autocorrelation time $\\tau_{{\\text{{int}}}}$ is approximately {tau_int:.2f} Monte Carlo Sweeps. This means that to get one statistically independent sample, the simulation must run for about {tau_int:.0f} sweeps. This correlation drastically reduces the Effective Sample Size (ESS) to only {ESS:.0f}, confirming that the sequential nature of MCMC yields highly dependent data points, which must be corrected for when calculating error bars.")
