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


def scoreListMinMax(alphaBeta_list, player_id):
    min_score = alphaBeta_list[0]
    max_score = alphaBeta_list[0]
    for ab_score in alphaBeta_list[1:]:
        if ab_score.marginFor(player_id) > max_score.marginFor(player_id):
            max_score = ab_score

        if ab_score.marginFor(player_id) < min_score.marginFor(player_id):
            min_score = ab_score

    return min_score, max_score

def findBestScore_alphabeta_dispatch(previous_id, state, score_cls, alphaBeta_list, depth, depth_max):
        try:
            edge_list = state.getEdges()
            deciding_id = state.activePlayer_id

            if previous_id is None:
                previous_id = deciding_id

        except IndexError:
            return score_cls(state), []
        else:
            if previous_id == deciding_id:
                findBestScore_alphabeta_continue(state, score_cls, alphaBeta_list, depth+1, depth_max)
            else:
                findBestScore_alphabeta_impl(state, score_cls, alphaBeta_list, depth+1, depth_max)





def findBestScore_alphabeta_impl(state, score_cls, alphaBeta_list, depth, depth_max):
    pass

def findBestScore_alphabeta_continue(state, score_cls, alphaBeta_list, depth, depth_max):
    pass

def findBestScore_alphabeta(state, score_cls, alphaBeta_list=None, depth=0, depth_max=100):
    # assert depth <= depth_max
    global totalStates_count

    if alphaBeta_list is None:
        alphaBeta_list = []
        for player_id in range(state.const.player_count):
            init_list = [0] * state.const.player_count

            alphaBeta_list.append(score_cls(None, init_list, _lossFor=player_id))
    else:
        # Shallow copy is okay, since we don't modify the score objects
        alphaBeta_list = alphaBeta_list[:]

    best_score = None
    bestEdge_list = []

    if depth > depth_max:
        log.info("Hit depth max...")
        best_score = score_cls(state)
    else:
        if depth == 0:
            totalStates_count = 0
        totalStates_count += 1

        try:
            edge_list = state.getEdges()
            deciding_id = state.activePlayer_id
        except IndexError:
            best_score = score_cls(state)
        else:
            # best_score = min
            min_score, max_score = scoreListMinMax(alphaBeta_list, deciding_id)
            best_score = min_score

            # for each child of n
            #     child_score := minimax (child,d-1,...,...)
            #     if child_score > best_score
            #         best_score = child_score
            #     if best_score > max return max
            # return best_score

            for edge in edge_list:
                child_state = edge.getExactState(state)

                # print len(alphaBeta_list), deciding_id
                
                alphaBeta_list[deciding_id] = best_score

                child_score, childEdge_list, childDeciding_id = findBestScore_alphabeta(child_state, score_cls, alphaBeta_list, depth+1, depth_max)

                if childDeciding_id != deciding_id:
                    assert child_score.marginFor(deciding_id) >= min_score.marginFor(deciding_id), "[{}] {}, {}".format(deciding_id, child_score, min_score)
                    assert child_score.marginFor(deciding_id) <= max_score.marginFor(deciding_id), "[{}] {}, {}".format(deciding_id, child_score, max_score)

                if child_score.marginFor(deciding_id) > best_score.marginFor(deciding_id):
                    try:
                        bestEdge_list = [edge] + childEdge_list
                        best_score = child_score
                    except:
                        print best_score.individual_list, best_score.marginFor(deciding_id)
                        print child_score.individual_list, child_score.marginFor(deciding_id)
                        print edge
                        print bestEdge_list
                        raise


                if best_score.marginFor(deciding_id) > max_score.marginFor(deciding_id):
                    return max_score, None

                # alpha_score = alphaBeta_list[deciding_id]
                # if best_score.marginFor(deciding_id) > alpha_score.marginFor(deciding_id):
                #     alpha_score = alphaBeta_list[deciding_id] = best_score
                #
                # beta_score = None
                # beta_id = None
                # for contender_id, contender_score in enumerate(alphaBeta_list):
                #     if contender_id == deciding_id:
                #         continue
                #
                #     if beta_score is None:
                #         beta_score = contender_score
                #         beta_id = contender_id
                #
                #     elif contender_score.marginFor(deciding_id) > beta_score.marginFor(deciding_id):
                #         beta_score = contender_score
                #         beta_id = contender_id
                #
                # alphaBeta_list[beta_id] = beta_score
                #
                # if alpha_score.marginFor(deciding_id) > beta_score.marginFor(deciding_id):
                #     return beta_score, bestEdge_list

    return best_score, bestEdge_list




def max_value(state, game, depth, cutoff_test, eval_fn, alpha, beta):
    if cutoff_test(state, depth):
        return eval_fn(state)
    v = float('-inf') ### FIXME

    for (a, s) in game.successors(state):
        v = max(v, min_value(s, game, depth+1, cutoff_test, eval_fn, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(state, game, depth, cutoff_test, eval_fn, alpha, beta):
    if cutoff_test(state, depth):
        return eval_fn(state)

    v = float('inf') ### FIXME

    for (a, s) in game.successors(state):
        v = min(v, max_value(s, game, depth+1, cutoff_test, eval_fn, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def argmax(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    """
    best = seq[0]
    best_score = fn(best)

    for x in seq:
        x_score = fn(x)
        if x_score > best_score:
            best, best_score = x, x_score
    return best

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)



    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    action, state = argmax(game.successors(state),
                           lambda ((a, s)): min_value(s, game, 0, cutoff_test, eval_fn, float('-inf'), float('inf')))
    return action

