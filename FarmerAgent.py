from mesa import Agent
from CropAgent import CropAgent
import random

class FarmerAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.crop_types = ["potato", "tomato", "cucumber"]
        self.crop_strategy = "diverse"  # Can be modified to "specialized" later
        self.territory = []
        self.initial_pos = None

        # Stats for this farmer
        self.total_crops_planted = 0
        self.total_crops_harvested = 0
        self.total_crops_spoiled = 0
        self.total_crops_destroyed = 0

    def step(self):
        # Remove spoiled or harvested crops
        for pos in self.territory:
            cell_contents = self.model.grid.get_cell_list_contents([pos])
            for agent in cell_contents[:]:
                if isinstance(agent, CropAgent):
                    if agent.is_mature():
                        self.model.grid.remove_agent(agent)
                        self.model.schedule.remove(agent)
                        self.total_crops_harvested += 1
                        print(f"Farmer {self.unique_id} harvested {agent.crop_type} at {pos}")
                    elif agent.spoiled:
                        self.model.grid.remove_agent(agent)
                        self.model.schedule.remove(agent)
                        # Update farmer stats depending on spoil reason
                        if agent.spoil_reason == "storm_destroyed":
                            self.total_crops_destroyed += 1
                            print(f"Farmer {self.unique_id} removed storm-destroyed {agent.crop_type} at {pos}")
                        elif agent.spoil_reason == "overwatered":
                            self.total_crops_spoiled += 1
                            print(f"Farmer {self.unique_id} removed overwatered {agent.crop_type} at {pos}")

        # Water all crops in the territory
        weather = self.model.current_weather
        for pos in self.territory:
            cell_contents = self.model.grid.get_cell_list_contents([pos])
            for agent in cell_contents:
                if isinstance(agent, CropAgent) and agent.water_received < agent.water_needs:
                    water_amount = self.get_water_amount(weather)
                    agent.water_received += water_amount
                    print(f"Farmer {self.unique_id} watered {agent.crop_type} at {pos} (+{water_amount})")

        # Plant crops in all empty positions in the territory
        for pos in self.territory:
            cell_contents = self.model.grid.get_cell_list_contents([pos])
            if not any(isinstance(agent, CropAgent) for agent in cell_contents):
                self.plant_crop(pos)

    def get_water_amount(self, weather):
        # Returns water amount based on weather conditions
        return {
            "rain": 3,
            "sun": 2,
            "cloudy": 1,
            "stormy": 0
        }.get(weather, 1)

    def plant_crop(self, pos):
        crop_type = random.choice(self.crop_types)
        new_crop = CropAgent(self.model.next_id(), self.model, crop_type)
        self.model.grid.place_agent(new_crop, pos)
        self.model.schedule.add(new_crop)
        self.total_crops_planted += 1
        print(f"Farmer {self.unique_id} planted {crop_type} at {pos}")

    def move(self):
        # Optional movement logic (if needed)
        neighbors = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_position)