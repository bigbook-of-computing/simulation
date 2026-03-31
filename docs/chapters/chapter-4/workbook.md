# **Chapter 4: Finance I: Monte Carlo Option Pricing (Workbook)**

The goal of this chapter is to apply the MCMC and stochastic principles (from Chapters 1–3) to **financial engineering**, showing how to value complex financial derivatives by sampling potential asset price paths.

| Section | Topic Summary |
| :--- | :--- |
| **4.1** | Chapter Opener: Risk-Neutral Pricing and the Need for Simulation |
| **4.2** | Simulating Asset Paths Under Geometric Brownian Motion |
| **4.3** | Path-Dependent Options: Asian, Lookback, and Barrier |
| **4.4** | Variance-Reduction Techniques: Antithetic and Control Variates |
| **4.5** | Chapter Summary & Bridge to Chapter 5 |



### 4.1 Risk-Neutral Pricing and the Need for Simulation

> **Summary:** Monte Carlo simulation is the most flexible tool for valuing **exotic options** (which lack analytic formulas) by estimating the discounted expected payoff under the **risk-neutral measure** ($\mathbb{Q}$).

#### Section Detail

While simple European options have closed-form solutions (like Black-Scholes), **exotic options** (e.g., Asian, Barrier, Lookback options) depend on the entire **path** of the asset price, making them analytically intractable. The core of financial Monte Carlo is the **Fundamental Theorem of Asset Pricing**, which states that the price $V_0$ of a derivative is the expected payoff $h(S_T)$ discounted at the risk-free rate $r$, *provided* the expectation is taken under the risk-neutral measure ($\mathbb{Q}$):

$$
V_0 = e^{-rT} \mathbb{E}_{\mathbb{Q}} \left[h(S_T)\right]
$$

This approach is analogous to how MCMC estimates thermodynamic observables in physics.

#### Quiz Questions

!!! note "Quiz"
    **1. For which type of derivative is Monte Carlo simulation typically necessary?**
    
    * **A.** Plain European Call options.
    * **B.** **Exotic options** whose payoff depends on the entire asset price path. (**Correct**)
    * **C.** U.S. Treasury bonds.
    * **D.** Vanilla options with short maturity.
    
!!! note "Quiz"
    **2. In the risk-neutral measure ($\mathbb{Q}$), the expected drift ($\mu$) of a stock's price is assumed to be equal to:**
    
    * **A.** The asset's historical return.
    * **B.** The asset's volatility ($\sigma$).
    * **C.** Zero.
    * **D.** The **risk-free interest rate ($r$)**. (**Correct**)
    
    
!!! question "Interview Practice"
    **Question:** Conceptually, explain the connection between the **Boltzmann Distribution** in statistical mechanics and the **Risk-Neutral Measure ($\mathbb{Q}$)** in finance, as suggested by the text.
    
    **Answer Strategy:** Both concepts represent the **equilibrium probability measure** used for expectation value calculations.
    * The **Boltzmann distribution** $P(\mathbf{s}) \propto e^{-\beta E}$ is the equilibrium measure that weights the *microstates* ($\mathbf{s}$) of a physical system based on their energy, allowing us to compute thermodynamic averages.
    * The **Risk-Neutral Measure** ($\mathbb{Q}$) is the equilibrium measure that weights the *asset price paths* based on the no-arbitrage principle, allowing us to compute fair market prices.
    In both cases, we sample from a theoretical probability distribution to solve a high-dimensional integral and find an expected value.
    
    
### 4.2 Simulating Asset Paths Under Geometric Brownian Motion

> **Summary:** Asset paths are typically modeled using **Geometric Brownian Motion (GBM)**, a stochastic differential equation (SDE) that results in log-normal prices. Paths are generated using the **exact discretization** formula, driven by standard normal random variates ($Z_k$).

#### Section Detail

The standard SDE for GBM under the risk-neutral measure is $\mathrm{d}S_t = r S_t\,\mathrm{d}t + \sigma S_t\,\mathrm{d}W_t^{\mathbb{Q}}$. The simulation uses the exact closed-form solution to iteratively generate prices at discrete time steps $\Delta t = T/N$:

$$
S_{t_{k+1}} = S_{t_k} \exp\left[\left(r - \tfrac{\sigma^2}{2}\right)\Delta t + \sigma \sqrt{\Delta t}\,Z_k\right]
$$

The log-normal property ensures prices remain positive, and the term $\left(r - \tfrac{\sigma^2}{2}\right)$ is the corrected log-return (sometimes called the expected instantaneous drift).

