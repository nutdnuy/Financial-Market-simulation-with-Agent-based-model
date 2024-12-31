import numpy as np
import matplotlib.pyplot as plt

def simulate_market(n_steps, P0, Pf, total_shares, agents):
    prices = [P0]
    volume = []

    for step in range(n_steps):
        demand = 0
        for agent_type in agents:
            trade_vol = 0
            if agent_type in ['technical', 'program_technical']:
                trade_vol = agents[agent_type]['trade_func'](prices, agent_type) * np.random.randint(1, agents[agent_type]['count'] + 1)
            elif agent_type == 'fundamental':
                trade_vol = agents[agent_type]['trade_func'](prices[-1], Pf, agent_type) * np.random.randint(1, agents[agent_type]['count'] + 1)
            elif agent_type == 'hft':
                trade_vol = agents[agent_type]['trade_func'](prices, agent_type) * np.random.randint(1, agents[agent_type]['count'] + 1)
            elif agent_type == 'passive':
                trade_vol = agents[agent_type]['trade_func'](agent_type, prices[-1]) * agents[agent_type]['count']

            agents[agent_type]['update_func'](agent_type, trade_vol, prices[-1])
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
    return fig

