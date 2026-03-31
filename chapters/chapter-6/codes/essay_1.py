# Source: Simulation/chapter-6/essay.md -- Block 1

import numpy as np
import matplotlib.pyplot as plt

# Define double-well potential
def E(x):
    return x**4 - 2*x**2  # Two wells at x = ±1

x = np.linspace(-2.5, 2.5, 400)
plt.plot(x, E(x), 'k', lw=2)
plt.title("Double-Well Energy Landscape")
plt.xlabel("$x$")
plt.ylabel("$E(x)$")
plt.grid(True)
plt.show()
