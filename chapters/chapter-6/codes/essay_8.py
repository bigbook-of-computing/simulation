# Source: Simulation/chapter-6/essay.md -- Block 8

def thermodynamic_averages(beta, E_bins, g):
    Z = np.sum(g * np.exp(-beta * E_bins))
    avgE = np.sum(E_bins * g * np.exp(-beta * E_bins)) / Z
    Cv = beta**2 * np.sum((E_bins - avgE)**2 * g * np.exp(-beta * E_bins)) / Z
    return avgE, Cv

betas = np.linspace(0.1, 2.0, 50)
E_avg, Cv = [], []

for b in betas:
    e, c = thermodynamic_averages(b, E_bins, g)
    E_avg.append(e)
    Cv.append(c)

plt.figure(figsize=(7,3))
plt.plot(1/betas, Cv, lw=2)
plt.xlabel("Temperature $T$")
plt.ylabel("Heat Capacity $C_V$")
plt.title("Thermodynamics from Density of States")
plt.grid(True)
plt.show()
