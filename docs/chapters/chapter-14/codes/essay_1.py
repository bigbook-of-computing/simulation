# Source: Simulation/chapter-14/essay.md -- Block 1

import numpy as np

def hopfield_encode(patterns):
    """
    Encode memory patterns using Hebbian learning.
    
    Parameters:
    - patterns: List of M binary patterns, each of shape (N,)
              Values should be +1 or -1
    
    Returns:
    - W: Weight matrix (N, N) with zero diagonal
    """
    M = len(patterns)
    N = patterns[0].shape[0]
    
    # Initialize weight matrix
    W = np.zeros((N, N))
    
    # Hebbian learning: w_ij = (1/M) * sum over patterns of s_i * s_j
    for pattern in patterns:
        W += np.outer(pattern, pattern)
    
    W = W / M
    
    # Zero diagonal (no self-connections)
    np.fill_diagonal(W, 0)
    
    return W

def hopfield_energy(state, W, theta=None):
    """
    Compute Hopfield energy for a given state.
    
    E = -0.5 * sum(w_ij * s_i * s_j) + sum(theta_i * s_i)
    """
    if theta is None:
        theta = np.zeros(len(state))
    
    interaction_energy = -0.5 * state @ W @ state
    threshold_energy = theta @ state
    
    return interaction_energy + threshold_energy

def hopfield_retrieve(initial_state, W, theta=None, max_iter=1000):
    """
    Retrieve memory from noisy input via asynchronous update.
    
    Parameters:
    - initial_state: Corrupted pattern (N,) with values +1 or -1
    - W: Weight matrix from encoding
    - theta: Threshold vector (default: zeros)
    - max_iter: Maximum iterations before stopping
    
    Returns:
    - state: Converged state (retrieved memory)
    - energy_history: Energy at each iteration
    """
    N = len(initial_state)
    state = initial_state.copy()
    
    if theta is None:
        theta = np.zeros(N)
    
    energy_history = [hopfield_energy(state, W, theta)]
    
    for iteration in range(max_iter):
        # Asynchronous update: pick random neuron
        i = np.random.randint(N)
        
        # Compute local field (weighted input)
        h_i = np.sum(W[i, :] * state) - theta[i]
        
        # Update neuron state
        new_state_i = 1 if h_i >= 0 else -1
        
        # Check if state changed
        if state[i] != new_state_i:
            state[i] = new_state_i
            energy_history.append(hopfield_energy(state, W, theta))
        else:
            # Check for convergence (no neurons want to flip)
            converged = True
            for j in range(N):
                h_j = np.sum(W[j, :] * state) - theta[j]
                new_state_j = 1 if h_j >= 0 else -1
                if state[j] != new_state_j:
                    converged = False
                    break
            
            if converged:
                break
    
    return state, np.array(energy_history)

# Example usage:
# patterns = [np.array([1, -1, 1, -1, 1]),  # Pattern 1
#             np.array([-1, 1, -1, 1, -1])]  # Pattern 2
# W = hopfield_encode(patterns)
# noisy_input = np.array([1, -1, -1, -1, 1])  # Corrupted version of pattern 1
# retrieved, energy = hopfield_retrieve(noisy_input, W)
