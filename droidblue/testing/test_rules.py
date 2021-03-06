from __future__ import division

import copy

from droidblue.testing.fixtures import *
import droidblue.defaults.choose as choose

from droidblue.defaults.actions import PerformFocusActionRule, PerformFocusActionEdge


def test_doPerformAction(single_state):
    state = single_state
    new_state = None

    state.pushSteps(['doPerformAction'], active_id=0)

    edge_list, activePlayer_id = state.getFilteredEdges()

    assert edge_list

    for edge in edge_list:
        if isinstance(edge, PerformFocusActionEdge):
            new_state = edge.getExactState(state)
            break

    else:
        assert not edge_list
        assert False

    assert state.opportunity_set != new_state.opportunity_set

    edge_list, activePlayer_id = new_state.getFilteredEdges(fastforward_bool=False)
    assert not edge_list


def test_rules(vs_state):
    state = vs_state
    state.pushSteps(['*'], 0, 0)
    state.nextStep()

    print sorted(state.edgeRules_dict.keys())
    print sorted(state.const.edgeRules_dict.keys())

    for step_tup, (rule_list, _, _) in sorted(state.const.edgeRules_dict.iteritems()):
        print step_tup
        # print '    ', rule_list

        for rule in rule_list:
            # assert rule.getEdges(state)

            print '  ', rule
            for edge in rule._getEdges(state) or []:
                print '    ', edge

    # assert False

