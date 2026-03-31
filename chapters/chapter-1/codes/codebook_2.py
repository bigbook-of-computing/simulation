# Source: Simulation/chapter-1/codebook.md -- Block 2


import numpy as np
import random
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Functions (from Project 1)
# ====================================================================

# Potential: V(x) = x^4 - 2x^2 + 1
def potential_V(x):
    return x**4 - 2*x**2 + 1

# Target PDF (Unnormalized Boltzmann weight)
def target_pdf(x, beta):
    V = potential_V(x)
    return np.exp(-beta * V)

# Metropolis Acceptance Rule (Symmetric Proposal)
def metropolis_accept(P_old, P_new):
    """
    Implements the classic Metropolis acceptance criterion (symmetric proposal).
    g_forward and g_backward cancel out, so alpha = min(1, P_new / P_old).
    
    Args:
        P_old (float): Target PDF of the current state s.
        P_new (float): Target PDF of the proposed state s'.
        
    Returns:
        bool: True if the move is accepted, False otherwise.
    """
    if P_old == 0:
        return True # Should not happen with exp(-E)
        
    acceptance_ratio = P_new / P_old
    alpha = min(1.0, acceptance_ratio)
    
    u = random.uniform(0, 1)
    return u <= alpha

# ====================================================================
# 2. Metropolis MCMC Simulation Engine
# ====================================================================

def run_metropolis_simulation(beta, total_steps, delta_range=0.5):
    """Runs a Metropolis simulation for the 1D double-well potential."""
    
    # Initialize the chain (starting in the x=-1 well)
    current_x = -1.0 
    
    # Pre-allocate array to store positions
    positions = np.zeros(total_steps)
    
    # Calculate initial probability
    current_P = target_pdf(current_x, beta)
    
    accepted_moves = 0
    
    for t in range(total_steps):
        # 1. Propose a new state (symmetric random walk)
        delta = random.uniform(-delta_range, delta_range)
        proposed_x = current_x + delta
        
        # 2. Compute the new probability
        proposed_P = target_pdf(proposed_x, beta)
        
        # 3. Acceptance check (Metropolis rule)
        if metropolis_accept(current_P, proposed_P):
            current_x = proposed_x
            current_P = proposed_P
            accepted_moves += 1
        
        # 4. Record the current state
        positions[t] = current_x
        
    acceptance_rate = accepted_moves / total_steps
    return positions, acceptance_rate

# ====================================================================
# 3. Run and Visualize Cases
# ====================================================================

TOTAL_STEPS = 100000 
BURN_IN = 5000 
DELTA_RANGE = 0.5 

# --- Case A: Low Temperature (Beta=5) ---
BETA_A = 5.0
positions_A, rate_A = run_metropolis_simulation(BETA_A, TOTAL_STEPS, DELTA_RANGE)

# --- Case B: High Temperature (Beta=1) ---
BETA_B = 1.0
positions_B, rate_B = run_metropolis_simulation(BETA_B, TOTAL_STEPS, DELTA_RANGE)

# Create the visualization
fig, ax = plt.subplots(2, 2, figsize=(12, 8))

# Plot 1: Time Series (Low T)
ax[0, 0].plot(positions_A[BURN_IN:], linewidth=0.5, alpha=0.9)
ax[0, 0].set_title(f'Case A: Low Temperature ($\\beta={BETA_A}$)')
ax[0, 0].set_xlabel('Iteration Number (after burn-in)')
ax[0, 0].set_ylabel('Position $x_t$')
ax[0, 0].text(0.05, 0.9, f'Acceptance Rate: {rate_A:.2%}', transform=ax[0, 0].transAxes)

# Plot 2: Histogram (Low T)
ax[0, 1].hist(positions_A[BURN_IN:], bins=50, density=True, color='skyblue')
ax[0, 1].set_title(f'Distribution (Low T, $\\beta={BETA_A}$)')
ax[0, 1].set_xlabel('Position $x$')
ax[0, 1].set_ylabel('Probability Density')
ax[0, 1].text(0.05, 0.9, 'Observation: Trapped in well', transform=ax[0, 1].transAxes)

# Plot 3: Time Series (High T)
ax[1, 0].plot(positions_B[BURN_IN:], linewidth=0.5, alpha=0.9, color='darkorange')
ax[1, 0].set_title(f'Case B: High Temperature ($\\beta={BETA_B}$)')
ax[1, 0].set_xlabel('Iteration Number (after burn-in)')
ax[1, 0].set_ylabel('Position $x_t$')
ax[1, 0].text(0.05, 0.9, f'Acceptance Rate: {rate_B:.2%}', transform=ax[1, 0].transAxes)

# Plot 4: Histogram (High T)
ax[1, 1].hist(positions_B[BURN_IN:], bins=50, density=True, color='lightcoral')
ax[1, 1].set_title(f'Distribution (High T, $\\beta={BETA_B}$)')
ax[1, 1].set_xlabel('Position $x$')
ax[1, 1].set_ylabel('Probability Density')
ax[1, 1].text(0.05, 0.9, 'Observation: Mixed well across wells', transform=ax[1, 1].transAxes)

plt.tight_layout()
plt.show()

# Display the image tag
print("")
