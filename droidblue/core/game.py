import abc

from typing import List

from droidblue.core.agent import AgentBase
from droidblue.core.node import Node
from droidblue.util import FancyRepr


class Game(FancyRepr):

    def __init__(self, state_cls, agents):
        self.start_node: Node = Node.fromStartState(state_cls())
        self.played_nodes: List[Node] = [self.start_node]
        self.agents: List[AgentBase] = agents

    @property
    def current_node(self) -> Node:
        return self.played_nodes[-1]

    def playTurn(self):
        state = self.current_node.state
        agent = self.agents[state.active_player]

        new_edge = agent.chooseEdge(self, state, self.current_node.outgoingEdges)

        self.played_nodes.append(self.current_node.getNextNode(new_edge))

    def playGame(self):
        while self.current_node.outgoingEdges:
            self.playTurn()
