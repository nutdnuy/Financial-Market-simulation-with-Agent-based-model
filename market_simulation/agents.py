import numpy as np

def create_agents(n_agents, agent_types):
    agents = {}
    for agent_type in agent_types:
        count = int(n_agents * 0.2)
        position = 100
        wealth = 15000
        short_limit = 20
        agents[agent_type] = {
            'count': count,
            'position': position,
            'wealth': wealth,
            'short_limit': short_limit,
            'trade_func': globals()[f'trade_{agent_type}'],
            'update_func': update_wealth_and_position
        }
    return agents

def trade_technical(price_history, agent_type):
    return np.random.choice([-1, 1])

def trade_fundamental(current_price, fair_value, agent_type):
    return 1 if current_price < fair_value else -1

def trade_hft(price_history, agent_type):
    return np.random.choice([-1, 1])

def trade_passive(agent_type, current_price):
    return 1

def update_wealth_and_position(agent_type, trade_volume, current_price):
    # Update logic for positions and wealth
    pass
