from random import choice
from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """

        self.move_sheep(Wolf, GrassPatch)
        self.energy -= 1
        grass_agent = \
            [agent for agent in self.model.grid.get_cell_list_contents([self.pos]) if isinstance(agent, GrassPatch)][0]
        if grass_agent.fully_grown:
            self.energy += 1
            grass_agent.eat()

        if self.energy == 0:
            print(f"Sheep {self.unique_id} has died of hunger.")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


        elif self.random.random() < self.model.sheep_reproduce:
            self.energy /= 2
            child = Sheep(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(child, self.pos)
            self.model.schedule.add(child)

    def kill(self):
        print(f'Sheep {self.unique_id} has died from wolf.')
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.move_wolf(Sheep, GrassPatch)
        sheeps = \
            [agent for agent in self.model.grid.get_cell_list_contents([self.pos]) if isinstance(agent, Sheep)]

        self.energy -= 1

        if len(sheeps):
            choice(sheeps).kill()
            self.energy += self.model.wolf_gain_from_food

        if self.energy <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


        elif self.random.random() < self.model.wolf_reproduce:
            self.energy /= 2
            child = Wolf(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(child, self.pos)
            self.model.schedule.add(child)


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            self.countdown -= 1
            if self.countdown == 0:
                self.fully_grown = True

    def eat(self):
        self.fully_grown = False
        self.countdown = self.model.grass_regrowth_time
