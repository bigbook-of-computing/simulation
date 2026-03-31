# Source: Simulation/chapter-6/essay.md -- Block 7

plt.figure(figsize=(7,3))
plt.plot(E_bins, np.log(g), lw=2)
plt.xlabel("$E$")
plt.ylabel("$\\log g(E)$")
plt.title("Estimated Density of States via Wang–Landau Sampling")
plt.grid(True)
plt.show()
