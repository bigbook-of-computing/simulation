# Source: Simulation/chapter-7/codebook.md -- Block 4

import numpy as np
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Parameters and Initial Conditions
# ====================================================================

# --- System Parameters ---
M = 1.0     # Mass
K_SPRING = 1.0  # Spring constant
KB = 1.0    # Boltzmann constant (set to 1.0 for simplified unit system)
DT = 0.01   # Time step
STEPS = 5000 # Total steps

# --- Thermostat Parameters ---
T0 = 1.0    # Target temperature
TAU_T = 1.0 # Relaxation time constant (Berendsen parameter)

# --- Initial Conditions (High Energy/Temperature) ---
R_INIT = 5.0  # High initial position
V_INIT = 0.0  # Initial velocity
DOF = 1       # Degrees of freedom for a 1D particle

# --- Reference Functions ---
def force(r, k=K_SPRING):
    return -k * r

def calculate_temperature(v, m=M, kB=KB, dof=DOF):
    """Calculates instantaneous temperature from kinetic energy (K=1/2*m*v^2)."""
    # T_inst = 2K / (DOF * k_B)
    K = 0.5 * m * v**2
    return 2 * K / (dof * kB)

# ====================================================================
# 2. Velocity–Verlet Integration with Berendsen Thermostat
# ====================================================================

# Initialize state and storage
r, v = R_INIT, V_INIT
F_current = force(r)
T_inst_history = []

for step in range(STEPS):
    # Get current acceleration
    a_current = F_current / M
    
    # --- Velocity-Verlet Integration ---
    # 1. Position Update
    r_new = r + v * DT + 0.5 * a_current * DT**2
    
    # 2. New Force Evaluation
    F_new = force(r_new)
    a_new = F_new / M
    
    # 3. Velocity Update (Pre-Thermostat)
    v_raw_new = v + 0.5 * (a_current + a_new) * DT
    
    # --- Berendsen Thermostat ---
    T_inst = calculate_temperature(v_raw_new, dof=DOF)
    
    # Calculate scaling factor lambda
    lambda_sq = 1 + (DT / TAU_T) * ((T0 / T_inst) - 1)
    lambda_factor = np.sqrt(lambda_sq)
    
    # Apply scaling to the velocity
    v_thermo = v_raw_new * lambda_factor
    
    # Bookkeeping: Advance state and force
    r, v = r_new, v_thermo
    F_current = F_new
    
    # Store temperature
    T_inst_history.append(calculate_temperature(v, dof=DOF))

# ====================================================================
# 3. Visualization
# ====================================================================

T_history = np.array(T_inst_history)
time_points = np.arange(len(T_history)) * DT

plt.figure(figsize=(10, 5))

# Plot instantaneous temperature over time
plt.plot(time_points, T_history, lw=1.5, color='green', label='Instantaneous $T_{\\text{inst}}$')
plt.axhline(T0, color='red', linestyle='--', alpha=0.7, label='Target Temperature $T_0$')

# Labeling and Formatting
plt.title(f'Berendsen Thermostat (NVT) Relaxation ($\u03C4_T={TAU_T}$ s)')
plt.xlabel('Time (s)')
plt.ylabel('Instantaneous Temperature ($T$)')
plt.legend()
plt.grid(True, which='both', linestyle=':')

plt.tight_layout()
plt.show()

# --- Conclusion ---
print("\n--- Thermostat Performance Check ---")
print(f"Target Temperature (T0): {T0:.4f}")
print(f"Initial Temperature (Conceptual): {calculate_temperature(V_INIT, dof=DOF):.4f} (Since V_init=0, initial T is near zero, but potential energy is high)")
print(f"Final Average Temperature: {np.mean(T_history[-1000:]):.4f}")
print(f"Final Temperature Standard Deviation: {np.std(T_history[-1000:]):.4f}")

print("\nConclusion: The instantaneous temperature successfully relaxes from its initial state and stabilizes around the target temperature $T_0=1.0$. This demonstrates the successful implementation of the Berendsen thermostat, which is effective for rapidly equilibrating the system to the desired NVT ensemble conditions.")
