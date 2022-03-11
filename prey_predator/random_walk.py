"""
Generalized behavior for random walking, one grid cell at a time.
"""

from mesa import Agent


class RandomWalker(Agent):
    """
    Class implementing random walker methods in a generalized manner.

    Not indended to be used on its own, but to inherit its methods to multiple
    other agents.

    """

    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)            
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def move_sheep(self, wolf, grass):
        """
        The sheep moves where there is no wolf
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)

        #Save the information on the moves in a dictionnary
        next_moves_score = {}

        #For each possible move, check who are the neighbors
        for move in next_moves:
            score = 0
            #check the agents in the potential future position of the sheep
            agents = [agent for agent in self.model.grid.get_cell_list_contents([move])]
            #Update score of the move depending on the presence of wolves, grass and sheeps
            for agent in agents:
                if isinstance(agent, wolf):
                    score-=20
                elif isinstance(agent, grass):
                    if agent.fully_grown:
                        score+=15
                else:
                    score+=5
            next_moves_score[move] = score
 
        max_scores = [key for key, value in next_moves_score.items() if value == max(list(next_moves_score.values()))]
        next_move = self.random.choice(max_scores)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def move_wolf(self, sheep, grass):
        """
        The wolf moves where there is sheeps.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)

        #Save the information on the moves in a dictionnary
        next_moves_score = {}

        #For each possible move, check who are the neighbors
        for move in next_moves:
            score = 0
            #check the agents in the potential future position of the sheep
            agents = [agent for agent in self.model.grid.get_cell_list_contents([move])]
            #Update score of the move depending on the presence of wolves, grass and sheeps
            for agent in agents:
                if isinstance(agent, sheep):
                    score+=15
                elif isinstance(agent, grass):
                    score+=1
                else:
                    score-=5
            next_moves_score[move] = score
 
        max_scores = [key for key, value in next_moves_score.items() if value == max(list(next_moves_score.values()))]
        next_move = self.random.choice(max_scores)
        # Now move:
        self.model.grid.move_agent(self, next_move)
