import logging

import pytest
import numpy as np

from droidblue.core.basecls import PlayerId
from droidblue.core.agent import RandomAgentBase
from droidblue.core.game import Game
from droidblue.core.node import Node

from .battlecruiser import BattleCruiserState, BattleCruiserAgent, BattleCruiserShotEdge
# from .battlecruiser_training import Model

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def test_overlap():
    for i in range(20):
        agents = [
            RandomAgentBase(),
            RandomAgentBase(),
        ]
        game = Game(BattleCruiserState, agents)
        game.playGame()

        try:
            assert np.where(game.current_node.state.ships)[0].shape == (12,)
        except:
            print(i)
            print(game.current_node.state)
            raise



def test_game():
    agents = [
        BattleCruiserAgent(None, None),
        BattleCruiserAgent(None, None),
    ]
    game = Game(BattleCruiserState, agents)
    game.playGame()

    log.info(game.current_node.state)

    assert game.current_node.state.ships.sum() == game.current_node.state.ship_count * game.current_node.state.ship_size * 2

    # assert len(game.played_nodes) >= 7
    # assert len(game.played_nodes) <= 51
    assert game.current_node.state.getFinalScore(PlayerId(0)) not in {0, None}
    assert game.current_node.state.getFinalScore(PlayerId(1)) not in {0, None}

    # trainable_nodes = [node for node in game.played_nodes if BattleCruiserShotEdge in node.edgeType_to_trainingData]
    #
    # assert trainable_nodes

    # for i, node in enumerate(game.played_nodes[1:5]):
    #     assert node.state.isTrainable, repr([i, node])
    #     assert node.state.getTrainingSample()[1] == []
    #
    # for node in game.played_nodes[5:]:
    #     if node.state.isTrainable:
    #         assert node.state.getTrainingSample()[1] != []

    # assert False


def test_game_random():
    agents = [
        BattleCruiserAgent(None, None),
        BattleCruiserAgent(None, None),
    ]
    game1 = Game(BattleCruiserState, agents)
    game1.playGame()
    log.info(game1.current_node.state)

    game2 = Game(BattleCruiserState, agents)
    game2.playGame()
    log.info(game2.current_node.state)

    assert game1.current_node.state != game2.current_node.state


def test_ai_game_winrate():
    placeModel_path = None
    shotModel_path = "droidblue/games/bc/BattleCruiserShotModel-latest.state"

    agents = [
        RandomAgentBase(),
        BattleCruiserAgent(placeModel_path, shotModel_path),
    ]
    wins = 0
    games = 100

    for i in range(games):
        game = Game(BattleCruiserState, agents)
        game.playGame()

        wins += game.current_node.state.getFinalScore(PlayerId(1)) > 0

    log.info(f"wins: {wins}")

    assert wins > games * 0.9


    # assert False
    #
    # print(game.current_node.state)
    #
    # assert game.current_node.state.ships.sum() == game.current_node.state.ship_count * game.current_node.state.ship_size * 2
    #
    # assert len(game.played_nodes) >= 7
    # assert len(game.played_nodes) <= 51
    # assert game.current_node.state.getFinalScore(PlayerId(0)) not in {0, None}
    # assert game.current_node.state.getFinalScore(PlayerId(1)) not in {0, None}
    #
    # assert False


if __name__ == "__main__":
    pytest.main()
