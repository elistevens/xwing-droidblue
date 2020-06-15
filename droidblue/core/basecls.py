import abc
import copy

from typing import NewType, List, Set, Union, Optional

import numpy as np

from ..util import FancyRepr

from ..logging_config import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


PlayerId = NewType("PlayerId", int)


class RuleBase(FancyRepr):
    def proposeEdges(self, state: "StateBase") -> List["EdgeBase"]:
        return []

    def allowEdge(self, state: "StateBase", edge: "EdgeBase"):
        return True


class StateBase(FancyRepr, metaclass=abc.ABCMeta):
    cloneKeep_set: Set[str] = set()

    def __init__(self):
        self.active_player: PlayerId = PlayerId(0)
        self.frozen: bool = True
        self.isTrainable: bool = False

    @abc.abstractmethod
    def getFinalScore(self, player: PlayerId) -> Optional[float]:
        pass

    @abc.abstractmethod
    def getActiveRules(self) -> List["RuleBase"]:
        pass

    @abc.abstractmethod
    def getRawEdges(self) -> List["EdgeBase"]:
        pass

    def getFilteredEdges(self) -> List["EdgeBase"]:
        rule_list = self.getActiveRules()
        edge_list = self.getRawEdges()

        for rule in rule_list:
            edge_list = [edge for edge in edge_list if rule.allowEdge(self, edge)]

        return edge_list

    def clone(self) -> "StateBase":
        other = copy.copy(self)
        # other = copy.deepcopy(self)

        for k, v in list(self.__dict__.items()):
            if k not in self.cloneKeep_set:
                other.__dict__[k] = copy.deepcopy(v)

        other.frozen = False
        other.isTrainable = False

        return other

    def __eq__(self, other):
        if type(self) != type(other):
            log.debug("type({}) != type({})".format(type(self), type(other)))
            return False

        if self.__dict__.keys() != other.__dict__.keys():
            log.debug(
                "keys({}) != keys({})".format(
                    self.__dict__.keys(), other.__dict__.keys()
                )
            )
            return False

        for k, v in self.__dict__.items():
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


class TwoPlayerStateBase(StateBase):
    def __init__(self):
        super().__init__()
        self.other_player: PlayerId = PlayerId(1)

    def nextPlayer(self):
        assert not self.frozen

        self.active_player, self.other_player = (
            self.other_player,
            self.active_player,
        )


class EdgeBase(FancyRepr, metaclass=abc.ABCMeta):
    score = None

    # def __init__(self, parent_state: "StateBase"):
    #     assert isinstance(parent_state, StateBase)
    #     self.parent_state: StateBase = parent_state

    @abc.abstractmethod
    def updateState(self, state: StateBase):
        pass

    def setScore(self, score: Union[int, float]):
        self.score = score