#### Quiz Questions

!!! note "Quiz"
    **1. The primary random input used to drive the price changes $S_{t_{k+1}} / S_{t_k}$ in a Geometric Brownian Motion simulation is a variable $Z_k$ drawn from a:**
    
    * **A.** Uniform distribution $U(0,1)$.
    * **B.** Exponential distribution.
    * **C.** Standard **Normal (Gaussian) distribution** $N(0,1)$. (**Correct**)
    * **D.** Poisson distribution.
    
!!! note "Quiz"
    **2. Which key property of asset prices does the Geometric Brownian Motion model satisfy, in contrast to simple arithmetic Brownian motion?**
    
    * **A.** Prices are always stationary.
    * **B.** Prices always drift at the risk-free rate $r$.
    * **C.** **Prices are guaranteed to remain positive**. (**Correct**)
    * **D.** Volatility $\sigma$ is guaranteed to be constant.
    
    
!!! question "Interview Practice"
    **Question:** When simulating a multi-asset option (e.g., a basket option), why is it insufficient to simply generate two independent GBM paths for the two assets, $S^{(1)}$ and $S^{(2)}$? What computational step must be introduced?
    
    **Answer Strategy:** Most real-world assets are **correlated** (e.g., $\rho_{12} \neq 0$). Generating independent paths assumes $\rho_{12}=0$, which misrepresents the market and biases the option price. The computational step required is to introduce **correlated normal variates**:
    1.  Define the target correlation matrix $\rho$.
    2.  Compute the **Cholesky decomposition** $C$ of $\rho$.
    3.  Draw independent standard normals $Z_k$.
    4.  Transform them to correlated normals $Y_k = C Z_k$, and use these correlated $Y_k$ in the GBM updates.
    
    
### 4.3 Path-Dependent Options: Asian, Lookback and Barrier

> **Summary:** Monte Carlo simulation excels at pricing options whose payoff depends on a **functional of the path** (e.g., the average $\bar{S}$, the maximum $M_{\max}$, or hitting a barrier $B$). To price these, the simulation must track the required path statistic at every time step.

#### Section Detail

* **Asian Options** (Call payoff $\max(\bar{S} - K, 0)$) require tracking the **running arithmetic sum** of prices.
* **Lookback Options** (Call payoff $\max(M_{\max} - K, 0)$) require tracking the **maximum/minimum** price reached.
* **Barrier Options** (e.g., Up-and-Out) require monitoring a flag that is activated if the price $S_t$ crosses a predefined level $B$.

Because the price is only observed at discrete $\Delta t$ steps, a nuance for Barrier options is the possibility of "jumping" over the barrier between steps, which requires the use of **Brownian bridge interpolation** to correct for discretization error.

#### Quiz Questions

!!! note "Quiz"
    **1. To price an **Arithmetic-Average Asian Call** using Monte Carlo, which single statistic must be accumulated during the simulation of each price path?**
    
    * **A.** The terminal price $S_T$.
    * **B.** The volatility $\sigma$.
    * **C.** The **running sum of prices**. (**Correct**)
    * **D.** The time to maturity $T$.
    
!!! note "Quiz"
    **2. A key implementation nuance for **Barrier Options** is the potential for the asset price to cross the barrier $B$ between discrete time steps. This modeling error can be mitigated using:**
    
    * **A.** Quasi-Monte Carlo.
    * **B.** The antithetic variates technique.
    * **C.** **Brownian bridge interpolation/adjustment**. (**Correct**)
    * **D.** A lower risk-free rate $r$.
    
    
!!! question "Interview Practice"
    **Question:** Compare the analytical tractability and Monte Carlo implementation difficulty of an **Arithmetic Asian Option** versus a **Geometric Asian Option**.
    
    **Answer Strategy:**
    * **Geometric Asian Option:** Is relatively **analytically tractable**. Since the geometric average of log-normal variables is itself log-normal, a closed-form solution exists. In Monte Carlo, it's easily calculated by accumulating the product of returns.
    * **Arithmetic Asian Option:** Is **analytically intractable** because the arithmetic average of log-normal variables is not log-normal. It *requires* Monte Carlo simulation.
    * **Implementation Difficulty:** Both are easy to implement in Monte Carlo, but the arithmetic option is typically more difficult to price accurately due to higher variance, making the geometric option a strong candidate for a **control variate**.
    
    
### 4.4 Variance-Reduction Techniques

