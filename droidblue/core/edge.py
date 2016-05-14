from __future__ import division
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

__author__ = 'elis'

import copy
import cPickle
import random
import re


class Edge(object):
    priority = 50
    usesSlop_bool = False
    mandatory_bool = False

    def __init__(self, active_id, opportunity_list=None):
        assert isinstance(opportunity_list, (list, type(None))), repr(opportunity_list)

        self.active_id = active_id
        self.opportunity_list = opportunity_list

        self.sorting_key = "{}:{}:{}".format(type(self).__name__, id(self), active_id)


    def __repr__(self):
        extra_str = ', '.join(['{}:{!r}'.format(k, v) for k, v in sorted(self.__dict__.iteritems())])
        r = super(Edge, self).__repr__()
        r = re.sub(r'\<droidblue\.([a-z]+\.)+', '<', r)
        return r.replace('>', ' {}>'.format(extra_str))

    def _sortKey(self):
        return (self.priority, self.active_id, self.sorting_key)

    def __lt__(self, other):
        try:
            return self._sortKey() < other._sortKey()
        except:
            return True

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def computeLookaheadScore(self, score_cls, parent, slop, depth):
        state = copy.deepcopy(parent)
        state.slop = slop
        state = self.transitionImpl(state)

        return score_cls(state, slop, depth)

    def getExactState(self, parent, doCopy=True, count=1):
        if doCopy:
            # state = copy.deepcopy(parent)
            # state = cPickle.loads(cPickle.dumps(parent, protocol=cPickle.HIGHEST_PROTOCOL))
            if count >= 3:
                if parent.pickle_str is None:
                    parent.pickle_str = cPickle.dumps(parent, protocol=cPickle.HIGHEST_PROTOCOL)
                state = cPickle.loads(parent.pickle_str)
            else:
                state = copy.deepcopy(parent)

            state.fastforward_list = []
        else:
            state = parent

        state.useOpportunity(self.opportunity_list)
        # state.slop = None
        self.transitionImpl(state)
        return state

    def transitionImpl(self, state):
        raise NotImplementedError()

class ChoosePassEdge(Edge):
    priority = 90
    def transitionImpl(self, state):
        return state


class RandomEdge(Edge):
    priority = 30
    def __init__(self, active_id):
        super(RandomEdge, self).__init__(active_id)
        self.outcome2weightSubedge_dict = {}

    def addOutcome(self, outcome, subedge, weight=1.0):
        if outcome not in self.outcome2weightSubedge_dict:
            self.outcome2weightSubedge_dict[outcome] = (weight, subedge)
        else:
            self.outcome2weightSubedge_dict[outcome] = (weight + self.outcome2weightSubedge_dict[outcome][0], subedge)

    def computeScore(self, score_cls, parent, slop, depth):
        # avgScore_list = None
        score_list = []
        for weight, subedge in self.outcome2weightSubedge_dict.values():
            state = copy.deepcopy(parent)
            state.slop = slop
            state = self.transitionImpl(state)

            score_list.append((score_cls(state, slop, depth), weight))

        return score_cls.averageScores(score_list)

    def transitionImpl(self, state):
        weight_sum = sum(weight for weight, subedge in self.outcome2weightSubedge_dict.values())
        weight_sum *= random.random()

        for outcome, (weight, subedge) in self.outcome2weightSubedge_dict.iteritems():
            if weight_sum <= weight:
                # log.info("Randomly chose {!r}".format(outcome))
                return subedge.transitionImpl(state)
            weight_sum -= weight


class SpendTokenEdge(Edge):
    priority = 70
    token_str = None

    def __init__(self, active_id, token_id=None):
        super(SpendTokenEdge, self).__init__(active_id)
        self.token_id = token_id if token_id is not None else active_id

    def transitionImpl(self, state):
        # from droidblue.core.steps import Stepper
        state.removeToken(self.token_id, self.token_str)
        # state.pushStepper(Stepper(['spendToken-{}'.format(self.token_str)], active_id=self.active_id))


class SpendFocusTokenEdge(SpendTokenEdge):
    token_str = 'focus'

class SpendEvadeTokenEdge(SpendTokenEdge):
    token_str = 'evade'


