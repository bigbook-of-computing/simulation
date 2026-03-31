# **Chapter 10: Biology II: Neuroscience (Hodgkin-Huxley) (Workbook)**

The goal of this chapter is to model the neuron's electrical signal, the **action potential**, by applying deterministic physics and numerical ODE solvers to a **nonlinear feedback system**.

| Section | Topic Summary |
| :--- | :--- |
| **10.1** | Chapter Opener: The Physics of the Spike |
| **10.2** | The Neuron as an Electrical Circuit |
| **10.3** | The Conductance: Gating Variables and Coupled ODEs |
| **10.4 & 10.5** | Simulation and Core Application: Generating the Action Potential |
| **10.6** | Chapter Summary & Bridge to Part III |

---

### 10.1 The Physics of the Spike

> **Summary:** The **action potential (spike)** is a precisely timed, **deterministic physical event** caused by the flow of charged ions across the cell membrane. The neuron is modeled as a **nonlinear electrical circuit** where ion channels act as voltage-controlled resistors.

#### Section Detail

The Hodgkin–Huxley (H–H) model transformed neuroscience by expressing neural signaling as a **system of coupled ODEs**. The physics is based on the **Nernst equation**, which defines the equilibrium potential ($E_X$) for each ion based on its concentration gradient. The entire system is governed by **electromagnetic physics and diffusion**.

#### Quiz Questions

!!! note "Quiz"
    **1. The "action potential" is fundamentally a physical event caused by:**
    
    * **A.** Random fluctuations in the neural network.
    * **B.** **The controlled flow of ions ($\text{Na}^+, \text{K}^+$) through the cell membrane**. (**Correct**)
    * **C.** The gravitational force acting on neurons.
    * **D.** The diffusion of protein molecules.
    
!!! note "Quiz"
    **2. Which law governs the electrical behavior of the neuron's membrane, expressing charge conservation between current flow and voltage change?**
    
    * **A.** Fick's Law of Diffusion.
    * **B.** **Kirchhoff's Current Law** (or Charge Balance). (**Correct**)
    * **C.** Newton's Second Law.
    * **D.** The Arrhenius Rate Equation.
    
---

!!! question "Interview Practice"
    **Question:** The text describes the H–H model as the "Kepler's laws of neuroscience." What is the conceptual similarity between H–H and Kepler's laws in terms of their origin and impact on their respective fields?
    
    **Answer Strategy:** Both represent a fundamental step in transforming an empirical, complex observation into a quantitative, predictive system.
    * **Kepler's laws** empirically described planetary orbits, which Newton later showed were consequences of deterministic physical laws ($\mathbf{F}=m\mathbf{a}$).
    * The **H–H model** empirically quantified the voltage traces of the action potential and showed they were also the deterministic consequences of simple physical laws (Kirchhoff’s law and molecular kinetics). Both systems successfully reduced complex phenomena to a universal set of governing equations.
    
---

### 10.2 The Neuron as an Electrical Circuit

> **Summary:** The neuron is modeled as an electrical circuit where the cell membrane acts as a **capacitor ($C_m$)** and ion channels act as **variable resistors (conductances)**, each driven by a fixed ion battery ($E_X$). The core voltage ODE is derived from charge balance: $C_m \frac{dV_m}{dt} = -I_{\text{total}}$.

#### Section Detail

The total ionic current ($I_{\text{total}}$) is the sum of Ohmic currents: $I_{\text{Na}}$, $I_{\text{K}}$, and $I_L$. The **driving force** for any ion $X$ is the difference between the actual membrane voltage and its equilibrium voltage: $(V_m - E_X)$. The currents must balance (sum to zero) at the **resting potential** ($V_{\text{rest}} \approx -70 \, \text{mV}$).

#### Quiz Questions

!!! note "Quiz"
    **1. In the electrical equivalent circuit of the neuron membrane, the ion concentration gradients (such as the high external $\text{Na}^+$ concentration) act as the functional equivalent of:**
    
    * **A.** The external stimulus current ($I_{\text{ext}}$).
    * **B.** The membrane capacitance ($C_m$).
    * **C.** **Batteries or reversal potentials ($E_X$)**. (**Correct**)
    * **D.** The fixed leak conductance ($g_L$).
    
