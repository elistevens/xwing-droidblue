import abc
import random

from droidblue.util import FancyRepr


class AgentBase(FancyRepr, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def chooseEdge(self, game, state, outgoingEdges):
        pass


class FirstEdgeAgent(AgentBase):
    def chooseEdge(self, game, state, outgoingEdges):
        return outgoingEdges[0]


class RandomEdgeAgent(AgentBase):
    def chooseEdge(self, game, state, outgoingEdges):
        return random.choice(outgoingEdges)
