__author__ = 'elis'

import copy
import pickle
import random
import re

from typing import NewType, Optional, Dict, List, Tuple

from .node import PilotId
from ..util import FancyRepr

from ..logging_config import logging
log = logging.getLogger(__name__)
# log.setLevel(logging.WARNING)
# log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)


class Edge(FancyRepr):
    priority = 50
    usesSlop_bool = False
    mandatory_bool = False
    mandatoryIf_str = None

    def __init__(self, active_id, opportunity_list=None):
        assert isinstance(opportunity_list, (list, type(None))), repr(opportunity_list)

        self.active_id = active_id
        self.opportunity_list = opportunity_list

        self.sorting_key = "{}:{}:{}".format(type(self).__name__, id(self), active_id)


    def _sortKey(self):
        return (self.priority, self.active_id, self.sorting_key)

    def __lt__(self, other):
        try:
            return self._sortKey() < other._sortKey()
        except:
            return True

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def isMandatory(self, state):
        if self.mandatory_bool:
            return True

        if self.mandatoryIf_str and state.getStat(self.active_id, self.mandatoryIf_str):
            return True

        return False



    def computeLookaheadScore(self, score_cls, parent, slop, depth):
        state = copy.deepcopy(parent)
        state.slop = slop
        state = self.transitionImpl(state)

        return score_cls(state, slop, depth)

    def getExactState(self, parent, doCopy=True):
        if doCopy:
            # parent_copy = copy.deepcopy(parent)
            state = parent.clone()
        else:
            # parent_copy = None
            state = parent

        state.useOpportunity(self.opportunity_list)
        # state.slop = None
        self.transitionImpl(state)

        # if doCopy:
        #     assert parent_copy == parent

        return state

    def transitionImpl(self, state):
        raise NotImplementedError()

class ChoosePassEdge(Edge):
    priority = 90
    def transitionImpl(self, state):
        return state


# class RandomEdge(Edge):
#     mandatory_bool = True
#     priority = 30
#
#     def __init__(self, active_id):
#         super(RandomEdge, self).__init__(active_id)
#         self.outcome2weightSubedge_dict = {}
#
#     def addOutcome(self, outcome, subedge, weight=1.0):
#         if outcome not in self.outcome2weightSubedge_dict:
#             self.outcome2weightSubedge_dict[outcome] = (weight, subedge)
#         else:
#             self.outcome2weightSubedge_dict[outcome] = (weight + self.outcome2weightSubedge_dict[outcome][0], subedge)
#
#
#     def transitionImpl(self, state):
#         weight_sum = sum(weight for weight, subedge in self.outcome2weightSubedge_dict.values())
#         weight_sum *= random.random()
#
#         for outcome, (weight, subedge) in self.outcome2weightSubedge_dict.items():
#             if weight_sum <= weight:
#                 # log.info("Randomly chose {!r}".format(outcome))
#                 subedge.opportunity_list = self.opportunity_list
#                 return subedge.transitionImpl(state)
#             weight_sum -= weight
#
# class RandomDialEdge(RandomEdge):
#     pass
#
# class RandomDiceEdge(RandomEdge):
#     pass

class SpendTokenEdge(Edge):
    priority = 70
    token_str = None

    def __init__(self, active_id: PilotId, tokenOwner_id: Optional[PilotId] = None):
        super(SpendTokenEdge, self).__init__(active_id)
        self.tokenOwner_id: PilotId = tokenOwner_id if tokenOwner_id is not None else active_id

    def transitionImpl(self, state):
        # from droidblue.core.steps import Stepper
        state.removeToken(self.tokenOwner_id, self.token_str)
        # state.pushStepper(Stepper(['spendToken-{}'.format(self.token_str)], active_id=self.active_id))


class SpendFocusTokenEdge(SpendTokenEdge):
    token_str = 'focus'

class SpendEvadeTokenEdge(SpendTokenEdge):
    token_str = 'evade'


