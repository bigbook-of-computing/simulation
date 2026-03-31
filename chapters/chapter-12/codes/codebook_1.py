# Source: Simulation/chapter-12/codebook.md -- Block 1

import numpy as np
import matplotlib.pyplot as plt
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ====================================================================
# 1. Setup Parameters and Core Metropolis Functions (Ising)
# ====================================================================

# --- Market Parameters ---
N = 30                     # Grid size (N x N traders)
J = 1.0                    # Herding Strength (Coupling Constant)
H = 0.0                    # External News Bias (Field)
MCS_RUN = 5000             # Monte Carlo Sweeps
EQUILIBRATION_MCS = 500

# Critical Temperature (T_c approx 2.269) separates ordered from disordered
T_CRITICAL = 2.269

# Temperature Scenarios (T = 1/beta)
T_LOW = 1.0                # T < T_c: Ordered/Consensus Market
T_HIGH = 5.0               # T > T_c: Disordered/Chaotic Market

# --- Ising Core Functions ---
def create_lattice(N, initial_state='random'):
    """Initializes the market with random Buy/Sell decisions (+1 or -1)."""
    return np.random.choice([-1, 1], size=(N, N))

def get_local_field(i, j, spins, N=N, J=J, H=H):
    """Calculates the local influence (field) on trader (i, j) from neighbors and news."""
    # Periodic boundary conditions (PBCs) are essential
    up = spins[(i - 1) % N, j]
    down = spins[(i + 1) % N, j]
    left = spins[i, (j - 1) % N]
    right = spins[i, (j + 1) % N]
    
    # h_local = J * sum(neighbors) + H
    return J * (up + down + left + right) + H

def metropolis_update(spins, T, J=J, H=H):
    """
    Performs one full Monte Carlo Sweep (MCS) for the market dynamics.
    Trader (i, j) flips action based on the Boltzmann probability.
    """
    N = spins.shape[0]
    total_spins = N * N
    
    beta = 1.0 / T # Uncertainty parameter
    
    for _ in range(total_spins):
        # 1. Select a random trader
        i, j = random.randrange(N), random.randrange(N)
        
        # 2. Calculate the energy change for flipping the action
        h = get_local_field(i, j, spins, N, J, H)
        # dE = 2 * current_spin * h
        dE = 2 * spins[i, j] * h 
        
        # 3. Acceptance Rule (Metropolis)
        if dE < 0 or random.random() < np.exp(-dE * beta):
            spins[i, j] *= -1 # Trader flips action (Buy <-> Sell)

def calculate_magnetization(spins):
    """Calculates Net Order Flow (Magnetization) M."""
    return np.mean(spins)

# ====================================================================
# 2. Simulation and Magnetization Comparison
# ====================================================================

def run_market_simulation(T):
    spins = create_lattice(N, initial_state='random')
    M_series = []
    
    # 1. Equilibration (Thermalization)
    for _ in range(EQUILIBRATION_MCS):
        metropolis_update(spins, T)
    
    # 2. Measurement
    for _ in range(MCS_RUN):
        metropolis_update(spins, T)
        M_series.append(calculate_magnetization(spins))
        
    return np.array(M_series), spins

# --- Run Scenarios ---
M_low_T, spins_low_T = run_market_simulation(T_LOW)
M_high_T, spins_high_T = run_market_simulation(T_HIGH)

# Calculate final ensemble averages
M_avg_low = np.mean(np.abs(M_low_T)) # Use absolute M for a measure of consensus magnitude
M_avg_high = np.mean(np.abs(M_high_T))

# ====================================================================
# 3. Visualization and Analysis
# ====================================================================

fig, ax = plt.subplots(1, 3, figsize=(15, 5))

# Plot 1: Low T Magnetization (Consensus)
ax[0].plot(M_low_T, lw=1.5, color='darkred')
ax[0].axhline(0, color='gray', linestyle='--')
ax[0].set_title(f'T={T_LOW:.1f} (Low Uncertainty): Consensus')
ax[0].set_xlabel('MCS')
ax[0].set_ylabel('Net Order Flow ($M$)')
ax[0].set_ylim(-1.1, 1.1)
ax[0].text(0.05, 0.9, f'$\langle |M| \\rangle = {M_avg_low:.2f}$', transform=ax[0].transAxes)
ax[0].grid(True)

# Plot 2: High T Magnetization (Chaos)
ax[1].plot(M_high_T, lw=1.5, color='darkblue')
ax[1].axhline(0, color='gray', linestyle='--')
ax[1].set_title(f'T={T_HIGH:.1f} (High Uncertainty): Chaos')
ax[1].set_xlabel('MCS')
ax[1].set_ylabel('Net Order Flow ($M$)')
ax[1].set_ylim(-1.1, 1.1)
ax[1].text(0.05, 0.9, f'$\langle |M| \\rangle = {M_avg_high:.2f}$', transform=ax[1].transAxes)
ax[1].grid(True)

# Plot 3: Comparison
ax[2].bar(['Low T (Consensus)', 'High T (Chaos)'], [M_avg_low, M_avg_high], color=['darkred', 'darkblue'])
ax[2].set_title('Net Order Flow Magnitude Comparison $\\langle |M| \\rangle$')
ax[2].set_ylabel('Average Magnetization')
ax[2].grid(True, axis='y')

plt.tight_layout()
fig.savefig('Simulation/RESEARCH/docs/chapters/chapter-12/codes/ch12_ising_market.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# --- Analysis Summary ---
print("\n--- Ising Market Model Analysis Summary ---")
print(f"Average Net Order Flow (Low T={T_LOW}): {M_avg_low:.4f} (High Consensus)")
print(f"Average Net Order Flow (High T={T_HIGH}): {M_avg_high:.4f} (Randomized)")

print("\nConclusion: The simulation confirms the physics analogy. At low temperature (low uncertainty), herding (J) dominates, locking the market into a strong consensus (high net order flow). At high temperature (high uncertainty), random fluctuations prevent collective alignment, resulting in a randomized market with M \u2248 0.")
