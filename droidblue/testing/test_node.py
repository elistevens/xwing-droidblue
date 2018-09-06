import random

from typing import NewType, Optional, Dict, List, Tuple

from ..core.node import MctsNode, StateAbc, EdgeAbc, PlayerId, AiAbc, MctsHiddenEdge
from ..util import FancyRepr

from ..logging_config import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class RollDiceEdge(EdgeAbc):
    def __init__(self, num: int, nth: str, random_wt: float):
        super().__init__(random_wt=random_wt)
        self.num: int = num
        self.nth: str = nth

        # assert False

    def updateState(self, state: StateAbc) -> None:
        setattr(state, 'd' + self.nth, self.num)
        setattr(state, 'r' + self.nth, True)

        # assert False

    def updateMaskedState(self, state: StateAbc) -> None:
        setattr(state, 'r' + self.nth, True)

    def getHiddenKey(self):
        return self.nth

    def mctsChildKey(self):
        return self.num

class GuessNumberEdge(EdgeAbc):
    def __init__(self, guess: int, nth: str):
        super().__init__()
        self.guess: int = guess
        self.nth: str = nth
        
    def updateState(self, state: StateAbc):
        setattr(state, 'g' + self.nth, self.guess)

    def mctsChildKey(self):
        return self.guess


class RevealDiceEdge(EdgeAbc):
    def __init__(self, nth: str):
        super().__init__()
        self.nth: str = nth

    def updateState(self, state: StateAbc):
        setattr(state, 'v' + self.nth, True)

    def getRevealKey(self):
        return self.nth


class GuessDiceAi(AiAbc):
    exploit_wt = 0.1
    explore_wt = 10 * 2.0 ** 0.5
    predictedScore_wt = 10.0

    trustworthyPlayout_count = 10

    def getScores(self, state: StateAbc) -> List[float]:
        if state.v1 and getattr(state, 'v2', True):
            guess = state.g1 + getattr(state, 'g2', 0)
            dice = state.d1 + getattr(state, 'd2', 0)
            if guess < dice:
                # log.debug([guess])
                return [guess]

        return [0.0]
    
    def mctsPlayout_pickEdge(self, edges: List[EdgeAbc], player_id: PlayerId, _debug_ndx: int = None) -> EdgeAbc:
        if _debug_ndx is None:
            return random.choice(edges)
        return edges[_debug_ndx]

    def mctsPlayout_predictScores(self, state: StateAbc) -> List[float]:
        # if state.g1:
        #     return [state.g1]
        return [0.0]

    def mctsPlayout_shouldTrustMinimaxScores(self, node: MctsNode) -> bool:
        # return False
        return node.mctsPlayout_count > self.trustworthyPlayout_count

class PredictingGuessDiceAi(GuessDiceAi):
    def mctsPlayout_predictScores(self, state: StateAbc) -> List[float]:
        if state.g2:
            if state.g1 + state.g2 < state.d1 + 2:
                return [state.g1 + state.g2]
            else:
                return [0.0]

        if state.g1:
            return [[0,4,4,4,3,2,1][state.g1]]
        # if state.g1:
        #     return [state.g1]
        return [0.0]

