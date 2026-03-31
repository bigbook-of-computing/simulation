# Source: Simulation/chapter-6/essay.md -- Block 3

import numpy as np
import matplotlib.pyplot as plt

L = 50
J = 1.0
beta = 0.45  # near critical beta ≈ 0.4407 for 2D Ising
p_add = 1 - np.exp(-2 * beta * J)

# Initialize lattice randomly
spins = np.random.choice([-1, 1], size=(L, L))

def wolff_step(spins, p_add):
    L = spins.shape[0]
    visited = np.zeros_like(spins, dtype=bool)
    
    # pick random seed
    i, j = np.random.randint(L), np.random.randint(L)
    cluster_val = spins[i, j]
    cluster = [(i, j)]
    visited[i, j] = True
    
    while cluster:
        x, y = cluster.pop()
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            xn, yn = (x+dx)%L, (y+dy)%L
            if not visited[xn, yn] and spins[xn, yn] == cluster_val:
                if np.random.rand() < p_add:
                    visited[xn, yn] = True
                    cluster.append((xn, yn))
    # flip cluster
    spins[visited] *= -1
    return spins

# Run several cluster updates
for _ in range(200):
    spins = wolff_step(spins, p_add)

plt.imshow(spins, cmap="coolwarm")
plt.title("2D Ising configuration after Wolff updates")
plt.axis("off")
plt.show()
