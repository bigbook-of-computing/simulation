# **Chapter 5: Biology I: Stochastic Systems Biology () () () (Workbook)**

The goal of this chapter is to shift from continuous stochastic models (like GBM) to **discrete stochastic models**, introducing the **Gillespie Algorithm (SSA)** as the mathematically exact method for simulating biochemical reactions dominated by low copy number noise.

| Section | Topic Summary |
| :--- | :--- |
| **5.1** | Chapter Opener: Noise is the Whole Story |
| **5.2** | The Gillespie Algorithm (SSA) |
| **5.3** | Simulation: Modeling Simple Gene Expression |
| **5.4** | Application: Observing Transcriptional Bursting |
| **5.5** | Chapter Summary & Bridge to Chapter 6 |



### 5.1 Noise is the Whole Story

> **Summary:** Gene expression is a stochastic process where discrete, random events lead to significant **cell-to-cell variability** (noise). In low copy number regimes, this noise is significant, necessitating stochastic models over traditional deterministic ODEs.

#### Section Detail

Noise is classified into **intrinsic noise** (randomness within a single cell, leading to uncorrelated fluctuations in identical genes) and **extrinsic noise** (cell-to-cell variability in global factors, leading to correlated fluctuations). Noise is quantified using the **Fano Factor ($\eta$)**, which is the ratio of variance to mean ($\eta = \mathrm{Var}(X) / \langle X\rangle$). Super-Poissonian noise ($\eta > 1$) is often the signature of **transcriptional bursting**.

#### Quiz Questions

!!! note "Quiz"
```
**1. Which dimensionless measure is used to quantify the strength of gene expression noise by comparing the variance to the mean?**

* **A.** The Poisson Ratio.
* **B.** The Fano Factor ($\eta = \mathrm{Var}(X)/\langle X\rangle$). (**Correct**)
* **C.** The Autocorrelation Function.
* **D.** The $\mathcal{O}(1)$ complexity factor.

```
!!! note "Quiz"
```
**2. **Intrinsic Noise** in gene expression arises primarily from:**

* **A.** Cell-to-cell differences in cell size or cell cycle stage (extrinsic factors).
* **B.** **The random timing and nature of biochemical reactions** within a single cell. (**Correct**)
* **C.** Large copy numbers of mRNA molecules.
* **D.** Transcription and translation occurring at a perfectly steady rate.


```
!!! question "Interview Practice"
```
**Question:** An experiment measures the concentration of a protein and finds its Fano Factor is $\eta = 5.0$. Explain what this result suggests about the underlying molecular production process compared to a simple, continuous-rate birth-and-death process.

**Answer Strategy:** A simple, continuous birth-and-death process (like a Poisson process) should yield a Fano Factor of $\eta=1$. Finding $\eta = 5.0$ (which is $\eta > 1$, or **super-Poissonian noise**) strongly suggests that the production is **bursty**. This means that instead of producing molecules at a steady, continuous rate, the gene produces them in large, episodic bursts separated by long periods of inactivity, leading to large fluctuations in copy number.


```
### 5.2 The Gillespie Algorithm (SSA)

> **Summary:** The **Gillespie Algorithm (SSA)** provides an exact procedure for simulating the discrete trajectories consistent with the **Chemical Master Equation (CME)**. It uses two random numbers to determine the **time $\tau$ to the next reaction** and **which reaction $j$ occurs**, both governed by the **propensity functions $a_j(\mathbf{x})$**.

#### Section Detail

The SSA is a continuous-time Monte Carlo method. Its exactness relies on the Poisson process assumption for reaction events.
1.  **Waiting Time ($\tau$):** The time until the next reaction is exponentially distributed with parameter $a_0(\mathbf{x}) = \sum_j a_j(\mathbf{x})$ (the total propensity): $$\tau = \frac{1}{a_0} \ln\left(\frac{1}{r_1}\right)$$
2.  **Reaction Choice ($j$):** The probability of reaction $j$ occurring is proportional to its propensity: $\mathbb{P}(j) = a_j(\mathbf{x}) / a_0(\mathbf{x})$.

