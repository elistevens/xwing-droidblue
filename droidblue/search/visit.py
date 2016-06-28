from __future__ import division
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

__author__ = 'elis'

import copy
import math

from droidblue.core.edge import RandomEdge

def visitAllLeaves(callback,  state, weight=1.0):

    try:
        edge_list, activePlayer_id = state.getEdges()
    except IndexError:
        edge_list = None


    if not edge_list:
        callback(state, weight)
        return

    elif isinstance(edge_list[0], RandomEdge):
        random_edge = edge_list[0]
        subweight_sum = sum(v[0] for v in random_edge.outcome2weightSubedge_dict.values())
        for subweight, subedge in random_edge.outcome2weightSubedge_dict.values():
            if subweight:
                subedge.opportunity_list = random_edge.opportunity_list
                child_state = subedge.getExactState(state)

                visitAllLeaves(callback, child_state, weight * subweight / subweight_sum)

    else:
        for edge in edge_list:
            child_state = edge.getExactState(state)

            visitAllLeaves(callback, child_state, weight)
