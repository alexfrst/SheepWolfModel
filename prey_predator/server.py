from colour import Color
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from prey_predator.agents import Sheep,Wolf, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    if type(agent) is Sheep:
        portrayal.update({"Shape": "./prey_predator/images/sheep.png",
                          "Filled": "true",
                          "w": 0.6,
                          "h": 0.6,
                          "Layer": 1,
                          "Color": "#0000AA"})

    elif type(agent) is Wolf:
        portrayal.update({"Shape": "./prey_predator/images/wolf.png",
                          "Filled": "true",
                          "Layer": 2,
                          "r": 0.5,
                          "Color": "#AA0000"})

    elif type(agent) is GrassPatch:
        portrayal.update({
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "w": 1,
            "h": 1,
            "Color": get_color(agent)
        })

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    # ... to be completed
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521


def get_color(agent):
    brown = Color("#793b09")
    green = Color("#00d13f")
    colors = list(green.range_to(brown, agent.model.grass_regrowth_time + 1))
    try:
        return colors[agent.countdown].hex
    except IndexError:
        print(agent.countdown)
    return colors[agent.countdown].hex
