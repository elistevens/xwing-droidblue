from __future__ import division

import math
import pytest

from droidblue.state import BoardState
import droidblue.testing.squads as squads
import droidblue.defaults.generics as generics


@pytest.fixture
def single_state():
    state = BoardState([squads.tint_ept])

    return state


@pytest.fixture
def vs_state():
    state = BoardState([squads.xwt70_ept, squads.tint_ept])

    state.pilots[0].base._changePosition(-40 * 3.5, 0, math.pi/2)
    state.pilots[1].base._changePosition(40 * 3.5, 0, -math.pi/2)

    return state


def test_actionImpl_focus(single_state):
    assert single_state.getStat(0, 'focus') == 0

    generics.PerformFocusActionEdge(0).transitionImpl(single_state)

    assert single_state.getStat(0, 'focus') == 1

def test_actionState_focus(single_state):
    assert single_state.getStat(0, 'focus') == 0

    new_state = generics.PerformFocusActionEdge(0).getExactState(single_state)

    assert single_state.getStat(0, 'focus') == 0
    assert new_state.getStat(0, 'focus') == 1
