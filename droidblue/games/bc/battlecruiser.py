import copy
import logging

from typing import Any, Optional, Dict, List, Set, Tuple, Union

import numpy as np
import torch
import torch.nn as nn

from droidblue.core.basecls import (
    PlayerId,
    RuleBase,
    TwoPlayerStateBase,
    EdgeBase,
)
from droidblue.core.node import Node
from droidblue.core.model import ModelBase, LeakyHardTanh
from droidblue.core.agent import ShapedRandomAgent

log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)


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


class BattleCruiserState(TwoPlayerStateBase):
    # cloneKeep_set: Set[str] = set()

    placement_rules = [NoShipOverlapRule()]
    shooting_rules = [TakeShotRule()]

    board_size: int = 6
    ship_count: int = 2
    ship_size: int = 3

    def __init__(self):
        super().__init__()
        self._active_rules = self.placement_rules

        self._board_a = np.zeros(
            (3, 2, self.board_size, self.board_size), dtype=np.int8
        )

    def clone(self) -> "BattleCruiserState":
        other = copy.copy(self)
        other._board_a = self._board_a.copy()
        # other = copy.deepcopy(self)l

        # for k, v in list(self.__dict__.items()):
        #     if k not in self.cloneKeep_set:
        #         other.__dict__[k] = copy.deepcopy(v)

        other.frozen = False
        other.isTrainable = False

        return other

    @property
    def ships(self):
        return self._board_a[0]

    @property
    def shots(self):
        return self._board_a[1:3].sum(axis=0)

    @property
    def hits(self):
        return self._board_a[1]

    @property
    def misses(self):
        return self._board_a[2]

    def getFinalScore(self, player: PlayerId) -> Optional[float]:
        other = 0 if player else 1
        board_list = [
            (1, self.hits[player], self.misses[player], self.ships[other]),
            (-1, self.hits[other], self.misses[other], self.ships[player]),
        ]

        for win_loss, hits, misses, ships in board_list:
            if hits.sum() == self.ship_count * self.ship_size:
                return win_loss * (100 - misses.sum()) / 100.0

        return None

    def getActiveRules(self) -> List[RuleBase]:
        return self._active_rules

    def getRawEdges(self) -> List["BattleCruiserEdge"]:
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
                        if self.hits[other_player, row, col]:
                            chars.append("X")
                        else:
                            chars.append("#")
                    else:
                        if self.misses[other_player, row, col]:
                            chars.append("*")
                        else:
                            chars.append(".")
                chars.append("|")
            lines.append("| {}".format(" ".join(chars)))

        return "\n".join(lines)


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
        other_player = 0 if state.active_player else 1

        if state.ships[other_player, self.row, self.col]:
            state.hits[state.active_player, self.row, self.col] = 1
        else:
            state.misses[state.active_player, self.row, self.col] = 1

        state.nextPlayer()


class BattleCruiserShotModel(ModelBase):
    supportedEdgeTypes = {BattleCruiserShotEdge}

    def __init__(self, in_channels=2):
        super().__init__()

        layer_list = []

        for conv_channels in [6, 4, 2, 1]:
            layer_list.extend(
                [
                    nn.Conv2d(
                        in_channels, conv_channels, kernel_size=3, padding=1, bias=True,
                    ),
                    # nn.ReLU(inplace=True),
                    LeakyHardTanh(),
                ]
            )

            in_channels = conv_channels

        self.conv_seq = nn.Sequential(*layer_list)

        self._init_weights()

    def forward(self, input_t):
        conv_t = self.conv_seq(input_t)

        return conv_t

    def getEvaluationDataFromState(
        self, state: BattleCruiserState, device: str
    ) -> List[torch.Tensor]:
        input_a = np.stack(
            (state.hits[state.active_player], state.misses[state.active_player]),
        )

        with torch.no_grad():
            input_g = (
                torch.from_numpy(input_a)
                .unsqueeze(0)
                .to(device, torch.float32, non_blocking=True)
            )

            output_g = self(input_g)

        return [output_g.numpy()]#.to("cpu", non_blocking=True)]
        return [output_g]#.to("cpu", non_blocking=True)]

    @classmethod
    def evaluateEdge(
        cls, evaluationData: List[torch.Tensor], edge: "BattleCruiserShotEdge"
    ) -> float:
        return evaluationData[0][0, 0, edge.row, edge.col].item()

    @classmethod
    def getTrainingSampleFromNode(cls, node: Node, final_score: float) -> Tuple:
        state: BattleCruiserState = node.state
        input_a = np.stack(
            (state.hits[state.active_player], state.misses[state.active_player]),
        )

        label_a = state.ships[state.other_player : state.other_player + 1]

        return tuple(
            [
                torch.from_numpy(input_a).to(torch.float32),
                torch.from_numpy(label_a).to(torch.float32),
            ]
        )

    def getTrainingLossAndMetadata(
        self, batch_tup: Tuple, device: str
    ) -> Tuple[torch.Tensor, Dict[str, Any]]:
        input_t, label_t = batch_tup

        input_g = input_t.to(device, non_blocking=True)
        label_g = label_t.to(device, non_blocking=True)

        output_g = self(input_g)

        loss_func = nn.MSELoss()
        loss_g = loss_func(output_g, label_g)

        # log.debug(f"{output_g[0].min()}, {output_g[0].max()}, {loss_g}")

        return loss_g, {}


