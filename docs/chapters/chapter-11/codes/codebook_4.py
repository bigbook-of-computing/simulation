# Source: Simulation/chapter-11/codebook.md -- Block 4

# ====================================================================
# 1. System Setup and Pillars Definition
# ====================================================================

# --- PILLAR 1: AGENTS (Actors) ---
# We define the state vector for the two types of agents
# Note: Grass (Prey) may be treated as a consumable resource in the environment, 
# or as an agent if it has complex behaviors (e.g., self-propagating). 
# We define both as explicit agents for ABM consistency.

class GrassAgent:
    """Represents a Prey item on the grid."""
    # State Vector Components:
    STATUS = {
        'age': 0,           # Time until reproduction (Reproduction Rule)
        'type': 'prey',     
        'is_alive': True
    }
    
    # Rule Logic:
    def decide_and_act(self, neighborhood, environment):
        if self.STATUS['age'] >= 5: # Reproduce after 5 steps
            # Act 1: Find an empty spot to create a new Grass agent
            pass 
        # Act 2: Grow old
        self.STATUS['age'] += 1
        
class FoxAgent:
    """Represents a Predator on the grid."""
    # State Vector Components:
    STATUS = {
        'energy': 10,       # Consumed energy (Death/Reproduction Rule)
        'age': 0,
        'type': 'predator',
        'is_alive': True
    }
    
    # Rule Logic:
    def decide_and_act(self, neighborhood, environment):
        # Step 1: Sense - Find nearest Grass in neighborhood
        grass_nearby = [a for a in neighborhood if a.STATUS['type'] == 'prey']
        
        # Step 2: Decide - Prioritize Eating, then Reproduction, then Moving
        if grass_nearby:
            # Action: Eat -> Gain energy, Grass dies
            self.STATUS['energy'] += 5
            grass_nearby[0].STATUS['is_alive'] = False # Modify neighbor state
            self.move_towards(grass_nearby[0].position)
            return 'Eat'
        
        elif self.STATUS['energy'] >= 20:
            # Action: Reproduce -> Lose energy, create new Fox
            self.STATUS['energy'] -= 10
            return 'Reproduce'
            
        elif self.STATUS['energy'] <= 0:
            # Action: Death
            self.STATUS['is_alive'] = False
            return 'Die'
        
        else:
            # Action: Move randomly and lose energy
            self.STATUS['energy'] -= 1
            self.move_randomly()
            return 'Move'

# --- PILLAR 2: ENVIRONMENT (The Stage) ---
# The environment is a simple 2D Grid with wrapping (PBCs implied).
# Environment State: A list/array storing all active Agent objects, and the Grid itself.
ENVIRONMENT = {
    'grid_size': 50,
    'time_step': 0,
    'active_agents': [] # List of all GrassAgent and FoxAgent objects
}

# ====================================================================
# 2. Rule Logic Outline (The Feedback Loop)
# ====================================================================

# The core feedback loop is the Predator-Prey dynamic:
# Predation (Micro) -> Population Fluctuation (Macro) -> Rule Change (Micro)

print("--- Predator-Prey ABM: Core Feedback Loop Outline ---")

print("\n1. Predator/Prey Interaction (Local Rule)")
print("   - Action: Fox (Predator) moves to position of Grass (Prey) and consumes it.")
print("   - This is a local, heterogeneous rule based on immediate proximity.")

print("\n2. Emergent Population Dynamics (Macro Feedback)")
print("   - If Fox population is HIGH: Grass population LOW -> Fox energy LOW.")
print("   - If Fox energy is LOW: Fox reproduction rate DROPS, Fox death rate RISES.")
print("   - Result: Fox population crashes, allowing Grass population to recover, driving the emergent Lotka-Volterra cycle.")

print("\n3. Computational Flow (Asynchronous Update Implied)")
print("   - Agent updates are sequential: A Fox eats a piece of Grass immediately, and the next Fox in the update list will sense one less piece of Grass nearby.")

print("\nConclusion: The complexity of emergent population cycles is governed by the simple, decentralized energy conservation rules (Fox energy balance and Grass reproduction rate) and the local interaction pillar (eating in the neighborhood).")
