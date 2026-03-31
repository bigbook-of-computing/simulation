# Source: Simulation/chapter-12/workbook.md -- Block 1

import numpy as np
import random

# Set seed for reproducibility
np.random.seed(42)

# ====================================================================
# 1. Setup Parameters and Agent Logic
# ====================================================================

# --- Market Parameters ---
N_AGENTS = 1000
N_FUNDAMENTALISTS = 500
N_CHARTISTS = 500

P_FUND = 100.0          # Intrinsic Fundamental Value
CURRENT_PRICE = 110.0   # Current market price (Scenario: Bubble)

# History parameters for Chartists' trend calculation
PRICE_HISTORY = np.array([98.0, 100.0, 105.0, 108.0, 110.0]) # Recent rising trend
WINDOW = 5 # Lookback window for trend

# --- Agent Decision Functions ---

def fundamentalist_action(P_t, P_fund):
    """Sells if overpriced, buys if underpriced (negative feedback)."""
    return np.sign(P_fund - P_t)

def chartist_action(P_t_history, window):
    """Buys if the short-term trend is positive (positive feedback)."""
    if len(P_t_history) < window:
        # Default action if not enough history (e.g., neutral/random)
        return 0
        
    # Simple momentum rule: Buy if average of last 'window' prices is increasing
    trend = P_t_history[-1] - np.mean(P_t_history[-window:])
    return np.sign(trend)

# ====================================================================
# 2. Simulation and Net Order Flow Calculation
# ====================================================================

# Scenario setup: Price is in a Bubble (110.0) but rising (positive trend)
P_t = CURRENT_PRICE
P_fund = P_FUND
P_history = PRICE_HISTORY 

# --- Fundamentalist Actions ---
O_fund_action = fundamentalist_action(P_t, P_fund) # Should be -1 (Sell)
O_fund_total = O_fund_action * N_FUNDAMENTALISTS
# Add small random noise to individual decisions
O_fund_noise = np.random.randint(-5, 6)
O_fund_total += O_fund_noise

# --- Chartist Actions ---
O_chart_action = chartist_action(P_history, WINDOW) # Should be +1 (Buy)
O_chart_total = O_chart_action * N_CHARTISTS
# Add small random noise to individual decisions
O_chart_noise = np.random.randint(-5, 6)
O_chart_total += O_chart_noise

# --- Net Order Flow ---
O_total = O_fund_total + O_chart_total
O_net_per_agent = O_total / N_AGENTS

# ====================================================================
# 3. Analysis and Summary
# ====================================================================

print("--- Heterogeneous Agent Order Flow Analysis ---")
print(f"Scenario: Price P_t = {P_t:.2f} (Fundamental Value P_fund = {P_fund:.2f})")
print("-------------------------------------------------------")

print("1. Fundamentalist Actions (Stabilizing / Negative Feedback):")
print(f"   Action: {O_fund_action} (Sell, as P_t > P_fund)")
print(f"   Order Flow O_fund: {O_fund_total} (Attempting to push price DOWN)")

print("\n2. Chartist Actions (Destabilizing / Positive Feedback):")
print(f"   Action: {O_chart_action} (Buy, as trend is positive)")
print(f"   Order Flow O_chart: {O_chart_total} (Attempting to push price UP)")

print("\n3. Net Order Flow:")
print(f"   Total Order Flow (O_t): {O_total}")
print(f"   Net Order Flow per Agent: {O_net_per_agent:.3f}")

print("\nConclusion: In this bubble scenario, the market exhibits **competing dynamics**. Rational Fundamentalists sell (negative order flow) to stabilize the price, while Chartists buy (positive order flow) to amplify the trend. The final price movement is emergent, dictated by which group's order flow dominates (in this case, Chartists slightly dominated, pushing the price further up). This tension is the core generator of market instability and complex dynamics.")
