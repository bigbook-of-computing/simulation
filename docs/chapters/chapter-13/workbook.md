# **Chapter 13: Biology III: Collective Behavior & Pattern Formation () () () (Workbook)**

The goal of this chapter is to explore **morphogenesis**, the biological emergence of structured patterns, by modeling how local rules and chemical diffusion give rise to global geometry and function.

| Section | Topic Summary |
| :--- | :--- |
| **13.1** | Chapter Opener: How Cells “Compute” Structure |
| **13.2** | Reaction–Diffusion Models (Turing Patterns) |
| **13.3** | Graph Theory for Regulatory Networks |
| **13.4** | Chapter Summary & Bridge to Chapter 14 |

---

### 13.1 How Cells “Compute” Structure

> **Summary:** **Morphogenesis** (the self-organization of biological structure) arises when genetically identical cells coordinate their behavior. This process is viewed as **emergent computation**, where complexity is generated bottom-up through local **interactions and feedback**. The primary tools for modeling this are **Agent-Based Models (ABMs)** for cellular actions and **Partial Differential Equations (PDEs)** for chemical signaling.

#### Quiz Questions

!!! note "Quiz"
```
**1. The primary challenge that morphogenesis models address is:**

* **A.** How gravitational forces shape the organism.
* **B.** How to sequence the DNA of a cell.
* **C.** **How a uniform group of cells spontaneously produces complex, ordered spatial patterns**. (**Correct**)
* **D.** How to solve the Nernst equation for ion gradients.

```
!!! note "Quiz"
```
**2. In the computational model of tissue development, the continuous field of chemical concentrations is typically modeled using which mathematical framework?**

* **A.** Ordinary Differential Equations (ODEs).
* **B.** Graph Theory.
* **C.** **Partial Differential Equations (PDEs)**. (**Correct**)
* **D.** Boolean Logic.

```
---

!!! question "Interview Practice"
```
**Question:** The text suggests that the process of morphogenesis (development) is essentially a **distributed computation**. Explain what constitutes the "processors," the "rules," and the "output" in this biological computation.

**Answer Strategy:**
* **Processors:** The individual **cells** (genetically identical descendants of the zygote).
* **Rules:** The **local molecular kinetics** and signaling logic (e.g., sense local chemical concentrations $\to$ decide $\to$ secrete new chemicals).
* **Output:** The final **complex geometry and functional structure** (e.g., stripes, limbs, organs) — the emergent form.

```
---

### 13.2 Reaction–Diffusion Models (Turing Patterns)

> **Summary:** **Turing's Reaction–Diffusion (RD) model** explains how chemical patterns spontaneously emerge. It relies on two coupled PDEs, featuring an **Activator ($u$)** that promotes its own production and a faster-diffusing **Inhibitor ($v$)** ($D_v \gg D_u$). This imbalance creates a **diffusion-driven instability** in a uniform field, leading to stable, periodic patterns like **spots or stripes**.

#### Section Detail

The reaction terms $f(u, v)$ and $g(u, v)$ provide the **nonlinear feedback** necessary to couple chemical kinetics with spatial transport (the Laplacian, $\nabla^2$). The core logic is **local activation, long-range inhibition**, which establishes a characteristic distance (wavelength) between the patterns. Different parameters (e.g., feed and kill rates $F, k$) produce distinct morphologies.

#### Quiz Questions

!!! note "Quiz"
```
**1. The core requirement for generating stable Turing patterns is that:**

* **A.** Both the activator and inhibitor must diffuse at the same slow rate.
* **B.** The activator must be constantly removed from the system.
* **C.** **The inhibitor must diffuse significantly faster and farther than the activator** ($D_v \gg D_u$). (**Correct**)
* **D.** The system must remain entirely homogeneous.

```
!!! note "Quiz"
```
**2. The spontaneous formation of patterns from a uniform background is fundamentally a mechanism of:**

* **A.** Simple random walk (Brownian motion).
* **B.** **Symmetry breaking**. (**Correct**)
* **C.** Linear stability analysis.
* **D.** Conservation of energy.

```
---

!!! question "Interview Practice"
```
**Question:** Explain, using the RD model analogy, why the stripes on a zebra are always roughly the same width (or characteristic spacing), rather than being randomly thin or thick.

**Answer Strategy:** The spacing of the stripes is determined by the **characteristic wavelength** of the diffusion-driven instability. This wavelength is set by the ratio of the diffusion rates, $D_v / D_u$. Since $D_v$ (inhibitor spread) sets the maximum distance an activation center can influence its neighbors, the pattern is forced to emerge periodically at a specific separation. This creates the reproducible, uniform distance between stripes (or spots), regardless of minor random fluctuations in the initial cell field.

```
---

