# Source: Simulation/chapter-9/essay.md -- Block 1

def crank_nicolson_american_option(S_grid, t_grid, r, sigma, K, option_type='put'):
    """
    Solve American option pricing using Crank-Nicolson FDM with early exercise.
    
    Parameters:
    - S_grid: Stock price grid (spatial discretization)
    - t_grid: Time grid (temporal discretization, backward from T to 0)
    - r: Risk-free rate
    - sigma: Volatility
    - K: Strike price
    - option_type: 'put' or 'call'
    """
    M = len(S_grid) - 1  # Number of spatial steps
    N = len(t_grid) - 1  # Number of time steps
    dS = S_grid[1] - S_grid[0]
    dt = t_grid[1] - t_grid[0]
    
    # Initialize option value at maturity (terminal condition)
    if option_type == 'put':
        V = np.maximum(K - S_grid, 0)  # Intrinsic value at expiration
    else:
        V = np.maximum(S_grid - K, 0)
    
    # Build tridiagonal matrices A and B for Crank-Nicolson
    alpha = 0.25 * dt * (sigma**2 * (np.arange(M+1)**2) - r * np.arange(M+1))
    beta = -0.5 * dt * (sigma**2 * (np.arange(M+1)**2) + r)
    gamma = 0.25 * dt * (sigma**2 * (np.arange(M+1)**2) + r * np.arange(M+1))
    
    # March backward in time
    for n in range(N):
        # Solve A * V_new = B * V_old (tridiagonal system)
        V_new = solve_tridiagonal_system(A, B, V)
        
        # Apply early exercise constraint (American option)
        if option_type == 'put':
            V_intrinsic = np.maximum(K - S_grid, 0)
        else:
            V_intrinsic = np.maximum(S_grid - K, 0)
        
        V = np.maximum(V_new, V_intrinsic)  # Choose max of hold vs exercise
    
    return V  # Option value at t=0 for all stock prices
