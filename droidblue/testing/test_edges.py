from __future__ import division

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

import random

import numpy as np


import droidblue.defaults.actions
from droidblue.testing.fixtures import *
import droidblue.defaults.choose as choose
from droidblue.defaults.maneuvers import SetDialRule
from droidblue.core.steps import steps_round
from droidblue.core.rules import default_oppKey

def test_PerformFocusActionEdge_impl(single_state):
    assert single_state.getStat(0, 'focus') == 0

    droidblue.defaults.actions.PerformFocusActionEdge(0, opportunity_list=[default_oppKey._replace(step='testing')]).transitionImpl(single_state)

    assert single_state.getStat(0, 'focus') == 1

def test_PerformFocusActionEdge_state(single_state):
    assert single_state.getStat(0, 'focus') == 0

    new_state = droidblue.defaults.actions.PerformFocusActionEdge(0, opportunity_list=[default_oppKey._replace(step='testing')]).getExactState(single_state)

    # It's okay for new_state.usedOpportunity_set to be set([None]) since the
    # PerformFocusActionEdge didn't come from an actual rule, so it never got
    # it's opportunity_list set.

    log.debug(single_state.opportunity_set)
    log.debug(new_state.opportunity_set)
    assert single_state.opportunity_set is not new_state.opportunity_set

    log.debug(id(single_state.stat_array))
    log.debug(single_state.stat_array)
    log.debug(id(new_state.stat_array))
    log.debug(new_state.stat_array)
    assert single_state.stat_array is not new_state.stat_array


    assert new_state.opportunity_set
    assert not single_state.opportunity_set

    assert single_state.getStat(0, 'focus') == 0
    assert new_state.getStat(0, 'focus') == 1


def test_DialsChooseActivePilotEdge_impl(single_state):
    choose.DialsChooseActivePilotEdge(0, (0, 0)).transitionImpl(single_state)
    single_state.nextStep()

    assert single_state.active_id == 0
    assert single_state.step == 'setDial'

def randomWalkUntil(state, step):
    for i in range(50):
        if state.step == step:
            break
        else:
            log.info("Step: {}".format(state.step))

        edge_list = state.getEdges(fastforward_bool=False)

        for ff_edge in state.fastforward_list:
            log.info("FF: {}".format(ff_edge))

        log.debug("Edges: {}".format(len(edge_list)))
        for edge in edge_list:
            log.debug("  {}".format(edge))

        if edge_list:
            random_edge = random.choice(edge_list)
            log.info("Rnd: {} {}".format(random_edge, len(edge_list)))

            state = random_edge.getExactState(state)
        else:
            state.nextStep()

    return state

def test_SetDialEdge_PerformManeuverEdge(single_state):
    state = single_state
    state.pushSteps(steps_round(dials=True))
    state = randomWalkUntil(state, 'setDial')

    edge_list = state.getEdges(fastforward_bool=False)
    for edge in edge_list:
        if edge.color_int == SetDialRule.white:
            state = edge.getExactState(state)
            break

    state = randomWalkUntil(state, 'doPerformManeuver')

    state.getEdges(fastforward_bool=False)

    assert len(edge_list) == 1

    # assert False

def test_SetDialEdge_PerformManeuverEdge_vs(vs_state):
    state = vs_state
    state.pushSteps(steps_round(dials=True))
    state = randomWalkUntil(state, 'setDial')

    edge_list = state.getEdges(fastforward_bool=False)
    for edge in edge_list:
        if edge.color_int == SetDialRule.white:
            state = edge.getExactState(state)
            break

    state = randomWalkUntil(state, 'doPerformManeuver')

    state.getEdges(fastforward_bool=False)

    assert len(edge_list) == 1

    # assert False