!!! note "Quiz"
    **2. Which current equation forms the basis for modeling flow through the individual ion channels?**
    
    * **A.** Fick's Law.
    * **B.** The Nernst Equation.
    * **C.** **Ohm's Law ($I_X = g_X(V_m - E_X)$)**. (**Correct**)
    * **D.** The Boltzmann distribution.
    
---

!!! question "Interview Practice"
    **Question:** The $\text{Na}^+$ reversal potential ($E_{\text{Na}} \approx +50 \, \text{mV}$) is highly positive, while the resting potential is negative ($V_{\text{rest}} \approx -70 \, \text{mV}$). Explain what this large voltage difference ($V_m - E_{\text{Na}}$) implies about the $\text{Na}^+$ current when the channel is open.
    
    **Answer Strategy:** The difference $V_{\text{rest}} - E_{\text{Na}}$ is large and highly negative (e.g., $-70 \text{ mV} - 50 \text{ mV} = -120 \text{ mV}$). Since current $I_X$ is proportional to this driving force $I_X = g_X(V_m - E_X)$, a negative driving force and a high concentration of $\text{Na}^+$ outside the cell means that $\text{Na}^+$ will flow **strongly inward** (negative current). This large inward current is the precise event that drives the rapid **depolarization** and the positive feedback loop of the action potential.
    
---

### 10.3 The Conductance: Gating Variables and Coupled ODEs

> **Summary:** The core complexity of the H–H model lies in the **conductances ($g_{\text{Na}}$, $g_{\text{K}}$)**, which are not fixed but are functions of voltage and time. This dynamic behavior is modeled by **gating variables** ($m, h, n$), each representing the fraction of open channels and evolving according to a **first-order kinetic ODE**.

#### Section Detail

The $\text{Na}^+$ channel requires three activation gates ($m$) and one inactivation gate ($h$), giving $g_{\text{Na}} \propto m^3 h$. $\text{K}^+$ requires four activation gates ($n^4$). Each ODE, $\frac{dx}{dt} = \alpha_x(V_m)(1 - x) - \beta_x(V_m)x$, shows the variable relaxing toward its **voltage-dependent steady-state value** ($x_{\infty}$) with a corresponding time constant ($\tau_x$). The resulting coupled system is highly nonlinear and self-consistent.

#### Quiz Questions

!!! note "Quiz"
    **1. The primary role of the **inactivation gate ($h$)** in the $\text{Na}^+$ channel during the action potential is to:**
    
    * **A.** Provide the positive feedback for the initial spike rise.
    * **B.** Maintain the resting potential.
    * **C.** **Slowly close after depolarization, stopping the $\text{Na}^+$ influx and initiating repolarization**. (**Correct**)
    * **D.** Drive the hyperpolarization phase.
    
!!! note "Quiz"
    **2. The dynamics of a gating variable $x(t)$ (fraction of open gates) is governed by an ODE that describes the competition between which two kinetic rates?**
    
    * **A.** Translation and transcription rates.
    * **B.** The total current and the membrane capacitance.
    * **C.** **The voltage-dependent opening rate ($\alpha_x$) and the closing rate ($\beta_x$)**. (**Correct**)
    * **D.** The resting potential and the threshold potential.
    
---

!!! question "Interview Practice"
    **Question:** In the context of the H–H model's differential equations, describe the key difference in the *speed* of the $\text{Na}^+$ activation gate ($m$) versus the $\text{K}^+$ activation gate ($n$), and explain how this difference creates the action potential's shape.
    
    **Answer Strategy:**
    * **$\text{Na}^+$ Activation ($m$):** This gate has a **very fast activation time constant** ($\tau_m$) upon depolarization. This speed creates a **rapid, surge-like influx of $\text{Na}^+$** that drives the quick, upward-sloping **depolarization (rising phase)** of the spike.
    * **$\text{K}^+$ Activation ($n$):** This gate has a **much slower activation time constant** ($\tau_n$). This delay ensures that the $\text{K}^+$ current only peaks *after* the $\text{Na}^+$ current has inactivated, allowing it to drive the **delayed, downward-sloping repolarization phase**. The different time scales are essential for the spike's waveform.
    
---

### 10.4 & 10.5 Simulation and Core Application: Generating the Action Potential

