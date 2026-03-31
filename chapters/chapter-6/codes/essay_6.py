# Source: Simulation/chapter-6/essay.md -- Block 6

import numpy as np
import matplotlib.pyplot as plt

def E(x):
    return x**4 - 2*x**2

# Discretize energy range
E_bins = np.linspace(-1.5, 2.0, 100)
g = np.ones_like(E_bins)  # initial guess
H = np.zeros_like(E_bins)
f = np.e  # modification factor
x = 0.0

def find_bin(E_val):
    return np.argmin(np.abs(E_bins - E_val))

flatness_threshold = 0.8
max_iter = 1000000

for step in range(max_iter):
    # Propose a move
    x_trial = x + np.random.uniform(-0.5, 0.5)
    Ei, Ej = E(x), E(x_trial)
    bi, bj = find_bin(Ei), find_bin(Ej)
    
    # Acceptance rule using g(E)
    if np.random.rand() < min(1, g[bi]/g[bj]):
        x = x_trial
        b = bj
    else:
        b = bi
    
    # Update g(E) and histogram
    g[b] *= f
    H[b] += 1
    
    # Periodic check for flatness
    if step % 5000 == 0 and np.min(H) > flatness_threshold * np.mean(H):
        f = np.sqrt(f)
        H[:] = 0
        if f < np.exp(1e-8):
            break
