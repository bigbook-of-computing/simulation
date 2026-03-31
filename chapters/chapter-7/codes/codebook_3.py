# Source: Simulation/chapter-7/codebook.md -- Block 3

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Set seed for reproducibility
np.random.seed(42)

# ====================================================================
# 1. Conceptual Trajectory Generation (Simulating a Diffusive System)
# ====================================================================

# --- Simulation Parameters ---
N_PARTICLES = 100       # Conceptual number of particles
DT = 0.01               # Time step
TOTAL_STEPS = 5000      # Total steps for the trajectory
TRAJECTORY_LENGTH = TOTAL_STEPS + 1
DIMENSIONS = 3          # For D calculation: use 3D (6*tau in denominator)

# Create a conceptual trajectory of positions R(t)
# We simulate random movement (Brownian-like) to ensure diffusion.
# R_history[t, i, d] = position of particle i at time t in dimension d
R_history = np.zeros((TRAJECTORY_LENGTH, N_PARTICLES, DIMENSIONS))

# Simulate the diffusion process
for t in range(1, TRAJECTORY_LENGTH):
    # R(t+dt) = R(t) + velocity * dt + random displacement
    # Simulate a small, random walk from the previous position
    random_displacement = np.random.normal(0, 0.1, size=(N_PARTICLES, DIMENSIONS))
    R_history[t] = R_history[t-1] + random_displacement

# ====================================================================
# 2. Mean-Squared Displacement (MSD) Calculation
# ====================================================================

# The maximum time lag (tau) to analyze is half the trajectory length
MAX_LAG = TOTAL_STEPS // 2
msd_history = np.zeros(MAX_LAG)

# Iterate over time lags (tau)
for tau in range(1, MAX_LAG):
    # Calculate displacement vector: dr(t) = R(t+tau) - R(t)
    # The average is over all possible time origins (t) and all particles (i)
    
    # 1. Displacements over lag tau
    dr = R_history[tau:] - R_history[:-tau]
    
    # 2. Squared displacement: sum |dr|^2 over dimensions
    dr_sq = np.sum(dr**2, axis=2)
    
    # 3. Mean: Average over all particles (axis=1) and all time origins (axis=0)
    msd_history[tau] = np.mean(dr_sq)

# Time axis for the MSD plot
time_lags = np.arange(MAX_LAG) * DT

# Identify the linear regime for fitting (long time)
FIT_START_LAG = 500 # Starting the fit after the initial ballistic/sub-diffusive regime

# ====================================================================
# 3. Diffusion Coefficient (D) Extraction
# ====================================================================

# Filter data for linear fitting
X_fit = time_lags[FIT_START_LAG:]
Y_fit = msd_history[FIT_START_LAG:]

# Perform linear regression: MSD(tau) = 6*D*tau + C
# linregress returns (slope, intercept, r_value, p_value, std_err)
slope, intercept, r_value, p_value, std_err = linregress(X_fit, Y_fit)

# Extract Diffusion Coefficient D from the slope (D = slope / 6)
D_CALCULATED = slope / (2 * DIMENSIONS) # D = slope / 6 in 3D

# Create the best-fit line data for visualization
fit_line = intercept + slope * X_fit

# ====================================================================
# 4. Visualization
# ====================================================================

fig, ax = plt.subplots(figsize=(8, 5))

# Plot the raw MSD curve
ax.plot(time_lags[1:], msd_history[1:], lw=2, color='darkblue', label='MSD($\\tau$) Simulation')

# Plot the linear fit line
ax.plot(X_fit, fit_line, '--', color='red', 
        label=f'Linear Fit (Slope = {slope:.3f})')

# Labeling and Formatting
ax.set_title('Mean-Squared Displacement (MSD) and Diffusion')
ax.set_xlabel('Time Lag $\\tau$ (s)')
ax.set_ylabel('MSD ($\mathregular{r^2}$)')
ax.text(0.65, 0.2, f'Diffusion Coeff. $D \\approx {D_CALCULATED:.4f}$', 
        transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
ax.legend()
ax.grid(True, which='both', linestyle=':')

plt.tight_layout()
plt.show()

# --- Conclusion ---
print("\n--- Diffusion Coefficient Analysis Summary ---")
print(f"Calculated MSD Slope (6D): {slope:.4f}")
print(f"Calculated Diffusion Coefficient (D): {D_CALCULATED:.5f}")
print(f"R-squared of Fit: {r_value**2:.4f}")

print("\nConclusion: The Mean-Squared Displacement (MSD) curve shows linear growth at long times, confirming normal diffusion in the system. The Diffusion Coefficient (D) is accurately extracted from the slope of this linear regime using the Einstein relation (MSD = 6D\u03C4).")
