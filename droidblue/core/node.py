import copy
import math
import random
import re
import uuid

from typing import NewType, Optional, Dict, List, Tuple

import numpy as np

from ..util import Jsonable, FancyRepr

from ..logging_config import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


PlayerId = NewType('PlayerId', int)
PilotId = NewType('PilotId', int)


class EdgeAbc(Jsonable, FancyRepr):
    def __init__(self, random_wt: Optional[float] = None):
        self.random_wt = random_wt

    def updateState(self, state: 'StateAbc') -> None:
        raise NotImplementedError()

    def updateMaskedState(self, state: 'StateAbc') -> None:
        raise NotImplementedError()

    def getHiddenKey(self) -> str:
        return ''

    def getRevealKey(self) -> str:
        return ''
    
    def mctsChildKey(self):
        return None


class MctsHiddenEdge(EdgeAbc):
    def __init__(self, edges: List[EdgeAbc], key=None):
        super().__init__()
        self.edges: List[EdgeAbc] = edges
        self.key = edges[0].getHiddenKey()

    def updateState(self, state: 'StateAbc') -> None:
        self.edges[0].updateMaskedState(state)

    # def isHidden(self) -> bool:
    #     return True


class MctsRevealEdge(EdgeAbc):
    def __init__(self, hidden_edge: EdgeAbc, reveal_edge: EdgeAbc, random_wt: Optional[float]):
        super().__init__(random_wt=random_wt)
        
        self.hidden_edge: EdgeAbc = hidden_edge
        self.reveal_edge: EdgeAbc = reveal_edge

    def updateState(self, state: 'StateAbc') -> None:
        self.hidden_edge.updateState(state)
        self.reveal_edge.updateState(state)

    # def isReveal(self) -> bool:
    #     return True

    def mctsChildKey(self):
        return self.hidden_edge.mctsChildKey()


class AiAbc(object):
    exploit_wt = 1.0
    explore_wt = 2.0 ** 0.5
    predictedScore_wt = 1.0

    expand_minPlayouts = 10
    expand_randomChance = 0.1
    
    def getScores(self, state: 'StateAbc') -> List[float]:
        raise NotImplementedError()
    
    def mctsPlayout_pickEdge(self, edges: List[EdgeAbc], player_id: PlayerId) -> EdgeAbc:
        raise NotImplementedError()

    def mctsPlayout_predictScores(self, state: 'StateAbc') -> List[float]:
        raise NotImplementedError()

    def mctsPlayout_shouldExpandChildren(self, node: 'MctsNode') -> bool:
        if node.mctsChild_list:
            return False

        if not node.outgoingEdges:
            return False

        if node.mctsPlayout_count < self.expand_minPlayouts * len(node.outgoingEdges):
            return False

        if not random.random() < self.expand_randomChance:
            return False

        return True

    def mctsPlayout_shouldTrustMinimaxScores(self, node) -> bool:
        return False

    def mctsNodeSortValue(
            self,
            mcts_node: 'MctsNode',
            parentPlayouts_count: int,
        ) -> float:
        return sum(self.mctsNodeSortValue_terms(mcts_node, parentPlayouts_count)[:3])

    def mctsNodeSortValue_terms(
            self,
            mcts_node: 'MctsNode',
            parentPlayouts_count: int,
        ) -> List[float]:
        # Note this is in a different order from the terms on https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
        # also adds a predicted initial value that decays with plays

        exploit_term = self.exploit_wt * mcts_node.mctsMinimax_scores[mcts_node.state.activePlayer_id]

        prediction_term = self.predictedScore_wt \
                          * mcts_node.mctsPredicted_scores[mcts_node.state.activePlayer_id] \
                          / ((self.predictedScore_wt + mcts_node.mctsPlayout_count) or 1)

        explore_term = self.explore_wt \
                       * math.sqrt(math.log2(parentPlayouts_count or 1)
                                   / (mcts_node.mctsPlayout_count or 1))

        return [exploit_term, prediction_term, explore_term, mcts_node.mctsPlayout_count]

    def mctsPlayout_getOutgoingEdges(self, state: 'StateAbc') -> List[EdgeAbc]:
        edges = state.getOutgoingEdges()

        # log.debug([state.isMasked, edges])

        if edges and state.isMasked:
            hidden_list = [e.getHiddenKey() for e in edges]
            reveal_list = [e.getRevealKey() for e in edges]
            assert any(hidden_list) == all(hidden_list), repr(hidden_list)
            assert any(reveal_list) == all(reveal_list), repr(reveal_list)

            # log.debug([hidden_list, reveal_list, edges])

            if any(hidden_list):
                edges = self.mctsPlayout_replaceHiddenEdges(edges, state)

            elif any(reveal_list):
                assert len(edges) == 1
                edges = self.mctsPlayout_replaceRevealEdges(edges)

        return edges

    # Expected that this will have to be overridden for dials
    def mctsPlayout_replaceHiddenEdges(self, edges: List[EdgeAbc], state: 'StateAbc') -> List[EdgeAbc]:
        hidden_edge = MctsHiddenEdge(edges)

        self.__dict__.setdefault('key2hiddenEdges', {})[hidden_edge.key] = edges

        # log.debug([self.key2hiddenEdges])

        return [hidden_edge]

    def mctsPlayout_replaceRevealEdges(self, edges: List[EdgeAbc]) -> List[EdgeAbc]:
        # log.debug([edges])

        key = edges[0].getRevealKey()
        hidden_edges = self.__dict__.setdefault('key2hiddenEdges', {})[key]

        reveal_edges = [MctsRevealEdge(he, edges[0], random_wt=he.random_wt) for he in hidden_edges]

        return reveal_edges




