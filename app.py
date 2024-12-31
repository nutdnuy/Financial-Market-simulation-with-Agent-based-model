import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit UI
st.title("Market Simulation with Streamlit")

# UI for Market Setup
P0 = st.sidebar.number_input("Initial Price", value=100)
Pf = st.sidebar.number_input("Fair Value", value=120)
n_steps = st.sidebar.number_input("Number of Time Steps", value=100, min_value=1)
total_shares = st.sidebar.number_input("Total Shares Available for Trading", value=1000, min_value=1)

# UI for Agents Setup
n_agents = st.sidebar.number_input("Number of Agents", value=100, min_value=1)
agent_types = ['technical', 'fundamental', 'hft', 'program_technical', 'passive']
agents = {}

for agent_type in agent_types:
    st.sidebar.subheader(f"{agent_type.capitalize()} Agents")
    count = st.sidebar.number_input(f"Number of {agent_type.capitalize()} Agents", value=int(n_agents * 0.2), key=f"{agent_type}_count")
    position = st.sidebar.number_input(f"Initial Position for {agent_type.capitalize()}", value=100, key=f"{agent_type}_position")
    wealth = st.sidebar.number_input(f"Initial Wealth for {agent_type.capitalize()}", value=15000, key=f"{agent_type}_wealth")
    short_limit = st.sidebar.number_input(f"Short Limit for {agent_type.capitalize()}", value=20, key=f"{agent_type}_short_limit")
    agents[agent_type] = {'count': count, 'position': position, 'wealth': wealth, 'short_limit': short_limit}




# Check if the trade is valid based on current wealth
def is_valid_trade(agent_type, trade_volume, current_price):
    cost = trade_volume * current_price
    # Check if selling more than allowed in short sale or if buying more than wealth permits
    if trade_volume < 0:  # Selling
        max_sell = agents[agent_type]['position'] + agents[agent_type]['short_limit']
        return max(trade_volume, -max_sell), True
    else:  # Buying
        if agents[agent_type]['wealth'] >= cost:
            return trade_volume, True
        else:  # Adjust trade volume to what can be afforded
            max_buy = agents[agent_type]['wealth'] // current_price
            return max_buy, False
    return 0, False

# Update wealth and position for each agent type
def update_wealth_and_position(agent_type, trade_volume, current_price):
    valid_trade_volume, _ = is_valid_trade(agent_type, trade_volume, current_price)
    agents[agent_type]['position'] += valid_trade_volume
    agents[agent_type]['wealth'] -= valid_trade_volume * current_price

# Randomized agent behavior definitions with trade validation
def trade_randomly(agent_behavior):
    def wrapper(*args, **kwargs):
        if np.random.rand() > 0.5:  # 50% chance to act
            return agent_behavior(*args, **kwargs)
        else:
            return 0  # No action
    return wrapper

@trade_randomly
def trade_technical(price_history, agent_type):
    if len(price_history) < 2:
        return 0
    suggested_trade = np.random.choice([1, -1])  # Buy or sell with randomness
    trade_volume, _ = is_valid_trade(agent_type, suggested_trade, price_history[-1])
    return trade_volume

@trade_randomly
def trade_fundamental(current_price, fair_value, agent_type):
    suggested_trade = 1 if current_price < fair_value else -1  # Buy if below fair, sell if above
    trade_volume, _ = is_valid_trade(agent_type, suggested_trade, current_price)
    return trade_volume

@trade_randomly
def trade_hft(price_history, agent_type):
    suggested_trade = np.random.choice([-1, 0, 1])  # Random action
    trade_volume, _ = is_valid_trade(agent_type, suggested_trade, price_history[-1])
    return trade_volume

def trade_passive(agent_type, current_price):
    suggested_trade = 1  # Always buy
    trade_volume, _ = is_valid_trade(agent_type, suggested_trade, current_price)
    return trade_volume



# Simplified trading strategy functions
def trade_technical(prices, agent_type):
    if len(prices) < 2:
        return 0
    # Example strategy: buy (1) if price is increasing, sell (-1) if decreasing
    return 1 if prices[-1] > prices[-2] else -1

def trade_fundamental(current_price, fair_value, agent_type):
    # Buy (1) if price below fair value, otherwise sell (-1)
    return 1 if current_price < fair_value else -1

def trade_hft(prices, agent_type):
    # Example HFT strategy: random choice
    return np.random.choice([-1, 1])

def trade_passive(agent_type, current_price):
    # Passive strategy: always buy (1)
    return 1

# Update wealth and position for each agent type
def update_wealth_and_position(agents, agent_type, trade_vol, current_price):
    # This function should be expanded to accurately adjust wealth and position
    # Here is a simplified version
    agent = agents[agent_type]
    agent['position'] += trade_vol
    # Assuming each trade is one unit of currency for simplicity
    agent['wealth'] -= trade_vol * current_price

# Updated simulate_market function to return final wealth and positions
def simulate_market(n_steps, P0, Pf, total_shares, agents):
    prices = [P0]
    volume = []

    for step in range(n_steps):
        demand = 0
        for agent_type in agents:
            trade_vol = 0
            if agent_type in ['technical', 'program_technical']:
                trade_vol = trade_technical(prices, agent_type) * np.random.randint(1, agents[agent_type]['count'] + 1)
            elif agent_type == 'fundamental':
                trade_vol = trade_fundamental(prices[-1], Pf, agent_type) * np.random.randint(1, agents[agent_type]['count'] + 1)
            elif agent_type == 'hft':
                trade_vol = trade_hft(prices, agent_type) * np.random.randint(1, agents[agent_type]['count'] + 1)
            elif agent_type == 'passive':
                trade_vol = trade_passive(agent_type, prices[-1]) * agents[agent_type]['count']
            
            update_wealth_and_position(agents, agent_type, trade_vol, prices[-1])
            demand += trade_vol

        price_change = demand * 0.1
        new_price = prices[-1] + price_change
        prices.append(new_price)
        volume.append(abs(demand))

    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].plot(prices, label="Price")
    ax[0].plot([0, n_steps], [Pf, Pf], 'k--', label="Fair Value")
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Price")
    ax[0].legend()

    ax[1].bar(range(n_steps), volume, label="Volume")
    ax[1].set_xlabel("Time")
    ax[1].set_ylabel("Volume")
    ax[1].legend()

    plt.tight_layout()
    
    # Collecting final wealth and position for each agent type
    final_stats = {agent_type: {"final_position": agent["position"], "final_wealth": agent["wealth"]} for agent_type, agent in agents.items()}
    
    return fig, final_stats



# Assuming UI code for inputs is defined here as before

# Button to run simulation and display results
if st.button('Run Simulation'):
    fig, final_stats = simulate_market(n_steps, P0, Pf, total_shares, agents)
    st.pyplot(fig)
    
    # Displaying final wealth and position for each agent type
    st.subheader("Final Wealth and Position for Each Agent Type")
    for agent_type, stats in final_stats.items():
        st.write(f"{agent_type.capitalize()} Agents - Final Position: {stats['final_position']}, Final Wealth: {stats['final_wealth']}")
