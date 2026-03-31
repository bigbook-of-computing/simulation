# Source: Simulation/chapter-13/codebook.md -- Block 2

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx # For plotting the conceptual network structure

# ====================================================================
# 1. Setup Network Rules (3-Gene System with Negative Feedback)
# ====================================================================

# Rule: A -> B, B -> C, C -> NOT A (Creating a negative feedback cycle)
# This design is prone to oscillation (limit cycles).

# Boolean Logic Functions
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

# ====================================================================
# 2. Simulation: State Space Trajectory
# ====================================================================

MAX_STEPS = 15 # Max steps to find the attractor
# Initial State (Arbitrary starting point)
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

# Convert history to DataFrame for plotting
df_history = pd.DataFrame(history, columns=['Gene A', 'Gene B', 'Gene C'])
df_history['Time'] = df_history.index

# ====================================================================
# 3. Visualization
# ====================================================================

# 1. Time Series Plot (to visualize the oscillation)
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

# 2. State Space Plot (Conceptual Graph)
# Define the graph structure for visualization
G = nx.DiGraph()
for t in range(len(history) - 1):
    src = str(list(history[t]))
    dest = str(list(history[t+1]))
    G.add_edge(src, dest, weight=t)

# Use spring layout for visualization (optional)
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(6, 6))
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
nx.draw_networkx_labels(G, pos, font_size=8)
plt.title('Attractor Cycle in State Space')
plt.axis('off')
plt.show()


# --- Analysis Summary ---
print("\n--- Boolean Network Attractor Analysis ---")
attractor_cycle = df_history.iloc[history.index(history[-1]) - 1:]
print(f"Attractor Cycle Length: {len(attractor_cycle)} steps")
print("\nAttractor Cycle States (Steady State):")
print(attractor_cycle.iloc[:-1].to_markdown(index=False))

print("\nConclusion: The simulation confirms that the finite-state network converges to a stable **limit cycle attractor** (a repeating sequence of states). Biologically, this attractor represents the final, stable **cell identity** (e.g., muscle cell or neuron) computed by the gene circuit.")