class GuessOneDieState(StateAbc, FancyRepr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.r1: bool = False
        self.d1: int = None
        self.g1: int = None
        self.v1: bool = False

    @property
    def activePlayer_id(self) -> PlayerId:
        return PlayerId(0)

    def getPlayerCount(self) -> int:
        return 1

    def maskHiddenInfo(self, player_id: PlayerId) -> 'GuessOneDieState':
        masked_state = self.clone()
        
        if not masked_state.v1:
            masked_state.d1 = 0

        masked_state.isMasked = True

        return masked_state

    def getOutgoingEdges(self) -> List[EdgeAbc]:
        if not self.r1:
            edges = []
            for i in range(1, 7):
                edges.append(RollDiceEdge(i, '1', random_wt=1))
            return edges
        
        if self.g1 is None:
            return [GuessNumberEdge(i, '1') for i in range(1, 7)]
        
        if not self.v1:
            return [RevealDiceEdge('1')]
        
        return []

class GuessTwoDiceState(StateAbc, FancyRepr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.r1: bool = False
        self.d1: int = None
        self.g1: int = None
        self.v1: bool = False

        self.r2: bool = False
        self.d2: int = None
        self.g2: int = None
        self.v2: bool = False

    @property
    def activePlayer_id(self) -> PlayerId:
        return PlayerId(0)

    def getPlayerCount(self) -> int:
        return 1

    def maskHiddenInfo(self, player_id: PlayerId) -> 'GuessTwoDiceState':
        masked_state = self.clone()

        if not masked_state.v1:
            masked_state.d1 = 0
        if not masked_state.v2:
            masked_state.d2 = 0

        masked_state.isMasked = True

        return masked_state

    def getOutgoingEdges(self) -> List[EdgeAbc]:
        if not self.r1:
            # assert False

            edges = []
            for i in range(1, 7):
                edges.append(RollDiceEdge(i, '1', random_wt=1/6))
            return edges

        if not self.r2:
            edges = []
            for i in range(1, 7):
                edges.append(RollDiceEdge(i, '2', random_wt=1/6))
            return edges

        if self.g1 is None:
            return [GuessNumberEdge(i, '1') for i in range(1, 7)]

        if not self.v1:
            return [RevealDiceEdge('1')]

        if self.g2 is None:
            return [GuessNumberEdge(i, '2') for i in range(1, 7)]

        if not self.v2:
            return [RevealDiceEdge('2')]

        return []


def test_guess_one():
    ai = GuessDiceAi()
    start_state = GuessOneDieState()
    start_node = MctsNode.fromStartState(start_state)
    mcts_node = start_node.createMctsMaskedNode(PlayerId(0), ai)

    assert start_node.incomingEdges == None
    assert start_node.state.d1 is None
    assert type(start_node.outgoingEdges[0]) == RollDiceEdge

    assert mcts_node.incomingEdges == None
    assert mcts_node.state.d1 is 0
    assert type(mcts_node.outgoingEdges[0]) == MctsHiddenEdge

    mcts_node.mctsPlayout(ai)
    print("start")
    mcts_node.mctsPrintTree(ai, depth=10)

    for i in range(1000):
        mcts_node.mctsPlayout(ai)
    print("select playout")
    mcts_node.mctsPrintTree(ai, depth=10)

    for i in range(10000):
        mcts_node.mctsPlayout(ai)
    print("final playout")
    mcts_node.mctsPrintTree(ai, depth=10)

    rollsDone_node = mcts_node.mctsChild_list[0]

    assert type(rollsDone_node.outgoingEdges[0]) == GuessNumberEdge
    
    guess6_node = rollsDone_node[6]

    assert guess6_node.mctsMinimax_scores[0] == 0

    guess3_node = rollsDone_node[3]
    guess3_node.mctsPrintTree(ai, depth=3)
    reveal31_node = guess3_node[1]
    reveal31_edge = reveal31_node.incomingEdges[0]
    assert reveal31_edge.hidden_edge.num == 1
    assert reveal31_edge.random_wt == 1
    
    guess4_node = rollsDone_node[4]
    print('guess4_node')
    guess4_node.mctsPrintTree(ai, depth=4)
    reveal41_node = guess4_node[1]
    reveal41_edge = reveal41_node.incomingEdges[0]
    assert reveal41_edge.hidden_edge.num == 1
    assert reveal41_edge.random_wt == 1

    score2guess = []
    for guess_node in rollsDone_node.mctsChild_list:
        score2guess.append((guess_node.mctsMinimax_scores[0], guess_node.state.g1))

    score2guess.sort(reverse=True)
    for s, g in score2guess:
        log.debug([s, g])
    assert score2guess[0][1] == 3
    assert score2guess[-1][1] == 6
    assert score2guess[-1][0] == 0

    assert 1.4 <= score2guess[0][0] <= 1.6
    assert 1.25 <= score2guess[1][0] <= 1.4
    assert 1.25 <= score2guess[2][0] <= 1.4
    assert 0.75 <= score2guess[3][0] <= 0.9
    assert 0.75 <= score2guess[4][0] <= 0.9

    # assert False


def test_guess_two():
    print()

    for g1 in range(1, 7):
        g1s = 0.0
        for d1 in range(1, 7):
            m = 0.0
            for g2 in range(1, 7):
                g2s = 0.0
                for r2 in range(1, 7):
                    if g1+g2 < d1+r2:
                        # g1s += (g1+g2) / (6**3)
                        g2s += (g1+g2) / 6
                m = max(m, g2s)
                # print(g1, d1, g2, '  s', f'{g2s:.2f}')
            g1s += m / 6
            # print()
        print(g1, g1s)
        # print()


    ai = GuessDiceAi()
    start_state = GuessTwoDiceState()
    start_node = MctsNode.fromStartState(start_state)
    mcts_node = start_node.createMctsMaskedNode(PlayerId(0), ai)

    assert start_node.incomingEdges == None
    assert start_node.state.d1 is None
    assert type(start_node.outgoingEdges[0]) == RollDiceEdge

    assert mcts_node.incomingEdges == None
    assert mcts_node.state.d1 is 0
    assert type(mcts_node.outgoingEdges[0]) == MctsHiddenEdge

    for i in range(50000):
        mcts_node.mctsPlayout(ai)

    rollsDone_node = mcts_node.mctsChild_list[0]
    assert type(rollsDone_node.outgoingEdges[0]) == GuessNumberEdge

    g1 = rollsDone_node[1]
    g1v1 = g1[1]
    g1v1g1 = g1v1[1]

    # print('g1')
    # g1.mctsPrintTree(ai, depth=3)

    print('g1v1')
    g1v1.mctsPrintTree(ai, depth=3)

    score2guess = []
    for guess_node in g1v1.mctsChild_list:
        score2guess.append((guess_node.mctsMinimax_scores[0], guess_node.state.g2))

    score2guess.sort(reverse=True)
    for s, g in score2guess:
        log.debug([s, g])
    assert score2guess[-1][1] == 6
    assert score2guess[-1][0] == 0

    assert 1.9 <= score2guess[0][0] <= 2.1
    assert 1.9 <= score2guess[1][0] <= 2.1
    assert 1.6 <= score2guess[2][0] <= 1.75
    assert 1.6 <= score2guess[3][0] <= 1.75
    assert 0.9 <= score2guess[4][0] <= 1.1

    # print('g1v1g1')
    # g1v1g1.mctsPrintTree(ai, depth=3)

    score2guess = []
    for guess_node in rollsDone_node.mctsChild_list:
        score2guess.append((guess_node.mctsMinimax_scores[0], guess_node.state.g1))

    score2guess.sort(reverse=True)
    for s, g in score2guess:
        log.debug([s, g])

    assert [g for s, g in score2guess][3:] == [4, 5, 6]

    assert 3.8 <= score2guess[0][0] <= 3.9
    assert 3.8 <= score2guess[1][0] <= 3.9
    assert 3.8 <= score2guess[2][0] <= 3.9
    assert 3.7 <= score2guess[3][0] <= 3.8
    assert 3.4 <= score2guess[4][0] <= 3.6
    assert 2.8 <= score2guess[5][0] <= 3.0

    # assert False

def test_guess_two_predicting():
    print()

    for g1 in range(1, 7):
        g1s = 0.0
        for d1 in range(1, 7):
            m = 0.0
            for g2 in range(1, 7):
                g2s = 0.0
                for r2 in range(1, 7):
                    if g1+g2 < d1+r2:
                        # g1s += (g1+g2) / (6**3)
                        g2s += (g1+g2) / 6
                m = max(m, g2s)
                # print(g1, d1, g2, '  s', f'{g2s:.2f}')
            g1s += m / 6
            # print()
        print(g1, g1s)
        # print()


    ai = PredictingGuessDiceAi()
    start_state = GuessTwoDiceState()
    start_node = MctsNode.fromStartState(start_state)
    mcts_node = start_node.createMctsMaskedNode(PlayerId(0), ai)

    assert start_node.incomingEdges == None
    assert start_node.state.d1 is None
    assert type(start_node.outgoingEdges[0]) == RollDiceEdge

    assert mcts_node.incomingEdges == None
    assert mcts_node.state.d1 is 0
    assert type(mcts_node.outgoingEdges[0]) == MctsHiddenEdge

    for i in range(30000):
        mcts_node.mctsPlayout(ai)

    rollsDone_node = mcts_node.mctsChild_list[0]
    assert type(rollsDone_node.outgoingEdges[0]) == GuessNumberEdge

    g1 = rollsDone_node[1]
    g1v1 = g1[1]
    g4 = rollsDone_node[4]
    g4v1 = g4[1]
    g4v1g1 = g4v1[1]

    print('rollsDone_node')
    rollsDone_node.mctsPrintTree(ai, depth=2)

    # print('g4')
    # g4.mctsPrintTree(ai, depth=3)

    print('g1v1')
    g1v1.mctsPrintTree(ai, depth=3)

    score2guess = []
    for guess_node in g1v1.mctsChild_list:
        score2guess.append((guess_node.mctsMinimax_scores[0], guess_node.state.g2))

    score2guess.sort(reverse=True)
    for s, g in score2guess:
        log.debug([s, g])
    assert score2guess[-1][1] == 6
    assert score2guess[-1][0] == 0

    assert 1.9 <= score2guess[0][0] <= 2.1
    assert 1.9 <= score2guess[1][0] <= 2.1
    assert 1.5 <= score2guess[2][0] <= 1.85
    assert 1.5 <= score2guess[3][0] <= 1.85
    assert 0.8 <= score2guess[4][0] <= 1.2

    # print('g1v1g1')
    # g1v1g1.mctsPrintTree(ai, depth=3)

    score2guess = []
    for guess_node in rollsDone_node.mctsChild_list:
        score2guess.append((guess_node.mctsMinimax_scores[0], guess_node.state.g1))

    score2guess.sort(reverse=True)
    for s, g in score2guess:
        log.debug([s, g])

    assert set([g for s, g in score2guess][3:]) == set([4, 5, 6])

    assert 3.8 <= score2guess[0][0] <= 3.9
    assert 3.8 <= score2guess[1][0] <= 3.9
    assert 3.8 <= score2guess[2][0] <= 3.9
    assert 3.7 <= score2guess[3][0] <= 3.8
    assert 3.4 <= score2guess[4][0] <= 3.6
    assert 2.8 <= score2guess[5][0] <= 3.0

    # assert False