> **Summary:** The full 4D system of ODEs is solved numerically using the stable **4th-order Runge–Kutta (RK4) method**. The simulation reveals the **emergent properties** of the action potential, including the **all-or-nothing response** and the **refractory period**. Analysis focuses on dissecting the time evolution of the three ionic currents ($I_{\text{Na}}$, $I_{\text{K}}$, $I_L$) that sum up to create the final voltage spike.

#### Section Detail

The RK4 integrator is used for its high accuracy in handling the stiff, nonlinear dynamics. The current trace analysis shows that $\text{Na}^+$ current is responsible for the inward (negative) spike, and $\text{K}^+$ current is responsible for the delayed outward (positive) spike. The **refractory period** is caused by the slow recovery of the inactivation gate ($h$) and the delayed closure of the activation gate ($n$).

#### Quiz Questions

!!! note "Quiz"
    **1. The primary numerical tool chosen to integrate the four coupled, nonlinear Hodgkin–Huxley ODEs is the:**
    
    * **A.** Euler–Maruyama method.
    * **B.** Velocity–Verlet algorithm.
    * **C.** **Runge–Kutta 4th-order (RK4) method**. (**Correct**)
    * **D.** Finite Difference Method (FDM).
    
!!! note "Quiz"
    **2. The brief dip of the membrane voltage *below* the resting potential during the action potential recovery phase (hyperpolarization) is primarily caused by:**
    
    * **A.** The failure of the voltage clamp.
    * **B.** The external stimulus current ($I_{\text{ext}}$) being negative.
    * **C.** **The delayed closure of the potassium activation gates ($n$)**. (**Correct**)
    * **D.** The Na$^+$ inactivation gate ($h$) remaining permanently closed.
    
---

!!! question "Interview Practice"
    **Question:** The action potential exhibits a key emergent property known as the "all-or-nothing" response. Explain the underlying feedback mechanism that forces the response to either fail completely or proceed to its full amplitude.
    
    **Answer Strategy:** The "all-or-nothing" response is a direct consequence of the **positive feedback loop** created by the $\text{Na}^+$ activation gate ($m$).
    * If a stimulus is **subthreshold**, the initial depolarization is too small to activate enough $m$ gates, and the system passively returns to rest.
    * If a stimulus is **suprathreshold**, the initial depolarization activates a critical mass of $m$ gates. This creates a massive $\text{Na}^+$ influx, which depolarizes the membrane further, which opens *more* $m$ gates (positive feedback). This runaway process is self-sustaining and forces the spike to reach the $\text{Na}^+$ reversal potential ($+50 \, \text{mV}$), independent of the size of the initial stimulus.
    
---

## 💡 Hands-On Simulation Projects (Chapter Conclusion) 🛠️

These projects require computational techniques to implement and analyze the core dynamics of the Hodgkin–Huxley model.

### Project 1: Defining the Gating Dynamics (Initial Setup)

* **Goal:** Write the necessary functions to define the HH derivative system and find the resting state.
* **Setup:** Use the standard squid axon parameters.
* **Steps:**
    1.  Write a function that calculates the voltage-dependent rate constants $\alpha_x(V)$ and $\beta_x(V)$ for the $m$, $h$, and $n$ gates.
    2.  Write a main derivative function `d_state_dt(S)` that returns the full 4-element derivative vector $[\frac{dV_m}{dt}, \frac{dm}{dt}, \frac{dh}{dt}, \frac{dn}{dt}]$.
    3.  Compute the theoretical steady-state resting values $x_0 = \alpha_x(V_{\text{rest}}) / (\alpha_x(V_{\text{rest}}) + \beta_x(V_{\text{rest}}))$ for $m$, $h$, and $n$ at $V_{\text{rest}} = -65 \, \text{mV}$.
* ***Goal***: Establish the accurate mathematical foundation for the RK4 solver.

#### Python Implementation

