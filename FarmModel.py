from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from WeatherAgent import WeatherAgent
from FarmerAgent import FarmerAgent

class FarmModel(Model):
    """Manages agents and ensures correct execution order."""
    def __init__(self, N, W):
        super().__init__()
        self.grid = MultiGrid(10, 10, True)
        self.current_weather = None
        self.schedule = BaseScheduler(self)
        
        # Add WeatherAgents first
        for i in range(W):
            weather_agent = WeatherAgent(i + 1000, self)  # Unique IDs
            self.schedule.add(weather_agent)

        # Add FarmerAgents
        for i in range(N):
            farmer = FarmerAgent(i, self)
            self.schedule.add(farmer)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(farmer, (x, y))

    def step(self):
        """Let Mesa handle execution order"""
        self.schedule.step()