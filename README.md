Market Simulation

A Python-based agent-based market simulation that models the interactions of various agent types and their impact on market prices over time. The project provides a framework to study the dynamics of a trading market with customizable parameters for agents and trading strategies.

Features

Agent Types:

Technical

Fundamental

High-Frequency Trading (HFT)

Programmatic Technical

Passive Investors

Customizable Parameters:

Initial price, fair value, and total shares available for trading.

Number of agents and specific configurations for each agent type (e.g., wealth, position, short limits).

Simulation:

Models market price evolution based on the aggregated actions of agents.

Visualizes market prices and trading volume over time.

Requirements

Python 3.7+

numpy

matplotlib

Installation

Clone the repository:

git clone https://github.com/your-username/market-simulation.git
cd market-simulation

Install the required packages:

pip install -r requirements.txt

Usage

Run the simulation:

python market_simulation.py

Observe the market dynamics:

A plot of market prices and trading volume will be displayed.

Final wealth and positions for each agent type will be printed in the console.

File Structure

market_simulation.py: Main simulation script.

README.md: Project documentation (this file).

Example Output

Price and Volume Graphs: A graph showing market price changes over time and trading volume.

Agent Statistics: Console output of final wealth and positions for each agent type.

Contributing

Contributions are welcome! Please follow these steps:

Fork the repository.

Create a feature branch:

git checkout -b feature-name

Commit your changes:

git commit -m "Description of feature"

Push to your fork:

git push origin feature-name

Submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments

This project was inspired by the need to explore and analyze market dynamics using agent-based modeling.
