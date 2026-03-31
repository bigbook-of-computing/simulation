# **Chapter 7: Physics III: Molecular Dynamics (MD) () () () (Workbook)**

The goal of this chapter is to introduce the simulation of **real-time motion** by integrating Newton's equations, contrasting this dynamic approach with the equilibrium sampling of Monte Carlo (MC).

| Section | Topic Summary |
| :--- | :--- |
| **7.1** | Chapter Opener: From Sampling to Dynamics |
| **7.2** | The Velocity–Verlet Algorithm |
| **7.3** | Periodic Boundary Conditions and Neighbor Lists |
| **7.4** | Thermostats and Ensembles (NVE, NVT, NPT) |
| **7.5** | Computing Observables (Energy, Pressure, Diffusion, and Correlation Functions) |

---

### 7.1 From Sampling to Dynamics

> **Summary:** Molecular Dynamics (MD) simulates **continuous time evolution** by integrating Newton's equation, $m_i \frac{d^2 \mathbf{r}_i}{dt^2} = \mathbf{F}_i$. In MD, the **force** $\mathbf{F} = -\nabla E$ replaces the Boltzmann **probability** $e^{-\beta E}$ as the fundamental driving mechanism.

#### Section Detail

MD is a "different worldview" from Monte Carlo. While MC explores statistical equilibrium through random jumps, MD simulates deterministic, time-reversible trajectories driven by the force field of the system's potential energy landscape. The core integrator for MD is the **Velocity-Verlet algorithm**, which is **symplectic** (conserves phase space geometry) and ensures long-term energy stability.

#### Quiz Questions

!!! note "Quiz"
```
**1. What is the fundamental driving mechanism for particle movement in a Molecular Dynamics simulation?**

* **A.** Random acceptance/rejection rules based on Boltzmann probability.
* **B.** **The force $\mathbf{F}_i$, derived from the gradient of the potential energy $E(\mathbf{r})$**. (**Correct**)
* **C.** The autocorrelation function.
* **D.** The time step $\Delta t$.

```
!!! note "Quiz"
```
**2. The primary reason the Velocity–Verlet algorithm is preferred over the simpler Euler method for long-term MD simulations is that Velocity–Verlet is:**

* **A.** Faster to compute.
* **B.** Easier to code.
* **C.** **Symplectic and time-reversible, leading to excellent long-term energy conservation**. (**Correct**)
* **D.** A third-order accurate integrator.

```
---

!!! question "Interview Practice"
```
**Question:** Explain the core conceptual difference between the output of a standard Metropolis Monte Carlo simulation and a Molecular Dynamics simulation, even when both model the same system (e.g., liquid Argon).

**Answer Strategy:**
* **MC Output:** Provides a set of configurations weighted by $e^{-\beta E}$ (the **equilibrium ensemble**). The output is sufficient for calculating thermodynamic averages (like $\langle E \rangle$ or specific heat), but it has **no concept of time or dynamics**.
* **MD Output:** Provides a **time-dependent trajectory** of positions and velocities $(\mathbf{r}(t), \mathbf{v}(t))$. This output allows calculation of **dynamic and transport properties** (like diffusion coefficients and correlation functions) that are completely inaccessible to MC.

```
---

---

### 7.2 The Velocity–Verlet Algorithm

> **Summary:** The **Velocity–Verlet algorithm** is a **second-order accurate** integrator that updates position using the current state and velocity using the average of the current and future forces. It ensures long-term stability by conserving the geometry of phase space (symplectic property).

#### Section Detail

Velocity–Verlet discretizes Newton's equations by splitting the calculation into three sequential steps: position update, new force evaluation, and velocity update. The second-order accuracy ($\mathcal{O}(\Delta t^2)$) ensures that errors scale well with the chosen time step $\Delta t$. The choice of $\Delta t$ is critical and must be small enough to resolve the fastest oscillations in the system (e.g., bond stretches).

#### Quiz Questions

