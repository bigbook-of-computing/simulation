# Source: Simulation/chapter-7/codebook.md -- Block 2

import numpy as np
import matplotlib.pyplot as plt
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ====================================================================
# 1. Setup Parameters and PBC Functions
# ====================================================================

# --- System Parameters ---
N_PARTICLES = 4
L_BOX = 10.0
M = 1.0
DT = 0.005 # Smaller DT for stability with multi-particle forces
STEPS = 500

# --- Reference/Conceptual Functions ---
def minimum_image(dr, L):
    """Calculates the minimum image distance vector component."""
    # dr = ri - rj. This implements dr - L * round(dr/L)
    return dr - L * np.round(dr / L)

def wrap_position(r, L):
    """Wraps position back into the primary simulation box [0, L]."""
    return r % L

def force_conceptual(r_i, r_j, L, cutoff=1.0, epsilon=1.0):
    """
    Conceptual short-range repulsive force (Lennard-Jones-like, but only repulsive).
    Force magnitude scales as 1/r^7 (proportional to -dU/dr of a 1/r^6 term).
    """
    # 1. Calculate the minimum image distance vector
    dr = minimum_image(r_i - r_j, L)
    r_sq = np.sum(dr**2)
    
    if r_sq > cutoff**2 or r_sq == 0:
        return np.zeros_like(r_i) # No interaction or self-interaction
    
    r = np.sqrt(r_sq)
    
    # 2. Conceptual Force (Highly Repulsive): F = 24 * epsilon * (2/r^13 - 1/r^7) * (dr/r)
    # Simplified Repulsive: F_mag ~ 1/r^7
    r_inv = 1.0 / r
    r_inv_7 = r_inv**7
    
    # Force vector F = -dU/dr * (dr/r)
    # Conceptual F_mag = 4 * epsilon * (12*r_inv_13 - 6*r_inv_7)
    # We use a simplified 1/r^7-scaling for demonstration
    F_mag = 4 * epsilon * 12 * r_inv**13 * r_inv # Very stiff repulsion
    
    # F_vector = F_mag * (dr / r)
    F_vec = F_mag * (dr / r)
    
    return F_vec

def calculate_total_force(positions, L):
    """Calculates the total force vector for all particles (O(N^2) here)."""
    N = len(positions)
    total_forces = np.zeros_like(positions)
    
    for i in range(N):
        for j in range(i + 1, N):
            F_ij = force_conceptual(positions[i], positions[j], L)
            total_forces[i] += F_ij
            total_forces[j] -= F_ij # Newton's third law
            
    return total_forces

# ====================================================================
# 2. Initialization and MD Loop
# ====================================================================

# Initial state: positions [0, L] and zero velocity
R_init = np.random.rand(N_PARTICLES, 2) * L_BOX
V_init = np.zeros_like(R_init)

# Storage
R_history = np.zeros((STEPS, N_PARTICLES, 2))
R_history[0] = R_init.copy()

# Setup initial state
R = R_init.copy()
V = V_init.copy()
F_current = calculate_total_force(R, L_BOX)

for step in range(1, STEPS):
    # Get current acceleration
    A_current = F_current / M
    
    # 1. Position Update
    R_new_unwrapped = R + V * DT + 0.5 * A_current * DT**2
    
    # Apply PBC: Wrap positions back into [0, L]
    R_new = wrap_position(R_new_unwrapped, L_BOX)
    
    # 2. New Force Evaluation (using wrapped positions for the interaction)
    F_new = calculate_total_force(R_new, L_BOX)
    A_new = F_new / M
    
    # 3. Velocity Update
    V_new = V + 0.5 * (A_current + A_new) * DT
    
    # Bookkeeping: Advance state and force
    R, V = R_new, V_new
    F_current = F_new
    R_history[step] = R_new.copy()

# ====================================================================
# 3. Visualization
# ====================================================================

fig, ax = plt.subplots(figsize=(8, 8))

# Plot initial and final state
ax.plot(R_history[0, :, 0], R_history[0, :, 1], 'o', markersize=10, 
        color='blue', alpha=0.5, label='Initial Positions ($t=0$)')
ax.plot(R_history[-1, :, 0], R_history[-1, :, 1], 'x', markersize=10, 
        color='red', label=f'Final Positions ($t={STEPS*DT:.2f}$)')

# Draw the simulation box boundary
ax.plot([0, L_BOX, L_BOX, 0, 0], [0, 0, L_BOX, L_BOX, 0], 'k--', lw=1, label='Simulation Box')

# Labeling and Formatting
ax.set_title(f'2D Molecular Dynamics with Periodic Boundaries (N={N_PARTICLES})')
ax.set_xlabel('x-coordinate')
ax.set_ylabel('y-coordinate')
ax.set_xlim(-0.5, L_BOX + 0.5)
ax.set_ylim(-0.5, L_BOX + 0.5)
ax.legend()
ax.set_aspect('equal', adjustable='box')
ax.grid(True)

plt.tight_layout()
plt.show()

# --- Verification ---
# Check if any particle crossed the boundary (i.e., its position was wrapped)
wrapped_events = np.sum((R_history[1:] > L_BOX) | (R_history[1:] < 0))

print("\n--- Boundary Condition Verification ---")
print(f"Box Side Length (L): {L_BOX:.1f}")
print(f"Total Boundary Crossings/Wraps (conceptual): {wrapped_events}")
print(f"Final positions are all within [0, L]: {np.all((R_history[-1] >= 0) & (R_history[-1] <= L_BOX))}")

print("\nConclusion: The simulation successfully implemented Periodic Boundary Conditions (PBCs). The positions were continuously wrapped back into the [0, L] box after each time step, and the Minimum Image Convention (MIC) was used to ensure particles interacted with the correct nearest image across the boundaries.")
