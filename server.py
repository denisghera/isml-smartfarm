from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, Choice

from FarmModel import FarmModel
from FarmerAgent import FarmerAgent
from CropAgent import CropAgent
from WeatherAgent import WeatherAgent

class WeatherDisplay(TextElement):
    def render(self, model):
        return f"Weather: {model.current_weather}"
    
class ForecastDisplay(TextElement):
    def render(self, model):
        return f"Forecast: {model.weather_forecast}"

class FarmStatsElement(TextElement):
    def render(self, model):
        style = (
            "border-collapse: collapse; "
            "font-family: Arial, sans-serif;"
        )
        cell_style = "border: 1px solid black; padding: 6px; text-align: center; word-break: break-word;"
        header_style = cell_style + "background-color: #f2f2f2; font-weight: bold;"

        html = f"<div style='text-align: center;'>"
        html += f"<table style='{style}'>"
        html += (
            "<tr>"
            f"<th style='{header_style}'>Farmer ID</th>"
            f"<th style='{header_style}'>Territory Size</th>"
            f"<th style='{header_style}'>Position</th>"
            f"<th style='{header_style}'>Planted</th>"
            f"<th style='{header_style}'>Harvested</th>"
            f"<th style='{header_style}'>Spoiled</th>"
            f"<th style='{header_style}'>Destroyed</th>"
            f"<th style='{header_style}'>Water</th>"
            "</tr>"
        )

        for agent in model.schedule.agents:
            if isinstance(agent, FarmerAgent):
                html += (
                    "<tr>"
                    f"<td style='{cell_style}'>{agent.unique_id}</td>"
                    f"<td style='{cell_style}'>{len(agent.territory)}</td>"
                    f"<td style='{cell_style}'>{agent.initial_pos}</td>"
                    f"<td style='{cell_style}'>{agent.total_crops_planted}</td>"
                    f"<td style='{cell_style}'>{agent.total_crops_harvested}</td>"
                    f"<td style='{cell_style}'>{agent.total_crops_spoiled}</td>"
                    f"<td style='{cell_style}'>{agent.total_crops_destroyed}</td>"
                    f"<td style='{cell_style}'>{agent.total_water}</td>"
                    "</tr>"
                )

        html += "</table></div>"

        return html

def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, FarmerAgent):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5
        portrayal["text"] = f"{agent.pos}"
        portrayal["text_color"] = "black"
    elif isinstance(agent, CropAgent):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = agent.get_color()
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8
    elif isinstance(agent, WeatherAgent):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "white"
        portrayal["Filled"] = "false"
        portrayal["Layer"] = 0
        portrayal["w"] = 0
        portrayal["h"] = 0
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
weather_display = WeatherDisplay()
forecast = ForecastDisplay()
stats = FarmStatsElement()

server = ModularServer(
    FarmModel,
    [grid, weather_display, forecast, stats],
    "Smart Farm Simulation",
    {
        "N": Slider("Number of Farmers", 2, 1, 10, 1),
        "W": Slider("Number of Weather Agents", 1, 1, 3, 1),
        "t_size" : Slider ("Size of territory", 3, 1, 10, 1),
        "watering_strategy": Choice(
            "Watering Strategy",
            value="Water Daily",
            choices=["Water Daily", "Conserve Water", "Balanced"]
        ),
        "planting_strategy": Choice(
            "Planting Strategy",
            value="Plant Daily",
            choices=["Plant Daily", "Skip Before Storm"]
        ),
    }
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()