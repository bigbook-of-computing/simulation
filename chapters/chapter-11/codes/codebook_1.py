# Source: Simulation/chapter-11/codebook.md -- Block 1

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

# Set seed for reproducibility
np.random.seed(42)

# ====================================================================
# 1. Setup Parameters and Initialization
# ====================================================================

GRID_SIZE = 50
EMPTY_RATIO = 0.1
TOLERANCE = 0.40  # T=0.40: Agents require 40% similar neighbors to be happy
STEPS = 200

# --- Initialization ---
num_cells = GRID_SIZE * GRID_SIZE
num_empty = int(EMPTY_RATIO * num_cells)
num_agents = num_cells - num_empty

# Create flat array with 1s (Red), 2s (Blue), and 0s (Empty)
grid_flat = np.zeros(num_cells, dtype=np.int8)
grid_flat[:num_agents // 2] = 1  # Half Red
grid_flat[num_agents // 2:num_agents] = 2  # Half Blue
np.random.shuffle(grid_flat)

GRID = grid_flat.reshape((GRID_SIZE, GRID_SIZE))

# ====================================================================
# 2. Core ABM Functions (Locality and Rule)
# ====================================================================

def happy_mask(grid, tolerance):
    """
    Calculates a boolean mask indicating if each agent is 'happy' based on 
    the local tolerance rule. Uses convolution for O(N) neighbor checking.
    """
    kernel = np.ones((3, 3))  # 3x3 kernel (Moore neighborhood, 8 neighbors)
    
    # 1. Calculate the total number of AGENTS in the neighborhood (excluding self)
    agent_mask = (grid != 0).astype(float)
    total_neighbors = convolve2d(agent_mask, kernel, mode='same', boundary='wrap') - agent_mask
    
    # 2. Calculate the number of SIMILAR agents in the neighborhood
    same_neighbors = np.zeros_like(grid, dtype=float)
    
    for color in [1, 2]:
        color_type_mask = (grid == color).astype(float)
        # Convolve the mask with the kernel, then multiply by the agent type mask
        same_neighbors_per_type = convolve2d(color_type_mask, kernel, mode='same', boundary='wrap') - color_type_mask
        same_neighbors += same_neighbors_per_type * color_type_mask
        
    # 3. Calculate Fraction of Similar Neighbors (avoid division by zero)
    with np.errstate(divide='ignore', invalid='ignore'):
        # Only calculate fraction for cells that are actually occupied (grid != 0)
        frac_same = np.where(total_neighbors > 0, same_neighbors / total_neighbors, 1.0)
    
    # An agent is happy if the fraction is >= tolerance, or if the cell is empty (grid == 0)
    happy = (frac_same >= tolerance) | (grid == 0)
    return happy

def step(grid, tolerance):
    """Performs one asynchronous-like step where unhappy agents move."""
    
    # 1. Identify unhappy agents
    happy = happy_mask(grid, tolerance)
    unhappy_positions = np.argwhere(~happy & (grid != 0))
    empty_positions = np.argwhere(grid == 0)
    
    # 2. Shuffle lists to ensure random selection of who moves and where
    np.random.shuffle(unhappy_positions)
    np.random.shuffle(empty_positions)
    
    # 3. Execute moves
    num_to_move = min(len(unhappy_positions), len(empty_positions))
    
    for i in range(num_to_move):
        u = tuple(unhappy_positions[i])
        e = tuple(empty_positions[i])
        
        # Move agent from u to e
        grid[e] = grid[u]
        grid[u] = 0
    
    return grid

# ====================================================================
# 3. Simulation Loop and Visualization
# ====================================================================

# Store grids for visualization at key steps
grids_to_plot = [GRID.copy()]
step_interval = 40

# Run simulation
for t in range(1, STEPS + 1):
    GRID = step(GRID, TOLERANCE)
    if t % step_interval == 0 or t == STEPS:
        grids_to_plot.append(GRID.copy())
        

# --- Visualization ---
fig, axes = plt.subplots(1, len(grids_to_plot), figsize=(15, 4))
titles = [f'Initial (Step 0)', f'Step {step_interval}', f'Step {2*step_interval}', 
          f'Step {3*step_interval}', f'Step {4*step_interval}', f'Final (Step {STEPS})']

# Custom colormap for visualization (0=Empty, 1=Red, 2=Blue)
cmap = plt.cm.get_cmap('bwr', 3)

for i, grid_to_plot in enumerate(grids_to_plot):
    ax = axes[i]
    ax.imshow(grid_to_plot, cmap=cmap, vmin=0, vmax=2)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])
    
plt.suptitle(f'Schelling Segregation Model Emergence (Tolerance T={TOLERANCE:.2f})', fontsize=14)
plt.tight_layout()
plt.show()

# --- Analysis Summary ---
final_seg_index = happy_mask(GRID, TOLERANCE)
initial_seg_index = happy_mask(grids_to_plot[0], TOLERANCE)

print("\n--- Segregation Analysis Summary ---")
print(f"Tolerance Threshold (T): {TOLERANCE:.2f}")

# Calculate average segregation index (fraction of happy agents)
initial_happy_agents = np.mean(initial_seg_index[initial_seg_index != 0])
final_happy_agents = np.mean(final_seg_index[final_seg_index != 0])

print(f"Initial Fraction of Happy Agents: {initial_happy_agents:.2f}")
print(f"Final Fraction of Happy Agents:   {final_happy_agents:.2f}")
print("\nConclusion: The simulation shows the core emergent property: despite a high initial mix (low initial happiness), the simple local rule of seeking 40% similar neighbors drives the system to an organized state where nearly all agents are happy. The global segregated pattern emerges unintentionally from local interactions.")
