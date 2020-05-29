from typing import NewType, Optional, Dict, List, Set, Tuple, Union

import numpy as np

from droidblue.core.basecls import PlayerId, RuleBase, EdgeBase, TwoPlayerStateBase


class NoShipOverlapRule(RuleBase):
    def allowEdge(self, state: "BattleCruiserState", edge: "BattleCruiserEdge"):
        if isinstance(edge, BattleCruiserPlaceEdge):
            existing_ships = state.ships[state.active_player]
            if (existing_ships * edge.getNewShipArray(state)).sum() > 0:
                return False

        return True


class BattleCruiserEdge(EdgeBase):
    parent_state: "BattleCruiserState"


class BattleCruiserPlaceEdge(BattleCruiserEdge):
    def __init__(
        self, row: int, col: int, isVertical: bool
    ):
        self.row: int = row
        self.col: int = col
        self.isVertical: bool = isVertical

    def updateState(self, state: "BattleCruiserState"):
        state.ships[state.active_player] += self.getNewShipArray(state)
        state.nextPlayer()

    def getNewShipArray(self, state: "BattleCruiserState"):
        new_ship = np.zeros(
            (state.board_size, state.board_size), dtype=np.int8
        )

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
        state.nextPlayer()

# TODO add BattleCruiserRevealEdge so that we can predict scores w/o knowing if the shot will land


class BattleCruiserState(TwoPlayerStateBase):
    cloneKeep_set: Set[str] = set()

    def __init__(self):
        super().__init__()
        self._active_rules = [NoShipOverlapRule()]

        self.board_size: int = 6
        self.ship_count: int = 2
        self.ship_size: int = 3  # Note: changing this isn't handled yet

        self.ships = np.zeros((2, self.board_size, self.board_size), dtype=np.int8)
        self.shots = np.zeros((2, self.board_size, self.board_size), dtype=np.int8)

    def getScore(self, player: PlayerId) -> float:
        board_list = [
            (1, self.shots[player], self.ships[0 if player else 1]),
            (-1, self.shots[0 if player else 1], self.ships[player]),
        ]

        for score, shots, ships in board_list:
            if (shots * ships).sum() == self.ship_count * self.ship_size:
                return score

        return 0

    def getActiveRules(self) -> List[RuleBase]:
        return self._active_rules

    def getRawEdges(self) -> List[BattleCruiserEdge]:
        outgoing_edges = []

        if self.ships[self.active_player].sum() < self.ship_count * self.ship_size:
            for row in range(1, self.board_size - 1):
                for col in range(0, self.board_size):
                    outgoing_edges.append(
                        BattleCruiserPlaceEdge(row, col, True)
                    )
            for row in range(0, self.board_size):
                for col in range(1, self.board_size - 1):
                    outgoing_edges.append(
                        BattleCruiserPlaceEdge(row, col, False)
                    )

            return outgoing_edges

        if self.getScore(self.active_player) == 0:
            rows, cols = np.where(self.shots[self.active_player] == 0)

            for row, col in zip(rows.flatten(), cols.flatten()):
                outgoing_edges.append(
                    BattleCruiserShotEdge(row, col)
                )

        return outgoing_edges

    def __str__(self):
        lines = [" Player 1      Player 2"]

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
