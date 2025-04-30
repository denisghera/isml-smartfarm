from mesa import Agent
import random

class CropAgent(Agent):
    def __init__(self, unique_id, model, crop_type):
        super().__init__(unique_id, model)
        self.crop_type = crop_type
        self.growth_stage = 0
        self.max_growth_stage = 5
        self.water_needs = random.randint(1, 2)
        self.water_received = 0

    def step(self):
        if self.pos:
            weather = self.model.current_weather
            if self.water_received >= self.water_needs:
                if weather == "rain":
                    self.growth_stage += 2
                elif weather == "sun":
                    self.growth_stage += 1
                elif weather == "cloudy":
                    self.growth_stage += 1
                elif weather == "stormy":
                    self.growth_stage = max(0, self.growth_stage - 1)
                self.water_received = 0

            self.growth_stage = min(self.max_growth_stage, max(0, self.growth_stage))
            print(f"Crop {self.crop_type} at {self.pos}: Stage {int(self.growth_stage)}")

    def is_mature(self):
        return self.growth_stage >= self.max_growth_stage