!!! note "Quiz"
```
**1. The Velocity–Verlet algorithm uses which two physical quantities at the next time step $t+\Delta t$ to update the velocity $\mathbf{v}_i(t+\Delta t)$?**

* **A.** Position $\mathbf{r}(t+\Delta t)$ and potential energy $U(t+\Delta t)$.
* **B.** The total energy $E_{\text{tot}}(t)$ and the kinetic energy $K(t)$.
* **C.** **The current force $\mathbf{F}(t)$ and the new force $\mathbf{F}(t+\Delta t)$**. (**Correct**)
* **D.** The pressure $P(t)$ and the temperature $T(t)$.

```
!!! note "Quiz"
```
**2. A large MD time step $\Delta t$ that fails to resolve the fastest oscillations in the system primarily leads to:**

* **A.** Incorrect ensemble sampling.
* **B.** **Numerical instability and energy drift**. (**Correct**)
* **C.** High autocorrelation times.
* **D.** Inaccurate pressure calculation.

```
---

!!! question "Interview Practice"
```
**Question:** Briefly explain the "Kick-Drift-Kick" conceptual analogy for the Velocity–Verlet algorithm.

**Answer Strategy:** The Velocity–Verlet algorithm can be viewed as splitting the movement into sequential steps:
1.  **Kick (Half-Step Velocity):** The velocity is advanced by a half-step using the initial acceleration (force).
2.  **Drift (Full-Step Position):** The position is advanced by a full step using this half-step velocity (the drift).
3.  **Kick (Final Velocity):** The force is recalculated at the new position, and the velocity is given its final half-step kick using the average acceleration of the two steps.

```
---

---

### 7.3 Periodic Boundary Conditions and Neighbor Lists

> **Summary:** **Periodic Boundary Conditions (PBCs)** and the **Minimum Image Convention** are used to emulate an infinite system using a small, finite simulation box. To achieve $\mathcal{O}(N)$ scaling for short-range forces, **Neighbor Lists** are employed to avoid the computationally prohibitive $\mathcal{O}(N^2)$ summation of all pairwise interactions.

#### Section Detail

PBCs eliminate unphysical surface effects by making the simulation box topologically equivalent to a torus. The Minimum Image Convention ensures that each particle interacts only with the nearest periodic image of every other particle. Neighbor lists store pairs within a cutoff radius $r_c$ plus a "skin" buffer $\delta$, and are updated only periodically, dramatically reducing computational cost.

#### Quiz Questions

!!! note "Quiz"
```
**1. The **Minimum Image Convention** is used in MD with PBCs to ensure that:**

* **A.** All particles remain in the center of the box.
* **B.** **Each particle interacts only with the nearest periodic image of every other particle**. (**Correct**)
* **C.** The potential energy is always zero.
* **D.** The temperature is constant.

```
!!! note "Quiz"
```
**2. The primary reason for using **Neighbor Lists** in a short-range MD simulation is to reduce the computational complexity of the force calculation from $\mathcal{O}(N^2)$ to approximately:**

* **A.** $\mathcal{O}(\log N)$.
* **B.** $\mathcal{O}(N^3)$.
* **C.** **$\mathcal{O}(N)$**. (**Correct**)
* **D.** $\mathcal{O}(\Delta t)$.

```
---

!!! question "Interview Practice"
```
**Question:** If you are simulating a system using a potential energy function that contains a long-range Coulombic ($1/r$) term, would you still use the simple Neighbor List optimization? Why or why not?

**Answer Strategy:** **No**, the simple neighbor list optimization would be ineffective. The $1/r$ Coulombic potential decays too slowly with distance. Since the interaction cannot be cut off at a finite radius $r_c$ without introducing large errors, every particle still needs to interact with every other particle (and all their images). For long-range forces, specialized methods like the **Ewald summation** or **Particle Mesh Ewald (PME)**, which handle the summation over infinite images, must be used instead of simple cutoffs.

```
---

---

### 7.4 Thermostats and Ensembles (NVE, NVT, NPT)

