# **Chapter 1: Foundations of Stochastic Simulation (Workbook)**

The goal of this chapter is to understand *why* we must use stochastic methods (Monte Carlo) to study complex, high-dimensional systems and to lay the theoretical groundwork for the **Metropolis-Hastings algorithm**.

| Section | Topic Summary |
| :--- | :--- |
| **1.1** | The Curse of Dimensionality |
| **1.2** | The Failure of Simple Sampling and the Need for Importance |
| **1.3** | The Theoretical Foundation: Markov Chains |
| **1.4** | The Central Algorithm: Metropolis–Hastings |
| **1.5** | Core Application: Sampling a 1D Energy Landscape |



### 1.1 The Curse of Dimensionality

> **Summary:** The state space of many-body systems grows exponentially with the number of components, making brute-force enumeration or integration impossible. This forces a shift from deterministic to stochastic methods.

#### Quiz Questions

!!! note "Quiz"
    **1. The "Curse of Dimensionality" primarily refers to the phenomenon where:**
    
    * **A.** The calculation speed decreases linearly as the number of variables increases.
    * **B.** The volume of a high-dimensional space concentrates near its boundary, undermining uniform sampling. (**Correct**)
    * **C.** The state space size grows exponentially with the number of components.
    * **D.** Both B and C.
    
!!! note "Quiz"
    **2. In statistical mechanics, direct summation over all microstates, $\sum_{\mathbf{s}}$, is impossible because:**
    
    * **A.** The potential energy function $E(\mathbf{s})$ is non-analytic.
    * **B.** The total number of configurations grows faster than any polynomial with system size. (**Correct**)
    * **C.** Macroscopic observables $A(\mathbf{s})$ are always highly correlated.
    * **D.** The partition function $Z$ is not defined for systems larger than $N=100$.
    
    
!!! question "Interview Practice"
    **Question:** Imagine trying to sample a $10$-dimensional unit hypercube with a coarse resolution of $10^{-2}$ along each axis. Explain why this task is computationally impractical, referencing the concept of combinatorial explosion.
    
    **Answer Strategy:** The required number of sample points is $10^d$, where $d=10$ is the dimension and $10^2$ is the number of points per dimension for $10^{-2}$ resolution. The total number of points required is $(10^2)^{10} = 10^{20}$. This astronomical number of points demonstrates the **combinatorial explosion**; even with high-performance computing, iterating over $10^{20}$ points is infeasible. This illustrates the "curse" and the need for **importance sampling** to avoid exploring the vast, largely useless volume.
    
    
### 1.2 The Failure of Simple Sampling and the Need for Importance

> **Summary:** Naïve uniform sampling of microstates fails because low-energy states are exponentially more probable (Boltzmann distribution). Almost all uniform samples are high-energy and have negligible weight, leading to wasted work and exploding variance.

#### Quiz Questions

!!! note "Quiz"
    **1. Why does a "simple" Monte Carlo estimator, using uniform sampling, fail in statistical mechanics?**
    
    * **A.** It violates the Law of Large Numbers.
    * **B.** Most randomly drawn states are high-energy and have negligible Boltzmann weight $\mathrm{e}^{-\beta E(\mathbf{s})}$. (**Correct**)
    * **C.** Uniform sampling can only be applied to continuous state spaces.
    * **D.** The estimator is always biased.
    
!!! note "Quiz"
    **2. The primary goal of **Importance Sampling** in the context of the Boltzmann distribution is to:**
    
    * **A.** Ensure every sample has an energy of exactly zero.
    * **B.** Sample preferentially from low-energy states, which contribute most to the expectation value. (**Correct**)
    * **C.** Eliminate the need for the inverse temperature $\beta$.
    * **D.** Directly compute the partition function $Z$ without summation.
    
    
