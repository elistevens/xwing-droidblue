import pytest

import numpy as np

from droidblue.core.basecls import PlayerId
from droidblue.core.agent import FirstAgent, RandomAgent, TrainedAgent
from droidblue.core.game import Game
from droidblue.core.node import Node

from .battlecruiser import BattleCruiserState


def test_overlap():
    for i in range(20):
        agents = [
            RandomAgent(),
            RandomAgent(),
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
        RandomAgent(),
        RandomAgent(),
    ]
    game = Game(BattleCruiserState, agents)
    game.playGame()

    print(game.current_node.state)

    assert game.current_node.state.ships.sum() == game.current_node.state.ship_count * game.current_node.state.ship_size * 2

    # assert len(game.played_nodes) >= 7
    # assert len(game.played_nodes) <= 51
    assert game.current_node.state.getFinalScore(PlayerId(0)) not in {0, None}
    assert game.current_node.state.getFinalScore(PlayerId(1)) not in {0, None}

    # assert False

def test_ai_game():
    agents = [
        TrainedAgent(),
        RandomAgent(),
    ]
    game = Game(BattleCruiserState, agents)
    game.playGame()

    print(game.current_node.state)

    assert game.current_node.state.ships.sum() == game.current_node.state.ship_count * game.current_node.state.ship_size * 2

    # assert len(game.played_nodes) >= 7
    # assert len(game.played_nodes) <= 51
    assert game.current_node.state.getFinalScore(PlayerId(0)) not in {0, None}
    assert game.current_node.state.getFinalScore(PlayerId(1)) not in {0, None}

    # assert False


if __name__ == "__main__":
    pytest.main()
