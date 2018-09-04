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


class AiAbc(object):
    exploit_wt = 1.0
    explore_wt = 2.0 ** 0.5
    predictedScore_wt = 1.0
    
    def getScores(self, state: 'StateAbc') -> List[float]:
        raise NotImplementedError()
    
    def mctsPlayout_pickEdge(self, edges: List[EdgeAbc], player_id: PlayerId) -> EdgeAbc:
        raise NotImplementedError()

    def mctsPlayout_predictScore(self, state: 'StateAbc') -> float:
        return 0.0

    def mctsNodeSortValue(
            self,
            mcts_node: 'MctsNode',
            parentPlayouts_count: int,
        ) -> float:
        return sum(self.mctsNodeSortValue_terms(mcts_node, parentPlayouts_count))

    def mctsNodeSortValue_terms(
            self,
            mcts_node: 'MctsNode',
            parentPlayouts_count: int,
        ) -> List[float]:
        # Note this is in a different order from the terms on https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
        # also adds a predicted initial value that decays with plays

        exploit_term = self.exploit_wt * (mcts_node.mctsScoreAvg(mcts_node.state.activePlayer_id) or 0.0)

        prediction_term = self.predictedScore_wt \
                          * mcts_node.mctsPredicted_score \
                          / ((self.predictedScore_wt + mcts_node.mctsPlayouts_count) or 1)

        explore_term = self.explore_wt \
                       * math.sqrt(math.log2(parentPlayouts_count or 1)
                                   / (mcts_node.mctsPlayouts_count or 1))

        return [exploit_term, prediction_term, explore_term]

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
                mctsPrevious:'Optional[MctsNode]'=None,
                fastforward:bool=True,
            ) -> 'MctsNode':
        state = previous_state.applyEdge(incoming_edge)

        mcts_kwargs = {}
        if mctsPrevious:
            mcts_kwargs['mctsPlayer_id'] = mctsPrevious.mctsPlayer_id
            mcts_kwargs['mctsPlayer_ai'] = mctsPrevious.mctsPlayer_ai

            outgoingEdges = mctsPrevious.mctsPlayer_ai.mctsPlayout_getOutgoingEdges(state)
        else:
            outgoingEdges = state.getOutgoingEdges()

        incomingEdge_list = [incoming_edge]
        while fastforward and len(outgoingEdges) == 1:
            # log.debug(['fastforwarding', outgoingEdges])
            incomingEdge_list.append(outgoingEdges[0])
            state = state.applyEdge(outgoingEdges[0])

            if mctsPrevious:
                outgoingEdges = mctsPrevious.mctsPlayer_ai.mctsPlayout_getOutgoingEdges(state)
            else:
                outgoingEdges = state.getOutgoingEdges()

        return cls(
            incomingEdge_list, state, outgoingEdges,
            **mcts_kwargs
        )

    def __init__(
            self, incomingEdges: Optional[List[EdgeAbc]], state: StateAbc, outgoingEdges: List[EdgeAbc],
            mctsPlayer_id: PlayerId = None,
            mctsPlayer_ai: AiAbc = None,

            # Only for fromJson
            mctsPredicted_score: Optional[float] = None,
            mctsChild_list: List['MctsNode'] = None,
            mctsScoreSum_list: List[float] = None,
            mctsPlays_count: int = 0
    ):
        self.incomingEdge_list: List[EdgeAbc] = incomingEdges
        self.state: StateAbc = state
        self.outgoingEdges: List[EdgeAbc] = outgoingEdges

        self.mctsPlayer_id = mctsPlayer_id
        self.mctsPlayer_ai = mctsPlayer_ai
        
        if mctsPredicted_score is None and mctsPlayer_ai is not None:
            mctsPredicted_score = mctsPlayer_ai.mctsPlayout_predictScore(self.state)
            
        self.mctsPredicted_score = mctsPredicted_score 
        self.mctsChild_list = mctsChild_list
        self.mctsScoreSum_list = mctsScoreSum_list
        self.mctsPlayouts_count = mctsPlays_count

    def __getitem__(self, key):
        for child_node in self.mctsChild_list:
            if child_node.incomingEdge_list[0].mctsChildKey() == key:
                return child_node

    def createMctsMaskedNode(
                self, mctsPlayer_id: PlayerId, mctsPlayer_ai: AiAbc,
            ) -> 'MctsNode':
        mctsMaskedInfo_state = self.state.maskHiddenInfo(mctsPlayer_id)

        edge_list = mctsPlayer_ai.mctsPlayout_getOutgoingEdges(mctsMaskedInfo_state)

        # log.debug(edge_list)

        return type(self)(
            None, mctsMaskedInfo_state, edge_list,
            mctsPlayer_id=mctsPlayer_id,
            mctsPlayer_ai=mctsPlayer_ai,
        )

    def mctsPlayout(self, ai):
        assert self.mctsPlayer_id is not None
        assert self.state.isMasked

        if self.mctsChild_list:
            # Selection
            selected = self._mctsPlayout_selectChildNode(ai)
            score_list = selected.mctsPlayout(ai)
        elif self.outgoingEdges:
            # Expansion of this node into all child nodes
            self.mctsChild_list = [self.fromPreviousState(self.state, edge, mctsPrevious=self) for edge in self.outgoingEdges]
            selected = self._mctsPlayout_selectChildNode(ai)
            score_list = selected._mctsPlayout_simulation(ai)
        else:
            # Round-terminal state reached
            score_list = ai.getScores(self.state)

        self._mctsPlayout_updateScores(score_list)

        return score_list

    def _mctsPlayout_simulation(self, ai: AiAbc):
        simulation_state = self.state.clone(readonly=False)

        next_edges: List[EdgeAbc] = self.outgoingEdges
        while next_edges:
            edge = ai.mctsPlayout_pickEdge(next_edges, simulation_state.activePlayer_id)
            edge.updateState(simulation_state)
            next_edges = ai.mctsPlayout_getOutgoingEdges(simulation_state)

        # Round-terminal state reached
        score_list = ai.getScores(simulation_state)

        self._mctsPlayout_updateScores(score_list)

        return score_list

    def _mctsPlayout_selectChildNode(self, ai: AiAbc):
        # TODO handle edge.random_wt here
        if self.mctsChild_list[0].incomingEdge_list[0].random_wt is not None:
            random.shuffle(self.mctsChild_list)
            self.mctsChild_list.sort(key=lambda n: n.incomingEdge_list[0].random_wt * random.random())
        else:
            self.mctsChild_list.sort(key=lambda n: ai.mctsNodeSortValue(n, self.mctsPlayouts_count))

        return self.mctsChild_list[-1]


    def _mctsPlayout_updateScores(self, score_list: List[float]):
        if self.mctsScoreSum_list:
            for i, score in enumerate(score_list):
                self.mctsScoreSum_list[i] += score
        else:
            self.mctsScoreSum_list = score_list
            
        self.mctsPlayouts_count += 1

    def mctsScoreAvg(self, player_id: PlayerId) -> Optional[float]:
        if self.mctsScoreSum_list:
            return self.mctsScoreSum_list[player_id] / self.mctsPlayouts_count
        else:
            return None


