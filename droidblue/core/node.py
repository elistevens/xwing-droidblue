from typing import Dict, Optional, List, Type, Tuple

from droidblue.core.basecls import StateBase, EdgeBase, PlayerId
from droidblue.util import FancyRepr


class Node(FancyRepr):
    def __init__(
        self,
        parent_state: StateBase,
        incomingEdge: Optional[EdgeBase] = None,
        new_state: StateBase = None,
    ):
        if new_state:
            self.state: StateBase = new_state
            self.incomingEdge: EdgeBase = incomingEdge
        else:
            self.state: StateBase = parent_state.clone()
            self.incomingEdge: EdgeBase = incomingEdge

            if self.incomingEdge:
                self.incomingEdge.updateState(self.state)

        self.edgeType_to_evalData: Dict[EdgeBase, Tuple] = {}
        self.outgoingEdge: Optional[EdgeBase] = None
