# Source: Simulation/chapter-1/codebook.md -- Block 1


import numpy as np
import random
import matplotlib.pyplot as plt

# ====================================================================
# 1. Core Functions: Target PDF and MH Acceptance
# ====================================================================

# Define the Target Unnormalized Probability Density (P(s))
# We will use the Boltzmann weight P(s) = exp(-beta * E(s))
# The potential V(x) = x^4 - 2x^2 + 1 (The Double-Well Potential)
def target_pdf(x, beta=1.0):
    """Calculates the unnormalized target probability (Boltzmann weight)."""
    V = x**4 - 2*x**2 + 1
    return np.exp(-beta * V)

# Metropolis-Hastings Acceptance Function
def metropolis_accept(P_old, P_new, g_forward, g_backward):
    """
    Implements the general Metropolis-Hastings acceptance criterion.
    
    Args:
        P_old (float): Target PDF of the current state s.
        P_new (float): Target PDF of the proposed state s'.
        g_forward (float): Proposal probability g(s -> s').
        g_backward (float): Proposal probability g(s' -> s).
        
    Returns:
        bool: True if the move is accepted, False otherwise.
    """
    if P_old == 0:
        # Avoid division by zero, though should not happen with exp(-E)
        return True
    
    # Calculate the full MH acceptance ratio A
    A = (P_new * g_backward) / (P_old * g_forward)
    
    # The acceptance probability alpha = min(1, A)
    alpha = min(1.0, A)
    
    # Accept the move if a uniform random number u <= alpha
    u = random.uniform(0, 1)
    return u <= alpha

# ====================================================================
# 2. Proposal Distributions (g)
# ====================================================================

# Simple symmetric random-walk proposal (Metropolis rule case)
def symmetric_proposal(delta_max=0.5):
    """Proposes a move s' = s + delta, where delta is uniform and symmetric."""
    return 1.0  # g_forward = g_backward, so ratio is 1

# Asymmetric proposal (Hastings rule case)
def asymmetric_proposal(s_prime, s, mean_shift=0.1, sigma=0.2):
    """
    Proposes a move s' from N(s + mean_shift, sigma).
    Uses Gaussian PDF to calculate g_forward and g_backward.
    """
    from scipy.stats import norm

    g_forward = norm.pdf(s_prime, loc=s + mean_shift, scale=sigma)
    g_backward = norm.pdf(s, loc=s_prime + mean_shift, scale=sigma)
    
    return g_forward, g_backward

# ====================================================================
# 3. Test Scenarios
# ====================================================================

# --- Setup Initial State and Proposed State ---
s_current = 0.5
s_proposed = 0.6
BETA = 1.0

P_old = target_pdf(s_current, BETA)
P_new = target_pdf(s_proposed, BETA)

print(f"--- MH Acceptance Test (Beta={BETA}) ---")
print(f"Current State (s): {s_current:.2f}, P(s): {P_old:.4f}")
print(f"Proposed State (s'): {s_proposed:.2f}, P(s'): {P_new:.4f}\n")

# Scenario 1: Symmetric Proposal (Metropolis Rule)
g_symm_ratio = symmetric_proposal()
is_accepted_symm = metropolis_accept(P_old, P_new, g_symm_ratio, g_symm_ratio)
ratio_symm = P_new / P_old
alpha_symm = min(1.0, ratio_symm)

print("Scenario 1: Symmetric Proposal (Metropolis)")
print(f"  P_new / P_old Ratio: {ratio_symm:.4f}")
print(f"  Acceptance Prob (alpha): {alpha_symm:.4f}")
print(f"  Move Accepted (Sampled): {is_accepted_symm}\n")

# Scenario 2: Asymmetric Proposal (General MH Rule)
try:
    g_forward, g_backward = asymmetric_proposal(s_proposed, s_current)
    is_accepted_asymm = metropolis_accept(P_old, P_new, g_forward, g_backward)
    
    ratio_asymm = (P_new * g_backward) / (P_old * g_forward)
    alpha_asymm = min(1.0, ratio_asymm)

    print("Scenario 2: Asymmetric Proposal (General Metropolis-Hastings)")
    print(f"  g(s -> s'): {g_forward:.4f}, g(s' -> s): {g_backward:.4f}")
    print(f"  Full MH Ratio: {ratio_asymm:.4f}")
    print(f"  Acceptance Prob (alpha): {alpha_asymm:.4f}")
    print(f"  Move Accepted (Sampled): {is_accepted_asymm}")

except ImportError:
    print("Scenario 2 skipped: 'scipy' library not installed. Cannot run asymmetric proposal test.")

# Optional: Visualize the potential for context
def plot_potential(V_func):
    x = np.linspace(-2.0, 2.0, 400)
    V = V_func(x)
    
    plt.figure(figsize=(6, 4))
    plt.plot(x, V, label='$V(x) = x^4 - 2x^2 + 1$')
    plt.axvline(s_current, color='green', linestyle='--', label='Current $s$', alpha=0.7)
    plt.axvline(s_proposed, color='red', linestyle='--', label='Proposed $s\'$', alpha=0.7)
    
    plt.title("1D Double-Well Potential")
    plt.xlabel("$x$")
    plt.ylabel("$V(x)$")
    plt.ylim(-1.1, 4.0)
    plt.legend()
    plt.grid(True)
    plt.show()

plot_potential(lambda x: x**4 - 2*x**2 + 1)
# Uncomment the line above to show the plot if needed