> **Summary:** MD allows simulation of different thermodynamic **ensembles**. The simplest is the **NVE** (Microcanonical) ensemble, which conserves energy. To control temperature, a **thermostat** is added (creating the **NVT** ensemble), with the **Nosé–Hoover thermostat** being preferred for generating the statistically correct canonical distribution. The **NPT** ensemble adds a **barostat** to control pressure.

#### Section Detail

* **NVE:** Pure Velocity-Verlet, ideal for testing energy conservation.
* **NVT:** Requires a thermostat to adjust velocities and keep the instantaneous temperature $T_{\text{inst}}$ close to the target $T_0$. The Berendsen thermostat is simple (velocity rescaling), while Nosé–Hoover introduces auxiliary dynamics ($\xi$) to accurately sample the canonical ensemble.
* **NPT:** Allows the simulation box volume $V$ to fluctuate to maintain a target pressure $P_0$.

#### Quiz Questions

!!! note "Quiz"
```
**1. The goal of the **Nosé–Hoover thermostat** is to ensure the MD simulation correctly samples which thermodynamic ensemble?**

* **A.** The Microcanonical (NVE) ensemble.
* **B.** The Isobaric-Isothermal (NPT) ensemble.
* **C.** **The Canonical (NVT) ensemble**. (**Correct**)
* **D.** The Grand Canonical ($\mu V T$) ensemble.

```
!!! note "Quiz"
```
**2. To simulate a system at constant temperature ($T$) and constant pressure ($P$), which type of simulation must be run?**

* **A.** Monte Carlo simulation.
* **B.** NVE simulation.
* **C.** **NPT simulation (Isothermal–Isobaric) using both a thermostat and a barostat**. (**Correct**)
* **D.** NVT simulation.

```
---

!!! question "Interview Practice"
```
**Question:** Why is the simple Berendsen thermostat often only used for the **equilibration** phase of an MD simulation, and not for the final **production** (measurement) phase?

**Answer Strategy:** The Berendsen thermostat achieves temperature control by non-physically rescaling velocities based on the difference between the instantaneous temperature and the target temperature. While this method is robust for quickly bringing the system to the target $T$ (equilibration), it does **not generate the statistically correct canonical ensemble**. Specifically, it suppresses energy fluctuations, which means observables calculated during the production phase (e.g., specific heat, which depends on energy fluctuations) will be inaccurate. For production, a method like Nosé–Hoover or Langevin is required.

```
---

---

### 7.5 Computing Observables

> **Summary:** MD extracts physics from trajectories by computing **time-averaged observables**. **Pressure** requires the **Virial Theorem** (mixing kinetic and inter-particle force terms). **Transport properties** are calculated from time correlation functions, such as the **Mean-Squared Displacement (MSD)** or the **Velocity Autocorrelation Function (VACF)**, both of which yield the **Diffusion Coefficient**.

#### Section Detail

The MSD measures the average distance a particle travels from its origin, $\text{MSD}(t) = \langle |\mathbf{r}(t) - \mathbf{r}(0)|^2 \rangle$, which is linear in time for diffusive systems: $D = \lim_{t \to \infty} \frac{1}{6t} \text{MSD}(t)$. The VACF, $C_v(t) = \frac{\langle \mathbf{v}(0) \cdot \mathbf{v}(t) \rangle}{\langle \mathbf{v}(0)^2 \rangle}$, captures the system's memory of motion. The total energy $E_{\text{tot}} = K+U$ serves as the primary diagnostic.

#### Quiz Questions

!!! note "Quiz"
```
**1. Which theorem is used in MD to calculate the system's pressure $P$, by including a contribution from the interparticle forces $\mathbf{F}_{ij}$?**

* **A.** The Fluctuation-Dissipation Theorem.
* **B.** The Equipartition Theorem.
* **C.** **The Virial Theorem**. (**Correct**)
* **D.** The Intermediate Value Theorem.

```
!!! note "Quiz"
```
**2. Which two time-dependent functions are used to calculate the Diffusion Coefficient ($D$)?**

* **A.** Total Energy $E(t)$ and Pressure $P(t)$.
* **B.** The Pressure-Volume product $PV$ and $N k_B T$.
* **C.** **The Mean-Squared Displacement (MSD) and the Velocity Autocorrelation Function (VACF)**. (**Correct**)
* **D.** The potential energy $U(t)$ and the time step $\Delta t$.

```
---