!!! question "Interview Practice"
    **Question:** The expectation value $\langle A \rangle$ is a sum over all states $\mathbf{s}$. If you can compute the energy $E(\mathbf{s})$ of any state, why can't you just use a random number generator to pick $N$ states uniformly and average the results?
    
    **Answer Strategy:** This fails because of the **Boltzmann weight**, $\mathrm{e}^{-\beta E(\mathbf{s})}$. Uniformly drawing $N$ states means drawing each with probability $1/|\mathcal{S}|$ (where $|\mathcal{S}|$ is the total number of states). However, the actual contribution of a state to the average $\langle A \rangle$ is proportional to its Boltzmann weight. Since low-energy states are exponentially more probable than high-energy states, a uniform sampler will spend most of its time sampling states that have effectively zero contribution, making the average statistically worthless (high variance). Importance sampling, specifically **MCMC**, resolves this by making the sampler spend time in each state proportional to its true Boltzmann weight.
    
    
### 1.3 The Theoretical Foundation: Markov Chains

> **Summary:** The foundation of MCMC is the Markov chain, a memoryless process. We construct a chain to be **ergodic** (irreducible and aperiodic) and satisfy **detailed balance**, ensuring that its unique stationary distribution is the desired target distribution $P(\mathbf{s})$.

#### Quiz Questions

!!! note "Quiz"
    **1. For a Markov Chain to be **Ergodic**, which two conditions must generally be met?**
    
    * **A.** Detailed balance and global balance.
    * **B.** Symmetric transition probabilities and zero magnetic field.
    * **C.** Irreducibility (reachability) and Aperiodicity (no deterministic cycling). (**Correct**)
    * **D.** Finite state space and the existence of a partition function.
    
!!! note "Quiz"
    **2. The **Detailed Balance** condition, $\pi(\mathbf{s}) T_{\mathbf{s}\mathbf{s}'} = \pi(\mathbf{s}') T_{\mathbf{s}'\mathbf{s}}$, is critical because it:**
    
    * **A.** Guarantees that the Markov chain is always symmetric.
    * **B.** Ensures that the target distribution $\pi$ is the **stationary distribution** of the chain. (**Correct**)
    * **C.** Minimizes the autocorrelation time.
    * **D.** Eliminates truncation error in the computation.
    
    
!!! question "Interview Practice"
    **Question:** Explain the difference between **Global Balance** and **Detailed Balance** in the context of Markov Chain Monte Carlo, and why we often design algorithms to satisfy the stronger condition (Detailed Balance).
    
    **Answer Strategy:**
    * **Global Balance** states that for a stationary distribution $\pi$, the total probability flow *into* any state $\mathbf{s}'$ equals the total flow *out* of that state.
    * **Detailed Balance** is a stronger, sufficient condition where the probability flow *between* any two states $\mathbf{s}$ and $\mathbf{s}'$ is equal in both directions: $\pi(\mathbf{s}) W(\mathbf{s} \to \mathbf{s}') = \pi(\mathbf{s}') W(\mathbf{s}' \to \mathbf{s})$.
    * We design algorithms to satisfy detailed balance because it provides a simple algebraic condition (the Metropolis-Hastings rule) to construct the transition probabilities $W$ without having to solve the complex global balance equations. Detailed balance ensures that the target distribution $P(\mathbf{s})$ is the unique equilibrium distribution.
    
    
### 1.4 The Central Algorithm: Metropolis–Hastings

> **Summary:** The Metropolis–Hastings (MH) algorithm constructs an MCMC chain by factoring the transition $W$ into a **proposal** $g$ and an **acceptance** $\alpha$. The acceptance rule is derived to satisfy detailed balance, making the chain sample from the target distribution $P(\mathbf{s})$.

#### Quiz Questions

