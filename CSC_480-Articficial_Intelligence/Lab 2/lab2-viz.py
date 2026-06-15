from mesa.visualization import SolaraViz, make_space_component
from lab2 import *
# Define how each agent should be visualized
def agent_portrayal(agent):
    if isinstance(agent, Prey):
        return {
        "shape": "circle",
        "color": "green",
        "filled": True,
        "layer": 1,
        "r": 0.5, # Radius of the circle
        }
    elif isinstance(agent, Predator):
        return {
        "shape": "circle",
        "color": "red",
        "filled": True,
        "layer": 1,
        "r": 0.5,
        }
    return {} # Default portrayal for other agent types
    # Post-process visualization (optional, e.g., grid formatting)
def post_process(ax):
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
    # ax.set_title("Prey-Predator Simulation")
    # Model parameters to allow user customization in the Solara interface
model_params = {
    "height" : 10,
    "width" : 10,
    "prey_count" : 50,
    "predator_count" :3,
    "human_count":4,
    # "height": {
    # "type": "SliderInt",
    # "value": 10, # Default value
    # "label": "Grid Height",
    # "min": 5,
    # "max": 50,
    # "step": 1,
    # },
    # "width": {
    # "type": "SliderInt",
    # "value": 10, # Default value
    # "label": "Grid Width",
    # "min": 5,
    # "max": 50,
    # "step": 1,
    # },
    # "prey_count": {
    # "type": "SliderInt",
    # "value": 10, # Default value
    # "label": "Number of Prey",
    # "min": 1,
    # "max": 100,
    # "step": 1,
    # },
    # "predator_count": {
    # "type": "SliderInt",
    # "value": 5, # Defaultcl value
    # "label": "Number of Predators",
    # "min": 1,
    # "max": 50,
    # "step": 1,
    # },
    }
    # Create initial model instance
model = PreyPredatorModel(50,50,100, 50, 50)
    # Create the space visualization component
SpaceGraph = make_space_component(
    agent_portrayal, post_process=post_process, draw_grid=True
    )
    # Create SolaraViz page
page = SolaraViz(
    model,
    components=[SpaceGraph],
    model_params=model_params,
    name="Prey-Predator Simulation",
    )