This procedure generates a statistically exact trajectory of molecule counts over time.

#### Quiz Questions

!!! note "Quiz"
```
**1. In the Gillespie Algorithm, the waiting time ($\tau$) until the next reaction is drawn from which probability distribution?**

* **A.** A standard Normal distribution.
* **B.** A discrete binomial distribution.
* **C.** An **Exponential distribution**. (**Correct**)
* **D.** A uniform distribution.

```
!!! note "Quiz"
```
**2. Which mathematical equation governs the time evolution of the probability distribution over the vector of molecule counts in a well-mixed stochastic system?**

* **A.** The Black-Scholes-Merton Equation.
* **B.** The Schrödinger Equation.
* **C.** The **Chemical Master Equation (CME)**. (**Correct**)
* **D.** The Newton-Raphson formula.


```
!!! question "Interview Practice"
```
**Question:** The computational cost of the basic SSA scales linearly with the number of reaction channels, $\mathcal{O}(M)$. Why does the algorithm have to recompute and re-sum all $M$ reaction propensities at every single time step?

**Answer Strategy:** The SSA must recompute all propensities because the fundamental input for the next step—the **total propensity $a_0(\mathbf{x})$**—changes every time a reaction occurs. Since $a_0(\mathbf{x})$ defines the rate of the Poisson process, it changes the mean waiting time ($\tau = 1/a_0$). If $a_0$ were held constant, the simulation would violate the memoryless property of the Markov chain. More efficient variants exist (e.g., Next Reaction Method) that use priority queues to reduce this overhead to $\mathcal{O}(\log M)$.


```
### 5.3 Simulation: Modeling Simple Gene Expression

> **Summary:** The minimal gene expression model (the **telegraph model**) comprises gene switching (ON/OFF), transcription ($m$ production), and molecule degradation ($\gamma_m m$). Propensity functions are written to reflect current state, such as $a_{\text{transcription}} = k_m g$, where $g \in \{0, 1\}$ is the gene state.

#### Section Detail

The telegraph model is simplified to capture the core of bursting.
* Gene activation and inactivation rates ($k_{\text{on}}, k_{\text{off}}$) determine the burst frequency.
* Transcription ($k_m$) and mRNA degradation ($\gamma_m$) rates determine the burst size, with mean burst size being $k_m / \gamma_m$.
The simulation generates a time series of molecule counts, $\mathbf{x}(t)$, which, when run many times, yields the steady-state distribution.

#### Quiz Questions

!!! note "Quiz"
```
**1. In the simple gene expression telegraph model, the propensity function for mRNA decay ($m \xrightarrow{\gamma_m} \emptyset$) is $a_4 = \gamma_m m$. This form signifies that:**

* **A.** Decay occurs only when the gene is ON.
* **B.** The likelihood of decay is proportional to the number of existing mRNA molecules ($m$). (**Correct**)
* **C.** Decay is a second-order (bimolecular) reaction.
* **D.** The rate of decay is constant and independent of the state.

```
!!! note "Quiz"
```
**2. The expected **mean burst size** (average number of mRNAs produced in one burst) in the telegraph model is determined by the ratio of which two rates?**

* **A.** $k_{\text{on}} / k_{\text{off}}$.
* **B.** $k_{\text{off}} / k_m$.
* **C.** **Transcription rate ($k_m$) / mRNA degradation rate ($\gamma_m$)**. (**Correct**)
* **D.** $k_m / k_{\text{off}}$.


```
!!! question "Interview Practice"
```
**Question:** An engineer wants to use the telegraph model to minimize protein noise. They decide to reduce the transcription rate $k_m$ by a factor of 10 and increase the translation rate $k_p$ by a factor of 10. Analyze how these changes would affect the noise characteristics ($\eta$) and the mean protein level.

**Answer Strategy:**
1.  **Mean Protein Level ($\langle p \rangle$):** The steady-state mean is proportional to the product of production rates ($k_m \cdot k_p$) and inversely proportional to degradation rates. Since $k_m$ decreases by 10 and $k_p$ increases by 10, the **mean protein level remains roughly unchanged** (assuming other parameters are constant).
2.  **Noise ($\eta$):** Noise is largely driven by burst size $k_m / \gamma_m$. Reducing $k_m$ by a factor of 10 means the mean **burst size is reduced by a factor of 10**. Smaller bursts smooth out fluctuations, meaning the system transitions to a less-bursty, less-noisy regime. This change should **reduce the overall Fano Factor** ($\eta$), making the expression less super-Poissonian.


```
### 5.4 Application: Observing Transcriptional Bursting

