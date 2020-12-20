import abc
from renjuu.game.const import PlayerEntity


class Player(abc.ABC):
    def __init__(self, color, entity=PlayerEntity.human, name: str = None):
        self.color = color
        self.entity = entity
        self.name = name

    @abc.abstractmethod
    def make_move(self, board):
        pass


class HumanPlayer(Player):
    def make_move(self, board):
        return None
