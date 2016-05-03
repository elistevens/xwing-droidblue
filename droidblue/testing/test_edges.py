from __future__ import division

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

import random


import droidblue.defaults.actions
from droidblue.testing.fixtures import *
import droidblue.defaults.choose as choose
from droidblue.defaults.maneuvers import SetDialRule
from droidblue.core.steps import Stepper

def test_PerformFocusActionEdge_impl(single_state):
    single_state.nextStep()
    assert single_state._getStat(0, 'focus') == 0

    droidblue.defaults.actions.PerformFocusActionEdge(0, opportunity_list=['testing']).transitionImpl(single_state)

    assert single_state._getStat(0, 'focus') == 1

def test_PerformFocusActionEdge_state(single_state):
    single_state.nextStep()
    assert single_state._getStat(0, 'focus') == 0

    new_state = droidblue.defaults.actions.PerformFocusActionEdge(0, opportunity_list=['testing']).getExactState(single_state)

    # log.info(new_state.stepper)

    # It's okay for new_state.usedOpportunity_set to be set([None]) since the
    # PerformFocusActionEdge didn't come from an actual rule, so it never got
    # it's opportunity_list set.
    assert new_state.usedOpportunity_set
    assert not single_state.usedOpportunity_set

    assert single_state._getStat(0, 'focus') == 0
    assert new_state._getStat(0, 'focus') == 1


def test_DialsChooseActivePilotEdge_impl(single_state):
    single_state.nextStep()
    assert single_state.active_id == None
    assert single_state.step == ('placeObstacles',)

    choose.DialsChooseActivePilotEdge(0, (0, 0)).transitionImpl(single_state)
    single_state.nextStep()

    assert single_state.active_id == 0
    assert single_state.step == ('setDial',)

def randomWalkUntil(state, step_tup):
    for i in range(50):
        if state.step == step_tup:
            break
        else:
            log.info(state.step)

        state.getEdges(fastforward_bool=False)

        for ff_edge in state.fastforward_list:
            print "FF: ", ff_edge

        # print self.state.edge_list

        log.debug("Edges: {}".format(len(state.edge_list)))
        for edge in state.edge_list:
            log.debug("  {}".format(edge))

        if state.edge_list:
            random_edge = random.choice(state.edge_list)
            print "Rnd:", random_edge, len(state.edge_list)

            state = random_edge.getExactState(state)
        else:
            state.nextStep()

    return state

def test_SetDialEdge_PerformManeuverEdge(single_state):
    state = single_state
    state.pushStepper(Stepper(Stepper.steps_round(dials=True)))
    log.debug(state._stepper_count)
    log.debug(state._stepper_stack)
    # state.nextStep()
    state = randomWalkUntil(state, ('setDial',))

    state.getEdges(fastforward_bool=False)
    for edge in state.edge_list:
        if edge.color_int == SetDialRule.white:
            state = edge.getExactState(state)
            break

    state = randomWalkUntil(state, ('performManeuver',))

    for opp_key in sorted(state.usedOpportunity_set):
        log.info("Used opportunity: {}".format(opp_key))

    state.getEdges(fastforward_bool=False)

    assert len(state.edge_list) == 1

    # assert False

def test_SetDialEdge_PerformManeuverEdge_vs(vs_state):
    state = vs_state
    state.pushStepper(Stepper(Stepper.steps_round(dials=True)))
    log.debug(state._stepper_count)
    log.debug(state._stepper_stack)
    # state.nextStep()
    state = randomWalkUntil(state, ('setDial',))

    state.getEdges(fastforward_bool=False)
    for edge in state.edge_list:
        if edge.color_int == SetDialRule.white:
            state = edge.getExactState(state)
            break

    state = randomWalkUntil(state, ('performManeuver',))

    for opp_key in sorted(state.usedOpportunity_set):
        log.info("Used opportunity: {}".format(opp_key))

    state.getEdges(fastforward_bool=False)

    assert len(state.edge_list) == 1

    # assert False
