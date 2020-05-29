from typing import Optional, List, Type

from droidblue.core.basecls import StateBase, EdgeBase, PlayerId
from droidblue.util import FancyRepr


class Node(FancyRepr):
    def __init__(
        self,
        parent_state: StateBase,
        incomingEdge: Optional[EdgeBase] = None,
    ):
        self.state: StateBase = parent_state.clone()

        self.incomingEdge: EdgeBase = incomingEdge
        if self.incomingEdge:
            self.incomingEdge.updateState(self.state)

        self.childNodes: Optional[List[Node]] = None
        self.parent_active_player: PlayerId = parent_state.active_player
        # self.predicted_score: Optional[float] = self.state.getPredictedScore(parent_state.active_player)


    def populateChildren(self):
        outgoingEdges = self.state.getFilteredEdges()

        self.childNodes = [type(self)(self.state, outgoingEdge) for outgoingEdge in outgoingEdges]


    # def getNextNode(self, new_edge: EdgeBase) -> "Node":
    #     pass
    #     new_state = self.state.clone()
    #     outgoingEdges = [new_edge]
    #
    #     incomingEdges = []
    #     while len(outgoingEdges) == 1 and (fastforward or (len(incomingEdges) == 0)):
    #         # log.debug(['fastforwarding', outgoingEdges])
    #         incomingEdges.append(outgoingEdges[0])
    #         outgoingEdges[0].updateState(new_state)
    #
    #         outgoingEdges = new_state.getFilteredEdges()
    #
    #     new_state.frozen = True
    #
    #     return type(self)(incomingEdges, new_state, outgoingEdges)
    #
    # def getScore(self):
