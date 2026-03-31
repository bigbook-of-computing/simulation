# Source: Simulation/chapter-13/essay.md -- Block 1

def gray_scott_simulation(nx, ny, steps, Du, Dv, F, k, dt=1.0, dx=1.0):
    """
    Gray-Scott reaction-diffusion simulation for Turing patterns.
    
    Parameters:
    - nx, ny: Grid dimensions
    - steps: Number of time steps
    - Du, Dv: Diffusion coefficients (Dv > Du for patterns)
    - F: Feed rate (replenishment of u)
    - k: Kill rate (removal of v)
    - dt, dx: Time and space discretization
    """
    # Initialize concentrations with small random perturbations
    u = np.ones((nx, ny))  # Activator (start at 1)
    v = np.zeros((nx, ny))  # Inhibitor (start at 0)
    
    # Add small random seed in center to break symmetry
    u[nx//2-5:nx//2+5, ny//2-5:ny//2+5] = 0.5
    v[nx//2-5:nx//2+5, ny//2-5:ny//2+5] = 0.25
    
    # Discrete Laplacian kernel for diffusion
    laplacian_kernel = np.array([[0, 1, 0],
                                  [1, -4, 1],
                                  [0, 1, 0]]) / (dx**2)
    
    for step in range(steps):
        # Compute Laplacian (diffusion term) using convolution
        from scipy.ndimage import convolve
        laplacian_u = convolve(u, laplacian_kernel, mode='wrap')
        laplacian_v = convolve(v, laplacian_kernel, mode='wrap')
        
        # Reaction terms (Gray-Scott kinetics)
        reaction_u = -u * v**2 + F * (1 - u)
        reaction_v = u * v**2 - (F + k) * v
        
        # Update concentrations (Forward Euler)
        u += dt * (Du * laplacian_u + reaction_u)
        v += dt * (Dv * laplacian_v + reaction_v)
        
        # Optional: visualize every N steps
        if step % 100 == 0:
            # plot(v)  # v typically shows clearer patterns
            pass
    
    return u, v

# Example: Generate spots pattern
# u, v = gray_scott_simulation(256, 256, 10000, Du=0.16, Dv=0.08, F=0.035, k=0.065)