> **Summary:** SSA simulations generate trajectories that exhibit **transcriptional bursting**—episodic mRNA production—which explains the super-Poissonian noise ($\eta > 1$) observed experimentally. Simulations provide the full **distribution** of molecule counts, contrasting with deterministic ODEs that only yield the mean.

#### Section Detail

Bursting occurs because the gene stochastically switches between the ON and OFF promoter states. Analyzing the SSA trajectories allows us to estimate the burst frequency and size directly. The importance of the SSA lies in its ability to capture **phenotypic heterogeneity**—the cell-to-cell variability in molecule counts—which is crucial for understanding biological decisions but invisible to mean-field ODE models.

#### Quiz Questions

!!! note "Quiz"
```
**1. When simulating the mRNA copy number over time using the Gillespie algorithm for the telegraph model, the typical trajectory visually resembles a:**

* **A.** Smooth, exponentially decaying curve.
* **B.** A deterministic, fixed-point equilibrium line.
* **C.** A **"spike train" or episodic bursts** of production followed by exponential decay. (**Correct**)
* **D.** A continuous log-normal random walk.

```
!!! note "Quiz"
```
**2. A key failure of deterministic ODE models in the context of gene expression is that they cannot capture:**

* **A.** The average expression level.
* **B.** The fact that expression levels can be positive.
* **C.** The **probability distribution of expression levels (variance)** across a population of cells. (**Correct**)
* **D.** The steady-state mean concentration.


```
!!! question "Interview Practice"
```
**Question:** If you were simulating a batch of 100 identical cells using the SSA, and you notice that after 10,000 seconds, the fluctuations in all 100 cell trajectories look very similar (correlated), what source of noise would you investigate first?

**Answer Strategy:** Correlated fluctuations across a population of genetically identical cells suggest a high contribution of **Extrinsic Noise**. Extrinsic noise is due to cell-to-cell variability in global factors that affect *all* genes similarly, such as ribosome or polymerase copy numbers. The simulation would need to be modified by sampling these global parameters from a distribution *between* the 100 cell runs, rather than assuming they are identical.



## 💡 Hands-On Simulation Projects (Chapter Conclusion) 🧪

These projects are designed to implement the core Gillespie Algorithm and demonstrate its ability to capture molecular noise and bursting.


```
### Project 1: Implementing the Gillespie Core (The Engine)

* **Goal:** Implement the fundamental SSA step to generate the waiting time and select the reaction.
* **Setup:** Define a minimal system with two reactions: **A $\xrightarrow{k_1}$ B** and **B $\xrightarrow{k_2}$ $\emptyset$**, with initial counts $N_A=10, N_B=0$ and rates $k_1=1.0, k_2=0.1$.
* **Steps:**
    1.  Define the propensities $a_1 = k_1 N_A$ and $a_2 = k_2 N_B$.
    2.  Write a function `gillespie_step(NA, NB)` that:
        * Calculates $a_0 = a_1 + a_2$.
        * Draws $r_1$ and $r_2$.
        * Calculates $\tau$ and selects the reaction $j$ using the cumulative sum rule.
        * Returns $(\tau, j)$.
    3.  Run a loop for a few hundred steps, printing the time and $N_A, N_B$ after each update.
* ***Goal***: Verify that the simulation time advances stochastically and that reaction $j=1$ is 10 times more likely to occur than $j=2$ initially.

