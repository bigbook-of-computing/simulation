# Source: Simulation/chapter-14/codebook.md -- Block 4

import numpy as np
import matplotlib.pyplot as plt
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ====================================================================
# 1. Setup and Core Functions
# ====================================================================

N_NEURONS = 100 # Large network size
N_TEST_PATTERNS = 5 # Number of patterns to test recall fidelity on

# Hebbian encoding function
def encode_hebbian(N, M, patterns=None):
    if patterns is None:
        patterns = np.random.choice([-1, 1], size=(M, N))
    
    W = np.zeros((N, N))
    for p in patterns:
        W += np.outer(p, p)
    W /= M
    np.fill_diagonal(W, 0)
    return W, patterns

# Asynchronous retrieval function (runs until stabilization or max steps)
def retrieve_pattern(W, s_cue, max_steps=300):
    s = s_cue.copy()
    for step in range(max_steps):
        s_old = s.copy()
        
        # Randomly select and update N neurons (one sweep)
        indices = np.random.permutation(len(s))
        for i in indices:
            h_i = np.dot(W[i], s)
            s[i] = +1 if h_i > 0 else -1
            
        # Check for stabilization
        if np.array_equal(s, s_old):
            break
    return s

def calculate_recall_accuracy(W, patterns_to_test, noise_fraction=0.10):
    """Tests recall fidelity by checking overlap of final state with target."""
    overlap_list = []
    
    for target_pattern in patterns_to_test:
        # 1. Create a noisy cue
        s_cue = target_pattern.copy()
        num_flips = int(noise_fraction * len(target_pattern))
        flip_indices = np.random.choice(len(target_pattern), num_flips, replace=False)
        s_cue[flip_indices] *= -1
        
        # 2. Retrieve the memory
        s_retrieved = retrieve_pattern(W, s_cue)
        
        # 3. Calculate overlap
        overlap = np.dot(s_retrieved, target_pattern) / N_NEURONS
        overlap_list.append(overlap)
        
    return np.mean(overlap_list)

# ====================================================================
# 2. Capacity Testing Scenarios
# ====================================================================

# Theoretical Capacity Limit: M_max ≈ 0.138 * 100 ≈ 13.8

# --- Scenario A: Under Capacity (High Fidelity) ---
M_A = 5 
W_A, patterns_A = encode_hebbian(N_NEURONS, M_A)
accuracy_A = calculate_recall_accuracy(W_A, patterns_A)

# --- Scenario B: Over Capacity (Low Fidelity / Interference) ---
M_B = 50 
W_B, patterns_B = encode_hebbian(N_NEURONS, M_B)
accuracy_B = calculate_recall_accuracy(W_B, patterns_B[:N_TEST_PATTERNS]) # Test the first 5 patterns

# ====================================================================
# 3. Visualization and Summary
# ====================================================================

M_values = [M_A, M_B]
accuracy_values = [accuracy_A, accuracy_B]

plt.figure(figsize=(8, 5))

# Plot the accuracy comparison
plt.bar(['M=5 (Under Capacity)', 'M=50 (Over Capacity)'], accuracy_values, 
        color=['darkgreen', 'darkred'])
plt.axhline(0.138, color='gray', linestyle='--', label='Theoretical Capacity Limit (M/N=0.138)')
plt.axhline(1.0, color='blue', linestyle=':', label='Perfect Recall')

# Labeling and Formatting
plt.title(f'Network Capacity Test (N={N_NEURONS}, Recall after 10% Noise)')
plt.xlabel('Number of Stored Patterns (M)')
plt.ylabel('Average Recall Fidelity (Overlap)')
plt.ylim(0.0, 1.1)
plt.legend()
plt.grid(True, axis='y')

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- Network Capacity Analysis ---")
print(f"Network Size (N): {N_NEURONS}")
print(f"Theoretical Capacity Limit (0.138*N): {0.138 * N_NEURONS:.1f}")
print("--------------------------------------------------")
print(f"Under Capacity (M={M_A}): Average Recall Overlap = {accuracy_A:.4f}")
print(f"Over Capacity (M={M_B}): Average Recall Overlap = {accuracy_B:.4f}")

print("\nConclusion: The simulation demonstrates the fundamental capacity limit. When the number of stored memories (M=50) significantly exceeds the theoretical limit (M_max \u2248 13.8), **memory interference** causes the recall fidelity to drop dramatically, confirming that the energy landscape becomes too crowded for the network to reliably find the correct minimum.")
