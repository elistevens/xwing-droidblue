from typing import Optional, List

from droidblue.core.basecls import StateBase, EdgeBase
from droidblue.util import FancyRepr


class Node(FancyRepr):
    @classmethod
    def fromStartState(cls, state: StateBase, **kwargs) -> "Node":
        outgoingEdges = state.getFilteredEdges()

        return cls(None, state, outgoingEdges, **kwargs)

    def __init__(
        self,
        incomingEdges: Optional[List[EdgeBase]],
        state: StateBase,
        outgoingEdges: List[EdgeBase],
        **kwargs,
    ):
        self.incomingEdges: List[EdgeBase] = incomingEdges
        self.state: StateBase = state

        # TODO get rid of these next two
        self.outgoingEdges: List[EdgeBase] = outgoingEdges
        self.outgoingNodes: List[Optional[Node]] = [None] * len(outgoingEdges)

    def getNextNode(self, new_edge: EdgeBase, fastforward: bool = True,) -> "Node":
        new_state = self.state.clone()
        outgoingEdges = [new_edge]

        incomingEdges = []
        while len(outgoingEdges) == 1 and (fastforward or (len(incomingEdges) == 0)):
            # log.debug(['fastforwarding', outgoingEdges])
            incomingEdges.append(outgoingEdges[0])
            outgoingEdges[0].updateState(new_state)

            outgoingEdges = new_state.getFilteredEdges()

        new_state.frozen = True

        return type(self)(incomingEdges, new_state, outgoingEdges)

    # def getScore(self):