class StateAbc(Jsonable):
    cloneSkip_set = set()
    cloneKeep_set = set()

    def __init__(self, readonly: bool=True, isMasked: bool=False):
        self.readonly = readonly
        self.isMasked = isMasked

    @property
    def activePlayer_id(self) -> PlayerId:
        raise NotImplementedError()

    def getPlayerCount(self) -> int:
        raise NotImplementedError()

    def maskHiddenInfo(self, player_id: PlayerId) -> 'StateAbc':
        raise NotImplementedError()

    def getOutgoingEdges(self) -> List[EdgeAbc]:
        raise NotImplementedError()


    def __eq__(self, other):
        if type(self) != type(other):
            log.debug("type({}) != type({})".format(type(self), type(other)))
            return False

        if self.__dict__.keys() != other.__dict__.keys():
            log.debug("keys({}) != keys({})".format(self.__dict__.keys(), other.__dict__.keys()))
            return False

        for k,v in self.__dict__.items():
            o = other.__dict__[k]
            if type(v) != type(o):
                log.debug("{}: type({}) != type({})".format(k, type(v), type(o)))
                return False

            if isinstance(v, np.ndarray):
                if not (v == o).all():
                    log.debug(v)
                    log.debug(o)
                    return False
            else:
                if v != o:
                    log.debug("{}: {} != {}".format(k, v, o))
                    return False

        return True


    # def clone(self, **kwargs):
    def clone(self, readonly: bool=None) -> 'StateAbc':
        other = copy.copy(self)

        for k, v in list(self.__dict__.items()):
            if k not in self.cloneKeep_set:
                other.__dict__[k] = copy.deepcopy(v)

        if readonly is not None:
            other.readonly = readonly

        return other

    def applyEdge(self, edge: EdgeAbc) -> 'StateAbc':
        if self.readonly:
            new_state = self.clone()
        else:
            new_state = self

        # log.debug([edge])

        edge.updateState(new_state)

        return new_state

    # def assignDial(self, ship_id, move):
    #     raise NotImplementedError()
    #
    # def aiPlayout(self, ai_list):
    #     raise NotImplementedError()

# class HiddenInfoEstimateAbc(Jsonable):
#     def isValidForState(self, state: StateAbc) -> bool:
#         raise NotImplementedError()

