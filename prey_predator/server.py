from colour import Color
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
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
    "grass_regrowth_time": UserSettableParameter('slider', 'Grass Regrowth Time', 20, 1, 50),
    "initial_sheep": UserSettableParameter('slider', 'Initial Sheep Population', 100, 10, 300),
    "sheep_reproduce": UserSettableParameter('slider', 'Sheep Reproduction Rate', 0.04, 0.01, 1.0,
                                             0.01),
    "initial_wolves": UserSettableParameter('slider', 'Initial Wolf Population', 50, 10, 300),
    "wolf_reproduce": UserSettableParameter('slider', 'Wolf Reproduction Rate', 0.05, 0.01, 1.0,
                                            0.01,
                                            description="The rate at which wolf agents reproduce."),
    "wolf_gain_from_food": UserSettableParameter('slider', 'Wolf Gain From Food Rate', 20, 1, 50),
    "sheep_gain_from_food": UserSettableParameter('slider', 'Sheep Gain From Food', 4, 1, 10)
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