#### Python Implementation

```python
import numpy as np
import random
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Parameters and Initial State
# ====================================================================

# Define Reaction Rate Constants (k_1, k_2)
K1 = 1.0  # Rate for A -> B (Production)
K2 = 0.1  # Rate for B -> 0 (Decay)

# Initial Molecule Counts (State Vector x = [NA, NB])
NA_INIT = 10
NB_INIT = 0

# Define Stoichiometry Vectors (Delta_nu_j)
# Reaction 1 (A -> B): Delta_nu_1 = [-1, +1]
# Reaction 2 (B -> 0): Delta_nu_2 = [ 0, -1]
STOICHIOMETRY = np.array([
    [-1, +1],
    [ 0, -1]
])

# ====================================================================
# 2. The Gillespie SSA Core Step (The Engine)
# ====================================================================

def gillespie_step(NA, NB, K1, K2):
    """
    Performs one step of the Direct Gillespie Stochastic Simulation Algorithm.
    
    Returns: (tau, j, next_NA, next_NB)
    """
    
    # --- 1. Compute Propensities ---
    a1 = K1 * NA  # Propensity for Reaction 1 (A -> B)
    a2 = K2 * NB  # Propensity for Reaction 2 (B -> 0)
    
    # Propensity array and total propensity a_0
    propensities = np.array([a1, a2])
    a0 = np.sum(propensities)
    
    # Check for steady state (no more reactions possible)
    if a0 == 0:
        return np.inf, 0, NA, NB

    # --- 2. Draw Waiting Time (tau) ---
    r1 = random.uniform(0, 1)
    # tau = (1 / a0) * ln(1 / r1)
    tau = (1.0 / a0) * np.log(1.0 / r1)
    
    # --- 3. Select Reaction Channel (j) ---
    r2 = random.uniform(0, 1)
    
    # Cumulative sum rule: find smallest j such that sum(a_k) >= r2 * a0
    # The selected channel index (0 or 1)
    j = 0
    if r2 * a0 >= a1:
        j = 1 # Reaction 2 fires
        
    # --- 4. Update State ---
    # Apply the stoichiometry vector for the chosen reaction j
    delta_nu = STOICHIOMETRY[j, :]
    next_NA = NA + delta_nu[0]
    next_NB = NB + delta_nu[1]
    
    # Reaction index starts from 1 for output clarity
    return tau, j + 1, next_NA, next_NB

# ====================================================================
# 3. Trajectory Run and Verification
# ====================================================================

# Simulation Parameters
MAX_STEPS = 50 

# Trajectory Storage
trajectory = []
current_time = 0.0
NA = NA_INIT
NB = NB_INIT

for step in range(MAX_STEPS):
    # Perform one Gillespie step
    tau, reaction_j, next_NA, next_NB = gillespie_step(NA, NB, K1, K2)
    
    if tau == np.inf:
        break
        
    # Update time and state
    current_time += tau
    NA = next_NA
    NB = next_NB
    
    # Record the new state and event
    trajectory.append({
        'Step': step + 1,
        'Time': current_time,
        'Reaction': reaction_j,
        'NA': NA,
        'NB': NB,
        'a0': K1 * (NA + (STOICHIOMETRY[0, 0] if reaction_j==1 else 0)) + K2 * (NB + (STOICHIOMETRY[1, 1] if reaction_j==2 else 0)),
        'Prob_j1': (K1 * NA) / (K1 * NA + K2 * NB) if (K1 * NA + K2 * NB) > 0 else 0
    })

# Convert to DataFrame for clean display and print
import pandas as pd
df = pd.DataFrame(trajectory)
df_display = df[['Step', 'Time', 'Reaction', 'NA', 'NB']]

# --- Verification ---
print("--- Gillespie SSA Trajectory Verification (First 15 Steps) ---")
print(df_display.head(15).to_markdown(index=False))

print("\nVerification of Initial Propensity Weighting:")
# Initial State: NA=10, NB=0. Propensities: a1 = 10, a2 = 0. a0 = 10.
# P(j=1) = a1/a0 = 10/10 = 1.0. 
print(f"Initial Rates: K1={K1}, K2={K2}")
print(f"Initial State: NA={NA_INIT}, NB={NB_INIT}")
print(f"Initial Propensities: a1={K1*NA_INIT}, a2={K2*NB_INIT}. Total a0={K1*NA_INIT + K2*NB_INIT}")
print("Expected initial reaction: Reaction 1 (A -> B) with P=1.0. Time advance should be rapid (mean tau=1/10=0.1).")

# --- Visualization (Time Series of Molecule Counts) ---
plt.figure(figsize=(10, 4))
plt.step(df['Time'], df['NA'], where='post', label='Molecule A ($N_A$)', color='blue')
plt.step(df['Time'], df['NB'], where='post', label='Molecule B ($N_B$)', color='red')
plt.title('Gillespie Trajectory: $A \\to B$ and $B \\to \\emptyset$')
plt.xlabel('Time (t)')
plt.ylabel('Molecule Count')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()

print("\nConclusion: The core SSA step successfully simulates the discrete molecular events. Initially, only Reaction 1 (A -> B) occurs, causing $N_A$ to decrease and $N_B$ to increase. As $N_B$ grows, the propensity for Reaction 2 (B -> 0) increases, and the simulation time advances stochastically based on the total propensity.")
```
**Sample Output:**
```
--- Gillespie SSA Trajectory Verification (First 15 Steps) ---
|   Step |      Time |   Reaction |   NA |   NB |
|-------:|----------:|-----------:|-----:|-----:|
|      1 | 0.0972774 |          1 |    9 |    1 |
|      2 | 0.709687  |          1 |    8 |    2 |
|      3 | 0.832093  |          1 |    7 |    3 |
|      4 | 0.999353  |          1 |    6 |    4 |
|      5 | 1.18463   |          1 |    5 |    5 |
|      6 | 1.53601   |          1 |    4 |    6 |
|      7 | 1.71697   |          2 |    4 |    5 |
|      8 | 2.58877   |          2 |    4 |    4 |
|      9 | 2.68711   |          1 |    3 |    5 |
|     10 | 3.37939   |          1 |    2 |    6 |
|     11 | 3.70975   |          1 |    1 |    7 |
|     12 | 3.71389   |          1 |    0 |    8 |
|     13 | 3.9729    |          2 |    0 |    7 |
|     14 | 6.63298   |          2 |    0 |    6 |
|     15 | 8.09824   |          2 |    0 |    5 |

Verification of Initial Propensity Weighting:
Initial Rates: K1=1.0, K2=0.1
Initial State: NA=10, NB=0
Initial Propensities: a1=10.0, a2=0.0. Total a0=10.0
Expected initial reaction: Reaction 1 (A -> B) with P=1.0. Time advance should be rapid (mean tau=1/10=0.1).

Conclusion: The core SSA step successfully simulates the discrete molecular events. Initially, only Reaction 1 (A -> B) occurs, causing $N_A$ to decrease and $N_B$ to increase. As $N_B$ grows, the propensity for Reaction 2 (B -> 0) increases, and the simulation time advances stochastically based on the total propensity.
```


