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

    def updateState(self, state: 'GuessDiceState') -> None:
        setattr(state, self.nth + '_die', self.num)
        setattr(state, self.nth + '_rolled', True)

        # assert False

    def updateMaskedState(self, state: 'GuessDiceState') -> None:
        setattr(state, self.nth + '_rolled', True)

    def getHiddenKey(self):
        return self.nth

    def mctsChildKey(self):
        return self.num

class GuessNumberEdge(EdgeAbc):
    def __init__(self, guess: int, nth: str):
        super().__init__()
        self.guess: int = guess
        self.nth: str = nth
        
    def updateState(self, state: 'GuessDiceState'):
        setattr(state, self.nth + '_guess', self.guess)

    def mctsChildKey(self):
        return self.guess


class RevealDiceEdge(EdgeAbc):
    def __init__(self, nth: str):
        super().__init__()
        self.nth: str = nth

    def updateState(self, state: 'GuessDiceState'):
        setattr(state, self.nth + '_revealed', True)

    def getRevealKey(self):
        return self.nth


class GuessDiceAi(AiAbc):
    exploit_wt = 0.01
    explore_wt = 2.0 ** 0.5
    predictedScore_wt = 1.0

    def getScores(self, state: 'GuessDiceState') -> List[float]:
        if state.first_revealed and state.second_revealed:
            guess = state.first_guess + state.second_guess
            dice = state.first_die + state.second_die
            if guess <= dice:
                return [guess]

        return [0.0]
    
    def mctsPlayout_pickEdge(self, edges: List[EdgeAbc], player_id: PlayerId, _debug_ndx: int = None) -> EdgeAbc:
        if _debug_ndx is None:
            return random.choice(edges)
        return edges[_debug_ndx]

    def mctsPlayout_predictScores(self, state: 'GuessDiceState') -> List[float]:
        # if state.first_guess:
        #     return [state.first_guess]
        return [0.0]


class GuessDiceState(StateAbc, FancyRepr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.first_rolled: bool = False
        self.first_die: int = None
        self.first_guess: int = None
        self.first_revealed: bool = False

        self.second_rolled: bool = False
        self.second_die: int = None
        self.second_guess: int = None
        self.second_revealed: bool = False

    @property
    def activePlayer_id(self) -> PlayerId:
        return PlayerId(0)

    def maskHiddenInfo(self, player_id: PlayerId) -> 'StateAbc':
        masked_state = self.clone()
        
        if not masked_state.first_revealed:
            masked_state.first_die = 0
        if not masked_state.second_revealed:
            masked_state.second_die = 0

        masked_state.isMasked = True

        return masked_state

    def getOutgoingEdges(self) -> List[EdgeAbc]:
        if not self.first_rolled:
            # assert False

            edges = []
            for i in range(1, 7):
                edges.append(RollDiceEdge(i, 'first', random_wt=1/6))
            return edges
        
        if not self.second_rolled:
            edges = []
            for i in range(1, 7):
                edges.append(RollDiceEdge(i, 'second', random_wt=1/6))
            return edges

        if self.first_guess is None:
            return [GuessNumberEdge(i, 'first') for i in range(1, 7)]
        
        if not self.first_revealed:
            return [RevealDiceEdge('first')]
        
        if self.second_guess is None:
            return [GuessNumberEdge(i, 'second') for i in range(1, 7)]
        
        if not self.second_revealed:
            return [RevealDiceEdge('second')]
        
        return []


def test_guess():
    print()

    ai = GuessDiceAi()
    start_state = GuessDiceState()
    start_node = MctsNode.fromStartState(start_state)
    mcts_node = start_node.createMctsMaskedNode(PlayerId(0), ai)


    # print(start_node.incomingEdge_list)
    # print(start_node.outgoingEdges)

    assert start_node.incomingEdge_list == None
    assert start_node.state.first_die is None
    assert type(start_node.outgoingEdges[0]) == RollDiceEdge

    assert mcts_node.incomingEdge_list == None
    assert mcts_node.state.first_die is 0
    assert type(mcts_node.outgoingEdges[0]) == MctsHiddenEdge

    for i in range(100000):
        mcts_node.mctsPlayout(ai)
        
    rollsDone_node = mcts_node.mctsChild_list[0]

    assert type(rollsDone_node.outgoingEdges[0]) == GuessNumberEdge
    
    guess3_node = rollsDone_node[3]

    print(guess3_node.state.first_guess,
          '{:.2f}'.format(guess3_node.mctsScoreAvg(0)),
          ai.mctsNodeSortValue_terms(guess3_node, rollsDone_node.mctsPlayouts_count),
          guess3_node.mctsPlayouts_count,
          rollsDone_node.mctsPlayouts_count,
          guess3_node.outgoingEdges,
    )
    print()


    score2guess = []
    for guess_node in rollsDone_node.mctsChild_list:
        print(guess_node.state.first_guess,
              '{:.2f}'.format(guess_node.mctsScoreAvg(0)),
              ai.mctsNodeSortValue_terms(guess_node, rollsDone_node.mctsPlayouts_count),
              guess_node.mctsPlayouts_count,
              rollsDone_node.mctsPlayouts_count,
              guess_node.incomingEdge_list,
        )
        print()

        score2guess.append((guess_node.mctsScoreAvg(0), guess_node.state.first_guess))

    score2guess.sort(reverse=True)
    assert [g for s,g in score2guess] == [3, 4, 2, 5, 1, 6]




    # for child_node in mcts_node.mctsChild_list:
    #     print(child_node)
    #     print(child_node.state)

    # print(mcts_node.mctsScoreSum_list)
    # print(mcts_node.mctsChild_list)

    assert False
