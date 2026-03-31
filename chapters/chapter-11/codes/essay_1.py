# Source: Simulation/chapter-11/essay.md -- Block 1

def synchronous_abm_loop(agents, environment, n_steps):
    """
    Synchronous ABM simulation loop (all agents update in parallel).
    
    Parameters:
    - agents: List of agent objects with state and behavior methods
    - environment: Environment object (grid, network, continuous space)
    - n_steps: Number of simulation iterations
    """
    observables = []  # Store system-level measurements
    
    for step in range(n_steps):
        # Phase 1: SENSE & DECIDE (all agents perceive current state)
        intended_actions = []
        for agent in agents:
            neighbors = environment.get_neighbors(agent)
            action = agent.decide(agent.state, neighbors, environment)
            intended_actions.append(action)
        
        # Phase 2: ACT (execute all actions simultaneously)
        for agent, action in zip(agents, intended_actions):
            agent.execute(action)
            environment.update(agent, action)
        
        # Phase 3: MEASURE (compute global observables)
        observables.append(compute_order_parameter(agents, environment))
    
    return observables
