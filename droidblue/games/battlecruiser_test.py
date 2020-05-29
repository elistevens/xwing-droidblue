import pytest

import numpy as np

from droidblue.core.basecls import PlayerId
from droidblue.core.agent import FirstEdgeAgent, RandomEdgeAgent
from droidblue.core.game import Game
from droidblue.core.node import Node

from .battlecruiser import BattleCruiserState


def test_overlap():
    for i in range(100):
        agents = [
            RandomEdgeAgent(),
            RandomEdgeAgent(),
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
        RandomEdgeAgent(),
        RandomEdgeAgent(),
    ]
    game = Game(BattleCruiserState, agents)
    game.playGame()

    print(game.current_node.state)

    assert game.current_node.state.ships.sum() == game.current_node.state.ship_count * game.current_node.state.ship_size * 2

    # assert len(game.played_nodes) >= 7
    # assert len(game.played_nodes) <= 51
    assert game.current_node.state.getScore(PlayerId(0)) != 0
    assert game.current_node.state.getScore(PlayerId(1)) != 0

    # assert False


if __name__ == "__main__":
    pytest.main()