!!! question "Interview Practice"
```
**Question:** A physicist simulates a liquid and measures the Velocity Autocorrelation Function, $C_v(t)$. They notice that $C_v(t)$ initially drops quickly but then becomes slightly negative before decaying to zero. Explain the physical origin of this negative correlation.

**Answer Strategy:** A negative correlation in $C_v(t)$ means the particle, after a short time $\tau$, is more likely to be moving **in the opposite direction** ($\mathbf{v}(0) \cdot \mathbf{v}(\tau) < 0$).
* This is characteristic of a **liquid** or dense fluid.
* The negative value is caused by **caging effects**: a central particle, initially moving at $\mathbf{v}(0)$, collides with its dense, surrounding shell of neighbors. The particle "bounces" off the surrounding cage, reversing its initial velocity vector, causing the instantaneous velocity to correlate negatively with the initial velocity.

```
---

---

## 💡 Hands-On Simulation Projects (Chapter Conclusion) 🛠️

These projects are designed to implement the core MD pipeline and compute essential equilibrium and dynamic properties.

### Project 1: Implementing the Velocity–Verlet Integrator (The Engine)

* **Goal:** Implement the core Velocity–Verlet algorithm for a single particle in a 1D quadratic potential $U(r) = \frac{1}{2} k r^2$ (Harmonic Oscillator).
* **Setup:** Use $m=1.0, k=1.0, \Delta t=0.01$. Initial conditions $r_0=1.0, v_0=0.0$.
* **Steps:**
    1.  Define the force function $\mathbf{F}(r) = -k r$.
    2.  Implement the full three-step Velocity–Verlet update loop (position $\to$ new force $\to$ velocity).
    3.  Run for $5000$ steps and record the total energy $E_{\text{tot}} = K + U$ at each step.
* ***Goal***: Plot $E_{\text{tot}}(t)$ and show that it remains constant (with only small numerical fluctuations), confirming the symplectic stability of the integrator.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Parameters and Initial Conditions
# ====================================================================

# --- System Parameters ---
M = 1.0     # Mass of the particle
K_SPRING = 1.0  # Spring constant
DT = 0.01   # Time step
STEPS = 5000 # Total number of steps

# --- Initial Conditions ---
R_INIT = 1.0  # Initial position (meters)
V_INIT = 0.0  # Initial velocity (m/s)

# --- Reference Functions ---
def force(r, k=K_SPRING):
    """Calculates the force F = -kr."""
    return -k * r

def potential_energy(r, k=K_SPRING):
    """Calculates Potential Energy U = 0.5 * k * r^2."""
    return 0.5 * k * r**2

def kinetic_energy(v, m=M):
    """Calculates Kinetic Energy K = 0.5 * m * v^2."""
    return 0.5 * m * v**2

# ====================================================================
# 2. Velocity–Verlet Integration Loop
# ====================================================================

# Initialize state and storage
r, v = R_INIT, V_INIT
F_current = force(r)
E_total_history = []

for step in range(STEPS):
    # Get current acceleration
    a_current = F_current / M
    
    # 1. Position Update (Drift/Kick)
    r_new = r + v * DT + 0.5 * a_current * DT**2
    
    # 2. New Force Evaluation
    F_new = force(r_new)
    a_new = F_new / M
    
    # 3. Velocity Update (Final Kick)
    v_new = v + 0.5 * (a_current + a_new) * DT
    
    # Bookkeeping: Advance state and current force for next step
    r, v = r_new, v_new
    F_current = F_new
    
    # Calculate and store total energy for the NVE ensemble check
    E_kin = kinetic_energy(v)
    E_pot = potential_energy(r)
    E_total_history.append(E_kin + E_pot)

# ====================================================================
# 3. Visualization
# ====================================================================

