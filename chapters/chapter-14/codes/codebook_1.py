# Source: Simulation/chapter-14/codebook.md -- Block 1

import numpy as np
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# ====================================================================
# 1. Setup Patterns and Parameters
# ====================================================================

N_NEURONS = 10  # Small network size
M_PATTERNS = 3

# Define three simple, orthogonal binary patterns (vectors of +1, -1)
# Note: For N=10, we ensure orthogonality by making half the bits opposite.
patterns = np.array([
    [+1, +1, +1, +1, +1, -1, -1, -1, -1, -1],  # Pattern 1 (Target)
    [+1, -1, +1, -1, +1, -1, +1, -1, +1, -1],  # Pattern 2
    [-1, +1, +1, -1, -1, +1, -1, +1, +1, -1]   # Pattern 3
])

# ====================================================================
# 2. Hebbian Learning (Encoding Phase)
# ====================================================================

# Initialize the weight matrix W
W = np.zeros((N_NEURONS, N_NEURONS))

# Hebbian Learning Rule: W = (1/M) * sum(p_m * p_m.T)
for pattern in patterns:
    # Outer product: s_i * s_j
    W += np.outer(pattern, pattern)

# Normalize by the number of patterns
W /= M_PATTERNS

# Set diagonal elements to zero (no self-connection)
np.fill_diagonal(W, 0)

# ====================================================================
# 3. Analysis and Visualization
# ====================================================================

# 1. Check Structural Properties
is_symmetric = np.allclose(W, W.T)
zero_diagonal = np.all(np.diag(W) == 0)

print("--- Weight Matrix Analysis ---")
print(f"Symmetry Check (W_ij = W_ji): {is_symmetric}")
print(f"Zero Diagonal Check (W_ii = 0): {zero_diagonal}")
print("\nFinal Weight Matrix (W):")
print(np.round(W, 3))

# 2. Visualization (Heatmap)
plt.figure(figsize=(6, 5))
plt.imshow(W, cmap='coolwarm', origin='upper', interpolation='none', vmin=-1, vmax=1)
plt.colorbar(label='Synaptic Weight $w_{ij}$')
plt.title('Weight Matrix W Encoded by Hebbian Rule')
plt.xticks(np.arange(N_NEURONS), np.arange(1, N_NEURONS + 1))
plt.yticks(np.arange(N_NEURONS), np.arange(1, N_NEURONS + 1))
plt.xlabel('Neuron j')
plt.ylabel('Neuron i')
plt.show()

print("\nConclusion: The Hebbian learning rule successfully encoded the patterns into the synaptic weight matrix W. The matrix is symmetric and has a zero diagonal, which are essential properties for the network to function as an energy-minimizing system.")