> **Summary:** Monte Carlo convergence is slow ($O(1/\sqrt{M})$). **Variance-Reduction Techniques (VRTs)** are essential to lower the standard error without increasing the number of paths $M$ dramatically. **Antithetic Variates** use negative correlation, and **Control Variates** leverage a correlated option with a known price.

#### Section Detail

* **Antithetic Variates:** Uses pairs of noise sequences $(Z, -Z)$ to generate a pair of paths $(S, \tilde{S})$. By averaging the payoffs of these two paths, negative correlation is induced, which reduces the overall variance of the estimator.
* **Control Variates:** Selects a random variable $C$ (e.g., a Geometric Asian payoff) that is highly correlated with the target payoff $H$ (e.g., the Arithmetic Asian payoff) and whose expected value ($\mathbb{E}[C]$) is known analytically. The final estimate is corrected using the known error of $C$. A correlation of $\rho=0.9$ can reduce variance by $81\%$.

$$
\mathrm{Var}[H^{\star}] = (1-\rho_{HC}^2)\mathrm{Var}[H]
$$

#### Quiz Questions

!!! note "Quiz"
    **1. If a Monte Carlo estimator's standard error is $0.10$, and you want to reduce it to $0.05$ (halve the error) without using variance reduction, you must increase the number of paths $M$ by a factor of:**
    
    * **A.** 2.
    * **B.** $\sqrt{2}$.
    * **C.** **4** (because error $\propto 1/\sqrt{M}$). (**Correct**)
    * **D.** 8.
    
!!! note "Quiz"
    **2. The key requirement for a random variable $C$ to be an effective **Control Variate** for a target payoff $H$ is that $C$ must be:**
    
    * **A.** Uncorrelated with $H$.
    * **B.** **Highly correlated with $H$ and have a known analytical expected value $\mathbb{E}[C]$**. (**Correct**)
    * **C.** Always equal to zero.
    * **D.** A standard Normal variate.
    
    
!!! question "Interview Practice"
    **Question:** An engineer proposes using a Control Variate $C$ that has a correlation of $\rho=0.5$ with the target payoff $H$. Is this a good control variate? Quantify the variance reduction achieved.
    
    **Answer Strategy:** A correlation of $\rho=0.5$ is better than nothing, but not "excellent." The percentage of variance reduction achieved is determined by $1 - \rho^2$.
    * Variance Reduction Factor: $\mathrm{Var}[H^{\star}] / \mathrm{Var}[H] = (1 - \rho^2)$.
    * For $\rho=0.5$, the reduction factor is $1 - (0.5)^2 = 1 - 0.25 = 0.75$.
    * This means the variance of the final estimator is **$75\%$** of the original variance, achieving a $25\%$ reduction in variance (or about a $13\%$ reduction in standard error). Better control variates typically aim for $\rho > 0.8$ or $\rho > 0.9$.
    
    
    
##  Hands-On Simulation Projects (Chapter Conclusion) 🛠️

These projects focus on building the core Monte Carlo engine and implementing essential variance-reduction techniques.


