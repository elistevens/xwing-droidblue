from __future__ import division

from droidblue.testing.fixtures import *

def test_setFlag(single_state):
    before_sum = single_state.stat_array.sum()
    print single_state.stat_array

    single_state.setFlag(0, 'weaponsDisabled')

    after_sum = single_state.stat_array.sum()
    print single_state.stat_array

    assert single_state.getFlag(0, 'weaponsDisabled')

    assert after_sum == before_sum + 1

def test_playerId(vs_state):
    state = vs_state

    assert state.const._getRawStat(0, 'player_id') == 0
    assert state.const._getRawStat(1, 'player_id') == 1

def consumeSteps(state):
    step_list = []
    while state.step_list:
        try:
            state.nextStep()
            if state.step:
                step_list.append(state.step)
        except IndexError:
            break

    return step_list



def test_stepper_nextState_simple(empty_state):
    state = empty_state
    del state.step_list[:]

    state.pushSteps(['b', 'c'])

    assert consumeSteps(state) == ['b', 'c',]

def test_stepper_nextState_push(empty_state):
    state = empty_state
    del state.step_list[:]

    state.pushSteps(['a', 'c'])

    assert state.step == None
    state.nextStep()
    assert state.step == 'a'

    state.pushSteps(['b'])

    assert state.step == 'a'

    assert consumeSteps(state) == ['b', 'a', 'c',]
