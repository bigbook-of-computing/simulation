# Source: Simulation/chapter-7/essay.md -- Block 1

# Code snippet to illustrate the core Velocity-Verlet loop (1D)
# Based on the implementation in the provided files.

# F = force(r)
# a = F / m
    
# # Step 1: update position
# r_new = r + v*dt + 0.5*a*dt**2
    
# # Step 2: compute new force
# F_new = force(r_new)
# a_new = F_new / m
    
# # Step 3: update velocity
# v_new = v + 0.5*(a + a_new)*dt

# # Bookkeeping
# r, v = r_new, v_new
