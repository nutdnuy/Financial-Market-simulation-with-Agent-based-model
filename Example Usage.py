from market_simulation import simulate_market, create_agents

# Parameters
P0 = 100
Pf = 120
n_steps = 100
total_shares = 1000
agent_types = ['technical', 'fundamental', 'hft', 'passive', 'program_technical']
n_agents = 100

agents = create_agents(n_agents, agent_types)
simulate_market(n_steps, P0, Pf, total_shares, agents)