class MctsNode(Jsonable, FancyRepr):
    # state_cls = StateAbc
    mctsKeepDepth_int = 3
    mctsEstimateWeight_float = 10.0

    @classmethod
    def fromStartState(
                cls, state: StateAbc,
            ) -> 'MctsNode':
        edges = state.getOutgoingEdges()

        return cls(
            None, state, edges,
        )

    @classmethod
    def fromPreviousState(
                cls, previous_state: StateAbc, incoming_edge:EdgeAbc,
                mctsPlayer_id: PlayerId = None,
                mctsPlayer_ai: Optional[AiAbc] = None,
                fastforward:bool = True,
            ) -> 'MctsNode':
        state = previous_state.applyEdge(incoming_edge)

        if mctsPlayer_ai:
            outgoingEdges = mctsPlayer_ai.mctsPlayout_getOutgoingEdges(state)
        else:
            outgoingEdges = state.getOutgoingEdges()

        incomingEdges = [incoming_edge]
        while fastforward and len(outgoingEdges) == 1:
            # log.debug(['fastforwarding', outgoingEdges])
            incomingEdges.append(outgoingEdges[0])
            state = state.applyEdge(outgoingEdges[0])

            if mctsPlayer_ai:
                outgoingEdges = mctsPlayer_ai.mctsPlayout_getOutgoingEdges(state)
            else:
                outgoingEdges = state.getOutgoingEdges()

        if mctsPlayer_ai:
            mctsPredicted_scores = mctsPlayer_ai.mctsPlayout_predictScores(state)
            mctsCurrent_scores = mctsPlayer_ai.getScores(state)
        else:
            mctsPredicted_scores = None
            mctsCurrent_scores = None

        return cls(
            incomingEdges, state, outgoingEdges,
            mctsPlayer_id=mctsPlayer_id,
            mctsPredicted_scores=mctsPredicted_scores,
            mctsCurrent_scores=mctsCurrent_scores,
        )

    def __init__(
            self, incomingEdges: Optional[List[EdgeAbc]], state: StateAbc, outgoingEdges: List[EdgeAbc],
            mctsPlayer_id: PlayerId = None,

            mctsPredicted_scores: Optional[List[float]] = None,

            # Only for fromJson
            mctsChild_list: List['MctsNode'] = None,
            mctsPlays_count: int = 0,

            mctsCurrent_scores: List[float] = None,
            mctsSimulation_scores: List[float] = None,
            mctsMinimax_scores: List[float] = None,

    ):
        self.incomingEdges: List[EdgeAbc] = incomingEdges
        self.state: StateAbc = state
        self.outgoingEdges: List[EdgeAbc] = outgoingEdges

        self.mctsPlayer_id = mctsPlayer_id
        self.mctsChild_list = mctsChild_list
        self.mctsPlayout_count = mctsPlays_count

        self.mctsPredicted_scores = mctsPredicted_scores or [0.0 for _ in range(state.getPlayerCount())]
        self.mctsCurrent_scores = mctsCurrent_scores or [0.0 for _ in range(state.getPlayerCount())]
        self.mctsSimulation_scores = mctsSimulation_scores or [0.0 for _ in range(state.getPlayerCount())]
        self.mctsMinimax_scores = mctsMinimax_scores or [0.0 for _ in range(state.getPlayerCount())]






    def __getitem__(self, key):
        for child_node in self.mctsChild_list:
            if child_node.incomingEdges[0].mctsChildKey() == key:
                return child_node

    def createMctsMaskedNode(
                self, mctsPlayer_id: PlayerId, mctsPlayer_ai: AiAbc,
            ) -> 'MctsNode':
        mctsMaskedInfo_state = self.state.maskHiddenInfo(mctsPlayer_id)

        edge_list = mctsPlayer_ai.mctsPlayout_getOutgoingEdges(mctsMaskedInfo_state)
        mctsPredicted_scores = mctsPlayer_ai.mctsPlayout_predictScores(mctsMaskedInfo_state)
        mctsCurrent_scores = mctsPlayer_ai.getScores(self.state)

        # log.debug(edge_list)

        return type(self)(
            None, mctsMaskedInfo_state, edge_list,
            mctsPlayer_id=mctsPlayer_id,
            mctsPredicted_scores=mctsPredicted_scores,
            mctsCurrent_scores=mctsCurrent_scores,
        )

    def mctsPlayout(self, ai):
        assert self.mctsPlayer_id is not None
        assert self.state.isMasked

        if ai.mctsPlayout_shouldExpandChildren(self):
            # Expansion of this node into all child nodes
            self.mctsChild_list = [
                self.fromPreviousState(self.state, edge, mctsPlayer_id=self.mctsPlayer_id, mctsPlayer_ai=ai)
                for edge in self.outgoingEdges
            ]

        if self.mctsChild_list:
            # Selection of already expanded nodes
            selected = self._mctsPlayout_selectChildNode(ai)
            simulation_scores = selected.mctsPlayout(ai)

        else:
            # Otherwise we're at a leaf of our simulation tree (not the game tree, just our mcts nodes),
            # and should do a random playout from here
            if self.outgoingEdges:
                simulation_state = self.state.clone(readonly=False)

                next_edges: List[EdgeAbc] = self.outgoingEdges
                while next_edges:
                    edge = ai.mctsPlayout_pickEdge(next_edges, simulation_state.activePlayer_id)
                    edge.updateState(simulation_state)
                    next_edges = ai.mctsPlayout_getOutgoingEdges(simulation_state)
            else:
                simulation_state = self.state

            # Round-terminal state reached, so at a leaf of the game state for this round
            simulation_scores = ai.getScores(simulation_state)

        self._mctsPlayout_updateScores(ai, simulation_scores)

        return simulation_scores


    def _mctsPlayout_selectChildNode(self, ai: AiAbc):
        if self.mctsChild_list[0].incomingEdges[0].random_wt is not None:
            random.shuffle(self.mctsChild_list)
            self.mctsChild_list.sort(key=lambda n: n.incomingEdges[0].random_wt * random.random())
        else:
            self.mctsChild_list.sort(key=lambda n: ai.mctsNodeSortValue(n, self.mctsPlayout_count))

        for child_node in self.mctsChild_list:
            if child_node.mctsPlayout_count == 0:
                return child_node

        return self.mctsChild_list[-1]


    def _mctsPlayout_updateScores(self, ai: AiAbc, simulation_scores: List[float]):
        oldAvgUpdate_frac = self.mctsPlayout_count / (self.mctsPlayout_count + 1)
        newAvg_frac = 1 / (self.mctsPlayout_count + 1)

        for i, score in enumerate(simulation_scores):
            self.mctsSimulation_scores[i] *= oldAvgUpdate_frac
            self.mctsSimulation_scores[i] += score * newAvg_frac

        self.mctsPlayout_count += 1

        if self.mctsChild_list and ai.mctsPlayout_shouldTrustMinimaxScores(self):
            if self.outgoingEdges[0].random_wt:
                random_sum = sum(child_node.incomingEdges[0].random_wt for child_node in self.mctsChild_list)
                minimax_scores = [0.0 for _ in self.mctsMinimax_scores]
                for child_node in self.mctsChild_list:
                    child_scores = child_node.mctsMinimax_scores

                    for i in range(len(minimax_scores)):
                        minimax_scores[i] += child_scores[i] * child_node.incomingEdges[0].random_wt / random_sum

            else:
                player_id = self.state.activePlayer_id
                minimax_scores = self.mctsChild_list[0].mctsMinimax_scores
                for child_node in self.mctsChild_list:
                    child_scores = child_node.mctsMinimax_scores
                    if child_scores[player_id] > minimax_scores[player_id]:
                        minimax_scores = child_scores

            self.mctsMinimax_scores = list(minimax_scores)
        else:
            self.mctsMinimax_scores = list(self.mctsSimulation_scores)

    # def mctsSimulationScore(self) -> Optional[List[float]]:
    #     return [s / (self.mctsPlayout_count or 1) for s in self.mctsPlayout_scores]
    #
    # def mctsOptimalScore(self) -> Optional[List[float]]:
    #     player_id = self.state.activePlayer_id
    #     high_scores = self.mctsSimulationScore()
    #
    #     if not self.outgoingEdges:
    #         # This means that the node is terminal and the sim score is exact, as per the AI
    #         return high_scores
    #
    #     elif self.outgoingEdges[0].random_wt:
    #         # this means that the child node is random
    #         if self.mctsChild_list:
    #             random_sum = sum(child_node.incomingEdges[0].random_wt for child_node in self.mctsChild_list)
    #             random_scores = [0.0 for _ in high_scores]
    #             for child_node in self.mctsChild_list:
    #                 child_scores = child_node.mctsOptimalScore()
    #
    #                 if child_scores:
    #                     for i in range(len(high_scores)):
    #                         random_scores[i] += child_scores[i] * child_node.incomingEdges[0].random_wt / random_sum
    #                 else:
    #                     # If a child doesn't have a score, the avg random score will be off anyway
    #                     break
    #             else:
    #                 # if we don't break, we guess that random_scores is a reasonable guess
    #                 high_scores = random_scores
    #
    #         # otherwise we just accept the simulated average through this node
    #         return high_scores
    #
    #     elif self.mctsChild_list:
    #         # If we have visited the child node enough to expand it out
    #         # ...or if the child node is terminal
    #         # then we can trust the score from that child node to be a decent approximation
    #         for child_node in self.mctsChild_list:
    #             child_scores = child_node.mctsOptimalScore()
    #             if child_scores and child_scores[player_id] > high_scores[player_id]:
    #                 high_scores = child_scores
    #
    #     return high_scores

    def mctsPrintTree(self, ai: AiAbc, parentPlayouts_count: int = 0, indent: str = '', depth: int = 99):
        if depth <= 0:
            return

        if self.incomingEdges:
            edge = self.incomingEdges[0]
            print(f"{indent}--{edge}")
            for edge in self.incomingEdges[1:]:
                print(f"{indent} -{edge}")

        print(f"{indent}  <>"
              + f" mnmx [{', '.join(['{:.3f}'.format(x) for x in self.mctsMinimax_scores])}]"
              + f" simu [{', '.join(['{:.3f}'.format(x) for x in self.mctsSimulation_scores])}]"
              + f" [{', '.join(['{:.3f}'.format(x) for x in ai.mctsNodeSortValue_terms(self, parentPlayouts_count)])}]"
              + f" {self.state}"
              )

        if self.mctsChild_list:
            for child_node in sorted(self.mctsChild_list, reverse=True, key=lambda n: n.mctsMinimax_scores[n.state.activePlayer_id]):
                child_node.mctsPrintTree(ai, self.mctsPlayout_count, indent=indent + '    ', depth=depth - 1)

        print()