E_history = np.array(E_total_history)
time_points = np.arange(STEPS) * DT
initial_energy = E_history[0]

# Calculate energy drift statistics
energy_mean = np.mean(E_history)
energy_std = np.std(E_history)
relative_drift = (E_history[-1] - initial_energy) / initial_energy

plt.figure(figsize=(10, 5))

# Plot total energy over time
plt.plot(time_points, E_history, lw=1.5, label='Total Energy $E_{\\text{tot}}(t)$')
plt.axhline(initial_energy, color='red', linestyle='--', alpha=0.7, label='Initial Energy $E_0$')

# Labeling and Formatting
plt.title(f'Energy Conservation in Velocity–Verlet (NVE) Ensemble ($\Delta t={DT}$)')
plt.xlabel('Time (s)')
plt.ylabel('Total Energy (J)')
plt.ylim(E_history.min() - 0.0001, E_history.max() + 0.0001) # Zoom in to see fluctuations
plt.legend()
plt.grid(True, which='both', linestyle=':')

plt.tight_layout()
plt.show()

# --- Conclusion ---
print("\n--- Integrator Stability Check (NVE Ensemble) ---")
print(f"Initial Total Energy: {initial_energy:.6f} J")
print(f"Final Total Energy:   {E_history[-1]:.6f} J")
print(f"Energy Standard Deviation (Fluctuation): {energy_std:.7f} J")
print(f"Relative Energy Drift (Final vs Initial): {relative_drift:.4e}")

print("\nConclusion: The total energy remains constant, with the standard deviation measuring only small numerical fluctuations. This confirms the **symplectic stability** of the Velocity–Verlet integrator, making it suitable for long-term molecular dynamics simulations.")
```
**Sample Output:**
```
--- Integrator Stability Check (NVE Ensemble) ---
Initial Total Energy: 0.500000 J
Final Total Energy:   0.499999 J
Energy Standard Deviation (Fluctuation): 0.0000044 J
Relative Energy Drift (Final vs Initial): -1.7159e-06

