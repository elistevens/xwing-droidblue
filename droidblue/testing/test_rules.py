from __future__ import division

import copy

from droidblue.testing.fixtures import *
import droidblue.defaults.generics as generics
import droidblue.defaults.choose as choose

from droidblue.core.steps import Stepper
from droidblue.defaults.actions import PerformFocusActionRule, PerformFocusActionEdge


def test_performAction(single_state):
    state = single_state
    new_state = None

    state.pushStepper(Stepper([('performAction',)], active_id=0))

    edge_list = state.getEdges()

    assert edge_list

    for edge in edge_list:
        if isinstance(edge, PerformFocusActionEdge):
            new_state = edge.getExactState(state)
            break

    else:
        assert not edge_list
        assert False

    opp_set = copy.deepcopy(new_state.usedOpportunity_set)

    # set([, (<PerformFocusActionRule object at 0x10b864c10 pilot_id:0, upgrade_id:None>,)])

    assert ('performAction', 0, 1, 'performAction') in opp_set

    opp_set -= {('performAction', 0, 1, 'performAction')}
    assert type(opp_set.pop()[0]) == PerformFocusActionRule


    assert not new_state.getEdges(fastforward_bool=False)


def test_rules(single_state):
    print sorted(single_state.edgeRules_dict.keys())
    print sorted(single_state.const.edgeRules_dict.keys())

    for step_tup, rule_list in sorted(single_state.const.edgeRules_dict.iteritems()):
        print step_tup
        # print '    ', rule_list

        for rule in rule_list:
            # assert rule.getEdges(single_state)

            print '  ', rule
            for edge in rule._getEdges(single_state):
                print '    ', edge


    # assert False


# combination
# 2 orders beef stew non spicy, alicha wot
# shiro
# gomen
# potato cabbage

