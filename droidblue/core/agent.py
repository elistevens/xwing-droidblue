import abc
import random

from typing import Optional

from droidblue.core.basecls import StateBase
from droidblue.core.node import Node
from droidblue.util import FancyRepr


class AgentBase(FancyRepr, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def chooseNextNode(self, node: Node):
        pass

    def getScore(self, node: Node) -> float:
        score: Optional[float] = node.state.getFinalScore(node.parent_active_player)

        if score is not None:
            return score

        return self.predictScore(node)

    def predictScore(self, node: Node) -> float:
        return 0.0


class FirstAgent(AgentBase):
    def chooseNextNode(self, node: Node) -> Node:
        return node.childNodes[0]


class RandomAgent(AgentBase):
    def chooseNextNode(self, node: Node) -> Node:
        return random.choice(node.childNodes)

class TrainedAgent(AgentBase):
    def chooseNextNode(self, node: Node) -> Node:

        if node.state.isTrainable:
            print(node.state.getTrainableInput())

        return random.choice(node.childNodes)
