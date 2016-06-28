from __future__ import division
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

__author__ = 'elis'

import copy
import math

from droidblue.core.edge import RandomDiceEdge, RandomDialEdge


totalStates_count = 0
depthStates_count = 0
leafStates_count = 0
skippedStates_count = 0

def findBestScore_minmax(state, score_cls, depth=0, depth_max=4):
    # assert depth <= depth_max
    global totalStates_count, depthStates_count, leafStates_count, skippedStates_count

    if depth == 0:
        totalStates_count = 0
        depthStates_count = 0
        leafStates_count = 0
        skippedStates_count = 0

    totalStates_count += 1

    try:
        edge_list, activePlayer_id = state.getEdges()
    except IndexError:
        edge_list = None
        activePlayer_id = None

    if not edge_list or depth > depth_max:
        if not edge_list:
            leafStates_count += 1
        else:
            depthStates_count += 1

        score = score_cls(state)
        maneuvers2score_dict = {
            tuple(state.maneuver_list): score,
        }

        return score, state.fastforward_list, maneuvers2score_dict


    elif isinstance(edge_list[0], RandomDiceEdge):
        return _findBestScore_minmax_dice(state, score_cls, depth, depth_max, edge_list)


    elif isinstance(edge_list[0], RandomDialEdge):
        return _findBestScore_minmax_dial(state, score_cls, depth, depth_max, edge_list)


    else:
        best_score, bestEdge_list, best_maneuvers2score_dict = None, None, None

        for edge in edge_list:
            child_state = edge.getExactState(state, count=len(edge_list))

            child_score, childEdge_list, child_maneuvers2score_dict = \
                findBestScore_minmax(child_state, score_cls, depth+1, depth_max)

            if best_score is None or child_score.marginFor(activePlayer_id) > best_score.marginFor(activePlayer_id):
                best_score = child_score
                bestEdge_list = state.fastforward_list + [edge] + childEdge_list
                best_maneuvers2score_dict = child_maneuvers2score_dict

        return best_score, bestEdge_list, best_maneuvers2score_dict


def _findBestScore_minmax_dice(state, score_cls, depth, depth_max, edge_list):
    assert len(edge_list) == 1, repr(edge_list)
    random_edge = edge_list[0]

    scoreWeight_list = []
    avg_maneuvers2score_dict = {}
    for weight, subedge in random_edge.outcome2weightSubedge_dict.values():
        subedge.opportunity_list = random_edge.opportunity_list
        sub_state = subedge.getExactState(state)
        sub_score, _, maneuvers2score_dict = findBestScore_minmax(sub_state, score_cls, depth+1, depth_max)

        for m_tup, m_score in maneuvers2score_dict.iteritems():
            avg_maneuvers2score_dict.setdefault(m_tup, []).append((m_score, weight))

        assert set(maneuvers2score_dict) == set(avg_maneuvers2score_dict)

        scoreWeight_list.append((sub_score, weight))

    maneuvers2score_dict = {
        m_tup: score_cls.averageScores(m_list) for m_tup, m_list in avg_maneuvers2score_dict.iteritems()
    }

    return score_cls.averageScores(scoreWeight_list), state.fastforward_list + [random_edge], maneuvers2score_dict


def _findBestScore_minmax_dial(state, score_cls, depth, depth_max, edge_list):
    assert len(edge_list) == 1, repr(edge_list)
    random_edge = edge_list[0]

    scoreWeight_list = []
    all_maneuvers2score_dict = {}
    for weight, subedge in random_edge.outcome2weightSubedge_dict.values():
        subedge.opportunity_list = random_edge.opportunity_list
        sub_state = subedge.getExactState(state)
        sub_score, _, maneuvers2score_dict = findBestScore_minmax(sub_state, score_cls, depth+1, depth_max)

        assert set(maneuvers2score_dict) & set(all_maneuvers2score_dict) == set()

        scoreWeight_list.append((sub_score, weight))

    return score_cls.averageScores(scoreWeight_list), state.fastforward_list + [random_edge], all_maneuvers2score_dict
