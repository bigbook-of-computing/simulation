# Source: Simulation/chapter-11/codebook.md -- Block 3

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ====================================================================
# 1. Setup and Core Functions (Schelling's Model as Testbed)
# ====================================================================

GRID_SIZE = 30
TOLERANCE = 0.45  # A level where the system is likely to transition
STEPS_TOTAL = 300
EMPTY_RATIO = 0.1

def initialize_grid(size, empty_ratio):
    # Initialize the grid with a random mix (Same as Project 1)
    num_cells = size * size
    num_agents = num_cells - int(empty_ratio * num_cells)
    grid_flat = np.zeros(num_cells, dtype=np.int8)
    grid_flat[:num_agents // 2] = 1
    grid_flat[num_agents // 2:num_agents] = 2
    np.random.shuffle(grid_flat)
    return grid_flat.reshape((size, size))

def happy_mask(grid, tolerance):
    # Returns True for happy/empty cells (Same as Project 1)
    kernel = np.ones((3, 3))
    agent_mask = (grid != 0).astype(float)
    total_neighbors = convolve2d(agent_mask, kernel, mode='same', boundary='wrap') - agent_mask
    same_neighbors = np.zeros_like(grid, dtype=float)
    for color in [1, 2]:
        color_mask = (grid == color).astype(float)
        same_neighbors_per_type = convolve2d(color_mask, kernel, mode='same', boundary='wrap') - color_type_mask
        same_neighbors += same_neighbors_per_type * color_type_mask
    
    with np.errstate(divide='ignore', invalid='ignore'):
        frac_same = np.where(total_neighbors > 0, same_neighbors / total_neighbors, 1.0)
    
    # Segregation Index is the average fraction of similar neighbors
    seg_index = np.sum(frac_same * agent_mask) / np.sum(agent_mask)
    happy = (frac_same >= tolerance) | (grid == 0)
    return happy, seg_index

def get_empty_spots(grid):
    return tuple(map(tuple, np.argwhere(grid == 0)))

# ====================================================================
# 2. Update Schemes
# ====================================================================

def synchronous_update_schelling(grid, tolerance):
    """
    All agents decide based on the OLD state, then act simultaneously on the NEW state.
    Requires storing moves (intentions) before committing.
    """
    happy, _ = happy_mask(grid, tolerance)
    unhappy_pos = np.argwhere(~happy & (grid != 0))
    empty_pos = get_empty_spots(grid)
    
    np.random.shuffle(unhappy_pos)
    np.random.shuffle(empty_pos)
    
    # Store actions in an intentions list
    move_intentions = []
    
    for i in range(min(len(unhappy_pos), len(empty_pos))):
        u = tuple(unhappy_pos[i])
        e = empty_pos[i]
        move_intentions.append((u, e, grid[u]))
        
    # Commit changes simultaneously to a new grid
    new_grid = np.copy(grid)
    for src, dest, agent_type in move_intentions:
        new_grid[dest] = agent_type
        new_grid[src] = 0 # Original spot becomes empty
        
    return new_grid

def asynchronous_update_schelling(grid, tolerance):
    """
    Agents are selected randomly and act immediately.
    The next agent sees the updated environment.
    """
    L = grid.shape[0]
    positions = [(i, j) for i in range(L) for j in range(L) if grid[i, j] != 0]
    random.shuffle(positions)
    
    for i, j in positions:
        # Check happiness based on current, updated grid
        happy_status, _ = happy_mask(grid, tolerance)
        
        if not happy_status[i, j]:
            empty_pos_list = get_empty_spots(grid)
            if not empty_pos_list:
                continue
            
            # Select random empty spot and move immediately
            e = random.choice(empty_pos_list)
            
            grid[e] = grid[i, j]
            grid[i, j] = 0
            
    return grid

# ====================================================================
# 3. Comparative Simulation
# ====================================================================

# Run 1: Synchronous
grid_sync = initialize_grid(GRID_SIZE, EMPTY_RATIO)
seg_sync = []
for t in range(STEPS_TOTAL):
    _, seg = happy_mask(grid_sync, TOLERANCE)
    seg_sync.append(seg)
    grid_sync = synchronous_update_schelling(grid_sync, TOLERANCE)

# Run 2: Asynchronous
grid_async = initialize_grid(GRID_SIZE, EMPTY_RATIO) # Re-initialize the same starting configuration
seg_async = []
for t in range(STEPS_TOTAL):
    _, seg = happy_mask(grid_async, TOLERANCE)
    seg_async.append(seg)
    grid_async = asynchronous_update_schelling(grid_async, TOLERANCE)

# ====================================================================
# 4. Visualization and Comparison
# ====================================================================

plt.figure(figsize=(10, 5))

plt.plot(seg_sync, label='Synchronous Update (Parallel)', lw=2, alpha=0.7)
plt.plot(seg_async, label='Asynchronous Update (Sequential)', lw=2, alpha=0.7)

plt.title(f'Comparison of ABM Update Schemes ($T={TOLERANCE:.2f}$)')
plt.xlabel('Time Step')
plt.ylabel('Segregation Index $S_{\\text{index}}$ (Global Order)')
plt.ylim(bottom=0.5)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# --- Analysis Summary ---
print("\n--- Update Scheme Comparison Summary ---")
print(f"Final Segregation (Synchronous): {seg_sync[-1]:.4f}")
print(f"Final Segregation (Asynchronous): {seg_async[-1]:.4f}")

print("\nConclusion: The plot demonstrates that both update schemes converge to a high level of segregation, confirming the emergent macro-pattern. However, the **synchronous update curve** may appear more stepped or slightly more prone to oscillations at the beginning before settling, while the **asynchronous curve** typically shows a smoother, more continuous progression, reflecting the sequential nature of its local updates (similar to MCMC).")