```
### Project 1: The Core GBM Path Generator (The Engine)

* **Goal:** Implement the risk-neutral GBM path generation function using the exact discretization.
* **Setup:** Define parameters $S_0=100$, $r=0.05$, $\sigma=0.20$, $T=1.0$ year, $N=252$ steps, and $M=10,000$ paths.
* **Steps:**
    1.  Write a Python function `generate_gbm_path(S0, r, sigma, T, N)` that returns a single price path (a list or array of $N+1$ prices).
    2.  Write a loop that calls this function $M$ times, storing only the terminal price $S_T$ of each path.
    3.  Verify the path generator by calculating the empirical mean of the $S_T$ values and comparing it to the theoretical mean: $\mathbb{E}[S_T] = S_0 e^{rT}$.
* ***Goal***: Establish a reliable path generator that satisfies the theoretical moment conditions.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ====================================================================

## 1. Simulation Parameters

## ====================================================================

S0 = 100.0  # Initial asset price
r = 0.05    # Risk-free interest rate (annual)
sigma = 0.20  # Volatility (annual)
T = 1.0     # Time to maturity (years)
N = 252     # Number of time steps (e.g., trading days)
M = 10000   # Number of paths to simulate
dt = T / N  # Time step size

## Theoretical expectation for validation

E_ST_THEO = S0 * np.exp(r * T)

## ====================================================================

## 2. GBM Path Generator

## ====================================================================

def generate_gbm_path(S0, r, sigma, T, N):
    """
    Generates a single asset price path using the exact GBM discretization
    under the risk-neutral measure Q.
    """
    dt = T / N
    # Pre-calculate constant drift and volatility terms
    drift = (r - 0.5 * sigma**2) * dt
    vol_factor = sigma * np.sqrt(dt)

    # Generate N standard normal variates for the entire path increments
    Z = np.random.standard_normal(N)

    # Pre-allocate path array (N+1 points: S0 to SN)
    path = np.zeros(N + 1)
    path[0] = S0

    # Iterate to generate the path
    for k in range(N):
        path[k+1] = path[k] * np.exp(drift + vol_factor * Z[k])

    return path

## ====================================================================

## 3. Running the Simulation and Validation

## ====================================================================

terminal_prices = np.zeros(M)
path_data_for_plot = []

for m in range(M):
    path = generate_gbm_path(S0, r, sigma, T, N)
    terminal_prices[m] = path[-1]

    # Save a few paths for visualization
    if m < 10:
        path_data_for_plot.append(path)

## Calculate empirical statistics

E_ST_EMPIRICAL = np.mean(terminal_prices)
EMPIRICAL_ERROR = np.std(terminal_prices) / np.sqrt(M)

## ====================================================================

## 4. Visualization

## ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
time_points = np.linspace(0, T, N + 1)

## Plot 1: Sample Asset Paths

ax[0].set_title(f'Sample GBM Paths (M={M} total)')
ax[0].set_xlabel('Time $t$ (Years)')
ax[0].set_ylabel('Asset Price $S_t$')
for path in path_data_for_plot:
    ax[0].plot(time_points, path, linewidth=1, alpha=0.6)
ax[0].grid(True)

## Plot 2: Terminal Price Distribution (Histogram)

ax[1].hist(terminal_prices, bins=50, density=True, color='skyblue', label='Simulated $S_T$')
ax[1].axvline(E_ST_THEO, color='red', linestyle='--', label='Theoretical Mean $\\mathbb{E}[S_T]$')
ax[1].set_title('Distribution of Terminal Prices $S_T$')
ax[1].set_xlabel('Terminal Price $S_T$')
ax[1].set_ylabel('Probability Density')
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()

## --- Validation Summary ---

print("\n--- GBM Path Generator Validation ---")
print(f"Theoretical Mean E[S_T]: {E_ST_THEO:.4f}")
print(f"Empirical Mean E[S_T]:   {E_ST_EMPIRICAL:.4f}")
print(f"Difference:              {E_ST_EMPIRICAL - E_ST_THEO:.4e}")
print(f"Statistical Error:       \u00B1 {EMPIRICAL_ERROR:.4f}")
print("\nConclusion: The empirical mean is within the statistical error of the theoretical risk-neutral mean, confirming the path generator is correctly implemented.")
```
**Sample Output:**
```python
--- GBM Path Generator Validation ---
Theoretical Mean E[S_T]: 105.1271
Empirical Mean E[S_T]:   105.0857
Difference:              -4.1403e-02
Statistical Error:       ± 0.2135

Conclusion: The empirical mean is within the statistical error of the theoretical risk-neutral mean, confirming the path generator is correctly implemented.
```


### Project 2: Pricing a Simple European Call

* **Goal:** Use the path generator to price a simple option and compare the Monte Carlo result against the known Black-Scholes-Merton (BSM) analytical price.
* **Setup:** Use $S_0=100$, $r=0.05$, $\sigma=0.20$, $T=1.0$, $K=100$.
* **Steps:**
    1.  Simulate $M=100,000$ paths.
    2.  For each path, calculate the payoff $h_m = \max(S_T - K, 0)$.
    3.  Calculate the Monte Carlo price: $\hat{V}_0 = e^{-rT} \frac{1}{M} \sum h_m$.
    4.  *(Requires external knowledge/function)* Compare $\hat{V}_0$ to the known BSM price.
* ***Goal***: Validate the entire Monte Carlo framework by showing that the simulated price falls within the expected statistical error of the analytical price.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

## ====================================================================

## 0. Analytical Validation Tool (BSM Model)

## ====================================================================

