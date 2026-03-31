# Source: Simulation/chapter-6/essay.md -- Block 2

np.random.seed(0)

def metropolis(E, x0=0.0, beta=5.0, steps=10000, step_size=0.5):
    x = np.zeros(steps)
    x[0] = x0
    for i in range(1, steps):
        x_trial = x[i-1] + np.random.uniform(-step_size, step_size)
        dE = E(x_trial) - E(x[i-1])
        if np.random.rand() < np.exp(-beta * dE) or dE < 0:
            x[i] = x_trial
        else:
            x[i] = x[i-1]
    return x

x_traj = metropolis(E, beta=5.0)
plt.plot(x_traj, lw=1)
plt.title("Metropolis Simulation in a Double-Well Potential")
plt.xlabel("Step")
plt.ylabel("$x$")
plt.grid(True)
plt.show()
