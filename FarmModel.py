from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from WeatherAgent import WeatherAgent
from FarmerAgent import FarmerAgent

class FarmModel(Model):
    def __init__(self, N, W, watering_strategy, planting_strategy, t_size):
        super().__init__()
        self.grid = MultiGrid(10, 10, True)
        self.schedule = BaseScheduler(self)
        self.assigned_cells = set()
        self.current_weather = None
        self.weather_forecast = []
        self.watering_strategy = watering_strategy
        self.planting_strategy = planting_strategy

        # Add WeatherAgents (only one for now)
        for i in range(W):
            weather_agent = WeatherAgent(i + 1000, self)
            self.schedule.add(weather_agent)

        # Add FarmerAgents
        for i in range(N):
            farmer = FarmerAgent(i, self)
            self.schedule.add(farmer)

            max_attempts = 100
            attempts = 0
            while attempts < max_attempts:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                territory = []
                overlap = False
                half_size = t_size // 2
                for dx in range(-half_size, half_size + 1):
                    for dy in range(-half_size, half_size + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.grid.width and 0 <= ny < self.grid.height:
                            if (nx, ny) in self.assigned_cells:
                                overlap = True
                                break
                            territory.append((nx, ny))
                    if overlap:
                        break
                if not overlap:
                    farmer.initial_pos = (x, y)
                    break
                attempts += 1

            if attempts == max_attempts:
                print(f"Could not place farmer {i} without overlap after {max_attempts} attempts.")
                continue

            farmer.territory = territory
            self.assigned_cells.update(territory)
            self.grid.place_agent(farmer, (x, y))
            print(f"Farmer {farmer.unique_id} placed at ({x}, {y}) with territory: {territory}")

    def step(self):
        # Let all agents (including WeatherAgent) take their step
        self.schedule.step()
        print(f"=== End of Day {self.schedule.steps} ===\n")