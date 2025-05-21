from mesa import Agent
import random

class WeatherAgent(Agent):
    """Simulates changing weather conditions and maintains a 3-day forecast."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.current_weather = random.choice(["rain", "sun", "cloudy", "stormy"])
        self.forecast = [random.choice(["rain", "sun", "cloudy", "stormy"]) for _ in range(3)]

    def step(self):
        # Shift forecast: today becomes current, new weather added
        self.current_weather = self.forecast.pop(0)
        new_forecast = random.choice(["rain", "sun", "cloudy", "stormy"])
        self.forecast.append(new_forecast)

        # Update model-wide access
        self.model.current_weather = self.current_weather
        self.model.weather_forecast = list(self.forecast)  # Copy for safety

        print(f"\n=== Day {self.model.schedule.steps + 1} ===")
        print(f"Today's weather: {self.current_weather}")
        print(f"Forecast: {self.forecast}")