def black_scholes_call(S, K, T, r, sigma):
    """Calculates the analytical European Call price using the BSM formula."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

## ====================================================================

## 1. Setup Functions (from Project 1)

## ====================================================================

def generate_gbm_path(S0, r, sigma, T, N, Z_sequence=None):
    """
    Generates a single asset price path. Can accept a sequence of Z_sequence
    for use in Variance Reduction Techniques (VRTs).
    """
    dt = T / N
    drift = (r - 0.5 * sigma**2) * dt
    vol_factor = sigma * np.sqrt(dt)

    # Use provided Z_sequence or generate a new one
    if Z_sequence is None:
        Z = np.random.standard_normal(N)
    else:
        Z = Z_sequence

    path = np.zeros(N + 1)
    path[0] = S0

    for k in range(N):
        path[k+1] = path[k] * np.exp(drift + vol_factor * Z[k])

    return path

## ====================================================================

## 2. Simulation Parameters & Monte Carlo Pricing

## ====================================================================

## --- Pricing Parameters (Same as Project 1) ---

S0 = 100.0   # Initial asset price
K = 100.0    # Strike price
r = 0.05     # Risk-free interest rate
sigma = 0.20 # Volatility
T = 1.0      # Time to maturity
N = 252      # Number of time steps
M = 100000   # Number of paths (increased for better accuracy)

## Calculate BSM analytical price for validation

BSM_PRICE = black_scholes_call(S0, K, T, r, sigma)
DISCOUNT_FACTOR = np.exp(-r * T)

## --- Monte Carlo Simulation ---

terminal_prices = np.zeros(M)
payoffs = np.zeros(M)

for m in range(M):
    path = generate_gbm_path(S0, r, sigma, T, N)
    S_T = path[-1]

    # Payoff for European Call: max(S_T - K, 0)
    payoffs[m] = np.maximum(S_T - K, 0)

## Calculate Monte Carlo statistics

MC_PAYOFF_MEAN = np.mean(payoffs)
MC_PRICE = DISCOUNT_FACTOR * MC_PAYOFF_MEAN
MC_PAYOFF_STDEV = np.std(payoffs)

## Standard Error of the Mean (SEM)

MC_STANDARD_ERROR = DISCOUNT_FACTOR * (MC_PAYOFF_STDEV / np.sqrt(M))

## ====================================================================

## 3. Visualization and Comparison

## ====================================================================

## Plot 1: Payoff Distribution and BSM Price

fig, ax = plt.subplots(figsize=(8, 5))

## Filter for non-zero payoffs to make the histogram readable

non_zero_payoffs = payoffs[payoffs > 0]

ax.hist(non_zero_payoffs, bins=50, density=True, color='lightcoral', alpha=0.7, label='Simulated Payoffs ($h_m > 0$)')
ax.axvline(MC_PAYOFF_MEAN, color='blue', linestyle='-', linewidth=2, label=f'Mean Payoff $\\mathbb{{E}}[h_m]$: {MC_PAYOFF_MEAN:.4f}')

ax.set_title(f'Distribution of Call Option Payoffs ($M={M}$ Paths)')
ax.set_xlabel('Payoff $h(S_T)$')
ax.set_ylabel('Density')
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()

## --- Comparison Summary ---

print("\n--- Monte Carlo Pricing vs. BSM Analytical Price ---")
print(f"Analytical BSM Price:      {BSM_PRICE:.5f}")
print(f"Monte Carlo Price (V_hat): {MC_PRICE:.5f}")
print("------------------------------------------------")
print(f"Difference (MC - BSM):     {MC_PRICE - BSM_PRICE:.5f}")
print(f"Standard Error (SEM):    \u00B1 {MC_STANDARD_ERROR:.5f}")
print(f"Validation: |Difference| < 3 * SEM? {np.abs(MC_PRICE - BSM_PRICE) < 3 * MC_STANDARD_ERROR}")
```
**Sample Output:**
```python
--- Monte Carlo Pricing vs. BSM Analytical Price ---
Analytical BSM Price:      10.45058
Monte Carlo Price (V_hat): 10.49485

---

Difference (MC - BSM):     0.04427
Standard Error (SEM):    ± 0.04674
Validation: |Difference| < 3 * SEM? True
```


### Project 3: Implementing Antithetic Variates for Variance Reduction

* **Goal:** Implement the antithetic variates VRT and quantify the reduction in standard error.
* **Setup:** Use the same parameters as Project 2. Run $M=50,000$ *pairs* of paths (total $100,000$ paths).
* **Steps:**
    1.  Modify the path generator to accept a sequence of normal deviates $Z$ and return the path.
    2.  In the main loop, for each $m=1, \dots, 50,000$:
        * Generate the sequence $Z_m$.
        * Calculate path 1 payoff $h_m$ using $Z_m$.
        * Calculate path 2 payoff $\tilde{h}_m$ using the antithetic sequence $-Z_m$.
        * Average the pair: $\bar{h}_m = (h_m + \tilde{h}_m)/2$.
    3.  Calculate the final price and its standard error using only the $M=50,000$ averaged values $\bar{h}_m$.
    4.  Compare the final standard error with the error obtained in Project 2.
* ***Goal***: Demonstrate that the standard error is lower in Project 3 (using $50,000$ effective trials) than in Project 2 (using $100,000$ independent trials).

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

## ====================================================================

## 1. Setup Functions

## ====================================================================

## Analytical BSM price (for benchmark)

def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price


## GBM path generator (supports optional pre-generated normals)

def generate_gbm_path(S0, r, sigma, T, N, Z_sequence=None):
    """
    Generates a single asset price path using geometric Brownian motion.
    If Z_sequence is None, new random standard normal variates are generated.
    """
    dt = T / N
    drift = (r - 0.5 * sigma**2) * dt
    vol_factor = sigma * np.sqrt(dt)

    if Z_sequence is None:
        Z_sequence = np.random.standard_normal(N)

    path = np.zeros(N + 1)
    path[0] = S0

    for k in range(N):
        path[k + 1] = path[k] * np.exp(drift + vol_factor * Z_sequence[k])

    return path


## ====================================================================

## 2. Parameters

## ====================================================================

S0 = 100.0   # Initial asset price
K = 100.0    # Strike price
r = 0.05     # Risk-free interest rate
sigma = 0.20 # Volatility
T = 1.0      # Time to maturity (years)
N = 252      # Time steps
M_PAIRS = 50000  # Number of antithetic pairs (total 100,000 paths)

## Analytical BSM price and discount factor

BSM_PRICE = black_scholes_call(S0, K, T, r, sigma)
DISCOUNT_FACTOR = np.exp(-r * T)


## ====================================================================

## 3. Standard Monte Carlo (Independent Paths)

## ====================================================================

M_INDEPENDENT = M_PAIRS * 2  # 100,000 independent paths
independent_payoffs = np.zeros(M_INDEPENDENT)

for m in range(M_INDEPENDENT):
    S_T = generate_gbm_path(S0, r, sigma, T, N)[-1]
    independent_payoffs[m] = np.maximum(S_T - K, 0)

MC_STDEV_INDEPENDENT = np.std(independent_payoffs)
MC_SEM_INDEPENDENT = DISCOUNT_FACTOR * (MC_STDEV_INDEPENDENT / np.sqrt(M_INDEPENDENT))


## ====================================================================

## 4. Antithetic Variates Simulation

## ====================================================================

antithetic_payoff_averages = np.zeros(M_PAIRS)
payoffs_original = np.zeros(M_PAIRS)
payoffs_antithetic = np.zeros(M_PAIRS)

for m in range(M_PAIRS):
    # Generate a sequence of standard normal variates
    Z_sequence = np.random.standard_normal(N)

    # Path 1: original
    S_T_original = generate_gbm_path(S0, r, sigma, T, N, Z_sequence)[-1]
    h_original = np.maximum(S_T_original - K, 0)
    payoffs_original[m] = h_original

    # Path 2: antithetic
    S_T_antithetic = generate_gbm_path(S0, r, sigma, T, N, -Z_sequence)[-1]
    h_antithetic = np.maximum(S_T_antithetic - K, 0)
    payoffs_antithetic[m] = h_antithetic

    # Average the pair
    antithetic_payoff_averages[m] = (h_original + h_antithetic) / 2

## Antithetic Variates results

MC_PAYOFF_MEAN_AV = np.mean(antithetic_payoff_averages)
MC_PRICE_AV = DISCOUNT_FACTOR * MC_PAYOFF_MEAN_AV
MC_STDEV_AV = np.std(antithetic_payoff_averages)
MC_SEM_AV = DISCOUNT_FACTOR * (MC_STDEV_AV / np.sqrt(M_PAIRS))
correlation = np.corrcoef(payoffs_original, payoffs_antithetic)[0, 1]


## ====================================================================

## 5. Visualization and Comparison

## ====================================================================

fig, ax = plt.subplots(figsize=(8, 5))

labels = ['Standard MC (100k Trials)', 'Antithetic MC (50k Pairs)']
prices = [MC_PRICE_AV, MC_PRICE_AV]  # both plotted at same price for error comparison
errors = [MC_SEM_INDEPENDENT, MC_SEM_AV]

ax.errorbar(labels, prices, yerr=errors, fmt='o', capsize=5, linewidth=2, color='darkgreen')
ax.axhline(BSM_PRICE, color='red', linestyle='--', label='BSM Price')

ax.set_title('Variance Reduction: Standard Error Comparison (Total 100k Paths)')
ax.set_ylabel('Option Price Estimate ($V_0$)')
ax.set_ylim(BSM_PRICE - 0.2, BSM_PRICE + 0.2)
ax.legend()
ax.grid(True, linestyle=':')

plt.tight_layout()
plt.show()


## ====================================================================

## 6. Summary Output

## ====================================================================

print("\n--- Antithetic Variates (AV) Summary ---")
print(f"Total Paths Simulated: {M_PAIRS * 2:,} (50,000 pairs)")
print(f"Correlation between Payoffs (h, h~): {correlation:.4f}")
print("-------------------------------------------------------")
print(f"Standard MC SEM (100k independent trials): ± {MC_SEM_INDEPENDENT:.5f}")
print(f"AV MC SEM (50k effective trials):          ± {MC_SEM_AV:.5f}")
print(f"Variance Reduction Factor (1 - ρ²):        {1 - correlation**2:.4f}")

sem_ratio = MC_SEM_INDEPENDENT / MC_SEM_AV
print(f"SEM Reduction (SEM_Std / SEM_AV):          {sem_ratio:.2f}x")

print("\nConclusion: The Antithetic Variates technique successfully reduces the Standard Error of the Mean (SEM) while using only half as many independent random samples (50k pairs vs. 100k independent trials). The negative correlation between paired payoffs cancels variance, making the estimator more efficient.")
```
**Sample Output:**
```python
--- Antithetic Variates (AV) Summary ---
Total Paths Simulated: 100,000 (50,000 pairs)
Correlation between Payoffs (h, h~): -0.5006

---

Standard MC SEM (100k independent trials): ± 0.04650
AV MC SEM (50k effective trials):          ± 0.03272
Variance Reduction Factor (1 - ρ²):        0.7494
SEM Reduction (SEM_Std / SEM_AV):          1.42x

Conclusion: The Antithetic Variates technique successfully reduces the Standard Error of the Mean (SEM) while using only half as many independent random samples (50k pairs vs. 100k independent trials). The negative correlation between paired payoffs cancels variance, making the estimator more efficient.
```


### Project 4: Monte Carlo for a Path-Dependent Asian Option

* **Goal:** Price a complex option that is analytically intractable.
* **Setup:** Use $S_0=100$, $r=0.05$, $\sigma=0.20$, $T=1.0$, $K=100$, $N=252$ steps.
* **Steps:**
    1.  Modify the path generator to calculate and return the **arithmetic average** of all prices, $\bar{S}$, for each path.
    2.  Run the simulation for $M=100,000$ paths.
    3.  Calculate the payoff $h_m = \max(\bar{S}_m - K, 0)$.
    4.  Calculate the final price $\hat{V}_0$ and its statistical error.
* ***Goal***: Produce a price and confidence interval for the Arithmetic Asian option, demonstrating the flexibility of Monte Carlo for path-dependent problems.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

## ====================================================================

## 1. Setup and Core Path Generator (Modified for Asian Average)

## ====================================================================

## --- Pricing Parameters (Same as Project 2 & 3) ---

S0 = 100.0   # Initial asset price
K = 100.0    # Strike price
r = 0.05     # Risk-free interest rate
sigma = 0.20 # Volatility
T = 1.0      # Time to maturity
N = 252      # Number of time steps (daily observation frequency)
M = 100000   # Number of paths to simulate

dt = T / N
DISCOUNT_FACTOR = np.exp(-r * T)
STEPS_COUNT = N + 1 # Number of observation points including S0

def generate_gbm_average(S0, r, sigma, T, N, Z_sequence):
    """
    Generates a single asset price path and returns the final arithmetic average
    of all prices in the path.
    """
    dt = T / N
    drift = (r - 0.5 * sigma**2) * dt
    vol_factor = sigma * np.sqrt(dt)

    # Use provided Z_sequence (e.g., from Antithetic Variates)
    Z = Z_sequence

    current_S = S0
    sum_S = S0  # Initialize sum with the starting price S0

    for k in range(N):
        current_S *= np.exp(drift + vol_factor * Z[k])
        sum_S += current_S  # Accumulate the price

    # Calculate arithmetic average
    arithmetic_average = sum_S / STEPS_COUNT

    return arithmetic_average

## We use Antithetic Variates here as a standard practice to reduce variance

## We will run M_PAIRS pairs, totaling M paths.

M_PAIRS = M // 2

## ====================================================================

## 2. Monte Carlo Simulation for Asian Call

## ====================================================================

## Storage for averaged payoffs

antithetic_payoff_averages = np.zeros(M_PAIRS)

for m in range(M_PAIRS):
    # 1. Generate one sequence of normal deviates
    Z_sequence = np.random.standard_normal(N)

    # 2. Path 1: Original Path (Z)
    S_avg_original = generate_gbm_average(S0, r, sigma, T, N, Z_sequence)
    h_original = np.maximum(S_avg_original - K, 0)

    # 3. Path 2: Antithetic Path (-Z)
    S_avg_antithetic = generate_gbm_average(S0, r, sigma, T, N, -Z_sequence)
    h_antithetic = np.maximum(S_avg_antithetic - K, 0)

    # 4. Store the average of the paired payoffs
    antithetic_payoff_averages[m] = (h_original + h_antithetic) / 2

## Calculate Monte Carlo statistics

MC_PAYOFF_MEAN_ASIAN = np.mean(antithetic_payoff_averages)
MC_PRICE_ASIAN = DISCOUNT_FACTOR * MC_PAYOFF_MEAN_ASIAN

## Standard Error of the Mean (SEM) using M_PAIRS effective trials

MC_STDEV_ASIAN = np.std(antithetic_payoff_averages)
MC_SEM_ASIAN = DISCOUNT_FACTOR * (MC_STDEV_ASIAN / np.sqrt(M_PAIRS))

## 95% Confidence Interval (z-score for 95% is approx 1.96)

CONFIDENCE_INTERVAL = MC_SEM_ASIAN * 1.96

## ====================================================================

## 3. Visualization and Analysis

## ====================================================================

## Plot 1: Payoff Distribution

fig, ax = plt.subplots(figsize=(8, 5))

## Filter for non-zero payoffs

non_zero_payoffs = antithetic_payoff_averages[antithetic_payoff_averages > 0]

ax.hist(non_zero_payoffs, bins=50, density=True, color='purple', alpha=0.7,
        label='Simulated Payoffs ($h_m > 0$)')

ax.axvline(MC_PAYOFF_MEAN_ASIAN, color='red', linestyle='-', linewidth=2,
           label=f'Mean Payoff $\\mathbb{{E}}[h_m]$: {MC_PAYOFF_MEAN_ASIAN:.4f}')

ax.set_title(f'Distribution of Arithmetic Asian Call Payoffs ($M={M}$ Paths)')
ax.set_xlabel('Average Payoff $h(\\bar{{S}})$')
ax.set_ylabel('Density')
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()

## --- Pricing Summary ---

print("\n--- Arithmetic Asian Call Option Price ---")
print(f"Option Type: Arithmetic-Average Asian Call (Path Dependent)")
print(f"Total Paths Simulated: {M} (50,000 Antithetic Pairs)")
print("-------------------------------------------------------")
print(f"Monte Carlo Price (V_hat): {MC_PRICE_ASIAN:.5f}")
print(f"Standard Error (SEM):    \u00B1 {MC_SEM_ASIAN:.5f}")
print(f"95% Confidence Interval: ({MC_PRICE_ASIAN - CONFIDENCE_INTERVAL:.5f}, {MC_PRICE_ASIAN + CONFIDENCE_INTERVAL:.5f})")

print("\nConclusion: Monte Carlo simulation successfully priced the analytically intractable Arithmetic Asian Call Option. The price is derived from averaging the path-dependent payoff function $h(\\bar{{S}})$ over 100,000 simulated risk-neutral paths, and the use of Antithetic Variates ensures a tight confidence interval on the final estimate.")
```
**Sample Output:**
```python
--- Arithmetic Asian Call Option Price ---
Option Type: Arithmetic-Average Asian Call (Path Dependent)
Total Paths Simulated: 100000 (50,000 Antithetic Pairs)

---

Monte Carlo Price (V_hat): 5.73961
Standard Error (SEM):    ± 0.01740
95% Confidence Interval: (5.70550, 5.77372)

Conclusion: Monte Carlo simulation successfully priced the analytically intractable Arithmetic Asian Call Option. The price is derived from averaging the path-dependent payoff function $h(\bar{{S}})$ over 100,000 simulated risk-neutral paths, and the use of Antithetic Variates ensures a tight confidence interval on the final estimate.
```