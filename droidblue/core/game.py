import abc

from typing import List

from droidblue.core.agent import AgentBase
from droidblue.core.node import Node
from droidblue.util import FancyRepr


class Game(FancyRepr):

    def __init__(self, state_cls, agents):
        self.start_node: Node = Node(state_cls())
        self.played_nodes: List[Node] = [self.start_node]
        self.agents: List[AgentBase] = agents

    @property
    def current_node(self) -> Node:
        return self.played_nodes[-1]

    def playTurn(self):
        state = self.current_node.state
        agent = self.agents[state.active_player]

        self.current_node.populateChildren()
        # print(self.current_node.childNodes, self.current_node.state.getFinalScore(self.current_node.state.active_player))

        # print(self.current_node.state)
        next_node = agent.chooseNextNode(self.current_node)

        self.played_nodes.append(next_node)

    def playGame(self):
        while self.current_node.state.getFinalScore(self.current_node.state.active_player) is None:
            self.playTurn()