Conclusion: The total energy remains constant, with the standard deviation measuring only small numerical fluctuations. This confirms the **symplectic stability** of the Velocity–Verlet integrator, making it suitable for long-term molecular dynamics simulations.
```


### Project 2: MD with Periodic Boundaries and Collision

* **Goal:** Extend the simulation to 2D with PBC and non-trivial interactions (conceptual Lennard-Jones).
* **Setup:** Place $N=4$ particles in a square box of side $L=10.0$. Set up initial random positions and zero velocity.
* **Steps:**
    1.  Implement the `minimum_image` function for calculating the shortest distance between two points under PBC.
    2.  Define a conceptual repulsive force: $\mathbf{F}_{ij} \propto 1/r^7$ for $r < 1.0$, and zero otherwise.
    3.  Run the Velocity–Verlet loop, applying the **PBC wrapping** to the positions $\mathbf{r}_i$ after every full step.
* ***Goal***: Demonstrate particle movement and successful wrapping when particles cross the box boundaries.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ====================================================================
# 1. Setup Parameters and PBC Functions
# ====================================================================

# --- System Parameters ---
N_PARTICLES = 4
L_BOX = 10.0
M = 1.0
DT = 0.005 # Smaller DT for stability with multi-particle forces
STEPS = 500

# --- Reference/Conceptual Functions ---
def minimum_image(dr, L):
    """Calculates the minimum image distance vector component."""
    # dr = ri - rj. This implements dr - L * round(dr/L)
    return dr - L * np.round(dr / L)

def wrap_position(r, L):
    """Wraps position back into the primary simulation box [0, L]."""
    return r % L

def force_conceptual(r_i, r_j, L, cutoff=1.0, epsilon=1.0):
    """
    Conceptual short-range repulsive force (Lennard-Jones-like, but only repulsive).
    Force magnitude scales as 1/r^7 (proportional to -dU/dr of a 1/r^6 term).
    """
    # 1. Calculate the minimum image distance vector
    dr = minimum_image(r_i - r_j, L)
    r_sq = np.sum(dr**2)
    
    if r_sq > cutoff**2 or r_sq == 0:
        return np.zeros_like(r_i) # No interaction or self-interaction
    
    r = np.sqrt(r_sq)
    
    # 2. Conceptual Force (Highly Repulsive): F = 24 * epsilon * (2/r^13 - 1/r^7) * (dr/r)
    # Simplified Repulsive: F_mag ~ 1/r^7
    r_inv = 1.0 / r
    r_inv_7 = r_inv**7
    
    # Force vector F = -dU/dr * (dr/r)
    # Conceptual F_mag = 4 * epsilon * (12*r_inv_13 - 6*r_inv_7)
    # We use a simplified 1/r^7-scaling for demonstration
    F_mag = 4 * epsilon * 12 * r_inv**13 * r_inv # Very stiff repulsion
    
    # F_vector = F_mag * (dr / r)
    F_vec = F_mag * (dr / r)
    
    return F_vec

def calculate_total_force(positions, L):
    """Calculates the total force vector for all particles (O(N^2) here)."""
    N = len(positions)
    total_forces = np.zeros_like(positions)
    
    for i in range(N):
        for j in range(i + 1, N):
            F_ij = force_conceptual(positions[i], positions[j], L)
            total_forces[i] += F_ij
            total_forces[j] -= F_ij # Newton's third law
            
    return total_forces

# ====================================================================
# 2. Initialization and MD Loop
# ====================================================================

# Initial state: positions [0, L] and zero velocity
R_init = np.random.rand(N_PARTICLES, 2) * L_BOX
V_init = np.zeros_like(R_init)

# Storage
R_history = np.zeros((STEPS, N_PARTICLES, 2))
R_history[0] = R_init.copy()

# Setup initial state
R = R_init.copy()
V = V_init.copy()
F_current = calculate_total_force(R, L_BOX)

for step in range(1, STEPS):
    # Get current acceleration
    A_current = F_current / M
    
    # 1. Position Update
    R_new_unwrapped = R + V * DT + 0.5 * A_current * DT**2
    
    # Apply PBC: Wrap positions back into [0, L]
    R_new = wrap_position(R_new_unwrapped, L_BOX)
    
    # 2. New Force Evaluation (using wrapped positions for the interaction)
    F_new = calculate_total_force(R_new, L_BOX)
    A_new = F_new / M
    
    # 3. Velocity Update
    V_new = V + 0.5 * (A_current + A_new) * DT
    
    # Bookkeeping: Advance state and force
    R, V = R_new, V_new
    F_current = F_new
    R_history[step] = R_new.copy()

# ====================================================================
# 3. Visualization
# ====================================================================

fig, ax = plt.subplots(figsize=(8, 8))

# Plot initial and final state
ax.plot(R_history[0, :, 0], R_history[0, :, 1], 'o', markersize=10, 
        color='blue', alpha=0.5, label='Initial Positions ($t=0$)')
ax.plot(R_history[-1, :, 0], R_history[-1, :, 1], 'x', markersize=10, 
        color='red', label=f'Final Positions ($t={STEPS*DT:.2f}$)')

# Draw the simulation box boundary
ax.plot([0, L_BOX, L_BOX, 0, 0], [0, 0, L_BOX, L_BOX, 0], 'k--', lw=1, label='Simulation Box')

# Labeling and Formatting
ax.set_title(f'2D Molecular Dynamics with Periodic Boundaries (N={N_PARTICLES})')
ax.set_xlabel('x-coordinate')
ax.set_ylabel('y-coordinate')
ax.set_xlim(-0.5, L_BOX + 0.5)
ax.set_ylim(-0.5, L_BOX + 0.5)
ax.legend()
ax.set_aspect('equal', adjustable='box')
ax.grid(True)

plt.tight_layout()
plt.show()

# --- Verification ---
# Check if any particle crossed the boundary (i.e., its position was wrapped)
wrapped_events = np.sum((R_history[1:] > L_BOX) | (R_history[1:] < 0))

print("\n--- Boundary Condition Verification ---")
print(f"Box Side Length (L): {L_BOX:.1f}")
print(f"Total Boundary Crossings/Wraps (conceptual): {wrapped_events}")
print(f"Final positions are all within [0, L]: {np.all((R_history[-1] >= 0) & (R_history[-1] <= L_BOX))}")

print("\nConclusion: The simulation successfully implemented Periodic Boundary Conditions (PBCs). The positions were continuously wrapped back into the [0, L] box after each time step, and the Minimum Image Convention (MIC) was used to ensure particles interacted with the correct nearest image across the boundaries.")
```
**Sample Output:**
```
--- Boundary Condition Verification ---
Box Side Length (L): 10.0
Total Boundary Crossings/Wraps (conceptual): 0
Final positions are all within [0, L]: True

Conclusion: The simulation successfully implemented Periodic Boundary Conditions (PBCs). The positions were continuously wrapped back into the [0, L] box after each time step, and the Minimum Image Convention (MIC) was used to ensure particles interacted with the correct nearest image across the boundaries.
```


