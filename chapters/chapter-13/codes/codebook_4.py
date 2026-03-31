# Source: Simulation/chapter-13/codebook.md -- Block 4

import numpy as np
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Parameters and The ODE System
# ====================================================================

# --- Toggle Switch Parameters ---
# Parameters chosen to ensure bistability (high Hill coefficients)
ALPHA1 = 5.0  # Max synthesis rate for u
ALPHA2 = 5.0  # Max synthesis rate for v
BETA_HILL = 3.0 # Hill coefficient (cooperativity) for v repressing u
GAMMA_HILL = 3.0 # Hill coefficient (cooperativity) for u repressing v

# --- Simulation Parameters ---
DT = 0.01  # Time step
T_FINAL = 50.0  # Total time (ms)

def toggle_ode_system(S_current):
    """
    Implements the coupled ODEs for the genetic toggle switch:
    S = [u, v]
    """
    u, v = S_current
    
    # ODE for u: du/dt = alpha1 / (1 + v^beta) - u 
    dudt = (ALPHA1 / (1.0 + v**BETA_HILL)) - u
    
    # ODE for v: dv/dt = alpha2 / (1 + u^gamma) - v
    dvdt = (ALPHA2 / (1.0 + u**GAMMA_HILL)) - v
    
    return np.array([dudt, dvdt])

# ====================================================================
# 2. RK4 Solver Implementation
# ====================================================================

def rk4_step(func, S, dt):
    """Performs one RK4 time step for the state vector S = [u, v]."""
    k1 = func(S)
    k2 = func(S + 0.5 * dt * k1)
    k3 = func(S + 0.5 * dt * k2)
    k4 = func(S + dt * k3)
    return S + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

def run_simulation(S_initial):
    """Runs the simulation from a given initial state and records history."""
    steps = int(T_FINAL / DT)
    u_history = np.zeros(steps)
    v_history = np.zeros(steps)
    
    S = S_initial.copy()
    
    for i in range(steps):
        S = rk4_step(toggle_ode_system, S, DT)
        u_history[i] = S[0]
        v_history[i] = S[1]
        
    return u_history, v_history

# ====================================================================
# 3. Bistability Scenarios and Simulation
# ====================================================================

# --- Run A: Initial State biased towards u (u HIGH, v LOW) ---
S_INIT_A = np.array([10.0, 1.0])
uA, vA = run_simulation(S_INIT_A)

# --- Run B: Initial State biased towards v (u LOW, v HIGH) ---
S_INIT_B = np.array([1.0, 10.0])
uB, vB = run_simulation(S_INIT_B)

time_points = np.arange(0, T_FINAL, DT)

# ====================================================================
# 4. Visualization
# ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Trajectories (Time Series)
ax[0].plot(time_points, uA, label='u (Run A: High u0)', color='darkblue', lw=2)
ax[0].plot(time_points, vA, label='v (Run A: High u0)', color='skyblue', lw=2)
ax[0].plot(time_points, uB, label='u (Run B: High v0)', color='darkred', lw=2, linestyle='--')
ax[0].plot(time_points, vB, label='v (Run B: High v0)', color='salmon', lw=2, linestyle='--')
ax[0].set_title('Genetic Toggle Switch: Trajectories')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Concentration')
ax[0].legend()
ax[0].grid(True)

# Plot 2: Bistability (Phase Space/u vs v)
ax[1].plot(uA, vA, label='Run A: Attractor 1 (u HIGH)', color='darkblue', lw=2)
ax[1].plot(uB, vB, label='Run B: Attractor 2 (v HIGH)', color='darkred', lw=2, linestyle='--')
ax[1].plot(uA[0], vA[0], 'ko', label='Start A', markersize=6)
ax[1].plot(uB[0], vB[0], 'ks', label='Start B', markersize=6)
ax[1].plot(uA[-1], vA[-1], 'go', label='End A', markersize=8)
ax[1].plot(uB[-1], vB[-1], 'g^', label='End B', markersize=8)

ax[1].set_title('Bistability: Convergence to Two Attractors')
ax[1].set_xlabel('Concentration u')
ax[1].set_ylabel('Concentration v')
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- Genetic Toggle Switch Bistability Analysis ---")
print(f"Run A (Start u=10, v=1): Final State (u={uA[-1]:.2f}, v={vA[-1]:.2f}) -> Attractor 1 (u HIGH)")
print(f"Run B (Start u=1, v=10): Final State (u={uB[-1]:.2f}, v={vB[-1]:.2f}) -> Attractor 2 (v HIGH)")

print("\nConclusion: The simulation demonstrates **bistability**—the fundamental mechanism for binary decision-making in cells. Despite the identical governing equations, the system converges to one of two distinct stable states (attractors) based entirely on the initial conditions, confirming the logical switch functionality of the mutually inhibitory genetic circuit.")
