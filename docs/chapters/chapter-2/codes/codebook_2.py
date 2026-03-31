# Source: Simulation/chapter-2/codebook.md -- Block 2

import numpy as np
import matplotlib.pyplot as plt
import random

# ====================================================================
# 1. Setup Functions (from Project 1)
# ====================================================================

# Potential and Metropolis Functions (simplified for this context: J=1, H=0)
def get_neighbors(N, i, j):
    """PBC neighbor coordinates."""
    return [
        ((i + 1) % N, j), 
        ((i - 1 + N) % N, j), 
        (i, (j + 1) % N), 
        (i, (j - 1 + N) % N)  
    ]

def calculate_delta_E(lattice, i, j, J=1.0, H=0.0):
    """O(1) Delta E calculation for J=1, H=0."""
    N = lattice.shape[0]
    spin_ij = lattice[i, j]
    sum_nn = 0
    for ni, nj in get_neighbors(N, i, j):
        sum_nn += lattice[ni, nj]
    
    # Delta E = 2 * J * spin_ij * sum_nn
    delta_E = 2 * J * spin_ij * sum_nn 
    
    # Add external field term if H != 0, but H=0 here
    if H != 0.0:
        delta_E += 2 * H * spin_ij
        
    return delta_E

def attempt_flip(lattice, i, j, beta, J=1.0, H=0.0):
    """Metropolis acceptance rule."""
    delta_E = calculate_delta_E(lattice, i, j, J, H)
    
    if delta_E <= 0:
        acceptance_prob = 1.0
    else:
        acceptance_prob = np.exp(-beta * delta_E)
        
    if random.random() < acceptance_prob:
        lattice[i, j] *= -1
        return True
    return False

def run_sweep(lattice, beta, J=1.0, H=0.0):
    """Performs one Monte Carlo Sweep (MCS)."""
    N = lattice.shape[0]
    total_spins = N * N
    
    for step in range(total_spins):
        i = random.randrange(N)
        j = random.randrange(N)
        attempt_flip(lattice, i, j, beta, J, H)

def calculate_magnetization(lattice):
    """Calculates the absolute magnetization per spin |M|."""
    return np.mean(np.abs(lattice))

# ====================================================================
# 2. Temperature Sweep Simulation
# ====================================================================

# --- Simulation Parameters ---
LATTICE_SIZE = 32
TEMP_MIN = 1.0
TEMP_MAX = 4.0
TEMP_STEP = 0.1
EQUILIBRATION_MCS = 1000
MEASUREMENT_MCS = 5000
J_COUPLING = 1.0
H_FIELD = 0.0

# Critical inverse temperature: beta_c approx 0.4407
BETA_CRITICAL = 0.4407

# Inverse temperatures to sweep
betas = np.arange(1/TEMP_MAX, 1/TEMP_MIN + TEMP_STEP, TEMP_STEP)
temperatures = 1.0 / betas

# Storage for results
avg_magnetizations = []

# --- Main Sweep ---
# Initialize a single lattice, which will be re-used (sequential sweep)
current_lattice = np.ones((LATTICE_SIZE, LATTICE_SIZE), dtype=np.int8)

print(f"Starting sweep for L={LATTICE_SIZE}...")

for beta in betas:
    
    # 1. Thermalization (Equilibration)
    for eq_step in range(EQUILIBRATION_MCS):
        run_sweep(current_lattice, beta, J_COUPLING, H_FIELD)
        
    # 2. Measurement Phase
    magnetizations = []
    for meas_step in range(MEASUREMENT_MCS):
        run_sweep(current_lattice, beta, J_COUPLING, H_FIELD)
        mag = calculate_magnetization(current_lattice)
        magnetizations.append(mag)
        
    # 3. Calculate Ensemble Average <|M|>
    avg_magnetizations.append(np.mean(magnetizations))
    
    # Simple console output for tracking progress
    # print(f"T={1/beta:.2f}, <|M|>={avg_magnetizations[-1]:.4f}")

# ====================================================================
# 3. Visualization
# ====================================================================

# Plot <|M|> vs. Temperature
fig, ax = plt.subplots(figsize=(8, 5))

# Plot the computed data
ax.plot(temperatures, avg_magnetizations, 'o-', color='darkred', label=f'L={LATTICE_SIZE} Simulation')

# Plot the analytic critical temperature (T_c)
ax.axvline(1/BETA_CRITICAL, color='gray', linestyle='--', label=f'Analytic $T_c \\approx 2.269$')

# Labeling and Formatting
ax.set_title(f'Magnetization Curve $\\langle |M| \\rangle(T)$ for 2D Ising Model')
ax.set_xlabel('Temperature $T$ ($J/k_B$)')
ax.set_ylabel('Absolute Magnetization $\\langle |M| \\rangle$')
ax.set_ylim(0, 1.1)
ax.grid(True, which='both', linestyle=':')
ax.legend()

plt.tight_layout()
plt.show()

print("\nMagnetization curve simulation complete. The sharp drop near T=2.269 indicates the phase transition.")
