import abc

from typing import List

from droidblue.core.agent import RandomAgentBase
from droidblue.core.node import Node
from droidblue.util import FancyRepr


class Game(FancyRepr):

    def __init__(self, state_cls, agents):
        self.start_node: Node = Node(state_cls())
        self.played_nodes: List[Node] = [self.start_node]
        self.agents: List[RandomAgentBase] = agents

    @property
    def current_node(self) -> Node:
        return self.played_nodes[-1]

    def playTurn(self):
        state = self.current_node.state
        agent = self.agents[state.active_player]

        next_node = agent.createNextNode(self.current_node)
        # TODO: this being here is weird
        self.current_node.outgoingEdge = next_node.incomingEdge

        self.played_nodes.append(next_node)

    def playGame(self):
        while self.current_node.state.getFinalScore(self.current_node.state.active_player) is None:
            self.playTurn()


# class TrainingGame(FancyRepr):
#
#     def __init__(self, state_cls, agents):
#         self.agents: List[AgentBase] = agents
#         self.state = state_cls()
#         self.trainingSamples = []
#         # self.start_node: Node = Node(state_cls())
#         # self.played_nodes: List[Node] = [self.start_node]
#
#     # @property
#     # def current_node(self) -> Node:
#     #     return self.played_nodes[-1]
#
#     def playTurn(self):
#         outgoingEdges = self.state.getFilteredEdges()
#
#         self.childNodes = [type(self)(self.state, outgoingEdge) for outgoingEdge in outgoingEdges]
#
#
#
#         state = self.current_node.state
#         agent = self.agents[state.active_player]
#
#         self.current_node.populateChildren()
#         # print(self.current_node.childNodes, self.current_node.state.getFinalScore(self.current_node.state.active_player))
#
#         # print(self.current_node.state)
#         next_node = agent.chooseNextNode(self.current_node)
#
#         self.played_nodes.append(next_node)
#
#     def playGame(self):
#         while self.current_node.state.getFinalScore(self.current_node.state.active_player) is None:
#             self.playTurn()
