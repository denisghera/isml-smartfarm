from mesa import Agent
from CropAgent import CropAgent

class FarmerAgent(Agent):
    """Handles planting, watering, and harvesting crops."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pos = None

    def step(self):
        """Perform actions based on current weather."""
        weather = self.model.current_weather
        cell_content = self.model.grid.get_cell_list_contents([self.pos])
        crops = [agent for agent in cell_content if isinstance(agent, CropAgent)]

        if not crops:
            self.plant_crop()
        else:
            for crop in crops:
                if crop.is_mature():
                    self.model.grid.remove_agent(crop)
                    self.model.schedule.remove(crop)
                    print(f"Farmer {self.unique_id} harvested at {self.pos}.")
                    self.plant_crop()
                else:
                    # Water the crop
                    if weather == "rain":
                        crop.water_received += 3
                    elif weather == "sun":
                        crop.water_received += 2
                    elif weather == "cloudy":
                        crop.water_received += 1
                    else:
                        crop.water_received += 1  # Stormy
                    print(f"Farmer {self.unique_id} watered at {self.pos}.")

    def plant_crop(self):
        new_crop = CropAgent(self.model.next_id(), self.model, "wheat")
        self.model.grid.place_agent(new_crop, self.pos)
        self.model.schedule.add(new_crop)
        print(f"Farmer {self.unique_id} planted new wheat at {self.pos}.")