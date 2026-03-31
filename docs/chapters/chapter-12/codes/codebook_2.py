# Source: Simulation/chapter-12/codebook.md -- Block 2

import numpy as np
import matplotlib.pyplot as plt
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ====================================================================
# 1. Setup Parameters and Ising Core (from Project 1)
# ====================================================================

N = 30
J = 1.0
H = 0.0
T_SIM = 2.5                 # Near critical temperature for high fluctuation
MCS_RUN = 10000             # Long run for path analysis
EQUILIBRATION_MCS = 500

P0 = 100.0                  # Initial Price
ALPHA_IMPACT = 0.5          # Price impact coefficient (\alpha)
EPSILON_NOISE = 0.01        # Minimal background noise (\epsilon)

def create_lattice(N, initial_state='random'):
    """Initializes the market with random Buy/Sell decisions (+1 or -1)."""
    return np.random.choice([-1, 1], size=(N, N))

def get_local_field(i, j, spins, N=N, J=J, H=H):
    """Calculates the local influence (field) on trader (i, j) from neighbors and news."""
    up = spins[(i - 1) % N, j]
    down = spins[(i + 1) % N, j]
    left = spins[i, (j - 1) % N]
    right = spins[i, (j + 1) % N]
    return J * (up + down + left + right) + H

def metropolis_update(spins, T, J=J, H=H):
    """Performs one full Monte Carlo Sweep (MCS) for the market dynamics."""
    N = spins.shape[0]
    total_spins = N * N
    beta = 1.0 / T
    for _ in range(total_spins):
        i, j = random.randrange(N), random.randrange(N)
        h = get_local_field(i, j, spins, N, J, H)
        dE = 2 * spins[i, j] * h 
        if dE < 0 or random.random() < np.exp(-dE * beta):
            spins[i, j] *= -1

def calculate_magnetization(spins):
    """Calculates Net Order Flow (Magnetization) M."""
    return np.mean(spins)

def run_market_simulation_for_price(T):
    spins = create_lattice(N, initial_state='random')
    M_series = []
    
    # 1. Equilibration
    for _ in range(EQUILIBRATION_MCS):
        metropolis_update(spins, T)
    
    # 2. Measurement (Record M_t for the price evolution)
    for _ in range(MCS_RUN):
        metropolis_update(spins, T)
        M_series.append(calculate_magnetization(spins))
        
    return np.array(M_series)

# ====================================================================
# 2. Price Path Simulation
# ====================================================================

M_t_series = run_market_simulation_for_price(T_SIM)

Price_t_series = np.zeros(MCS_RUN + 1)
Price_t_series[0] = P0
P_current = P0

# Generate a minimal background noise sequence
background_noise = np.random.normal(0, EPSILON_NOISE, MCS_RUN)

for t in range(MCS_RUN):
    M_t = M_t_series[t]
    
    # Price Update Rule: P_{t+1} = P_t + alpha * M_t + epsilon_t
    price_change = ALPHA_IMPACT * M_t + background_noise[t]
    P_current += price_change
    Price_t_series[t + 1] = P_current

# ====================================================================
# 3. Visualization and Analysis
# ====================================================================

time_steps = np.arange(MCS_RUN + 1)

fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# Plot 1: Emergent Price Path
ax[0].plot(time_steps, Price_t_series, lw=1.5, color='darkgreen')
ax[0].set_title(f'Emergent Price Dynamics (T={T_SIM:.2f}, Driven by Net Order Flow $M_t$)')
ax[0].set_ylabel('Asset Price $P(t)$')
ax[0].grid(True)

# Plot 2: Driving Force (Net Order Flow / Magnetization)
ax[1].plot(time_steps[:-1], M_t_series, lw=1.0, color='crimson')
ax[1].axhline(0, color='gray', linestyle='--')
ax[1].set_title('Market Sentiment (Net Order Flow $M_t$)')
ax[1].set_xlabel('Time Step')
ax[1].set_ylabel('Sentiment $M_t$')
ax[1].set_ylim(-0.15, 0.15)
ax[1].grid(True)

plt.tight_layout()
fig.savefig('Simulation/RESEARCH/docs/chapters/chapter-12/codes/ch12_price_dynamics.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# --- Analysis Summary ---
price_range = np.max(Price_t_series) - np.min(Price_t_series)

print("\n--- Emergent Price Path Analysis ---")
print(f"Simulation Temperature (Uncertainty): T={T_SIM:.2f} (Near Critical)")
print(f"Price Range Generated: {price_range:.2f}")

print("\nConclusion: The simulation demonstrates that the price path evolves as a random walk, with its drift and fluctuations directly reflecting the time evolution of the emergent Net Order Flow (M_t). The large swings in price are driven by periods of heightened collective alignment (high |M|) in the underlying trader sentiment.")
