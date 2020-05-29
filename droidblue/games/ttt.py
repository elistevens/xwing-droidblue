from typing import NewType, Optional, Dict, List, Set, Tuple, Union

import numpy as np

from droidblue.core.basecls import PlayerId, RuleBase, EdgeBase, TwoPlayerStateBase

class TicTacToeEdge(EdgeBase):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def updateState(self, state: "TicTacToeState"):
        state.board[state.active_player, self.row, self.col] = 1
        state.nextPlayer()


class TicTacToeState(TwoPlayerStateBase):
    cloneKeep_set: Set[str] = set()

    def __init__(self):
        super().__init__()

        self.board = np.zeros((2, 3, 3), dtype=np.int8)

    def getScore(self, player: PlayerId) -> float:
        board_list = [
            (1, self.board[player]),
            (-1, self.board[0 if player else 1]),
        ]

        for score, board in board_list:

            if board.sum(axis=0).max() == 3 or board.sum(axis=1).max() == 3:
                return score

            if board[0, 0] == board[1, 1] == board[2, 2] == 1:
                return score

            if board[0, 2] == board[1, 1] == board[2, 0] == 1:
                return score

        return 0

    def getActiveRules(self) -> List[RuleBase]:
        return []

    def getRawEdges(self) -> List[TicTacToeEdge]:
        outgoing_edges = []

        if self.getScore(self.active_player) == 0:
            rows, cols = np.where(self.board.sum(axis=0) == 0)

            for row, col in zip(rows.flatten(), cols.flatten()):
                outgoing_edges.append(TicTacToeEdge(row, col))

        return outgoing_edges

    def __str__(self):
        lines = []
        for row in range(3):
            chars = []
            for col in range(3):
                if self.board[0, row, col]:
                    chars.append('X')
                elif self.board[1, row, col]:
                    chars.append('O')
                else:
                    chars.append('-')
            lines.append("|{}|".format(' '.join(chars)))

        return "\n".join(lines)
