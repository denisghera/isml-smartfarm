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

        self.water_limit = self.water_needs * 1.5  # Max safe water
        self.spoiled = False
        self.spoil_reason = None

    def step(self):
        if self.pos is None or self.spoiled:
            return
        
        weather = self.model.current_weather
        
        # Storm destruction
        if weather == "stormy" and random.random() < 0.1:
            self.spoiled = True
            self.spoil_reason = "storm_destroyed"
            print(f"{self.crop_type} at {self.pos} destroyed by storm")
            return

        # Add natural water from rain
        if weather == "rain" or weather == "stormy":
            self.water_received += 1
            
        # Overwatered
        if self.water_received > self.water_limit:
            self.spoiled = True
            self.spoil_reason = "overwatered"
            print(f"{self.crop_type} at {self.pos} spoiled due to overwatering ({self.water_received} / {self.water_limit})")
            return

        # Grow if watered enough
        if self.water_received >= self.water_needs:
            self.water_received = 0
            self.growth_stage += 1
            self.growth_stage = min(self.growth_stage, self.max_growth_stage)

    def is_mature(self):
        return self.growth_stage >= self.max_growth_stage

    def get_color(self):
        if self.spoiled:
            return "#000000"
    
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