### Project 2: Simulating and Visualizing Transcriptional Noise

* **Goal:** Implement the full telegraph model (mRNA only) and compare the stochastic trajectory to the deterministic mean.
* **Setup:** Use the parameters: $k_{\text{on}}=0.01, k_{\text{off}}=0.1, k_m=1.0, \gamma_m=0.05$. Initial state $g=0, m=0$. Final time $T_{\text{final}} = 1000$ seconds.
* **Steps:**
    1.  Implement the full SSA loop for the gene switching, transcription, and mRNA decay reactions (4 channels).
    2.  Run the SSA once and plot the time series of the mRNA count $m(t)$.
    3.  Calculate the deterministic steady-state mean mRNA count: $\langle m \rangle_{\text{det}} = \frac{k_{\text{on}}}{k_{\text{on}} + k_{\text{off}}} \cdot \frac{k_m}{\gamma_m}$.
    4.  Plot the deterministic mean as a horizontal line over the stochastic trajectory.
* ***Goal***: Show that the stochastic trajectory exhibits large, irregular bursts around the smoother deterministic mean, visually demonstrating the noise.

#### Python Implementation

```python
import numpy as np
import random
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Parameters and Initial State
# ====================================================================

# Define Reaction Rate Constants (Bursty Regime)
K_ON = 0.01   # Gene activation rate (s^-1)
K_OFF = 0.1   # Gene inactivation rate (s^-1)
KM = 1.0      # Transcription rate (mRNA production rate when ON)
GAMMA_M = 0.05 # mRNA degradation rate (s^-1)

# Initial State
G_INIT = 0  # Gene state: 0=OFF, 1=ON
M_INIT = 0  # mRNA count

# Final Simulation Time
T_FINAL = 1000.0 # seconds

# Stoichiometry (State change vectors: [Delta_g, Delta_m])
STOICHIOMETRY = np.array([
    [+1, 0], # 1: Activation
    [-1, 0], # 2: Inactivation
    [ 0, +1],# 3: Transcription
    [ 0, -1] # 4: mRNA Decay
])

# Deterministic Steady-State Mean mRNA (for comparison)
# <m>_det = (k_on / (k_on + k_off)) * (k_m / gamma_m)
P_ON_SS = K_ON / (K_ON + K_OFF)
M_MEAN_DET = P_ON_SS * (KM / GAMMA_M)

# ====================================================================
# 2. The Gillespie SSA Simulation Loop
# ====================================================================

def run_ssa_gene_expression(T_final, g_init, m_init):
    """
    Runs a single SSA trajectory for the telegraph model (mRNA only).
    """
    time_points = [0.0]
    g_states = [g_init]
    m_counts = [m_init]
    
    t = 0.0
    g = g_init
    m = m_init
    
    while t < T_final:
        # --- Compute Propensities ---
        a1 = K_ON * (1 - g)  # OFF -> ON
        a2 = K_OFF * g       # ON -> OFF
        a3 = KM * g          # ON -> ON + m
        a4 = GAMMA_M * m     # m -> 0
        
        propensities = np.array([a1, a2, a3, a4])
        a0 = np.sum(propensities)
        
        if a0 == 0:
            t = T_final # Stop if no reactions are possible
            break
            
        # --- 1. Draw Waiting Time (tau) ---
        r1 = random.uniform(0, 1)
        tau = (1.0 / a0) * np.log(1.0 / r1)
        
        # --- 2. Select Reaction Channel (j) ---
        r2 = random.uniform(0, 1)
        cumulative_propensity = np.cumsum(propensities)
        
        # Find the smallest j such that cumulative_propensity[j] >= r2 * a0
        j = np.searchsorted(cumulative_propensity, r2 * a0)
        
        # --- 3. Update State and Time ---
        t += tau
        
        delta_nu = STOICHIOMETRY[j, :]
        g += delta_nu[0]
        m += delta_nu[1]
        
        # --- Record State ---
        time_points.append(t)
        g_states.append(g)
        m_counts.append(m)
        
    return np.array(time_points), np.array(m_counts)

# Run a single stochastic trajectory
time_ssa, m_ssa = run_ssa_gene_expression(T_FINAL, G_INIT, M_INIT)

# ====================================================================
# 3. Visualization
# ====================================================================

plt.figure(figsize=(10, 5))

# Plot the stochastic trajectory (discrete steps)
plt.step(time_ssa, m_ssa, where='post', label='Stochastic Trajectory $m(t)$', color='darkblue', linewidth=1.5, alpha=0.8)

# Plot the deterministic mean as a horizontal line
plt.axhline(M_MEAN_DET, color='red', linestyle='--', label=f'Deterministic Mean $\\langle m \\rangle_{{\\text{{det}}}}={M_MEAN_DET:.1f}$')

# Labeling and Formatting
plt.title('Gillespie Simulation of Transcriptional Bursting (mRNA only)')
plt.xlabel('Time (seconds)')
plt.ylabel('mRNA Copy Number ($m$)')
plt.ylim(bottom=0)
plt.legend()
plt.grid(True, which='both', linestyle=':', alpha=0.6)
plt.show()

# Display the image tag
print("")

# --- Summary ---
print("\n--- Simulation Summary ---")
print(f"Deterministic Mean <m>_det: {M_MEAN_DET:.2f}")
print(f"Burst Size Factor (k_m / gamma_m): {KM / GAMMA_M:.0f} mRNAs/burst")
print("\nObservation: The stochastic trajectory exhibits **transcriptional bursts**, where mRNA copy numbers spike rapidly during brief ON periods and then decay slowly during OFF periods. The mean of these fluctuations converges toward the smoother deterministic mean.")
```
**Sample Output:**
```
--- Simulation Summary ---
Deterministic Mean <m>_det: 1.82
Burst Size Factor (k_m / gamma_m): 20 mRNAs/burst

Observation: The stochastic trajectory exhibits **transcriptional bursts**, where mRNA copy numbers spike rapidly during brief ON periods and then decay slowly during OFF periods. The mean of these fluctuations converges toward the smoother deterministic mean.
```


