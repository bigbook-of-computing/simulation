# Source: Simulation/chapter-4/essay.md -- Block 1

# Monte Carlo pricing for path-dependent options
def monte_carlo_option_price(S0, r, sigma, T, N, M, payoff_func):
    """
    S0: initial asset price
    r: risk-free rate
    sigma: volatility
    T: time to maturity
    N: number of time steps
    M: number of simulation paths
    payoff_func: function computing payoff from path
    """
    dt = T / N
    drift = (r - 0.5 * sigma**2) * dt
    diffusion = sigma * sqrt(dt)
    
    payoffs = []
    for m in range(M):
        # Simulate one path
        S = S0
        path = [S]
        for k in range(N):
            Z = random_normal(0, 1)
            S = S * exp(drift + diffusion * Z)
            path.append(S)
        
        # Compute payoff for this path
        h_m = payoff_func(path)
        payoffs.append(h_m)
    
    # Estimate option price
    V_hat = exp(-r * T) * mean(payoffs)
    std_error = exp(-r * T) * std(payoffs) / sqrt(M)
    
    return V_hat, std_error
