from typing import NewType, Optional, Dict, List, Set, Tuple, Union

import numpy as np

from droidblue.core.basecls import PlayerId, RuleBase, EdgeBase, TwoPlayerStateBase


class NoShipOverlapRule(RuleBase):
    def proposeEdges(self, state: "BattleCruiserState") -> List["BattleCruiserEdge"]:
        outgoing_edges = []

        if state.ships[state.active_player].sum() < state.ship_count * state.ship_size:
            for row in range(1, state.board_size - 1):
                for col in range(0, state.board_size):
                    outgoing_edges.append(BattleCruiserPlaceEdge(row, col, True))
            for row in range(0, state.board_size):
                for col in range(1, state.board_size - 1):
                    outgoing_edges.append(BattleCruiserPlaceEdge(row, col, False))

        return outgoing_edges

    def allowEdge(self, state: "BattleCruiserState", edge: "BattleCruiserEdge"):
        if isinstance(edge, BattleCruiserPlaceEdge):
            existing_ships = state.ships[state.active_player]
            if (existing_ships * edge.getNewShipArray(state)).sum() > 0:
                return False

        return True


class TakeShotRule(RuleBase):
    def proposeEdges(self, state: "BattleCruiserState") -> List["BattleCruiserEdge"]:
        outgoing_edges = []

        if state.getFinalScore(state.active_player) == None:
            rows, cols = np.where(state.shots[state.active_player] == 0)

            for row, col in zip(rows.flatten(), cols.flatten()):
                outgoing_edges.append(BattleCruiserShotEdge(row, col))

        return outgoing_edges


class HitOrMissRule(RuleBase):
    def proposeEdges(self, state: "BattleCruiserState") -> List["BattleCruiserEdge"]:
        outgoing_edges = [BattleCruiserHitOrMissEdge()]

        return outgoing_edges


class BattleCruiserEdge(EdgeBase):
    parent_state: "BattleCruiserState"


class BattleCruiserPlaceEdge(BattleCruiserEdge):
    def __init__(self, row: int, col: int, isVertical: bool):
        self.row: int = row
        self.col: int = col
        self.isVertical: bool = isVertical

    def updateState(self, state: "BattleCruiserState"):
        state.ships[state.active_player] += self.getNewShipArray(state)
        state.nextPlayer()
        state.isTrainable = True

        if state.ships.sum() == state.ship_count * state.ship_size * 2:
            state._active_rules = state.shooting_rules

    def getNewShipArray(self, state: "BattleCruiserState"):
        new_ship = np.zeros((state.board_size, state.board_size), dtype=np.int8)

        new_ship[self.row, self.col] = 1

        if self.isVertical:
            new_ship[self.row + 1, self.col] = 1
            new_ship[self.row - 1, self.col] = 1
        else:
            new_ship[self.row, self.col + 1] = 1
            new_ship[self.row, self.col - 1] = 1

        return new_ship


class BattleCruiserShotEdge(BattleCruiserEdge):
    def __init__(self, row: int, col: int):
        self.row: int = row
        self.col: int = col

    def updateState(self, state: "BattleCruiserState"):
        state.shots[state.active_player, self.row, self.col] = 1
        state.isTrainable = True
        state._active_rules = state.hitOrMiss_rules


class BattleCruiserHitOrMissEdge(BattleCruiserEdge):
    def __init__(self):
        pass

    def updateState(self, state: "BattleCruiserState"):
        state.hits[state.active_player] = (
            state.shots[state.active_player]
            * state.ships[0 if state.active_player else 1]
        )
        state.misses[state.active_player] = state.shots[state.active_player] * (
            1 - state.ships[0 if state.active_player else 1]
        )
        state.nextPlayer()
        state._active_rules = state.shooting_rules


class BattleCruiserState(TwoPlayerStateBase):
    cloneKeep_set: Set[str] = set()

    def __init__(self):
        super().__init__()
        self.placement_rules = [NoShipOverlapRule()]
        self.shooting_rules = [TakeShotRule()]
        self.hitOrMiss_rules = [HitOrMissRule()]

        self._active_rules = self.placement_rules

        self.board_size: int = 6
        self.ship_count: int = 2
        self.ship_size: int = 3  # Note: changing this isn't handled yet

        self.ships = np.zeros((2, self.board_size, self.board_size), dtype=np.int8)
        self.shots = np.zeros((2, self.board_size, self.board_size), dtype=np.int8)
        self.hits = np.zeros((2, self.board_size, self.board_size), dtype=np.int8)
        self.misses = np.zeros((2, self.board_size, self.board_size), dtype=np.int8)

    def getTrainableInput(self) -> np.array:
        assert self.isTrainable

        trainable_a = np.stack(
            (
                self.ships[self.active_player],
                self.shots[self.active_player],
                self.hits[self.active_player],
                self.misses[self.active_player],
            ),
        )

        # print(trainable_a.shape, trainable_a)

        return trainable_a

    def getFinalScore(self, player: PlayerId) -> Optional[float]:
        board_list = [
            (1, self.shots[player], self.ships[0 if player else 1]),
            (-1, self.shots[0 if player else 1], self.ships[player]),
        ]

        for win_loss, shots, ships in board_list:
            if (shots * ships).sum() == self.ship_count * self.ship_size:
                return win_loss * (100 - shots.sum())

        return None

    def getActiveRules(self) -> List[RuleBase]:
        return self._active_rules

    def getRawEdges(self) -> List[BattleCruiserEdge]:
        outgoing_edges = []
        for rule in self._active_rules:
            outgoing_edges += rule.proposeEdges(self)

        return outgoing_edges

    def __str__(self):
        lines = [
            " Player 1 {:3}  Player 2 {:3}".format(
                self.getFinalScore(PlayerId(0)) or "---",
                self.getFinalScore(PlayerId(1)) or "---",
            )
        ]

        for row in range(self.board_size):
            chars = []
            for player in range(2):
                other_player = 0 if player else 1

                for col in range(self.board_size):
                    if self.ships[player, row, col]:
                        if self.shots[other_player, row, col]:
                            chars.append("X")
                        else:
                            chars.append("#")
                    else:
                        if self.shots[other_player, row, col]:
                            chars.append("*")
                        else:
                            chars.append(".")
                chars.append("|")
            lines.append("| {}".format(" ".join(chars)))

        return "\n".join(lines)
