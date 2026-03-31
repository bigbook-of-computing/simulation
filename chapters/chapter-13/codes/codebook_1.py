# Source: Simulation/chapter-13/codebook.md -- Block 1

import numpy as np
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# ====================================================================
# 1. Setup Parameters and Grid
# ====================================================================

# --- PDE Parameters ---
D = 0.01    # Diffusion coefficient (D)
K = 0.5     # Logistic growth rate (k)

# --- Grid Parameters ---
L = 1.0     # Domain length
NX = 100    # Number of spatial grid points
DX = L / NX # Spatial step size (\Delta x)

# --- Time Parameters (Conditional Stability) ---
DT = 0.5 * DX**2 / D # Ensure stability for explicit scheme
T_FINAL = 20.0
NT = int(T_FINAL / DT)

# Initialize concentration vector (u)
U = np.zeros(NX + 1)
x_points = np.linspace(0, L, NX + 1)

# Initial Condition: Localized spike in the center of the domain
SPIKE_WIDTH = 5
U[NX // 2 - SPIKE_WIDTH : NX // 2 + SPIKE_WIDTH] = 0.5 

# ====================================================================
# 2. FDM Simulation Loop (Forward Euler)
# ====================================================================

# Storage for plotting snapshots
U_snapshots = [U.copy()]
snapshot_interval = NT // 5

for n in range(NT):
    U_new = U.copy()
    
    # 1. Calculate the spatial terms (Laplacian)
    # Uses the current time step values (U) to compute the derivatives
    U_laplacian = (np.roll(U, -1) - 2 * U + np.roll(U, 1)) / DX**2
    
    # 2. Apply the Forward Euler update
    # u_new = u_old + dt * [ D * u_xx + k * u * (1 - u) ]
    U_new = U + DT * (D * U_laplacian + K * U * (1 - U))
    
    # Boundary Conditions (Fixed Flux/Zero Concentration at boundaries)
    U_new[0] = 0.0
    U_new[NX] = 0.0
    
    U = U_new
    
    if (n + 1) % snapshot_interval == 0:
        U_snapshots.append(U.copy())

# ====================================================================
# 3. Visualization
# ====================================================================

plt.figure(figsize=(10, 5))

# Plot the concentration profile over time
for i, u_snap in enumerate(U_snapshots):
    time_snap = i * T_FINAL / 5
    plt.plot(x_points, u_snap, label=f'Time $\\approx {time_snap:.1f}$ s', lw=1.5)

# Labeling and Formatting
plt.title(f'1D Reaction–Diffusion System (D={D}, K={K})')
plt.xlabel('Position $x$')
plt.ylabel('Concentration $u(x, t)$')
plt.ylim(bottom=0, top=1.1)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- 1D Reaction–Diffusion Analysis Summary ---")
print(f"Diffusion Coefficient (D): {D}")
print(f"Reaction Rate (K): {K}")
print("\nConclusion: The simulation successfully demonstrates the coupling of diffusion and reaction. The initial spike both spreads out across the domain (diffusion) and grows in magnitude (reaction) until it approaches the saturation limit (u=1) imposed by the logistic growth term.")