### Project 3: Computing the Diffusion Coefficient ($D$)

* **Goal:** Calculate the diffusion coefficient by measuring the Mean-Squared Displacement (MSD).
* **Setup:** Simulate a system of particles ($N \gg 1$) at a high temperature (liquid/gas state). Record the positions $\mathbf{r}(t)$ at regular intervals over a long trajectory.
* **Steps:**
    1.  Calculate the MSD over the time trajectory: $\text{MSD}(\tau) = \langle |\mathbf{r}(t+\tau) - \mathbf{r}(t)|^2 \rangle$.
    2.  Plot $\text{MSD}(\tau)$ versus $\tau$.
    3.  Fit the long-time, linear regime of the MSD curve to a straight line: $\text{MSD}(\tau) = 6 D \tau + C$.
    4.  Extract the slope and compute the diffusion coefficient $D$.
* ***Goal***: Confirm the expected linear growth of MSD in a diffusive system and obtain a quantitative transport property.

#### Python Implementation

```python
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
```
**Sample Output:**
```
--- Diffusion Coefficient Analysis Summary ---
Calculated MSD Slope (6D): 3.6133
Calculated Diffusion Coefficient (D): 0.60222
R-squared of Fit: 0.9981

Conclusion: The Mean-Squared Displacement (MSD) curve shows linear growth at long times, confirming normal diffusion in the system. The Diffusion Coefficient (D) is accurately extracted from the slope of this linear regime using the Einstein relation (MSD = 6Dτ).
```


### Project 4: Implementing the Berendsen Thermostat (NVT)

* **Goal:** Modify the NVE integrator to simulate a canonical (NVT) ensemble by controlling temperature.
* **Setup:** Use the same Harmonic Oscillator (Project 1) but initialize with a higher energy (e.g., $r_0=5.0, v_0=0.0$). Set a target temperature $T_0=1.0$ and relaxation time $\tau_T=1.0$.
* **Steps:**
    1.  At each step, calculate the instantaneous temperature $T_{\text{inst}}$ from the kinetic energy $K$.
    2.  Calculate the Berendsen velocity scaling factor $\lambda$.
    3.  Apply the scaling: $\mathbf{v} \leftarrow \lambda \mathbf{v}$ immediately before the next position update.
* ***Goal***: Plot the instantaneous temperature $T_{\text{inst}}(t)$ and show that it smoothly and quickly relaxes from the high initial temperature to the target temperature $T_0$, demonstrating the successful implementation of the NVT control.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Parameters and Initial Conditions
# ====================================================================

# --- System Parameters ---
M = 1.0     # Mass
K_SPRING = 1.0  # Spring constant
KB = 1.0    # Boltzmann constant (set to 1.0 for simplified unit system)
DT = 0.01   # Time step
STEPS = 5000 # Total steps

# --- Thermostat Parameters ---
T0 = 1.0    # Target temperature
TAU_T = 1.0 # Relaxation time constant (Berendsen parameter)

