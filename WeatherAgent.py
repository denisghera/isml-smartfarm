from mesa import Agent
import random

class WeatherAgent(Agent):
    """Simulates changing weather conditions and updates the model's current weather."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.weather = None

    def step(self):
        self.weather = random.choice(["rain", "sun", "cloudy", "stormy"])
        self.model.current_weather = self.weather
        print(f"\n=== Day {self.model.schedule.steps + 1} ===")  # Clear day separator
        print(f"Today's weather: {self.weather}")