# Source: Simulation/chapter-10/essay.md -- Block 1

def hodgkin_huxley_rk4(V_m, m, h, n, I_ext, dt, params):
    """
    4th-order Runge-Kutta integration for Hodgkin-Huxley model.
    
    Parameters:
    - V_m: Membrane voltage (mV)
    - m, h, n: Gating variables (dimensionless, 0 to 1)
    - I_ext: External stimulus current (μA/cm²)
    - dt: Time step (ms)
    - params: Dictionary with {C_m, g_Na_bar, g_K_bar, g_L, E_Na, E_K, E_L}
    
    Returns:
    - Updated state: (V_m_new, m_new, h_new, n_new)
    """
    def alpha_m(V): return 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
    def beta_m(V):  return 4.0 * np.exp(-(V + 65) / 18)
    
    def alpha_h(V): return 0.07 * np.exp(-(V + 65) / 20)
    def beta_h(V):  return 1.0 / (1 + np.exp(-(V + 35) / 10))
    
    def alpha_n(V): return 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
    def beta_n(V):  return 0.125 * np.exp(-(V + 65) / 80)
    
    def derivatives(V, m, h, n, I_ext):
        # Compute ionic currents
        I_Na = params['g_Na_bar'] * m**3 * h * (V - params['E_Na'])
        I_K  = params['g_K_bar'] * n**4 * (V - params['E_K'])
        I_L  = params['g_L'] * (V - params['E_L'])
        
        # Voltage derivative
        dV_dt = (I_ext - I_Na - I_K - I_L) / params['C_m']
        
        # Gating variable derivatives
        dm_dt = alpha_m(V) * (1 - m) - beta_m(V) * m
        dh_dt = alpha_h(V) * (1 - h) - beta_h(V) * h
        dn_dt = alpha_n(V) * (1 - n) - beta_n(V) * n
        
        return np.array([dV_dt, dm_dt, dh_dt, dn_dt])
    
    # RK4 stages
    S = np.array([V_m, m, h, n])
    k1 = dt * derivatives(S[0], S[1], S[2], S[3], I_ext)
    k2 = dt * derivatives(S[0] + 0.5*k1[0], S[1] + 0.5*k1[1], 
                          S[2] + 0.5*k1[2], S[3] + 0.5*k1[3], I_ext)
    k3 = dt * derivatives(S[0] + 0.5*k2[0], S[1] + 0.5*k2[1], 
                          S[2] + 0.5*k2[2], S[3] + 0.5*k2[3], I_ext)
    k4 = dt * derivatives(S[0] + k3[0], S[1] + k3[1], 
                          S[2] + k3[2], S[3] + k3[3], I_ext)
    
    # Update state
    S_new = S + (k1 + 2*k2 + 2*k3 + k4) / 6.0
    
    return S_new[0], S_new[1], S_new[2], S_new[3]
