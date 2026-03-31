# Source: Simulation/chapter-6/essay.md -- Block 4

import numpy as np
import matplotlib.pyplot as plt

# Define potential
def E(x):
    return x**4 - 2*x**2

def metropolis_step(x, beta, step_size=0.5):
    x_trial = x + np.random.uniform(-step_size, step_size)
    dE = E(x_trial) - E(x)
    if np.random.rand() < np.exp(-beta * dE):
        return x_trial
    else:
        return x

# Initialize replicas at different temperatures
betas = np.array([0.5, 1.0, 2.0, 5.0])
n_replicas = len(betas)
steps = 20000

X = np.zeros((n_replicas, steps))
x_init = np.random.randn(n_replicas)

for t in range(1, steps):
    # Metropolis updates for each replica
    for i, beta in enumerate(betas):
        x_init[i] = metropolis_step(x_init[i], beta)
    
    # Attempt swaps between neighboring replicas
    for i in range(n_replicas - 1):
        d_beta = betas[i+1] - betas[i]
        dE = E(x_init[i+1]) - E(x_init[i])
        if np.random.rand() < np.exp(d_beta * dE):
            x_init[i], x_init[i+1] = x_init[i+1], x_init[i]
    
    X[:, t] = x_init