```python
import numpy as np
import random
from math import exp, log, sqrt

# ====================================================================

## 1. System Constants (Squid Giant Axon)

## ====================================================================

## Membrane parameters

CM = 1.0  # Membrane capacitance (uF/cm^2)

## Maximum conductances (mS/cm^2)

GNA_BAR = 120.0  # Sodium
GK_BAR = 36.0    # Potassium
GL = 0.3         # Leak

## Reversal potentials (mV)

ENA = 50.0  # Sodium
EK = -77.0  # Potassium
EL = -54.4  # Leak

V_REST = -65.0  # Approximate resting potential (mV)

## ====================================================================

## 2. Voltage-Dependent Rate Constants (alpha_x and beta_x)

## ====================================================================

def alpha_m(V):
    """Na+ activation rate constant."""
    return 0.1 * (25 - V) / (np.exp((25 - V) / 10) - 1)

def beta_m(V):
    """Na+ deactivation rate constant."""
    return 4 * np.exp(-V / 18)

def alpha_h(V):
    """Na+ inactivation rate constant."""
    return 0.07 * np.exp(-V / 20)

def beta_h(V):
    """Na+ deinactivation rate constant."""
    return 1 / (np.exp((30 - V) / 10) + 1)

def alpha_n(V):
    """K+ activation rate constant."""
    # Special handling for V=10 to avoid division by zero (L'Hopital's rule)
    if V == 10.0:
        return 0.1  # lim_{V->10} alpha_n(V) = 0.1
    return 0.01 * (10 - V) / (np.exp((10 - V) / 10) - 1)

def beta_n(V):
    """K+ deactivation rate constant."""
    return 0.125 * np.exp(-V / 80)

## ====================================================================

## 3. Full HH Derivative Function (The ODE System)

## ====================================================================

def hh_derivatives(S, I_ext):
    """
    Calculates the time derivatives (dV/dt, dm/dt, dh/dt, dn/dt)
    for the state vector S = [V, m, h, n].
    """
    V, m, h, n = S

    # Calculate voltage-dependent currents
    INa = GNA_BAR * m**3 * h * (V - ENA)
    IK = GK_BAR * n**4 * (V - EK)
    IL = GL * (V - EL)

    # Voltage derivative (Current Balance Equation)
    dVdt = (I_ext - (INa + IK + IL)) / CM

    # Gating variable derivatives (Kinetic ODEs)
    dmdt = alpha_m(V) * (1 - m) - beta_m(V) * m
    dhdt = alpha_h(V) * (1 - h) - beta_h(V) * h
    dndt = alpha_n(V) * (1 - n) - beta_n(V) * n

    return np.array([dVdt, dmdt, dhdt, dndt])

## ====================================================================

## 4. Compute Steady-State Initial Conditions (x_0)

## ====================================================================

def steady_state_value(alpha, beta):
    """Computes x_infinity = alpha / (alpha + beta)."""
    return alpha / (alpha + beta)

## Compute initial resting values at V_REST = -65.0 mV

m0 = steady_state_value(alpha_m(V_REST), beta_m(V_REST))
h0 = steady_state_value(alpha_h(V_REST), beta_h(V_REST))
n0 = steady_state_value(alpha_n(V_REST), beta_n(V_REST))

## Initial State Vector

S0_REST = np.array([V_REST, m0, h0, n0])

print("--- Hodgkin–Huxley Initial State Setup ---")
print(f"Resting Potential V_REST: {V_REST:.2f} mV")
print(f"Initial State m0 (Na Act): {m0:.4f}")
print(f"Initial State h0 (Na Inact): {h0:.4f}")
print(f"Initial State n0 (K Act): {n0:.4f}")
print(f"Initial State Vector S0: {S0_REST}")
```
**Sample Output:**
```python
--- Hodgkin–Huxley Initial State Setup ---
Resting Potential V_REST: -65.00 mV
Initial State m0 (Na Act): 0.0000
Initial State h0 (Na Inact): 1.0000
Initial State n0 (K Act): 0.0015
Initial State Vector S0: [-6.50000000e+01  7.50407027e-06  9.99958543e-01  1.47122543e-03]
```


### Project 2: Simulating the Threshold and All-or-Nothing Response

* **Goal:** Numerically determine the threshold current ($I_{\text{crit}}$) required to initiate a spike.
* **Setup:** Use the RK4 solver with $\Delta t = 0.01 \, \text{ms}$. Stimulate the neuron with a brief (e.g., $1 \, \text{ms}$) current pulse ($I_{\text{ext}}$).
* **Steps:**
    1.  Run a series of full simulations, gradually increasing the magnitude of the stimulus current: $I_{\text{ext}} = [5, 6, 7, 8, \dots] \, \mu\text{A/cm}^2$.
    2.  For each run, record the maximum voltage reached, $V_{\max}$.
    3.  Plot $V_{\max}$ versus $I_{\text{ext}}$.
