# Source: Simulation/chapter-12/essay.md -- Block 1

def santa_fe_asm_simulation(n_agents, n_steps, P_fund, alpha):
    """
    Santa Fe Artificial Stock Market simulation.
    
    Parameters:
    - n_agents: Number of traders
    - n_steps: Simulation time steps
    - P_fund: Fundamental value of asset
    - alpha: Price sensitivity to order flow
    """
    # Initialize agents (70% fundamentalists, 30% chartists)
    agents = []
    for i in range(n_agents):
        agent_type = 'fundamentalist' if i < 0.7 * n_agents else 'chartist'
        agents.append({'type': agent_type, 'profit': 0.0, 'position': 0})
    
    # Initialize price and history
    price = P_fund
    price_history = [price]
    returns = []
    
    for t in range(n_steps):
        # Phase 1: Agent decisions (based on current price)
        order_flow = 0
        for agent in agents:
            if agent['type'] == 'fundamentalist':
                # Buy if undervalued, sell if overvalued
                action = 1 if price < P_fund else -1
            else:  # chartist
                # Follow momentum (simple trend)
                if len(price_history) > 5:
                    momentum = price_history[-1] - price_history[-5]
                    action = 1 if momentum > 0 else -1
                else:
                    action = 0
            
            order_flow += action
            agent['position'] = action
        
        # Phase 2: Endogenous price update
        price_new = price + alpha * order_flow / n_agents
        returns.append((price_new - price) / price)
        price = price_new
        price_history.append(price)
        
        # Phase 3: Agent adaptation (profit-based strategy switching)
        for agent in agents:
            agent['profit'] += agent['position'] * returns[-1]
        
        # Strategy switching based on relative profitability (simplified)
        if t % 20 == 0:  # Periodic evaluation
            fund_profit = np.mean([a['profit'] for a in agents if a['type'] == 'fundamentalist'])
            chart_profit = np.mean([a['profit'] for a in agents if a['type'] == 'chartist'])
            
            # Agents switch to more profitable strategy
            if chart_profit > fund_profit:
                # Some fundamentalists become chartists
                for agent in agents[:int(0.1 * n_agents)]:
                    if agent['type'] == 'fundamentalist':
                        agent['type'] = 'chartist'
    
    return price_history, returns
