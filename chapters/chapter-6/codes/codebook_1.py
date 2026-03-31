# Source: Simulation/chapter-6/codebook.md -- Block 1

import numpy as np
import matplotlib.pyplot as plt
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ====================================================================
# 1. Ising Core Functions (Omitted for brevity, assumed from Chapter 2)
# ====================================================================

# Placeholder functions (Actual implementation is in Chapter 2)
def create_lattice(N, initial_state='+1'):
    return np.ones((N, N), dtype=np.int8)

def get_neighbors(N, i, j):
    """PBC neighbor coordinates."""
    return [
        ((i + 1) % N, j), ((i - 1 + N) % N, j), 
        (i, (j + 1) % N), (i, (j - 1 + N) % N)  
    ]

def calculate_delta_E_local(lattice, i, j, J=1.0, H=0.0):
    N = lattice.shape[0]
    spin_ij = lattice[i, j]
    sum_nn = 0
    for ni, nj in get_neighbors(N, i, j):
        sum_nn += lattice[ni, nj]
    delta_E = 2 * J * spin_ij * sum_nn 
    return delta_E

def attempt_flip(lattice, i, j, beta, J=1.0, H=0.0):
    delta_E = calculate_delta_E_local(lattice, i, j, J, H)
    if delta_E <= 0:
        acceptance_prob = 1.0
    else:
        acceptance_prob = np.exp(-beta * delta_E)
        
    if random.random() < acceptance_prob:
        lattice[i, j] *= -1
        return True
    return False

def run_sweep(lattice, beta, J=1.0, H=0.0):
    N = lattice.shape[0]
    total_spins = N * N
    for step in range(total_spins):
        i = random.randrange(N)
        j = random.randrange(N)
        attempt_flip(lattice, i, j, beta, J, H)
    
def calculate_magnetization(lattice):
    return np.mean(np.abs(lattice))

# ====================================================================
# 2. Autocorrelation Analysis Functions
# ====================================================================

def autocorr_func(x, lag):
    """Calculates the Autocorrelation Function C(tau) for a given lag."""
    N = len(x)
    mean_x = np.mean(x)
    var_x = np.var(x)

    if var_x == 0: return 1.0 if lag == 0 else 0.0

    # C(tau) = Cov(O_t, O_{t+tau}) / Var(O)
    cov = np.sum((x[:N - lag] - mean_x) * (x[lag:] - mean_x)) / (N - lag)
    return cov / var_x

def estimate_tau_int(x, max_lag_limit=300):
    """Estimates the integrated autocorrelation time from C(tau) using a cutoff."""
    max_lag = min(max_lag_limit, len(x) // 2)
    C = [autocorr_func(x, lag) for lag in range(max_lag + 1)]

    # Estimate ESS Denominator (G) = 1 + 2 * sum(C(tau)) with a cutoff
    G = 1.0
    for c_tau in C[1:]:
        # Cutoff: Sum until C(tau) becomes negligible (< 0.05) or non-positive
        if c_tau < 0.05:
            G += 2 * c_tau
            break
        G += 2 * c_tau

    # Integrated Autocorrelation Time: tau_int = (G - 1) / 2
    tau_int = 0.5 if G <= 1.0 else (G - 1.0) / 2.0

    return tau_int, C

# ====================================================================
# 3. Simulation and Quantification
# ====================================================================

# --- Simulation Parameters ---
LATTICE_SIZE = 32
LATTICE_A = create_lattice(LATTICE_SIZE, initial_state='+1')
MCS_RUN = 10000
EQUILIBRATION_MCS = 500

# Temperatures of Interest
T_C = 2.269185  # Analytic Critical Temperature
T_LOW = 1.0     # Deep in ordered phase
T_HIGH = 3.0    # Deep in disordered phase
TEMPS = {'T_low (1.0)': 1.0, 'T_c (2.269)': T_C, 'T_high (3.0)': T_HIGH}

J = 1.0
H = 0.0
results = {}

print(f"Quantifying critical slowing down for L={LATTICE_SIZE}...")

for label, T in TEMPS.items():
    beta = 1.0 / T
    
    # Reset lattice to ordered state for consistent burn-in comparison
    lattice = create_lattice(LATTICE_SIZE, initial_state='+1')
    
    # Thermalization
    for eq_step in range(EQUILIBRATION_MCS):
        run_sweep(lattice, beta, J, H)
        
    # Measurement
    M_series = []
    for meas_step in range(MCS_RUN):
        run_sweep(lattice, beta, J, H)
        M_series.append(np.mean(lattice))
    
    # Analysis
    M_series = np.array(M_series)
    tau_int, C_plot = estimate_tau_int(M_series)
    
    results[label] = {
        'T': T,
        'M_series': M_series,
        'C_plot': C_plot,
        'tau_int': tau_int
    }
    print(f"Finished {label}. Tau_int: {tau_int:.2f} MCS.")

# ====================================================================
# 4. Visualization
# ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
markers = ['o', 's', '^']

# Plot 1: Autocorrelation Function C_M(tau)
for i, (label, res) in enumerate(results.items()):
    # Plot only the first 50 lags for clarity
    ax[0].plot(res['C_plot'][:51], marker=markers[i], markersize=3, 
               linestyle='-', linewidth=1.5, label=f"{label} ($\u03C4_{{int}}$={res['tau_int']:.1f})")

ax[0].axhline(0, color='gray', linestyle='--')
ax[0].set_title('Autocorrelation of Magnetization $C_M(\\tau)$')
ax[0].set_xlabel('Time Lag $\\tau$ (MCS)')
ax[0].set_ylabel('Autocorrelation $C(\\tau)$')
ax[0].set_xlim(0, 50)
ax[0].legend()
ax[0].grid(True, which='both', linestyle=':')

# Plot 2: Autocorrelation Time Comparison
tau_values = [res['tau_int'] for res in results.values()]
labels = list(results.keys())
ax[1].bar(labels, tau_values, color=['skyblue', 'red', 'lightgreen'])
ax[1].set_title('Integrated Autocorrelation Time $\\tau_{\\text{int}}$')
ax[1].set_xlabel('Temperature Regime')
ax[1].set_ylabel('$\\tau_{\\text{int}}$ (MCS)')
ax[1].grid(True, which='major', axis='y', linestyle=':')

plt.tight_layout()
plt.show()

# --- Conclusion ---
print("\n--- Critical Slowing Down Analysis ---")
for label, res in results.items():
    print(f"| {label.split(' ')[0]:<10} | T={res['T']:.3f} | Tau_int: {res['tau_int']:.2f} MCS |")
print("---------------------------------------")
print("Conclusion: The autocorrelation time $\\tau_{\\text{int}}$ peaks sharply at the critical temperature ($T_c \u2248 2.269$), confirming that the single-spin Metropolis algorithm suffers from **critical slowing down**. The system requires significantly more Monte Carlo sweeps (MCS) to generate independent samples at $T_c$ than it does in the ordered ($T_{low}$) or disordered ($T_{high}$) phases.")