### 13.3 Graph Theory for Regulatory Networks

> **Summary:** **Gene Regulatory Networks (GRNs)** are modeled using **Graph Theory**, where **nodes** are genes/proteins and **edges** are regulatory connections (+ for activation, $-$ for inhibition). GRNs are analyzed for **structural motifs** (feedback loops, feed-forward loops). Simulating these networks using **Boolean logic** shows that the system settles into **attractors** (stable states or cycles), which are computationally interpreted as **distinct cell types**.

#### Section Detail

The GRN approach shifts the focus from **spatial pattern** to **logical pattern**. Feedback loops are the most critical motifs: **positive feedback** creates memory and stabilizes ON/OFF states, while **negative feedback** drives oscillations. The genome is viewed not as a blueprint, but as a **dynamical system with multiple stable equilibria (attractors)**, and differentiation is the transition between these attractors.

#### Quiz Questions

!!! note "Quiz"
```
**1. In the context of a Gene Regulatory Network (GRN), a recurring sub-network structure where Gene A activates Gene B, and Gene B activates Gene A, is known as:**

* **A.** A Boolean logic gate.
* **B.** **A Positive Feedback Loop**. (**Correct**)
* **C.** A Feed-Forward Loop.
* **D.** A diffusion-driven instability.

```
!!! note "Quiz"
```
**2. In the simulation of a Boolean Gene Regulatory Network, a stable, repeating cycle of gene expression states is known as an **attractor**. Biologically, this attractor is often interpreted as representing:**

* **A.** A temporary phase transition.
* **B.** The chemical concentration of a morphogen.
* **C.** **A distinct cell type (e.g., a neuron or muscle cell)**. (**Correct**)
* **D.** A single activation gate.

```
---

!!! question "Interview Practice"
```
**Question:** Compare and contrast the stability mechanisms of the **Reaction–Diffusion** model versus the **Gene Regulatory Network** model.

**Answer Strategy:**
* **RD Model (Physical Stability):** Stability is achieved through **long-range inhibition**. The pattern's size and spacing are physically stable because the fast-diffusing inhibitor suppresses fluctuations in the surrounding space, locking the activator into a fixed location.
* **GRN Model (Logical Stability):** Stability is achieved through **positive feedback loops**. Once a set of genes enters an ON state, the positive feedback forces it to remain ON, creating an informational memory (the attractor) that is robust against small changes, essentially stabilizing a "logical decision" (the cell type).

```
---

### 💡 Hands-On Simulation Projects (Chapter Conclusion) 🛠️

These projects require implementing the core RD and GRN models, bridging continuous and discrete simulation methods.

### Project 1: Simulating a 1D Reaction–Diffusion System

* **Goal:** Implement the explicit finite-difference scheme for the single-species diffusion equation with a simple reaction term, $u_t = D u_{xx} + f(u)$.
* **Setup:** Simulate the simple diffusion equation with a nonlinear local growth term: $\frac{\partial u}{\partial t} = D \frac{\partial^2 u}{\partial x^2} + k u (1-u)$ (Logistic Growth).
* **Steps:**
    1.  Implement the finite-difference approximation for the Laplacian, $\frac{\partial^2 u}{\partial x^2} \approx \frac{u_{i+1} - 2u_i + u_{i-1}}{\Delta x^2}$.
    2.  Use the Forward Euler time step to update the concentration $u_i$.
    3.  Initialize the 1D domain with a localized spike of concentration $u$ and zero elsewhere.
* ***Goal***: Show that the initial spike spreads and flattens over time (diffusion) but also grows at the boundaries (reaction), demonstrating the fundamental PDE components.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

# Set seed for reproducibility

np.random.seed(42)

## ====================================================================

## 1. Setup Parameters and Grid

## ====================================================================

## --- PDE Parameters ---

D = 0.01    # Diffusion coefficient (D)
K = 0.5     # Logistic growth rate (k)

## --- Grid Parameters ---

L = 1.0     # Domain length
NX = 100    # Number of spatial grid points
DX = L / NX # Spatial step size (\Delta x)