class BattleCruiserPlaceModel(ModelBase):
    supportedEdgeTypes = {BattleCruiserPlaceEdge}

    def __init__(self, in_channels=1):
        super().__init__()

        layer_list = []

        for conv_channels in [6, 4, 2]:
            layer_list.extend(
                [
                    nn.Conv2d(
                        in_channels, conv_channels, kernel_size=3, padding=1, bias=True,
                    ),
                    # nn.ReLU(inplace=True),
                    LeakyHardTanh(),
                ]
            )

            in_channels = conv_channels

        self.conv_seq = nn.Sequential(*layer_list)

        self._init_weights()

    def forward(self, input_t):
        conv_t = self.conv_seq(input_t)

        # print(conv_t.shape)
        # output_t = self.linear_layer(conv_t.view(conv_t.shape[0], -1))

        return conv_t

    def getEvaluationDataFromState(
        self, state: BattleCruiserState, device: str
    ) -> List[torch.Tensor]:
        # input_a = np.stack(
        #     (state.hits[state.active_player], state.misses[state.active_player]),
        # )

        input_g = (
            torch.from_numpy(state.ships[state.active_player : state.active_player + 1])
            .unsqueeze(0)
            .to(device, torch.float32, non_blocking=True)
        )

        output_g = self(input_g)

        return [output_g.to("cpu", non_blocking=True)]

    @classmethod
    def evaluateEdge(
        cls, evaluationData: List[torch.Tensor], edge: "BattleCruiserPlaceEdge"
    ) -> float:
        return evaluationData[0][0, int(edge.isVertical), edge.row, edge.col].item()

    @classmethod
    def getTrainingSampleFromNode(cls, node: Node, final_score: float) -> Tuple:
        state: BattleCruiserState = node.state
        edge: BattleCruiserPlaceEdge = node.outgoingEdge

        input_a = state.ships[state.active_player : state.active_player + 1]

        label_t = torch.zeros((2, state.board_size, state.board_size))
        # log.debug([label_t.shape, edge.isVertical, edge.row, edge.col])
        label_t[int(edge.isVertical), edge.row, edge.col] = final_score

        mask_t = torch.zeros((2, state.board_size, state.board_size))
        mask_t[int(edge.isVertical), edge.row, edge.col] = 1.0

        return tuple([torch.from_numpy(input_a).to(torch.float32), label_t, mask_t,])

    def getTrainingLossAndMetadata(
        self, batch_tup: Tuple, device: str
    ) -> Tuple[torch.Tensor, Dict[str, Any]]:
        input_t, label_t, mask_t = batch_tup

        input_g = input_t.to(device, non_blocking=True)
        mask_g = mask_t.to(device, non_blocking=True)
        label_g = label_t.to(device, non_blocking=True)

        output_g = self(input_g)

        loss_func = nn.MSELoss()

        # log.debug([output_g.type, mask_g.shape])
        loss_g = loss_func(output_g * mask_g, label_g)

        return loss_g, {}


class BattleCruiserAgent(ShapedRandomAgent):
    def __init__(self, placeModel_path, shotModel_path):
        models = []
        modelClasses = [BattleCruiserPlaceModel, BattleCruiserShotModel]

        if placeModel_path:
            place_model: BattleCruiserPlaceModel = BattleCruiserPlaceModel()
            place_model.load_state_dict(torch.load(placeModel_path)["model_state"])
            place_model.eval()

            models.append(place_model)

        if shotModel_path:
            shot_model: BattleCruiserShotModel = BattleCruiserShotModel()
            shot_model.load_state_dict(torch.load(shotModel_path)["model_state"])
            shot_model.eval()

            models.append(shot_model)

        super().__init__(models, modelClasses)
