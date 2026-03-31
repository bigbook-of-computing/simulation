# Source: Simulation/chapter-6/essay.md -- Block 5

plt.figure(figsize=(8, 3))
plt.plot(X[3, :], lw=0.7)
plt.title("Trajectory of Low-Temperature Replica in Parallel Tempering")
plt.xlabel("Step")
plt.ylabel("$x$")
plt.grid(True)
plt.show()