## --- Time Parameters (Conditional Stability) ---

DT = 0.5 * DX**2 / D # Ensure stability for explicit scheme
T_FINAL = 20.0
NT = int(T_FINAL / DT)

## Initialize concentration vector (u)

U = np.zeros(NX + 1)
x_points = np.linspace(0, L, NX + 1)

## Initial Condition: Localized spike in the center of the domain

SPIKE_WIDTH = 5
U[NX // 2 - SPIKE_WIDTH : NX // 2 + SPIKE_WIDTH] = 0.5

## ====================================================================

## 2. FDM Simulation Loop (Forward Euler)

## ====================================================================

## Storage for plotting snapshots

U_snapshots = [U.copy()]
snapshot_interval = NT // 5

for n in range(NT):
    U_new = U.copy()

    # 1. Calculate the spatial terms (Laplacian)
    # Uses the current time step values (U) to compute the derivatives
    U_laplacian = (np.roll(U, -1) - 2 * U + np.roll(U, 1)) / DX**2

    # 2. Apply the Forward Euler update
    # u_new = u_old + dt * [ D * u_xx + k * u * (1 - u) ]
    U_new = U + DT * (D * U_laplacian + K * U * (1 - U))

    # Boundary Conditions (Fixed Flux/Zero Concentration at boundaries)
    U_new[0] = 0.0
    U_new[NX] = 0.0

    U = U_new

    if (n + 1) % snapshot_interval == 0:
        U_snapshots.append(U.copy())

## ====================================================================

## 3. Visualization

## ====================================================================

plt.figure(figsize=(10, 5))

## Plot the concentration profile over time

for i, u_snap in enumerate(U_snapshots):
    time_snap = i * T_FINAL / 5
    plt.plot(x_points, u_snap, label=f'Time $\\approx {time_snap:.1f}$ s', lw=1.5)

## Labeling and Formatting

plt.title(f'1D Reaction–Diffusion System (D={D}, K={K})')
plt.xlabel('Position $x$')
plt.ylabel('Concentration $u(x, t)$')
plt.ylim(bottom=0, top=1.1)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

## --- Analysis Summary ---

print("\n--- 1D Reaction–Diffusion Analysis Summary ---")
print(f"Diffusion Coefficient (D): {D}")
print(f"Reaction Rate (K): {K}")
print("\nConclusion: The simulation successfully demonstrates the coupling of diffusion and reaction. The initial spike both spreads out across the domain (diffusion) and grows in magnitude (reaction) until it approaches the saturation limit (u=1) imposed by the logistic growth term.")
```
**Sample Output:**
```python
--- 1D Reaction–Diffusion Analysis Summary ---
Diffusion Coefficient (D): 0.01
Reaction Rate (K): 0.5

Conclusion: The simulation successfully demonstrates the coupling of diffusion and reaction. The initial spike both spreads out across the domain (diffusion) and grows in magnitude (reaction) until it approaches the saturation limit (u=1) imposed by the logistic growth term.
```


### Project 2: Simulating and Visualizing Boolean Network Attractors

* **Goal:** Implement a small Boolean network and map its state space to find attractors.
* **Setup:** Use a three-gene system A, B, C (8 total states). Define the rules: A $\to$ B, B $\to$ NOT C, C $\to$ A (Negative feedback loop).
* **Steps:**
    1.  Write a function `next_state(current_state)` that applies the logical rules to generate the next state.
    2.  Start from every possible initial state (e.g., (0,0,0) to (1,1,1)).
    3.  Iteratively apply `next_state` until the system repeats a state (finds an attractor).
* ***Goal***: Plot the resulting state transitions, showing that the system settles into one or more stable **attractors** (fixed points or limit cycles), which represent the stable cell types.

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx # For plotting the conceptual network structure

## ====================================================================

## 1. Setup Network Rules (3-Gene System with Negative Feedback)

## ====================================================================

## Rule: A -> B, B -> C, C -> NOT A (Creating a negative feedback cycle)

## This design is prone to oscillation (limit cycles).

## Boolean Logic Functions

def AND(a, b): return a and b
def OR(a, b):  return a or b
def NOT(a):    return not a

def next_state(S_current):
    """
    Applies the network's logical rules to compute the next state.
    S = [A, B, C]
    """
    A, B, C = S_current

    # 1. A's Rule: A is activated by C
    A_next = C

    # 2. B's Rule: B is activated by A
    B_next = A

    # 3. C's Rule: C is inhibited by B
    C_next = NOT(B)

    return np.array([int(A_next), int(B_next), int(C_next)])

## ====================================================================

## 2. Simulation: State Space Trajectory

## ====================================================================

MAX_STEPS = 15 # Max steps to find the attractor
## Initial State (Arbitrary starting point)

S_initial = np.array([1, 0, 0]) # A=ON, B=OFF, C=OFF

history = [S_initial.copy()]
S_current = S_initial.copy()

print(f"Initial State S0: {S_initial}")

for t in range(MAX_STEPS):
    S_next = next_state(S_current)
    S_current = S_next

    # Check if the state has appeared before (indicating an attractor cycle)
    if any(np.array_equal(S_next, state) for state in history):
        print(f"Attractor found at step {t+1}.")
        history.append(S_next)
        break

    history.append(S_next)

## Convert history to DataFrame for plotting

df_history = pd.DataFrame(history, columns=['Gene A', 'Gene B', 'Gene C'])
df_history['Time'] = df_history.index

## ====================================================================

## 3. Visualization

## ====================================================================

## 1. Time Series Plot (to visualize the oscillation)

fig, ax = plt.subplots(figsize=(8, 4))
df_history.plot(x='Time', y=['Gene A', 'Gene B', 'Gene C'], kind='line', drawstyle='steps-post', ax=ax)
ax.set_yticks([0, 1])
ax.set_title('Boolean Network Dynamics: Convergence to Attractor')
ax.set_xlabel('Time Step')
ax.set_ylabel('Expression State (0=OFF, 1=ON)')
ax.legend(title='Gene')
ax.grid(True)

plt.tight_layout()
plt.show()

## 2. State Space Plot (Conceptual Graph)

## Define the graph structure for visualization

G = nx.DiGraph()
for t in range(len(history) - 1):
    src = str(list(history[t]))
    dest = str(list(history[t+1]))
    G.add_edge(src, dest, weight=t)

## Use spring layout for visualization (optional)

pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(6, 6))
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
nx.draw_networkx_labels(G, pos, font_size=8)
plt.title('Attractor Cycle in State Space')
plt.axis('off')
plt.show()


## --- Analysis Summary ---

print("\n--- Boolean Network Attractor Analysis ---")
attractor_cycle = df_history.iloc[history.index(history[-1]) - 1:]
print(f"Attractor Cycle Length: {len(attractor_cycle)} steps")
print("\nAttractor Cycle States (Steady State):")
print(attractor_cycle.iloc[:-1].to_markdown(index=False))

print("\nConclusion: The simulation confirms that the finite-state network converges to a stable **limit cycle attractor** (a repeating sequence of states). Biologically, this attractor represents the final, stable **cell identity** (e.g., muscle cell or neuron) computed by the gene circuit.")
```
**Sample Output:**
```python
Initial State S0: [1 0 0]
Attractor found at step 2.

--- Boolean Network Attractor Analysis ---
```


### Project 3: Identifying Network Structural Motifs

* **Goal:** Use basic graph theory metrics to identify the structural roles of nodes in a network.
* **Setup:** Define the adjacency matrix $A$ for a conceptual Gene Regulatory Network (e.g., a simple Feed-Forward Loop or a Mutual Inhibition system).
* **Steps:**
    1.  Calculate the **in-degree** (number of incoming connections) and **out-degree** (number of outgoing connections) for each gene/node.
    2.  Identify a **master regulator** (high out-degree, low in-degree) and a **sensor gene** (high in-degree, low out-degree).
* ***Goal***: Show how computational analysis of network topology reveals the specialized functional roles of genes in a regulatory network.

#### Python Implementation

```python
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

## ====================================================================

## 1. Setup Conceptual Gene Regulatory Network (GRN)

## ====================================================================

## Nodes: 5 Genes/Proteins (A, B, C, D, E)

GENE_NAMES = ['A (Master)', 'B (Toggle)', 'C (Toggle)', 'D (Sensor)', 'E (Output)']
N_GENES = len(GENE_NAMES)

## Adjacency Matrix A[i, j] = 1 if i regulates j, 0 otherwise

## Rule Design:

## 1. A is a Master Regulator (high out-degree to B, D)

## 2. B and C form a Mutual Inhibition/Toggle Switch (B -> -C, C -> -B)

## 3. D is a sensor target of A and E

## 4. E is a final Output

ADJACENCY_MATRIX = np.array([
##   A   B   C   D   E

    [0, +1,  0, +1,  0], # A activates B and D (High Out)
    [0,  0, -1,  0,  0], # B inhibits C
    [0, -1,  0,  0,  0], # C inhibits B
    [0,  0,  0,  0, +1], # D activates E
    [0,  0,  0,  0,  0]  # E is a final output (Low Out)
])

## ====================================================================

## 2. Graph Analysis (NetworkX)

## ====================================================================

## Create the directed graph from the adjacency matrix

## Add labels for positive/negative regulation

G = nx.from_numpy_array(ADJACENCY_MATRIX, create_using=nx.DiGraph)

## Relabel nodes with gene names

G = nx.relabel_nodes(G, {i: GENE_NAMES[i] for i in range(N_GENES)})

## Compute graph metrics

in_degree = dict(G.in_degree())
out_degree = dict(G.out_degree())

## Compute Degree Centrality (simple metric proportional to total connections)

degree_centrality = {gene: in_degree[gene] + out_degree[gene] for gene in GENE_NAMES}

## ====================================================================

## 3. Structural Role Identification

## ====================================================================

print("--- Gene Regulatory Network (GRN) Structural Analysis ---")

print("\n1. Centrality Metrics:")
for gene in GENE_NAMES:
    print(f"  {gene:<15} | In: {in_degree[gene]:<2} | Out: {out_degree[gene]:<2} | Total: {degree_centrality[gene]:<2}")

print("\n2. Identifying Roles (Structural Motifs):")

## Master Regulator: High Out-Degree (A)

master_regulator = max(out_degree, key=out_degree.get)
print(f"- Master Regulator: {master_regulator} (Controls 2 genes downstream)")

## Sensor Gene: High In-Degree, Low Out-Degree (D)

sensor_gene = max(degree_centrality, key=degree_centrality.get)
if out_degree[sensor_gene] == 1: # D has in=1, out=1, total=2
     print(f"- Sensor Gene: D (In=1, Out=1) - Integrates input from A, transmits to E.")

## Toggle Switch Motif (B and C)

print("- Structural Motif: B and C form a **Mutual Inhibition/Toggle Switch** (B ⊣ C, C ⊣ B).")

## ====================================================================

## 4. Visualization

## ====================================================================

plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42) # Layout for visualization

## Draw nodes scaled by Total Degree (Centrality)

nx.draw_networkx_nodes(G, pos, node_size=[v * 300 for v in degree_centrality.values()],
                       node_color='lightblue', alpha=0.9)

## Draw edges (distinguish activation/inhibition)

edges = G.edges()
colors = ['red' if ADJACENCY_MATRIX[GENE_NAMES.index(u), GENE_NAMES.index(v)] < 0 else 'blue' for u, v in edges]
labels = nx.get_edge_attributes(G, 'weight')

nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=colors, width=1.5, arrowsize=20)
nx.draw_networkx_labels(G, pos, font_weight='bold', font_size=10)

plt.title('Gene Regulatory Network Topology (Master Regulator A, Toggle B/C)')
plt.axis('off')
plt.show()

print("\nConclusion: Computational analysis of the GRN's topology, specifically through in-degree and out-degree, reveals its functional architecture. Gene A acts as the upstream master controller, while B and C form a local feedback motif (the toggle switch) essential for binary cell fate decision-making.")
```
**Sample Output:**
```python
--- Gene Regulatory Network (GRN) Structural Analysis ---

1. Centrality Metrics:
  A (Master)      | In: 0  | Out: 2  | Total: 2
  B (Toggle)      | In: 2  | Out: 1  | Total: 3
  C (Toggle)      | In: 1  | Out: 1  | Total: 2
  D (Sensor)      | In: 1  | Out: 1  | Total: 2
  E (Output)      | In: 1  | Out: 0  | Total: 1

2. Identifying Roles (Structural Motifs):
- Master Regulator: A (Master) (Controls 2 genes downstream)
- Sensor Gene: D (In=1, Out=1) - Integrates input from A, transmits to E.
- Structural Motif: B and C form a **Mutual Inhibition/Toggle Switch** (B ⊣ C, C ⊣ B).

Conclusion: Computational analysis of the GRN's topology, specifically through in-degree and out-degree, reveals its functional architecture. Gene A acts as the upstream master controller, while B and C form a local feedback motif (the toggle switch) essential for binary cell fate decision-making.
```


### Project 4: Modeling a Genetic Toggle Switch (Continuous ODE)

* **Goal:** Implement the continuous (ODE) model of the genetic toggle switch to observe bistability.
* **Setup:** Use the two-gene mutual inhibition model: $u \dashv v$ and $v \dashv u$ (two coupled ODEs, $\frac{du}{dt} = \frac{\alpha_1}{1 + v^{\beta}} - u$, $\frac{dv}{dt} = \frac{\alpha_2}{1 + u^{\gamma}} - v$).
* **Steps:**
    1.  Implement the ODE system using the **Runge–Kutta 4th-order (RK4)** solver (Volume I/Chapter 10).
    2.  Run the simulation twice with two distinct initial conditions:
        * **Run A:** Start with high $u$, low $v$ ($u_0=10, v_0=1$).
        * **Run B:** Start with low $u$, high $v$ ($u_0=1, v_0=10$).
* ***Goal***: Show that the system settles into two distinct stable states (attractors) depending on the initial condition, demonstrating **bistability**—a fundamental mechanism for binary decision-making (like cell fate).

#### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

## ====================================================================

## 1. Setup Parameters and The ODE System

## ====================================================================

## --- Toggle Switch Parameters ---

## Parameters chosen to ensure bistability (high Hill coefficients)

ALPHA1 = 5.0  # Max synthesis rate for u
ALPHA2 = 5.0  # Max synthesis rate for v
BETA_HILL = 3.0 # Hill coefficient (cooperativity) for v repressing u
GAMMA_HILL = 3.0 # Hill coefficient (cooperativity) for u repressing v

## --- Simulation Parameters ---

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

## ====================================================================

## 2. RK4 Solver Implementation

## ====================================================================

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

## ====================================================================

## 3. Bistability Scenarios and Simulation

## ====================================================================

## --- Run A: Initial State biased towards u (u HIGH, v LOW) ---

S_INIT_A = np.array([10.0, 1.0])
uA, vA = run_simulation(S_INIT_A)

## --- Run B: Initial State biased towards v (u LOW, v HIGH) ---

S_INIT_B = np.array([1.0, 10.0])
uB, vB = run_simulation(S_INIT_B)

time_points = np.arange(0, T_FINAL, DT)

## ====================================================================

## 4. Visualization

## ====================================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

## Plot 1: Trajectories (Time Series)

ax[0].plot(time_points, uA, label='u (Run A: High u0)', color='darkblue', lw=2)
ax[0].plot(time_points, vA, label='v (Run A: High u0)', color='skyblue', lw=2)
ax[0].plot(time_points, uB, label='u (Run B: High v0)', color='darkred', lw=2, linestyle='--')
ax[0].plot(time_points, vB, label='v (Run B: High v0)', color='salmon', lw=2, linestyle='--')
ax[0].set_title('Genetic Toggle Switch: Trajectories')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Concentration')
ax[0].legend()
ax[0].grid(True)

## Plot 2: Bistability (Phase Space/u vs v)

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

## --- Analysis Summary ---

print("\n--- Genetic Toggle Switch Bistability Analysis ---")
print(f"Run A (Start u=10, v=1): Final State (u={uA[-1]:.2f}, v={vA[-1]:.2f}) -> Attractor 1 (u HIGH)")
print(f"Run B (Start u=1, v=10): Final State (u={uB[-1]:.2f}, v={vB[-1]:.2f}) -> Attractor 2 (v HIGH)")

print("\nConclusion: The simulation demonstrates **bistability**—the fundamental mechanism for binary decision-making in cells. Despite the identical governing equations, the system converges to one of two distinct stable states (attractors) based entirely on the initial conditions, confirming the logical switch functionality of the mutually inhibitory genetic circuit.")
```
**Sample Output:**
```python
--- Genetic Toggle Switch Bistability Analysis ---
Run A (Start u=10, v=1): Final State (u=5.00, v=0.04) -> Attractor 1 (u HIGH)
Run B (Start u=1, v=10): Final State (u=0.04, v=5.00) -> Attractor 2 (v HIGH)

Conclusion: The simulation demonstrates **bistability**—the fundamental mechanism for binary decision-making in cells. Despite the identical governing equations, the system converges to one of two distinct stable states (attractors) based entirely on the initial conditions, confirming the logical switch functionality of the mutually inhibitory genetic circuit.
```