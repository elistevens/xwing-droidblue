import abc
import math
from typing import List, Type, Tuple

import torch
import torch.functional as F
import torch.nn as nn

from droidblue.core.basecls import EdgeBase
from droidblue.core.node import Node


class ModelBase(nn.Module):
    supportedEdgeTypes: List[Type[EdgeBase]] = []

    # see also https://github.com/pytorch/pytorch/issues/18182
    def _init_weights(self):
        for m in self.modules():
            if type(m) in {
                nn.Linear,
                nn.Conv3d,
                nn.Conv2d,
                nn.ConvTranspose2d,
                nn.ConvTranspose3d,
            }:
                nn.init.kaiming_normal_(
                    m.weight.data, a=0, mode="fan_out", nonlinearity="relu",
                )
                if m.bias is not None:
                    fan_in, fan_out = nn.init._calculate_fan_in_and_fan_out(
                        m.weight.data
                    )
                    bound = 1 / math.sqrt(fan_out)
                    nn.init.normal_(m.bias, -bound, bound)

    @classmethod
    @abc.abstractmethod
    def evaluateEdge(cls, evaluationData: List[torch.Tensor], edge: EdgeBase) -> float:
        pass

    @classmethod
    @abc.abstractmethod
    def getTrainingSampleFromNode(cls, node: Node, final_score: float) -> Tuple:
        pass


class LeakyHardTanh(nn.Module):
    def __init__(self, leak_slope=0.01):
        super().__init__()

        self.leak_slope = leak_slope
        self.hardtanh = nn.Hardtanh(
            min_val=(-1 + leak_slope), max_val=(1 - leak_slope), inplace=False
        )

    def forward(self, input):
        return self.hardtanh(input) + input * self.leak_slope