### Project 3: Quantifying Super-Poissonian Noise ($\eta$)

* **Goal:** Quantitatively demonstrate that the telegraph model produces super-Poissonian noise (Fano Factor $\eta > 1$).
* **Setup:** Use the bursty parameters from Project 2.
* **Steps:**
    1.  Run $M=500$ independent SSA trajectories until they all reach the steady state ($T=10,000$ s).
    2.  Record the final mRNA count $m_i$ for each of the $M$ trajectories.
    3.  Calculate the ensemble mean $\langle m \rangle = \frac{1}{M} \sum m_i$ and the ensemble variance $\mathrm{Var}(m) = \frac{1}{M-1} \sum (m_i - \langle m \rangle)^2$.
    4.  Compute the Fano Factor $\eta = \mathrm{Var}(m) / \langle m \rangle$.
* ***Goal***: Show that the calculated $\eta$ is significantly greater than $1.0$ (e.g., $\eta \approx 10-20$), confirming the noise is dominated by large-size transcriptional bursts.

#### Python Implementation

```python
import numpy as np
import random
import matplotlib.pyplot as plt

# ====================================================================
# 1. Setup Functions and Parameters (from Project 2)
# ====================================================================

# --- Parameters (Bursty Regime) ---
K_ON = 0.01   # Gene activation rate (s^-1)
K_OFF = 0.1   # Gene inactivation rate (s^-1)
KM = 1.0      # Transcription rate
GAMMA_M = 0.05 # mRNA degradation rate
T_FINAL = 10000.0 # Time to reach steady state
M_TRAJECTORIES = 500 # Number of independent trajectories

# Stoichiometry (State change vectors: [Delta_g, Delta_m])
STOICHIOMETRY = np.array([
    [+1, 0], # 1: Activation
    [-1, 0], # 2: Inactivation
    [ 0, +1],# 3: Transcription
    [ 0, -1] # 4: mRNA Decay
])

# Deterministic Steady-State Mean (for reference)
P_ON_SS = K_ON / (K_ON + K_OFF)
M_MEAN_DET = P_ON_SS * (KM / GAMMA_M)

def run_ssa_gene_expression(T_final, g_init, m_init):
    """
    Runs a single SSA trajectory for the telegraph model (mRNA only) up to T_final.
    Returns the final mRNA count m_T.
    """
    t = 0.0
    g = g_init
    m = m_init
    
    while t < T_final:
        # --- Compute Propensities ---
        a1 = K_ON * (1 - g)
        a2 = K_OFF * g
        a3 = KM * g
        a4 = GAMMA_M * m
        propensities = np.array([a1, a2, a3, a4])
        a0 = np.sum(propensities)
        
        if a0 == 0:
            break
            
        # --- 1. Draw Waiting Time (tau) ---
        r1 = random.uniform(0, 1)
        tau = (1.0 / a0) * np.log(1.0 / r1)
        
        # --- 2. Select Reaction Channel (j) ---
        r2 = random.uniform(0, 1)
        cumulative_propensity = np.cumsum(propensities)
        j = np.searchsorted(cumulative_propensity, r2 * a0)
        
        # --- 3. Update State and Time ---
        t += tau
        
        delta_nu = STOICHIOMETRY[j, :]
        g += delta_nu[0]
        m += delta_nu[1]
        
    return m # Return the final mRNA count

# ====================================================================
# 2. Ensemble Simulation and Noise Quantification
# ====================================================================

final_m_ensemble = np.zeros(M_TRAJECTORIES)

for i in range(M_TRAJECTORIES):
    # Run each trajectory independently from the initial state
    final_m_ensemble[i] = run_ssa_gene_expression(T_FINAL, G_INIT, M_INIT)

# --- Calculate Ensemble Statistics ---
M_MEAN_EMPIRICAL = np.mean(final_m_ensemble)
M_VARIANCE_EMPIRICAL = np.var(final_m_ensemble, ddof=1) # Use ddof=1 for sample variance

# Calculate the Fano Factor (Noise Strength)
FANO_FACTOR = M_VARIANCE_EMPIRICAL / M_MEAN_EMPIRICAL

# ====================================================================
# 3. Visualization and Analysis
# ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Steady-State Distribution (Histogram of Final Counts)
ax[0].hist(final_m_ensemble, bins=np.arange(0, np.max(final_m_ensemble) + 1, 1), 
           density=True, color='purple', alpha=0.7, align='left')
ax[0].axvline(M_MEAN_EMPIRICAL, color='red', linestyle='--', label=f'Mean $\\langle m \\rangle$: {M_MEAN_EMPIRICAL:.1f}')
ax[0].set_title('Steady-State mRNA Distribution (Ensemble)')
ax[0].set_xlabel('Final mRNA Count ($m$)')
ax[0].set_ylabel('Probability Density')
ax[0].legend()
ax[0].grid(True, which='major', axis='y', linestyle=':')

# Plot 2: Fano Factor Visualization
bars = ax[1].bar(['Poisson ($\eta=1$)', f'Simulated ($\eta$)'], [1.0, FANO_FACTOR], color=['gray', 'darkred'])
bars[0].set_alpha(0.5)
ax[1].axhline(1.0, color='black', linestyle='--', label='Poisson Threshold')
ax[1].text(1, FANO_FACTOR + 0.5, f'{FANO_FACTOR:.2f}', ha='center', fontweight='bold', color='darkred')
ax[1].set_title('Noise Quantification: Fano Factor ($\eta$)')
ax[1].set_ylabel('Fano Factor ($\eta$)')
ax[1].set_ylim(0, np.max([FANO_FACTOR, 5]) * 1.1)
ax[1].grid(True, which='major', axis='y', linestyle=':')

plt.tight_layout()
plt.show()

# --- Summary ---
print("\n--- Super-Poissonian Noise Quantification ---")
print(f"Ensemble Mean <m>:      {M_MEAN_EMPIRICAL:.2f}")
print(f"Ensemble Variance Var(m): {M_VARIANCE_EMPIRICAL:.2f}")
print("-----------------------------------------")
print(f"Fano Factor ( = Var/Mean): {FANO_FACTOR:.2f}")
print(f"Deterministic Mean (Benchmark): {M_MEAN_DET:.2f}")

print("\nConclusion: The calculated Fano Factor (\u03B7) is significantly greater than 1.0 (Super-Poissonian), quantitatively confirming that the telegraph model successfully captures the **transcriptional bursting** regime, where noise is high due to episodic production of large numbers of mRNA molecules.")
```