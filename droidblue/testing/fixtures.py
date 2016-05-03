import math

import pytest
from droidblue.core.state import ConstantState, BoardState

from droidblue.core.dice import AttackDicePool, DefenseDicePool
from droidblue.testing import squads as squads
# s = BoardState([squads.tint_ept])

@pytest.fixture
def empty_state():
    const = ConstantState([])
    state = BoardState(const.const_id)

    return state

@pytest.fixture
def single_state():
    const = ConstantState([squads.tint_ept])
    state = BoardState(const.const_id)

    return state


@pytest.fixture
def vs_state():
    const = ConstantState([squads.xwt70_ept, squads.tint_ept])
    state = BoardState(const.const_id)

    state.pilots[0]._changePosition(-40 * 3.5, 0, math.pi/2)
    state.pilots[1]._changePosition(40 * 3.5, 0, -math.pi/2)

    return state

@pytest.fixture
def swarm_state():
    const = ConstantState([squads.awing_swarm, squads.howlcrack_swarm])
    state = BoardState(const.const_id)

    state.pilots[0]._changePosition(-40 * 3.5, 0, math.pi/2)
    state.pilots[1]._changePosition(40 * 3.5, 0, -math.pi/2)

    return state


@pytest.fixture
def atk1_pool():
    return AttackDicePool(1)


@pytest.fixture
def atk2_pool():
    return AttackDicePool(2)


@pytest.fixture
def atk3_pool():
    return AttackDicePool(3)


@pytest.fixture
def dfn1():
    return DefenseDicePool(1)


@pytest.fixture
def dfn2():
    return DefenseDicePool(2)


@pytest.fixture
def dfn3():
    return DefenseDicePool(3)
