import math

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


def max_value(state, game, depth, cutoff_test, eval_fn, alpha, beta):
    if cutoff_test(state, depth):
        return eval_fn(state)
    v = float('-inf')

    for (a, s) in game.successors(state):
        v = max(v, min_value(s, game, depth+1, cutoff_test, eval_fn, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(state, game, depth, cutoff_test, eval_fn, alpha, beta):
    if cutoff_test(state, depth):
        return eval_fn(state)
    v = float('inf')
    for (a, s) in game.successors(state):
        v = min(v, max_value(s, game, depth+1, cutoff_test, eval_fn, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

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

