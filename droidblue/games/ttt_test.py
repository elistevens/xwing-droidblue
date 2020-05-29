import pytest

from droidblue.core.basecls import PlayerId
from droidblue.core.agent import FirstAgent, RandomAgent
from droidblue.core.game import Game
from droidblue.core.node import Node

from .ttt import TicTacToeEdge, TicTacToeState


def test_board_init():
    state = TicTacToeState()

    assert len(state.getFilteredEdges()) == 9
    assert state.getFinalScore(PlayerId(0)) == None


def test_node_init():
    start_node = Node(TicTacToeState())

    assert start_node.state.active_player == 0

    start_node.populateChildren()
    second_node = start_node.childNodes[0]

    # edges = start_node.state.getFilteredEdges()
    # outgoing_edge = edges[0]
    # second_node = start_node.getNextNode(outgoing_edge)

    print(second_node.state)

    assert second_node.state.board[0, 0, 0] == 1
    assert second_node.state.active_player == 1

    second_edges = second_node.state.getFilteredEdges()
    assert len(second_edges) == 8

    for edge in second_edges:
        assert edge.row != 0 or edge.col != 0

    print(second_edges)

    # outgoing_edge = second_edges[3]
    second_node.populateChildren()
    third_node = second_node.childNodes[3]
    print(third_node.state)


def test_game():
    agents = [
        FirstAgent(),
        FirstAgent(),
    ]
    game = Game(TicTacToeState, agents)

    game.playGame()

    print(game.current_node.state)

    assert len(game.played_nodes) == 8
    assert game.current_node.state.getFinalScore(PlayerId(0)) == 1
    assert game.current_node.state.getFinalScore(PlayerId(1)) == -1

    # assert False


if __name__ == "__main__":
    pytest.main()
