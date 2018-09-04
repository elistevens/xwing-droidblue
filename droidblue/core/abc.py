import copy
import math

from typing import NewType, Optional, Dict, List, Tuple

import numpy as np

from ..util import Jsonable
from .node import MctsNode, StateAbc

from ..logging_config import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


PlayerId = NewType('PlayerId', int)

class RoundAbc(Jsonable):
    node_cls = MctsNode

    @classmethod
    def fromStartState(cls, start_state, mtcsPredicted_score, mctsHiddenInfoEstimate_list):
        node_list = [MctsNode.fromStartState(start_state, mtcsPredicted_score, mctsHiddenInfoEstimate_list)]

        return cls(start_state, node_list)

    def __init__(self, start_state: StateAbc, node_list):
        self.start_state = start_state
        self.node_list = node_list

    @property
    def current_state(self):
        return self.node_list[-1].current_state


class GameAbc(Jsonable):
    round_cls = RoundAbc

    def __init__(self, squad_list, start_state: StateAbc, round_list):
        self.squad_list = squad_list
        self.start_state = start_state
        self.round_list = round_list



