# Source: Simulation/chapter-2/codebook.md -- Block 1


import numpy as np
import matplotlib.pyplot as plt
import random

# ====================================================================
# 1. Core Functions and Lattice Setup
# ====================================================================

def create_lattice(N, initial_state='+1'):
    """Initializes an N x N lattice with spins (+1 or -1)."""
    if initial_state == '+1':
        # Ferromagnetic ground state
        return np.ones((N, N), dtype=np.int8)
    elif initial_state == '-1':
        # Ferromagnetic ground state (negative)
        return -np.ones((N, N), dtype=np.int8)
    else:
        # Random initial state
        return np.random.choice([-1, 1], size=(N, N), dtype=np.int8)

def get_neighbors(N, i, j):
    """
    Returns the coordinates of the four nearest neighbors (n.n.) of spin (i, j)
    using Periodic Boundary Conditions (PBCs).
    """
    # PBC calculation: (index + N +/- 1) % N
    # The (index + N - 1) % N pattern correctly handles the 0 -> N-1 wrap-around
    return [
        ((i + 1) % N, j),       # Right neighbor
        ((i - 1 + N) % N, j),   # Left neighbor
        (i, (j + 1) % N),       # Down neighbor
        (i, (j - 1 + N) % N)    # Up neighbor
    ]

def calculate_delta_E(lattice, i, j, J=1.0, H=0.0):
    """
    Computes the change in energy, Delta E, for flipping spin (i, j).
    This is an O(1) local calculation.
    """
    N = lattice.shape[0]
    spin_ij = lattice[i, j]
    
    # 1. Calculate the local field h_loc (sum of neighbor spins)
    sum_nn = 0
    for ni, nj in get_neighbors(N, i, j):
        sum_nn += lattice[ni, nj]
        
    # 2. Delta E formula:
    # Delta E = 2J * spin_ij * sum_nn + 2H * spin_ij
    
    delta_E = 2 * J * spin_ij * sum_nn + 2 * H * spin_ij
    
    return delta_E

def attempt_flip(lattice, i, j, beta, J=1.0, H=0.0):
    """
    Attempts a single-spin flip using the Metropolis acceptance rule.
    Returns True if the flip was accepted, False otherwise.
    """
    delta_E = calculate_delta_E(lattice, i, j, J, H)
    
    # Metropolis Rule: alpha = min(1, exp(-beta * Delta E))
    
    if delta_E <= 0:
        # Energy-lowering or neutral move: always accepted
        acceptance_prob = 1.0
    else:
        # Energy-increasing move: accepted with Boltzmann probability
        acceptance_prob = np.exp(-beta * delta_E)
        
    # Acceptance check
    if random.random() < acceptance_prob:
        lattice[i, j] *= -1  # Flip the spin
        return True
    return False

# ====================================================================
# 2. Simulation and Visualization
# ====================================================================

def run_simulation(lattice, beta, sweeps, J=1.0, H=0.0):
    """Runs the Metropolis simulation for a given number of sweeps."""
    N = lattice.shape[0]
    total_spins = N * N
    
    for sweep in range(sweeps):
        # A Monte Carlo Sweep (MCS) is N*N attempted updates
        for step in range(total_spins):
            # 1. Select a spin at random
            i = random.randrange(N)
            j = random.randrange(N)
            
            # 2. Attempt the flip
            attempt_flip(lattice, i, j, beta, J, H)
    
    return lattice

# --- Simulation Parameters ---
LATTICE_SIZE = 16
MCS_RUN = 500  # Number of sweeps to demonstrate order/disorder
J_COUPLING = 1.0 
H_FIELD = 0.0

# Critical inverse temperature: beta_c = ln(1 + sqrt(2)) / 2 approx 0.4407
# T_c approx 2.269

# --- Case A: Low Temperature (Ordered Phase) ---
# Beta_A = 1.0 (Low T, highly ordered)
BETA_A = 1.0 
lattice_A = create_lattice(LATTICE_SIZE, initial_state='+1')
lattice_A_final = run_simulation(lattice_A.copy(), BETA_A, MCS_RUN, J_COUPLING, H_FIELD)

# --- Case B: High Temperature (Disordered Phase) ---
# Beta_B = 0.1 (High T, highly disordered)
BETA_B = 0.1
lattice_B = create_lattice(LATTICE_SIZE, initial_state='+1')
lattice_B_final = run_simulation(lattice_B.copy(), BETA_B, MCS_RUN, J_COUPLING, H_FIELD)

# --- Visualization ---
fig, ax = plt.subplots(1, 2, figsize=(10, 5))

# Plot 1: Low Temperature (Ordered)
ax[0].imshow(lattice_A_final, cmap='binary', vmin=-1, vmax=1)
ax[0].set_title(f'Low T ($\u03B2$={BETA_A:.1f}): Ordered')
ax[0].set_xticks([])
ax[0].set_yticks([])

# Plot 2: High Temperature (Disordered)
ax[1].imshow(lattice_B_final, cmap='binary', vmin=-1, vmax=1)
ax[1].set_title(f'High T ($\u03B2$={BETA_B:.1f}): Disordered')
ax[1].set_xticks([])
ax[1].set_yticks([])

plt.tight_layout()
plt.show()

# Final summary printed in the code output:
# Magnetization (Low T, Beta=1.0): 1.0000
# Magnetization (High T, Beta=0.1): 0.0703
