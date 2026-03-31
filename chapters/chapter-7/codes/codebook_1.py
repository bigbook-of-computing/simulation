# Source: Simulation/chapter-7/codebook.md -- Block 1

import numpy as np
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Parameters and Initial Conditions
# ====================================================================

# --- System Parameters ---
M = 1.0     # Mass of the particle
K_SPRING = 1.0  # Spring constant
DT = 0.01   # Time step
STEPS = 5000 # Total number of steps

# --- Initial Conditions ---
R_INIT = 1.0  # Initial position (meters)
V_INIT = 0.0  # Initial velocity (m/s)

# --- Reference Functions ---
def force(r, k=K_SPRING):
    """Calculates the force F = -kr."""
    return -k * r

def potential_energy(r, k=K_SPRING):
    """Calculates Potential Energy U = 0.5 * k * r^2."""
    return 0.5 * k * r**2

def kinetic_energy(v, m=M):
    """Calculates Kinetic Energy K = 0.5 * m * v^2."""
    return 0.5 * m * v**2

# ====================================================================
# 2. Velocity–Verlet Integration Loop
# ====================================================================

# Initialize state and storage
r, v = R_INIT, V_INIT
F_current = force(r)
E_total_history = []

for step in range(STEPS):
    # Get current acceleration
    a_current = F_current / M
    
    # 1. Position Update (Drift/Kick)
    r_new = r + v * DT + 0.5 * a_current * DT**2
    
    # 2. New Force Evaluation
    F_new = force(r_new)
    a_new = F_new / M
    
    # 3. Velocity Update (Final Kick)
    v_new = v + 0.5 * (a_current + a_new) * DT
    
    # Bookkeeping: Advance state and current force for next step
    r, v = r_new, v_new
    F_current = F_new
    
    # Calculate and store total energy for the NVE ensemble check
    E_kin = kinetic_energy(v)
    E_pot = potential_energy(r)
    E_total_history.append(E_kin + E_pot)

# ====================================================================
# 3. Visualization
# ====================================================================

E_history = np.array(E_total_history)
time_points = np.arange(STEPS) * DT
initial_energy = E_history[0]

# Calculate energy drift statistics
energy_mean = np.mean(E_history)
energy_std = np.std(E_history)
relative_drift = (E_history[-1] - initial_energy) / initial_energy

plt.figure(figsize=(10, 5))

# Plot total energy over time
plt.plot(time_points, E_history, lw=1.5, label='Total Energy $E_{\\text{tot}}(t)$')
plt.axhline(initial_energy, color='red', linestyle='--', alpha=0.7, label='Initial Energy $E_0$')

# Labeling and Formatting
plt.title(f'Energy Conservation in Velocity–Verlet (NVE) Ensemble ($\Delta t={DT}$)')
plt.xlabel('Time (s)')
plt.ylabel('Total Energy (J)')
plt.ylim(E_history.min() - 0.0001, E_history.max() + 0.0001) # Zoom in to see fluctuations
plt.legend()
plt.grid(True, which='both', linestyle=':')

plt.tight_layout()
plt.show()

# --- Conclusion ---
print("\n--- Integrator Stability Check (NVE Ensemble) ---")
print(f"Initial Total Energy: {initial_energy:.6f} J")
print(f"Final Total Energy:   {E_history[-1]:.6f} J")
print(f"Energy Standard Deviation (Fluctuation): {energy_std:.7f} J")
print(f"Relative Energy Drift (Final vs Initial): {relative_drift:.4e}")

print("\nConclusion: The total energy remains constant, with the standard deviation measuring only small numerical fluctuations. This confirms the **symplectic stability** of the Velocity–Verlet integrator, making it suitable for long-term molecular dynamics simulations.")
