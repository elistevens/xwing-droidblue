from __future__ import division

from droidblue.testing.fixtures import *
from droidblue.core.steps import Stepper

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
    while state._stepper_stack:
        try:
            state.nextStep()
            step_list.append(state.step)
        except IndexError:
            break

    return step_list



def test_stepper_nextState_simple(empty_state):
    state = empty_state
    del state._stepper_stack[:]

    state.pushStepper(Stepper(['b', 'c']))

    assert consumeSteps(state) == [('b',), ('c',)]

def test_stepper_nextState_push(empty_state):
    state = empty_state
    del state._stepper_stack[:]

    state.pushStepper(Stepper(['a', 'c']))

    assert state.step == None
    state.nextStep()
    assert state.step == ('a',)

    state.pushStepper(Stepper(['b']))

    assert state.step == ('a',)

    assert consumeSteps(state) == [('b',), ('a',), ('c',)]

def test_stepper_nextState_append(empty_state):
    state = empty_state
    del state._stepper_stack[:]

    state.pushStepper(Stepper(['b', 'c']))
    state.appendStepper(Stepper(['d', 'e']))

    assert consumeSteps(state) == [('b',), ('c',), ('d',), ('e',)]

def test_stepper_nextState_pushappend(empty_state):
    state = empty_state
    del state._stepper_stack[:]

    state.pushStepper(Stepper(['d', 'e']))
    state.appendStepper(Stepper(['f', 'g']))
    state.pushStepper(Stepper(['b', 'c']))

    assert consumeSteps(state) == [('b',), ('c',), ('d',), ('e',), ('f',), ('g',)]



# def test_stepper_nextState(empty_state):
#     state = empty_state
#     del state._stepper_stack[:]
#
#     state.pushStepper(Stepper(['b']))
#
#     assert state.step == ('b',)
#
#     state.appendStepper(Stepper(['c']))
#     state.pushStepper(Stepper(['a']))
#
#     step_list = []
#     while state.nextStep():
#         step_list.append(state.step)
#
#     assert step_list == [('a',), ('b',), ('c',)]


# def test_activation(vs_state):
#     vs_state.roundsLeft_count = 0
#     del vs_state._stepper_stack[:]
#     vs_state.pushStepper(Stepper([('activation',)]))
#     vs_state.getEdges()
#
#     assert vs_state.getFlag(0, 'chosen_activation')
#     assert vs_state.getFlag(1, 'chosen_activation')
