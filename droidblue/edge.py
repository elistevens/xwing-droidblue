__author__ = 'elis'

import copy
import itertools
import random


# class EdgeSet(object):
#     def __init__(self, parent, skew=1.0, threshold=0.0):
#         self.parent = parent
#         self.edge_list = []
#         self.skew = float(skew)
#         self.threshold = float(threshold)
#
#     def addEdge(self, edge):
#         edge.transitionFrom(self.parent)
#         self.edge_list.append(edge)
#
#     def filter(self):
#         weight_max = float(max(edge.weight for edge in self.edge_list))
#
#         self.edge_list = [edge for edge in self.edge_list if edge.weight >= weight_max * self.threshold]
#         self.edge_list.sort(reverse=True, key=lambda edge: edge.weight)
#
#     def normalize(self):
#         weight_sum = float(sum(edge.weight for edge in self.edge_list))
#         if weight_sum != 1.0:
#             for edge in self.edge_list:
#                 edge.weight /= weight_sum
#
#     def randomChoice(self):
#         self.normalize()
#         rand_frac = random.random() ** self.skew
#
#         for i, edge in enumerate(self.edge_list):
#             if edge.weight >= rand_frac:
#                 return i, edge
#
#             rand_frac -= edge.weight
#         else:
#             assert rand_frac <= 1.0
#
#         assert False

class Edge(object):
    usesSlop_bool = False
    mandatory_bool = False

    def __init__(self, active_id):
        self.active_id = active_id

    def computeLookaheadScore(self, score_cls, parent, slop, depth):
        state = copy.deepcopy(parent)
        state.slop = slop
        state = self.transitionImpl(state)

        return score_cls(state, slop, depth)

    def getExactState(self, parent):
        state = copy.deepcopy(parent)
        state.slop = None
        self.transitionImpl(state)
        return state

    def transitionImpl(self, state):
        raise NotImplementedError()

class ChooseNoneEdge(Edge):
    def transitionImpl(self, state):
        state.nextStep()
        return state


class RandomEdge(Edge):
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



class SpendTokenEdge(Edge):
    token_str = None

    def __init__(self, active_id, token_id=None):
        super(SpendTokenEdge, self).__init__(active_id)
        self.token_id = token_id if token_id is not None else active_id

    def transitionImpl(self, state):
        from droidblue.steps import Stepper
        state.ship[self.token_id].removeToken(self.token_str)
        state.pushStepper(Stepper(['spendToken-{}'.format(self.token_str)], active_id=self.active_id))


class SpendFocusTokenEdge(SpendTokenEdge):
    token_str = 'focus'

class SpendEvadeTokenEdge(SpendTokenEdge):
    token_str = 'evade'


