from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

from FarmModel import FarmModel
from FarmerAgent import FarmerAgent
from CropAgent import CropAgent
from WeatherAgent import WeatherAgent

class WeatherDisplay(TextElement):
    def render(self, model):
        return f"Weather: {model.current_weather}"

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

server = ModularServer(
    FarmModel,
    [grid, weather_display],
    "Smart Farm Simulation",
    {
        "N": Slider("Number of Farmers", 2, 1, 10, 1),
        "W": Slider("Number of Weather Agents", 1, 1, 3, 1),
    }
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()