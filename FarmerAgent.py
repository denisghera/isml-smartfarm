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
        self.total_water = 0

    def step(self):
        forecast = self.model.weather_forecast  # list of upcoming days ["sun", "rain", "cloudy", "stormy"]
        current_weather = self.model.current_weather

        # Analyze forecast: is there a storm soon?
        storm_soon = "stormy" in forecast[:1] # Storm expected in the next 2 days

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

        # Water crops smarter
        for pos in self.territory:
            cell_contents = self.model.grid.get_cell_list_contents([pos])
            for agent in cell_contents:
                if isinstance(agent, CropAgent) and agent.water_received < agent.water_needs and not agent.spoiled:
                    water_amount = 0
                    # Decision logic for watering amount:
                    if current_weather in ["rain", "stormy"]:
                        water_amount = 0 if self.model.watering_strategy == "Conserve Water" else 1
                    elif current_weather in ["sun", "cloudy"]:
                        water_amount = 1

                    agent.water_received += water_amount
                    if water_amount > 0:
                        self.total_water += water_amount
                        print(f"Farmer {self.unique_id} watered {agent.crop_type} at {pos} ({agent.water_received} / {agent.water_needs})")

        # Planting decision - if storm is soon, maybe hold planting to avoid loss of seeds
        for pos in self.territory:
            cell_contents = self.model.grid.get_cell_list_contents([pos])
            empty = not any(isinstance(agent, CropAgent) for agent in cell_contents)

            if empty:
                if storm_soon and self.model.planting_strategy == "Skip Before Storm":
                    print(f"Farmer {self.unique_id} delays planting at {pos} due to upcoming storm")
                    continue  # skip planting this turn to save seeds

                self.plant_crop(pos)

    def plant_crop(self, pos):
        crop_type = random.choice(self.crop_types)
        new_crop = CropAgent(self.model.next_id(), self.model, crop_type)
        self.model.grid.place_agent(new_crop, pos)
        self.model.schedule.add(new_crop)
        self.total_crops_planted += 1
        print(f"Farmer {self.unique_id} planted {crop_type} at {pos}")