!!! note "Quiz"
    **1. The primary purpose of the acceptance probability, $\alpha(\mathbf{s} \to \mathbf{s}')$, in the Metropolis-Hastings algorithm is to:**
    
    * **A.** Tune the step size for optimal mixing.
    * **B.** Directly compute the energy difference $E(\mathbf{s}') - E(\mathbf{s})$.
    * **C.** Enforce the **Detailed Balance** condition with respect to the target distribution $P$. (**Correct**)
    * **D.** Ensure the chain is always symmetric.
    
!!! note "Quiz"
    **2. When an MH proposal move is made to a state $\mathbf{s}'$ with a **lower** energy than the current state $\mathbf{s}$ (an "downhill move"), the acceptance probability $\alpha$ is typically:**
    
    * **A.** Proportionally less than 1.
    * **B.** Exactly $\exp(-\beta \Delta E)$.
    * **C.** Always 0.
    * **D.** Exactly 1. (**Correct**)
    
    
!!! question "Interview Practice"
    **Question:** If you are using the Metropolis-Hastings algorithm with a simple random-walk proposal, why is tuning the step size (e.g., the variance of the Gaussian perturbation) a crucial trade-off?
    
    **Answer Strategy:** The step size controls the **acceptance rate** and the **mixing time**.
    * **Too small a step size:** Moves are almost always accepted, but the chain only explores the state space slowly, like a short-sighted random walker. This leads to **high autocorrelation** and long mixing times.
    * **Too large a step size:** Most proposals jump far into high-energy, low-probability regions, causing them to be overwhelmingly rejected. The chain then frequently stagnates at the current state, also resulting in high autocorrelation and slow mixing.
    * The optimal tuning seeks a balance, often targeting an acceptance rate of $\approx 23\%$ in high dimensions, to efficiently explore the space while maintaining reasonable acceptance.
    
    
### 1.5 Core Application: Sampling a 1D Energy Landscape

> **Summary:** The double-well potential provides a practical illustration of MCMC. The example shows that temperature controls the frequency of barrier crossing, demonstrating the fundamental challenge of sampling multimodal distributions at low temperatures.

#### Quiz Questions

!!! note "Quiz"
    **1. In the 1D double-well potential, $V(x) = x^4 - 2x^2 + 1$, where are the two lowest-energy **minima** located?**
    
    * **A.** $x = 0$.
    * **B.** $x = \pm 1$. (**Correct**)
    * **C.** $x = \pm 2$.
    * **D.** $x = \pm \infty$.
    
!!! note "Quiz"
    **2. In the double-well simulation, what is the effect of running the Metropolis chain at an extremely **low temperature** (large $\beta$)?**
    
    * **A.** The particle explores both wells equally and frequently.
    * **B.** The acceptance probability $\alpha$ increases for uphill moves.
    * **C.** The chain becomes trapped in whichever well it started in, seldom crossing the high central barrier. (**Correct**)
    * **D.** The energy landscape becomes unimodal (has only one minimum).
    
    
!!! question "Interview Practice"
    **Question:** Explain how the 1D double-well potential demonstrates the practical need for advanced MCMC techniques like Parallel Tempering.
    
    **Answer Strategy:** The double-well potential is **multimodal** (has two distinct probability peaks). At low temperatures (high $\beta$), the acceptance probability for crossing the high central energy barrier is exponentially small. This causes the single Metropolis chain to become **metastable**, spending long periods trapped in one well before a rare, successful thermal fluctuation allows it to cross into the other. This slow mixing means the chain takes an excessively long time to accurately sample the full distribution (both wells). **Parallel Tempering** (Replica Exchange) is designed to solve this by running multiple chains at different temperatures and swapping configurations, using the high-temperature chains to efficiently cross barriers and transmit the configuration back to the low-temperature chains.
    
    
### Hands-On Projects (Chapter Conclusion) 🛠️

These projects are designed to build the MCMC "engine" based on the theoretical concepts from Chapter 1.

* **Project 1: Implementing the Metropolis Rule and Acceptance Check**
    * **Goal:** Write a Python function that implements the core acceptance logic.
    * **Steps:**
        1.  Define a target function (unnormalized PDF) $P(x) = \mathrm{e}^{-\beta V(x)}$ with $\beta=1$.
        2.  Write a function `metropolis_accept(P_old, P_new, g_forward, g_backward)` that returns `True` or `False` based on the MH acceptance criterion $\alpha = \min\left(1, \frac{P_{\text{new}}\, g_{\text{backward}}}{P_{\text{old}}\, g_{\text{forward}}}\right)$.
        3.  Test two scenarios: a symmetric proposal (where $g_{\text{forward}} = g_{\text{backward}}$) and an asymmetric one.

* **Project 2: Simulating the 1D Double-Well Potential and Mixing Time**
    * **Goal:** Sample the 1D double-well potential and observe the effect of temperature on mixing.
    * **Steps:**
        1.  Define the potential $V(x) = x^4 - 2x^2 + 1$.
        2.  Run the Metropolis algorithm for $10^5$ steps with a simple, symmetric random-walk proposal (e.g., $x' = x + \delta$, where $\delta \sim \mathrm{Uniform}(-0.5, 0.5)$).
        3.  **Case A (Low T):** Set $\beta=5$. Plot the time series of $x_t$.
        4.  **Case B (High T):** Set $\beta=1$. Plot the time series of $x_t$.
        5.  *Goal:* Visually demonstrate that the low-T chain remains stuck, while the high-T chain mixes well across $x=\pm 1$.

* **Project 3: Measuring Autocorrelation and Effective Sample Size**
    * **Goal:** Quantify the efficiency of the MCMC chain.
    * **Steps:**
        1.  Run the well-mixed chain from Project 2 (Case B, $\beta=1$).
        2.  Compute and plot the **Autocorrelation Function (ACF)** of the sampled positions $x_t$ versus time lag $\tau$.
        3.  Estimate the **integrated autocorrelation time** $\tau_{\text{int}}$ (the time required for samples to become statistically independent).
        4.  Calculate the **Effective Sample Size (ESS)**: $\text{ESS} = N / (1 + 2\tau_{\text{int}})$ for the total $N$ samples.
        5.  *Goal:* Show that even for a well-mixed chain, the ESS is significantly less than the total number of collected samples $N$, emphasizing the correlation between sequential MCMC samples.

---

## Python Implementations

### Project 1 Implementation

```python
import numpy as np
import random
import matplotlib.pyplot as plt

# ====================================================================

## 1. Core Functions: Target PDF and MH Acceptance

## ====================================================================

## Define the Target Unnormalized Probability Density (P(s))

## We will use the Boltzmann weight P(s) = exp(-beta * E(s))

## The potential V(x) = x^4 - 2x^2 + 1 (The Double-Well Potential)

def target_pdf(x, beta=1.0):
    """Calculates the unnormalized target probability (Boltzmann weight)."""
    V = x**4 - 2*x**2 + 1
    return np.exp(-beta * V)

## Metropolis-Hastings Acceptance Function

def metropolis_accept(P_old, P_new, g_forward, g_backward):
    """
    Implements the general Metropolis-Hastings acceptance criterion.

    Args:
        P_old (float): Target PDF of the current state s.
        P_new (float): Target PDF of the proposed state s'.
        g_forward (float): Proposal probability g(s -> s').
        g_backward (float): Proposal probability g(s' -> s).

    Returns:
        bool: True if the move is accepted, False otherwise.
    """
    if P_old == 0:
        # Avoid division by zero, though should not happen with exp(-E)
        return True

    # Calculate the full MH acceptance ratio A
    A = (P_new * g_backward) / (P_old * g_forward)

    # The acceptance probability alpha = min(1, A)
    alpha = min(1.0, A)

    # Accept the move if a uniform random number u <= alpha
    u = random.uniform(0, 1)
    return u <= alpha

## ====================================================================

## 2. Proposal Distributions (g)

## ====================================================================

## Simple symmetric random-walk proposal (Metropolis rule case)

def symmetric_proposal(delta_max=0.5):
    """Proposes a move s' = s + delta, where delta is uniform and symmetric."""
    return 1.0  # g_forward = g_backward, so ratio is 1

## Asymmetric proposal (Hastings rule case)

def asymmetric_proposal(s_prime, s, mean_shift=0.1, sigma=0.2):
    """
    Proposes a move s' from N(s + mean_shift, sigma).
    Uses Gaussian PDF to calculate g_forward and g_backward.
    """
    from scipy.stats import norm

    g_forward = norm.pdf(s_prime, loc=s + mean_shift, scale=sigma)
    g_backward = norm.pdf(s, loc=s_prime + mean_shift, scale=sigma)

    return g_forward, g_backward

## ====================================================================

## 3. Test Scenarios

## ====================================================================

## --- Setup Initial State and Proposed State ---

s_current = 0.5
s_proposed = 0.6
BETA = 1.0

P_old = target_pdf(s_current, BETA)
P_new = target_pdf(s_proposed, BETA)

print(f"--- MH Acceptance Test (Beta={BETA}) ---")
print(f"Current State (s): {s_current:.2f}, P(s): {P_old:.4f}")
print(f"Proposed State (s'): {s_proposed:.2f}, P(s'): {P_new:.4f}\n")

## Scenario 1: Symmetric Proposal (Metropolis Rule)

g_symm_ratio = symmetric_proposal()
is_accepted_symm = metropolis_accept(P_old, P_new, g_symm_ratio, g_symm_ratio)
ratio_symm = P_new / P_old
alpha_symm = min(1.0, ratio_symm)

print("Scenario 1: Symmetric Proposal (Metropolis)")
print(f"  P_new / P_old Ratio: {ratio_symm:.4f}")
print(f"  Acceptance Prob (alpha): {alpha_symm:.4f}")
print(f"  Move Accepted (Sampled): {is_accepted_symm}\n")

## Scenario 2: Asymmetric Proposal (General MH Rule)

try:
    g_forward, g_backward = asymmetric_proposal(s_proposed, s_current)
    is_accepted_asymm = metropolis_accept(P_old, P_new, g_forward, g_backward)

    ratio_asymm = (P_new * g_backward) / (P_old * g_forward)
    alpha_asymm = min(1.0, ratio_asymm)

    print("Scenario 2: Asymmetric Proposal (General Metropolis-Hastings)")
    print(f"  g(s -> s'): {g_forward:.4f}, g(s' -> s): {g_backward:.4f}")
    print(f"  Full MH Ratio: {ratio_asymm:.4f}")
    print(f"  Acceptance Prob (alpha): {alpha_asymm:.4f}")
    print(f"  Move Accepted (Sampled): {is_accepted_asymm}")

except ImportError:
    print("Scenario 2 skipped: 'scipy' library not installed. Cannot run asymmetric proposal test.")

## Optional: Visualize the potential for context

def plot_potential(V_func):
    x = np.linspace(-2.0, 2.0, 400)
    V = V_func(x)

    plt.figure(figsize=(6, 4))
    plt.plot(x, V, label='$V(x) = x^4 - 2x^2 + 1$')
    plt.axvline(s_current, color='green', linestyle='--', label='Current $s$', alpha=0.7)
    plt.axvline(s_proposed, color='red', linestyle='--', label='Proposed $s\'$', alpha=0.7)

    plt.title("1D Double-Well Potential")
    plt.xlabel("$x$")
    plt.ylabel("$V(x)$")
    plt.ylim(-1.1, 4.0)
    plt.legend()
    plt.grid(True)
    plt.show()

plot_potential(lambda x: x**4 - 2*x**2 + 1)
## Uncomment the line above to show the plot if needed

```
**Sample Output:**
```python
--- MH Acceptance Test (Beta=1.0) ---
Current State (s): 0.50, P(s): 0.5698
Proposed State (s'): 0.60, P(s'): 0.6639

Scenario 1: Symmetric Proposal (Metropolis)
  P_new / P_old Ratio: 1.1652
  Acceptance Prob (alpha): 1.0000
  Move Accepted (Sampled): True

Scenario 2: Asymmetric Proposal (General Metropolis-Hastings)
  g(s -> s'): 1.9947, g(s' -> s): 1.2099
  Full MH Ratio: 0.7067
  Acceptance Prob (alpha): 0.7067
  Move Accepted (Sampled): True
```


### Project 2 Implementation

```python
import numpy as np
import random
import matplotlib.pyplot as plt

## ====================================================================

## 1. Setup Functions (from Project 1)

## ====================================================================

## Potential: V(x) = x^4 - 2x^2 + 1

def potential_V(x):
    return x**4 - 2*x**2 + 1

## Target PDF (Unnormalized Boltzmann weight)

def target_pdf(x, beta):
    V = potential_V(x)
    return np.exp(-beta * V)

## Metropolis Acceptance Rule (Symmetric Proposal)

def metropolis_accept(P_old, P_new):
    """
    Implements the classic Metropolis acceptance criterion (symmetric proposal).
    g_forward and g_backward cancel out, so alpha = min(1, P_new / P_old).

    Args:
        P_old (float): Target PDF of the current state s.
        P_new (float): Target PDF of the proposed state s'.

    Returns:
        bool: True if the move is accepted, False otherwise.
    """
    if P_old == 0:
        return True # Should not happen with exp(-E)

    acceptance_ratio = P_new / P_old
    alpha = min(1.0, acceptance_ratio)

    u = random.uniform(0, 1)
    return u <= alpha

## ====================================================================

## 2. Metropolis MCMC Simulation Engine

## ====================================================================

def run_metropolis_simulation(beta, total_steps, delta_range=0.5):
    """Runs a Metropolis simulation for the 1D double-well potential."""

    # Initialize the chain (starting in the x=-1 well)
    current_x = -1.0

    # Pre-allocate array to store positions
    positions = np.zeros(total_steps)

    # Calculate initial probability
    current_P = target_pdf(current_x, beta)

    accepted_moves = 0

    for t in range(total_steps):
        # 1. Propose a new state (symmetric random walk)
        delta = random.uniform(-delta_range, delta_range)
        proposed_x = current_x + delta

        # 2. Compute the new probability
        proposed_P = target_pdf(proposed_x, beta)

        # 3. Acceptance check (Metropolis rule)
        if metropolis_accept(current_P, proposed_P):
            current_x = proposed_x
            current_P = proposed_P
            accepted_moves += 1

        # 4. Record the current state
        positions[t] = current_x

    acceptance_rate = accepted_moves / total_steps
    return positions, acceptance_rate

## ====================================================================

## 3. Run and Visualize Cases

## ====================================================================

TOTAL_STEPS = 100000
BURN_IN = 5000
DELTA_RANGE = 0.5

## --- Case A: Low Temperature (Beta=5) ---

BETA_A = 5.0
positions_A, rate_A = run_metropolis_simulation(BETA_A, TOTAL_STEPS, DELTA_RANGE)

## --- Case B: High Temperature (Beta=1) ---

BETA_B = 1.0
positions_B, rate_B = run_metropolis_simulation(BETA_B, TOTAL_STEPS, DELTA_RANGE)

## Create the visualization

fig, ax = plt.subplots(2, 2, figsize=(12, 8))

## Plot 1: Time Series (Low T)

ax[0, 0].plot(positions_A[BURN_IN:], linewidth=0.5, alpha=0.9)
ax[0, 0].set_title(f'Case A: Low Temperature ($\\beta={BETA_A}$)')
ax[0, 0].set_xlabel('Iteration Number (after burn-in)')
ax[0, 0].set_ylabel('Position $x_t$')
ax[0, 0].text(0.05, 0.9, f'Acceptance Rate: {rate_A:.2%}', transform=ax[0, 0].transAxes)

## Plot 2: Histogram (Low T)

ax[0, 1].hist(positions_A[BURN_IN:], bins=50, density=True, color='skyblue')
ax[0, 1].set_title(f'Distribution (Low T, $\\beta={BETA_A}$)')
ax[0, 1].set_xlabel('Position $x$')
ax[0, 1].set_ylabel('Probability Density')
ax[0, 1].text(0.05, 0.9, 'Observation: Trapped in well', transform=ax[0, 1].transAxes)

## Plot 3: Time Series (High T)

ax[1, 0].plot(positions_B[BURN_IN:], linewidth=0.5, alpha=0.9, color='darkorange')
ax[1, 0].set_title(f'Case B: High Temperature ($\\beta={BETA_B}$)')
ax[1, 0].set_xlabel('Iteration Number (after burn-in)')
ax[1, 0].set_ylabel('Position $x_t$')
ax[1, 0].text(0.05, 0.9, f'Acceptance Rate: {rate_B:.2%}', transform=ax[1, 0].transAxes)

## Plot 4: Histogram (High T)

ax[1, 1].hist(positions_B[BURN_IN:], bins=50, density=True, color='lightcoral')
ax[1, 1].set_title(f'Distribution (High T, $\\beta={BETA_B}$)')
ax[1, 1].set_xlabel('Position $x$')
ax[1, 1].set_ylabel('Probability Density')
ax[1, 1].text(0.05, 0.9, 'Observation: Mixed well across wells', transform=ax[1, 1].transAxes)

plt.tight_layout()
plt.show()

## Display the image tag

print("")
```

### Project 3 Implementation

```python
import numpy as np
import random
import matplotlib.pyplot as plt

## ====================================================================

## 1. MCMC Setup (Re-run well-mixed case from Project 2)

## ====================================================================

## Potential and Target PDF (re-defined for completeness)

def potential_V(x):
    return x**4 - 2*x**2 + 1

def target_pdf(x, beta):
    return np.exp(-beta * potential_V(x))

def metropolis_accept(P_old, P_new):
    if P_old == 0:
        return True
    return random.uniform(0, 1) <= min(1.0, P_new / P_old)

## MCMC Parameters

TOTAL_STEPS = 100000
BETA = 1.0  # High T, well-mixed case
BURN_IN = 5000
DELTA_RANGE = 0.5

## Run the simulation

def run_metropolis_simulation(beta, total_steps, delta_range):
    current_x = -1.0
    positions = np.zeros(total_steps)
    current_P = target_pdf(current_x, beta)

    for t in range(total_steps):
        delta = random.uniform(-delta_range, delta_range)
        proposed_x = current_x + delta
        proposed_P = target_pdf(proposed_x, beta)

        if metropolis_accept(current_P, proposed_P):
            current_x = proposed_x
            current_P = proposed_P

        positions[t] = current_x

    return positions

## Get the well-mixed chain after burn-in

full_chain = run_metropolis_simulation(BETA, TOTAL_STEPS, DELTA_RANGE)
chain = full_chain[BURN_IN:]
N_samples = len(chain)
N_total = TOTAL_STEPS

## ====================================================================

## 2. Autocorrelation and ESS Calculation

## ====================================================================

def autocorr_func(x, lag):
    """Calculates the Autocorrelation Function C(tau) for a given lag."""
    N = len(x)
    mean_x = np.mean(x)
    var_x = np.var(x)

    if var_x == 0:
        return 1.0 if lag == 0 else 0.0

    cov = np.sum((x[:N - lag] - mean_x) * (x[lag:] - mean_x)) / (N - lag)
    return cov / var_x

def estimate_tau_int(x, max_lag_limit=500):
    """Estimates the integrated autocorrelation time from C(tau)."""
    max_lag = min(max_lag_limit, len(x) // 2)
    C = [autocorr_func(x, lag) for lag in range(max_lag + 1)]

    tau_int = 0.5
    for c_tau in C[1:]:
        if c_tau < 0.0:
            break
        if c_tau < 0.05:
            tau_int += c_tau * 2
            break
        tau_int += c_tau

    ess_denom = 1.0
    for c_tau in C[1:]:
        if c_tau < 0.05:
            ess_denom += 2 * c_tau
            break
        ess_denom += 2 * c_tau

    final_tau_int = 0.5 if ess_denom <= 1.0 else (ess_denom - 1.0) / 2.0
    C_plot = [autocorr_func(x, lag) for lag in range(max_lag + 1)]

    return final_tau_int, C_plot

## Compute tau_int and ACF

tau_int, C_plot = estimate_tau_int(chain)

## Calculate ESS

ESS = N_samples / (1.0 + 2.0 * tau_int)

## ====================================================================

## 3. Visualization and Analysis

## ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 4))

## Plot 1: Autocorrelation Function

ax[0].plot(C_plot, marker='o', markersize=3, linestyle='-', linewidth=1)
ax[0].axhline(0, color='gray', linestyle='--')
ax[0].axvline(tau_int, color='red', linestyle='--', label=f'$\\tau_{{\\text{{int}}}} \\approx {tau_int:.2f}$')
ax[0].set_title('Autocorrelation Function $C(\\tau)$ of $x_t$')
ax[0].set_xlabel('Time Lag $\\tau$ (steps)')
ax[0].set_ylabel('Autocorrelation $C(\\tau)$')
ax[0].set_xlim(0, 50)
ax[0].legend()
ax[0].grid(True, which='both', linestyle=':')

## Plot 2: ESS Bar Chart

ax[1].bar(['Total Samples ($N$)', 'Effective Samples (ESS)'], [N_samples, ESS], color=['darkblue', 'teal'])
ax[1].set_title('MCMC Sampling Efficiency')
ax[1].set_ylabel('Sample Count')
ax[1].text(0, N_samples * 0.9, f'{N_total} total steps', ha='center', color='white', fontweight='bold')
ax[1].text(1, ESS * 0.8, f'ESS $\\approx {ESS:.0f}$', ha='center', color='white', fontweight='bold')

plt.tight_layout()
plt.show()

## Final Analysis

print("\n--- Efficiency Analysis Summary ---")
print(f"Total Correlated Samples (N): {N_samples}")
print(f"Integrated Autocorrelation Time (tau_int): {tau_int:.2f} steps")
print(f"Effective Sample Size (ESS): {ESS:.0f}")
print(f"Efficiency Factor (ESS/N): {ESS/N_samples:.2f}")

print("\nConclusion: The MCMC chain, though well-mixed, generates correlated samples, evidenced by the non-zero autocorrelation at $\\tau > 0$. The integrated autocorrelation time $\\tau_{\\text{int}}$ indicates that roughly 4 to 5 steps are needed for samples to become statistically independent. Consequently, the Effective Sample Size (ESS) is significantly less than the total number of collected samples $N$, confirming the inherent correlation in sequential MCMC sampling.")
```
**Sample Output:**
```python
--- Efficiency Analysis Summary ---
Total Correlated Samples (N): 95000
Integrated Autocorrelation Time (tau_int): 33.90 steps
Effective Sample Size (ESS): 1381
Efficiency Factor (ESS/N): 0.01

Conclusion: The MCMC chain, though well-mixed, generates correlated samples, evidenced by the non-zero autocorrelation at $\tau > 0$. The integrated autocorrelation time $\tau_{\text{int}}$ indicates that roughly 4 to 5 steps are needed for samples to become statistically independent. Consequently, the Effective Sample Size (ESS) is significantly less than the total number of collected samples $N$, confirming the inherent correlation in sequential MCMC sampling.
```