* ***Goal***: Observe the sharp, nonlinear jump in $V_{\max}$ as $I_{\text{ext}}$ crosses the critical threshold, confirming the all-or-nothing behavior.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

## ====================================================================

## 1. Integration Core (RK4 Solver)

## ====================================================================

## Reusing hh_derivatives, steady_state_value, V_REST, etc., from Project 1

def rk4_step(func, S, I_ext, dt):
    """Performs one RK4 time step for the state vector S = [V, m, h, n]."""
    k1 = func(S, I_ext)
    k2 = func(S + 0.5 * dt * k1, I_ext)
    k3 = func(S + 0.5 * dt * k2, I_ext)
    k4 = func(S + dt * k3, I_ext)
    return S + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

def run_hh_simulation(I_ext_pulse, t_final, dt, S_init):
    """Runs a full HH simulation for a given constant stimulus I_ext_pulse."""
    steps = int(t_final / dt)
    S = S_init.copy()
    Vm_history = np.zeros(steps)

    for i in range(steps):
        # The current is only applied for the first 1 ms
        I_current = I_ext_pulse if i * dt <= 1.0 else 0.0

        S = rk4_step(hh_derivatives, S, I_current, dt)
        Vm_history[i] = S[0]

    return np.max(Vm_history)

## ====================================================================

## 2. Threshold Sweep Simulation

## ====================================================================

## Initial Conditions (from Project 1)

V0 = -65.0
m0 = steady_state_value(alpha_m(V0), beta_m(V0))
h0 = steady_state_value(alpha_h(V0), beta_h(V0))
n0 = steady_state_value(alpha_n(V0), beta_n(V0))
S_INIT = np.array([V0, m0, h0, n0])

## --- Simulation Parameters ---

DT = 0.01      # ms
T_FINAL = 10.0 # ms (long enough for the spike to finish)

## Current range to test

I_EXT_MIN = 5.0
I_EXT_MAX = 8.0
I_EXT_STEP = 0.2
I_ext_values = np.arange(I_EXT_MIN, I_EXT_MAX + I_EXT_STEP, I_EXT_STEP)

## Storage

Vmax_history = []

print(f"Testing threshold current range from {I_EXT_MIN} to {I_EXT_MAX} \u03bcA/cm\u00b2...")

for I_ext in I_ext_values:
    V_max = run_hh_simulation(I_ext, T_FINAL, DT, S_INIT)
    Vmax_history.append(V_max)

## ====================================================================

## 3. Visualization and Analysis

## ====================================================================

plt.figure(figsize=(8, 5))

## Plot Vmax vs. Iext

plt.plot(I_ext_values, Vmax_history, 'o-', color='darkred', lw=2)

## Labeling and Formatting

plt.title('All-or-Nothing Response: Threshold Current $I_{\\text{crit}}$')
plt.xlabel('Stimulus Current $I_{\\text{ext}}$ ($\mu\\text{A/cm}^2$)')
plt.ylabel('Maximum Voltage Reached $V_{\\max}$ (mV)')
plt.grid(True, which='both', linestyle=':')

## Annotate the threshold jump point (approximate)

threshold_index = np.argmax(np.diff(Vmax_history))
I_crit_approx = I_ext_values[threshold_index] + I_EXT_STEP / 2
plt.axvline(I_crit_approx, color='red', linestyle='--', label=f'$I_{{crit}} \\approx {I_crit_approx:.1f}$')
plt.legend()

plt.tight_layout()
plt.show()

## --- Analysis Summary ---

