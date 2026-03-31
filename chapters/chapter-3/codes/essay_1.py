# Source: Simulation/chapter-3/essay.md -- Block 1

# Metropolis update for a single link variable U_mu(n)
def metropolis_link_update(U, mu, n, beta_gauge, epsilon):
    # Compute staple sum Sigma_mu(n)
    Sigma = compute_staple(U, mu, n)
    
    # Current local action
    S_old = -beta_gauge / (2*N) * Re(Tr(U[mu,n] @ Sigma))
    
    # Propose new link: U' = delta_U * U[mu,n]
    delta_U = random_SU_N_near_identity(epsilon)  # small random matrix
    U_prime = delta_U @ U[mu,n]
    
    # New local action
    S_new = -beta_gauge / (2*N) * Re(Tr(U_prime @ Sigma))
    
    # Metropolis acceptance
    Delta_S = S_new - S_old
    if random_uniform(0,1) < exp(-Delta_S):
        U[mu,n] = U_prime  # accept
    # else reject and keep U[mu,n] unchanged
