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

        # Add WeatherAgents
        for i in range(W):
            weather_agent = WeatherAgent(i + 1000, self)
            self.schedule.add(weather_agent)

        # Add FarmerAgents
        for i in range(N):
            farmer = FarmerAgent(i, self)
            self.schedule.add(farmer)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(farmer, (x, y))
            # Define 3x3 territory
            territory = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.grid.width and 0 <= ny < self.grid.height:
                        territory.append((nx, ny))
            farmer.territory = territory
            print(f"Farmer {farmer.unique_id} placed at ({x}, {y}) with territory")

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