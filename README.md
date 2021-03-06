# Prey - Predator Model

## Summary

This repo contains the prey and predator model of:
- Alexandre FORESTIER
- Morgane SENEJKO

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

## Files

* ``prey_predator/random_walker.py``: This defines the ``RandomWalker`` agent, which implements the behavior of moving across a grid, one cell at a time. Both the Wolf and Sheep agents will inherit from it. There are several distinct functions : one for the random wlak, one for the intelligent walk according to the sheeps and one for the wolves.
* ``prey_predator/agents.py``: Defines the Wolf, Sheep, and GrassPatch agent classes.
* ``prey_predator/schedule.py``: Defines a custom variant on the RandomActivation scheduler, where all agents of one class are activated (in random order) before the next class goes -- e.g. all the wolves go, then all the sheep, then all the grass.
* ``prey_predator/model.py``: Defines the Prey-Predator model itself
* ``prey_predator/server.py``: Sets up the interactive visualization server
* ``run.py``: Launches a model visualization server.

## Introduced modifications

We've followed the given model. We've only added a `kill` method for wolves and sheeps agent.

We've made some assumptions for our model:
- Concerning reproduction, we've decided that it was an energy intensive process for agents. 
Hence we've decided to divide their energy by two while they were giving birth.

We've also brought some innovations:
- Concerning sheep moves they are now looking for fresh grass, avoiding places that are containing wolves, looking for other sheep to live with. Indeed, before moving to another cell, they look in all the possible positions and compute a score, finally choosing the move with the maximal score. The presence of wolves decreases the score whereas the presence of fresh grass increases it. Moreover, the presence of other sheeps increase the score as we made the assumption that a wolf can only eat one sheep at a time. So if a sheep go to a cell where there is another sheep, if a wolf goes to this cell it will have to choose between the sheeps.
- Concerning wolves, they are seeking for places where there is the biggest number of sheeps and they try to avoid each other. Indeed, if there are several wolves in the same place, they will have to share the sheeps.
- We've also added cosmetic upgrades with a color range depending on the grass growth state, and some pictures for wolves and sheeps.
<p align="center">
  <img src="./prey_predator/images/sheep.png" height="100">
  <img src="./prey_predator/images/wolf.png" height="100">
</p>

## Parameter tuning 

In order to have an acceptable curve where the dominant species varies overtime we have implemented sliders in order to make the testing easier.
Then we've run iteratively the simulation with the default parameters and finetuned params. When species were gaining way too much influence we reduced some of their values:
- Their reproduction rate
- Their energy gain from food

For sheep we've had an additional parameter the grass regrowth time.

After tuning, here is the obtained graph:

We've obtained this graph thanks to those parameters:
- Grass regrowth time:  49
- Sheep gain from food: 4
- Wolf gain from food: 5
- Initial sheep population: 34
- Initial wolf population: 13
- Sheep reproduction rate: 0.07
- Wolf reproduction rate: 0.05

![](prey_predator/images/agent_counts_overtime.png)

## Upgrade that can be done to our model

We could go further in the implementation of the model in order to make it more realistic. Here is a list of ideas we've had:

- `Seasons`: we could have added seasons with several parameters:
  - During the first 163 steps (winter) animals could lose 2 times more energy
  - During last 163 (summer) grass could grow 2 times faster

- `Reproduction`: Make reproduction possible only when two agent from same breed are in the same place

- 3rd idea to be placed here

- 4th idea to be placed here


Those ideas are pretty easy to implement. However those could have added way more complexity and made the tuning phase way more challenging