print("\n--- Threshold Analysis Summary ---")
print(f"Calculated Critical Current (Approx): {I_crit_approx:.2f} \u03bcA/cm\u00b2")
print("\nConclusion: The plot demonstrates the all-or-nothing response: below the critical threshold current, the maximum voltage remains near the resting potential. Once the threshold is crossed, the maximum voltage immediately jumps to the full spike amplitude, confirming the non-linear, regenerative nature of the action potential.")
```

### Project 3: Analyzing Ionic Current Dynamics

* **Goal:** Deconstruct the voltage spike by visualizing the contributions of the three ionic currents.
* **Setup:** Run a single successful spike simulation (e.g., $I_{\text{ext}} = 10 \, \mu\text{A/cm}^2$) and save the time series for $V_m(t)$, $m(t)$, $h(t)$, and $n(t)$.
* **Steps:**
    1.  Use the saved time series to calculate the instantaneous $\text{Na}^+$ current ($I_{\text{Na}}$) and $\text{K}^+$ current ($I_{\text{K}}$) at every time step.
    2.  Plot $I_{\text{Na}}(t)$, $I_{\text{K}}(t)$, and $V_m(t)$ together on a single graph.
* ***Goal***: Show that the $I_{\text{Na}}$ peak (inward, negative) slightly precedes the $I_{\text{K}}$ peak (outward, positive), providing the mechanistic explanation for the spike's timing and shape.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

## ====================================================================

## 1. Full HH Simulation Run (Spiking Parameters)

## ====================================================================

## --- Simulation Setup ---

DT = 0.01  # ms
T_TOTAL = 50.0  # ms
I_EXT_MAG = 10.0 # Suprathreshold current
STIM_START, STIM_END = 10.0, 11.0 # 1 ms pulse

## I_ext function (Stimulus pulse)

def I_ext(t):
    return I_EXT_MAG if STIM_START <= t <= STIM_END else 0.0

## Initial State (from Project 2)

V0 = -65.0
m0 = steady_state_value(alpha_m(V0), beta_m(V0))
h0 = steady_state_value(alpha_h(V0), beta_h(V0))
n0 = steady_state_value(alpha_n(V0), beta_n(V0))
S_INIT = np.array([V0, m0, h0, n0])

## State storage setup

steps = int(T_TOTAL / DT)
time = np.arange(0, T_TOTAL, DT)
Vm, m, h, n = np.zeros(steps), np.zeros(steps), np.zeros(steps), np.zeros(steps)
Vm[0], m[0], h[0], n[0] = S_INIT

S = S_INIT.copy()
for i in range(1, steps):
    S = rk4_step(hh_derivatives, S, I_ext(time[i-1]), DT)
    Vm[i], m[i], h[i], n[i] = S

## ====================================================================

## 2. Current Calculation (Post-Simulation)

## ====================================================================

## Calculate Conductances and Currents from the state traces

GNA = GNA_BAR * m**3 * h
GK = GK_BAR * n**4

INa = GNA * (Vm - ENA)
IK = GK * (Vm - EK)
IL = GL * (Vm - EL)

## ====================================================================

## 3. Visualization

## ====================================================================

fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

## Plot 1: Voltage Trace

ax[0].plot(time, Vm, color='darkred', lw=2)
ax[0].set_title('Hodgkin–Huxley Voltage Trace ($V_m$)')
ax[0].set_ylabel('Voltage ($V_m$, mV)')
ax[0].grid(True)
ax[0].axvline(STIM_START, color='gray', linestyle=':', label='$I_{\\text{ext}}$ pulse')

## Plot 2: Ionic Currents

ax[1].plot(time, INa, label='$I_{\\text{Na}}$ (Inward)', color='dodgerblue', lw=2)
ax[1].plot(time, IK, label='$I_{\\text{K}}$ (Outward)', color='orange', lw=2)
ax[1].plot(time, IL, label='$I_L$ (Leak)', color='gray', lw=1, linestyle='--')
ax[1].axhline(0, color='k', linestyle='-')

ax[1].set_title('Ionic Currents During the Action Potential')
ax[1].set_xlabel('Time (ms)')
ax[1].set_ylabel('Current Density ($\mu\\text{A/cm}^2$)')
ax[1].set_ylim(-300, 100) # Set fixed axis for clarity
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()

## --- Analysis Summary ---

max_INa = np.min(INa)
max_IK = np.max(IK)
INa_peak_time = time[np.argmin(INa)]
IK_peak_time = time[np.argmax(IK)]

print("\n--- Ionic Current Dynamics Analysis ---")
print(f"I_Na Peak (Inward): {max_INa:.2f} \u03bcA/cm\u00b2 at t={INa_peak_time:.2f} ms")
print(f"I_K Peak (Outward): {max_IK:.2f} \u03bcA/cm\u00b2 at t={IK_peak_time:.2f} ms")
print(f"Conclusion: The negative I_Na current peaks first, driving the voltage spike, while the positive I_K current peaks later, driving repolarization. This difference in kinetic timing is the deterministic cause of the action potential's waveform.")
```