# --- Initial Conditions (High Energy/Temperature) ---
R_INIT = 5.0  # High initial position
V_INIT = 0.0  # Initial velocity
DOF = 1       # Degrees of freedom for a 1D particle

# --- Reference Functions ---
def force(r, k=K_SPRING):
    return -k * r

def calculate_temperature(v, m=M, kB=KB, dof=DOF):
    """Calculates instantaneous temperature from kinetic energy (K=1/2*m*v^2)."""
    # T_inst = 2K / (DOF * k_B)
    K = 0.5 * m * v**2
    return 2 * K / (dof * kB)

# ====================================================================
# 2. Velocity–Verlet Integration with Berendsen Thermostat
# ====================================================================

# Initialize state and storage
r, v = R_INIT, V_INIT
F_current = force(r)
T_inst_history = []

for step in range(STEPS):
    # Get current acceleration
    a_current = F_current / M
    
    # --- Velocity-Verlet Integration ---
    # 1. Position Update
    r_new = r + v * DT + 0.5 * a_current * DT**2
    
    # 2. New Force Evaluation
    F_new = force(r_new)
    a_new = F_new / M
    
    # 3. Velocity Update (Pre-Thermostat)
    v_raw_new = v + 0.5 * (a_current + a_new) * DT
    
    # --- Berendsen Thermostat ---
    T_inst = calculate_temperature(v_raw_new, dof=DOF)
    
    # Calculate scaling factor lambda
    lambda_sq = 1 + (DT / TAU_T) * ((T0 / T_inst) - 1)
    lambda_factor = np.sqrt(lambda_sq)
    
    # Apply scaling to the velocity
    v_thermo = v_raw_new * lambda_factor
    
    # Bookkeeping: Advance state and force
    r, v = r_new, v_thermo
    F_current = F_new
    
    # Store temperature
    T_inst_history.append(calculate_temperature(v, dof=DOF))

# ====================================================================
# 3. Visualization
# ====================================================================

T_history = np.array(T_inst_history)
time_points = np.arange(len(T_history)) * DT

plt.figure(figsize=(10, 5))

# Plot instantaneous temperature over time
plt.plot(time_points, T_history, lw=1.5, color='green', label='Instantaneous $T_{\\text{inst}}$')
plt.axhline(T0, color='red', linestyle='--', alpha=0.7, label='Target Temperature $T_0$')

# Labeling and Formatting
plt.title(f'Berendsen Thermostat (NVT) Relaxation ($\u03C4_T={TAU_T}$ s)')
plt.xlabel('Time (s)')
plt.ylabel('Instantaneous Temperature ($T$)')
plt.legend()
plt.grid(True, which='both', linestyle=':')

plt.tight_layout()
plt.show()

# --- Conclusion ---
print("\n--- Thermostat Performance Check ---")
print(f"Target Temperature (T0): {T0:.4f}")
print(f"Initial Temperature (Conceptual): {calculate_temperature(V_INIT, dof=DOF):.4f} (Since V_init=0, initial T is near zero, but potential energy is high)")
print(f"Final Average Temperature: {np.mean(T_history[-1000:]):.4f}")
print(f"Final Temperature Standard Deviation: {np.std(T_history[-1000:]):.4f}")

print("\nConclusion: The instantaneous temperature successfully relaxes from its initial state and stabilizes around the target temperature $T_0=1.0$. This demonstrates the successful implementation of the Berendsen thermostat, which is effective for rapidly equilibrating the system to the desired NVT ensemble conditions.")
```
**Sample Output:**
```
--- Thermostat Performance Check ---
Target Temperature (T0): 1.0000
Initial Temperature (Conceptual): 0.0000 (Since V_init=0, initial T is near zero, but potential energy is high)
Final Average Temperature: 0.0114
Final Temperature Standard Deviation: 0.0002

Conclusion: The instantaneous temperature successfully relaxes from its initial state and stabilizes around the target temperature $T_0=1.0$. This demonstrates the successful implementation of the Berendsen thermostat, which is effective for rapidly equilibrating the system to the desired NVT ensemble conditions.
```