from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from WeatherAgent import WeatherAgent
from FarmerAgent import FarmerAgent
from CropAgent import CropAgent

class FarmModel(Model):
    def __init__(self, N, W):
        super().__init__()
        self.grid = MultiGrid(10, 10, True)
        self.current_weather = None
        self.schedule = BaseScheduler(self)
        self.assigned_cells = set()

        # Add WeatherAgents
        for i in range(W):
            weather_agent = WeatherAgent(i + 1000, self)
            self.schedule.add(weather_agent)

        # Add FarmerAgents
        for i in range(N):
            farmer = FarmerAgent(i, self)
            self.schedule.add(farmer)

            max_attempts = 100
            attempts = 0
            # Find a position with a non-overlapping 3x3 territory
            while attempts < max_attempts:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                territory = []
                overlap = False
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.grid.width and 0 <= ny < self.grid.height:
                            if (nx, ny) in self.assigned_cells:
                                overlap = True
                                break
                            territory.append((nx, ny))
                    if overlap:
                        break
                if not overlap:
                    break  # Found a valid territory
                attempts += 1

            if attempts == max_attempts:
                print(f"Could not place farmer {i} without overlap after {max_attempts} attempts.")
                continue

            # Assign and track territory
            farmer.territory = territory
            self.assigned_cells.update(territory)
            self.grid.place_agent(farmer, (x, y))
            print(f"Farmer {farmer.unique_id} placed at ({x}, {y}) with territory: {territory}")

    def step(self):
        # Weather phase: Determine today's weather
        for agent in self.schedule.agents:
            if isinstance(agent, WeatherAgent):
                agent.step()

        # Farmers phase: All farmers act
        for agent in self.schedule.agents:
            if isinstance(agent, FarmerAgent):
                agent.step()

        # Crops phase: All crops grow
        for agent in self.schedule.agents:
            if isinstance(agent, CropAgent):
                agent.step()

        self.schedule.steps += 1
        print(f"=== End of Day {self.schedule.steps} ===\n")