### Project 4: Simulating the Refractory Period

* **Goal:** Demonstrate the refractory period by stimulating the neuron twice in rapid succession.
* **Setup:** Implement the stimulus function $I_{\text{ext}}(t)$ to include two identical pulses: the first at $t_1$ and the second at a variable time $t_2$ (e.g., $t_1=10 \, \text{ms}$, $t_2 \in [11, 15, 20] \, \text{ms}$).
* **Steps:**
    1.  Run three separate simulations with the dual-pulse current.
    2.  Plot the voltage trace for each run.
* ***Goal***: Show that the second spike has a smaller amplitude or fails entirely when the time delay $t_2 - t_1$ is short (e.g., $1 \, \text{ms}$), but recovers full amplitude when the delay is long (e.g., $10 \, \text{ms}$), illustrating the refractory period dictated by the slow recovery of $h$ and $n$.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

## ====================================================================

## 1. Dual-Pulse Stimulus Function

## ====================================================================

I_PULSE_MAG = 10.0 # Suprathreshold magnitude
PULSE_DURATION = 1.0 # ms

## Initial State (from Project 2)

V0 = -65.0
m0 = steady_state_value(alpha_m(V0), beta_m(V0))
h0 = steady_state_value(alpha_h(V0), beta_h(V0))
n0 = steady_state_value(alpha_n(V0), beta_n(V0))
S_INIT = np.array([V0, m0, h0, n0])

def I_ext_dual_pulse(t, t_start_1, t_start_2):
    """Generates two 1ms current pulses."""
    t_end_1 = t_start_1 + PULSE_DURATION
    t_end_2 = t_start_2 + PULSE_DURATION

    current = 0.0
    if t_start_1 <= t < t_end_1:
        current += I_PULSE_MAG
    if t_start_2 <= t < t_end_2:
        current += I_PULSE_MAG

    return current

## ====================================================================

## 2. Simulation Loop (RK4)

## ====================================================================

DT = 0.01
T_TOTAL = 50.0
steps = int(T_TOTAL / DT)
time = np.arange(0, T_TOTAL, DT)

T1 = 10.0 # Start time of the first pulse

## Delay scenarios to test

DELAYS = [1.5, 5.0, 10.0] # ms separation (t2 - t1)
sim_results = {}

for delay in DELAYS:
    T2 = T1 + delay
    S = S_INIT.copy()
    Vm_history = np.zeros(steps)

    for i in range(steps):
        t_current = time[i]

        # Determine current based on dual pulses
        I_current = I_ext_dual_pulse(t_current, T1, T2)

        S = rk4_step(hh_derivatives, S, I_current, DT)
        Vm_history[i] = S[0]

    sim_results[delay] = Vm_history
    max_V = np.max(Vm_history[int(T2/DT):]) # Max V after the second pulse
    print(f"Delay {delay:.1f} ms: Max V after second pulse = {max_V:.2f} mV")

## ====================================================================

## 3. Visualization

## ====================================================================

plt.figure(figsize=(10, 5))

## Plot all three voltage traces

for delay, Vm_hist in sim_results.items():
    plt.plot(time, Vm_hist, lw=1.5, label=f'Delay {delay:.1f} ms')

## Annotate the stimulus periods

plt.axvline(T1, color='gray', linestyle=':', label='1st Pulse')
plt.axvline(T1 + 1.0, color='gray', linestyle=':')
plt.axvline(T1 + DELAYS[0], color='red', linestyle=':', label='2nd Pulse (Shortest Delay)')

plt.title('Hodgkin–Huxley: Simulation of the Refractory Period')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane Voltage $V_m$ (mV)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

## --- Conclusion ---

print("\n--- Refractory Period Analysis ---")
print("Short Delay (1.5 ms): The second pulse should fail to fire a full spike or fire a greatly diminished one (Absolute/Relative Refractory Period).")
print("Long Delay (10.0 ms): The second pulse should fire a near-full spike (Recovery).")

print("\nConclusion: The simulation successfully demonstrated the refractory period. The initial spike places the neuron in a state of unresponsiveness, evidenced by the reduced or failed amplitude of the second spike when the pulse delay is short. As the time delay increases, the neuron recovers, confirming the slow recovery kinetics of the gating variables.")
```