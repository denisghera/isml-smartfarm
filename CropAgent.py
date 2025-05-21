from mesa import Agent
import random

class CropAgent(Agent):
    # Define crop characteristics
    CROP_PROPERTIES = {
        "potato": {
            "color": ("#FFF3B0", "#E09F3E"),  # Light yellow to dark yellow/orange
            "max_growth_stage": 4,
            "water_needs_range": (1, 2)
        },
        "tomato": {
            "color": ("#FFCCCB", "#D00000"),  # Light red to dark red
            "max_growth_stage": 3,
            "water_needs_range": (2, 3)
        },
        "cucumber": {
            "color": ("#E9F5DB", "#679436"),  # Light green to dark green
            "max_growth_stage": 5,
            "water_needs_range": (3, 4)
        }
    }

    def __init__(self, unique_id, model, crop_type):
        super().__init__(unique_id, model)
        self.crop_type = crop_type
        self.growth_stage = 0
        props = self.CROP_PROPERTIES[crop_type]
        
        self.max_growth_stage = props["max_growth_stage"]
        self.water_needs = random.randint(*props["water_needs_range"])
        self.water_received = 0
        self.color_range = props["color"]

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

    def is_mature(self):
        return self.growth_stage >= self.max_growth_stage

    def get_color(self):
        if self.is_mature():
            return self.color_range[1]
        
        # Interpolate between light and dark colors based on growth stage
        progress = self.growth_stage / self.max_growth_stage
        return self.interpolate_color(self.color_range[0], self.color_range[1], progress)

    @staticmethod
    def interpolate_color(start_hex, end_hex, progress):
        # Convert hex to RGB components
        start = tuple(int(start_hex[i:i+2], 16) for i in (1, 3, 5))
        end = tuple(int(end_hex[i:i+2], 16) for i in (1, 3, 5))
        
        # Calculate intermediate color
        r = int(start[0] + (end[0] - start[0]) * progress)
        g = int(start[1] + (end[1] - start[1]) * progress)
        b = int(start[2] + (end[2] - start[2]) * progress)
        
        return f"#{r:02x}{g:02x}{b:02x}"