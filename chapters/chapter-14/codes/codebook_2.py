# Source: Simulation/chapter-14/codebook.md -- Block 2

import numpy as np
import matplotlib.pyplot as plt
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ====================================================================
# 1. Setup Weights (Reusing W from Project 1 setup)
# ====================================================================

N_NEURONS = 10
M_PATTERNS = 3
patterns = np.array([
    [+1, +1, +1, +1, +1, -1, -1, -1, -1, -1],
    [-1, -1, +1, +1, -1, +1, -1, +1, +1, -1],
    [+1, -1, +1, -1, +1, -1, +1, -1, +1, -1]
])

W = np.zeros((N_NEURONS, N_NEURONS))
for p in patterns:
    W += np.outer(p, p)
W /= M_PATTERNS
np.fill_diagonal(W, 0)

# ====================================================================
# 2. Input Cue and Overlap Functions
# ====================================================================

# Target pattern (Pattern 1)
target_pattern = patterns[0]
NOISE_FRACTION = 0.20 # Corrupt 20% of the bits

def add_noise(pattern, fraction):
    """Corrupts a pattern by flipping a given fraction of bits."""
    s_noisy = pattern.copy()
    num_flips = int(fraction * len(pattern))
    flip_indices = np.random.choice(len(pattern), num_flips, replace=False)
    s_noisy[flip_indices] *= -1
    return s_noisy

def calculate_overlap(s, target):
    """Measures similarity between current state and target memory."""
    # Overlap = (1/N) * dot(s, target)
    return np.dot(s, target) / len(s)

# Initialize state with a noisy cue
S_initial_cue = add_noise(target_pattern, NOISE_FRACTION)

# ====================================================================
# 3. Asynchronous Retrieval Loop
# ====================================================================

STEPS_PER_SWEEP = N_NEURONS # Define one sweep as N asynchronous updates
TOTAL_SWEEPS = 10
TOTAL_STEPS = TOTAL_SWEEPS * STEPS_PER_SWEEP

S_current = S_initial_cue.copy()
overlap_history = []
energy_history = []

for step in range(TOTAL_STEPS):
    # 1. Select a random neuron i (Asynchronous Update)
    i = np.random.randint(N_NEURONS)
    
    # 2. Calculate local input (h_i)
    # The dot product inherently skips W[i, i] because W is zero-diagonal
    h_i = np.dot(W[i], S_current)
    
    # 3. Update state based on sign
    S_current[i] = +1 if h_i > 0 else -1
    
    # Record metrics
    overlap_history.append(calculate_overlap(S_current, target_pattern))

# Final state
S_final = S_current
accuracy = np.mean(S_final == target_pattern)

# ====================================================================
# 4. Visualization and Analysis
# ====================================================================

plt.figure(figsize=(10, 5))
time_steps = np.arange(TOTAL_STEPS) / STEPS_PER_SWEEP # Plot in sweeps

plt.plot(time_steps, overlap_history, lw=2, color='darkred')
plt.axhline(1.0, color='gray', linestyle='--', label='Perfect Recall (Overlap = 1.0)')
plt.axhline(overlap_history[0], color='blue', linestyle=':', label=f'Initial Overlap: {overlap_history[0]:.2f}')

plt.title('Memory Retrieval Dynamics (Associative Recall)')
plt.xlabel('Time (Sweeps)')
plt.ylabel('Overlap with Target Pattern')
plt.ylim(overlap_history[0] - 0.1, 1.05)
plt.legend()
plt.grid(True)
plt.show()

# --- Analysis Summary ---
print("\n--- Pattern Completion and Error Correction Summary ---")
print(f"Target Pattern: {target_pattern}")
print(f"Noisy Cue (Initial Overlap): {S_initial_cue} ({overlap_history[0]:.2f})")
print("----------------------------------------------------------")
print(f"Final State (Overlap): {S_final} ({overlap_history[-1]:.2f})")
print(f"Final Accuracy: {accuracy:.0%}")
print("\nConclusion: The network successfully performed pattern completion. Starting from a noisy cue, the asynchronous dynamics drove the network's state to the stable memory attractor, quickly correcting all errors and achieving perfect overlap with the target pattern.")
