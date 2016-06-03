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


totalStates_count = 0
depthStates_count = 0
leafStates_count = 0
skippedStates_count = 0

def findBestScore_minmax(state, score_cls, depth=0, depth_max=4):
    # assert depth <= depth_max
    global totalStates_count, depthStates_count, leafStates_count, skippedStates_count

    try:
        edge_list, activePlayer_id = state.getEdges()
    except IndexError:
        leafStates_count += 1
        return score_cls(state), state.fastforward_list, True

    if depth == 0:
        totalStates_count = 0
        depthStates_count = 0
        leafStates_count = 0
        skippedStates_count = 0
    elif depth > depth_max:
        # log.info("Hit depth max...")
        depthStates_count += 1
        skippedStates_count += len(edge_list)
        return score_cls(state), state.fastforward_list, True
    elif len(edge_list) == 0:
        leafStates_count += 1
        return score_cls(state), state.fastforward_list, True

    totalStates_count += 1

    if isinstance(edge_list[0], RandomEdge):
        assert len(edge_list) == 1, repr(edge_list)
        random_edge = edge_list[0]

        scoreWeight_list = []
        for weight, subedge in random_edge.outcome2weightSubedge_dict.values():
            subedge.opportunity_list = random_edge.opportunity_list
            sub_state = subedge.getExactState(state)
            sub_score, _, _ = findBestScore_minmax(sub_state, score_cls, depth+1, depth_max)

            scoreWeight_list.append((sub_score, weight))

        return score_cls.averageScores(scoreWeight_list), state.fastforward_list + [random_edge], False

    else:
        edge = edge_list.pop(0)
        child_state = edge.getExactState(state, count=len(edge_list))

        best_score, childEdge_list, bestIsDeterministic_bool = \
            findBestScore_minmax(child_state, score_cls, depth+1, depth_max)
        bestEdge_list = state.fastforward_list + [edge] + childEdge_list

        for edge in edge_list:
            child_state = edge.getExactState(state, count=len(edge_list))

            child_score, childEdge_list, childIsDeterministic_bool = \
                findBestScore_minmax(child_state, score_cls, depth+1, depth_max)

            if best_score is None or child_score.marginFor(activePlayer_id) > best_score.marginFor(activePlayer_id):
                best_score = child_score
                bestIsDeterministic_bool = childIsDeterministic_bool
                bestEdge_list = state.fastforward_list + [edge] + childEdge_list

        return best_score, bestEdge_list, bestIsDeterministic_bool
