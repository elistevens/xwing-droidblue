import abc
import random

from pathlib import Path
from typing import List, Dict, Optional, Tuple, Type, Union

import numpy as np
import torch

from droidblue.core.basecls import StateBase, EdgeBase
from droidblue.core.model import ModelBase
from droidblue.core.node import Node
from droidblue.util import FancyRepr

from ..logging_config import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class RandomAgentBase(FancyRepr, metaclass=abc.ABCMeta):
    def __init__(self, models: List[ModelBase] = None, modelClasses: List[Type[ModelBase]] = None):
        self.edgeType_to_model: Dict[Type[EdgeBase], Tuple[Type, ModelBase]] = {}

        # These may get overwritten by actual models
        for model_cls in modelClasses or []:
            for edge_type in model_cls.supportedEdgeTypes:
                self.edgeType_to_model[edge_type] = (model_cls, None)

        for model in models or []:
            for edge_type in model.supportedEdgeTypes:
                self.edgeType_to_model[edge_type] = (type(model), model)



    def createNextNode(self, node: Node) -> Node:
        edge: EdgeBase
        new_state: Optional[StateBase]

        outgoingEdges: List[EdgeBase] = node.state.getFilteredEdges()

        if len(outgoingEdges) > 1:
            weightedEdgeState_list = self.get_weightedEdgeState_list(node, outgoingEdges)

            population = []
            weights = np.zeros(len(weightedEdgeState_list), dtype=np.float32)
            for i, (w, e, s) in enumerate(weightedEdgeState_list):
                weights[i] = w
                population.append((e, s))

            weights = self.modifyWeights(weights)

            edge, new_state =  random.choices(population, weights)[0]
        else:
            edge = outgoingEdges[0]
            new_state = None

        return Node(node.state, edge, new_state)

    @classmethod
    def modifyWeights(cls, weights):
        return weights

    def get_weightedEdgeState_list(
        self, node: Node, outgoingEdges: List[EdgeBase]
    ) -> List[Tuple[float, EdgeBase, Optional[StateBase]]]:
        weightedEdgeState_list = []

        for edge in outgoingEdges:
            weight = 1.0

            edge_type = type(edge)
            if edge_type in self.edgeType_to_model:
                model_cls, model = self.edgeType_to_model[edge_type]

                # if edge_type not in node.edgeType_to_trainingData:
                #     node.edgeType_to_trainingData[edge_type] = model_cls.getTrainingSampleFromNode(node)

                if model:
                    if edge_type not in node.edgeType_to_evalData:
                        node.edgeType_to_evalData[
                            edge_type
                        ] = model.getEvaluationDataFromState(node.state, "cpu")

                    weight = model.evaluateEdge(node.edgeType_to_evalData[edge_type], edge)

            weightedEdgeState_list.append((weight, edge, None))

        return weightedEdgeState_list


class FirstAgent(RandomAgentBase):
    @classmethod
    def modifyWeights(cls, weights):
        weights[1:] = 0.0
        return weights


class ShapedRandomAgent(RandomAgentBase):
    exponent = 3
    cutoff = 0.5

    @classmethod
    def modifyWeights(cls, weights):
        if weights.min() != weights.max():
            if weights.max() > 0:
                weights[weights < 0] = 0.0
            else:
                weights -= weights.min()

            weights /= weights.max()

            weights **= cls.exponent
            weights[weights < cls.cutoff] = 0.0

        return weights

#
# class TrainedAgent(AgentBase):
#     def __init__(self, thisState_model_cls, thisState_model_path, nextState_model_cls, nextState_model_path, ):
#         thisState_model_dict = torch.load(thisState_model_path)
#
#         self.thisState_model = thisState_model_cls()
#         self.thisState_model.load_state_dict(thisState_model_dict["model_state"])
#         self.thisState_model.eval()
#
#         nextState_model_dict = torch.load(nextState_model_path)
#
#         self.nextState_model = nextState_model_cls()
#         self.nextState_model.load_state_dict(nextState_model_dict["model_state"])
#         self.nextState_model.eval()
#
#
#     def get_weightedEdgeState_list(self, outgoingEdges: List[EdgeBase]) -> List[Tuple[float, EdgeBase, Optional[StateBase]]]:
#
#
#         return [(random.random(), e, None) for e in outgoingEdges]
#
#     def predictScore(self, node: Node) -> float:
#         if node.state.isTrainable:
#             # modelInput_tup = node.state.getTrainableInput()
#             # input_t = torch.from_numpy(node.state.getTrainingSample()).to(torch.float32)
#             # input_t = input_t.unsqueeze(0)
#
#             inputs, _ = node.state.getTrainingSample()
#
#             with torch.no_grad():
#                 score = self.nextState_model(
#                     *[
#                         torch.from_numpy(x).to(torch.float32).unsqueeze(0)
#                         for x in inputs
#                     ]
#                 ).item()
#             # assert type(score) == float
#             return score + random.random() / 100
#         else:
#             return random.random()
