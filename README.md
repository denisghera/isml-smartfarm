# SmartFarm

SmartFarm is a simulation platform designed to model and automate various aspects of smart farming using modern technologies. The system enables efficient monitoring, data collection, and control over farm operations.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Strategy Analysis](#strategy-analysis)

## About

SmartFarm leverages intelligent algorithms to help simulate farmers managing their crops and resources. The system collects real-time data and provides actionable insights to optimize farm productivity.

## Features

- Simulates multiple farmers working on land
- Configurable number of farmers and territory size per farmer
- Adjustable number of weather agents (weather zones)
- Customizable planting and watering strategies, each affecting outcomes differently
- Real-time and historical data visualization
- Modular and extensible architecture

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/denisghera/isml-smartfarm.git
    cd isml-smartfarm
    ```

2. **Install dependencies:**
    ```bash
    pip install mesa==2.3.2
    ```

3. **Start the application:**
    ```bash
    python server.py
    ```

## Usage

1. **Parameter Setup:** Choose the number of farmers, territory size, weather zones, and strategies for planting and watering.
2. **Simulation Control:** 
    - **Reset:** Initializes the simulation with the selected parameters and randomizes farmer positions.
    - **Step:** Advances the simulation by one day.
    - **Start/Stop:** Runs or pauses the simulation in real time, with adjustable speed.
3. **Data Collection:** The system gathers data on resources, crops, and farmer actions.
4. **Visualization:** The dashboard displays real-time and historical data for analysis.

## Strategy Analysis

SmartFarm supports multiple **watering** and **planting** strategies, each impacting farm outcomes differently. Below is a structured comparison of the available strategies and their combined effects.

### Watering Strategies

- **Balanced:** Waters crops frequently, but avoiding spoilage, aiming for optimal growth and resource use.
- **Conserve:** Waters less frequently to minimize water usage, accepting some risk of lower yields.
- **Water Daily:** Waters crops every day, maximizing growth but increasing water consumption and risk of spoilage.

### Planting Strategies

- **Aggressive Planting:** Plants crops at every opportunity, maximizing potential yield but increasing risk during adverse weather.
- **Cautious Planting:** Skips planting before predicted storms or unfavorable conditions, reducing potential losses.

### Summary
  
- The **Balanced watering** strategy generally achieves good yields with moderate water use and crop loss.
- The **Conserve watering** strategy reduces water consumption but can lead to lower yields and, with aggressive planting, higher losses.
- The **Water Daily** strategy maximizes yield but at the cost of high water usage and increased risk of spoilage, especially with aggressive planting.
- **Cautious planting** helps reduce losses, particularly when combined with more aggressive watering strategies.

Experimenting with these combinations allows users to find the optimal balance for their simulated farm objectives.