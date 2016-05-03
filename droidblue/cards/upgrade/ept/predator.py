from droidblue.steps import Stepper

from droidblue.core.rules import ActiveAbilityRule
from droidblue.defaults.actions import PerformFocusActionEdge


class PredatorRule(ActiveAbilityRule):
    card_type = 'upgrade'
    card_name = 'Predator'

    def __init__(self, state, pilot_id):
        step_list = [Stepper.wildcard_key]
        super(PredatorRule, self).__init__(state, pilot_id, step_list)

    def filterEdges(self, edge_list, state):
        new_list = []
        for edge in edge_list:
            if type(edge) == PerformFocusActionEdge:
                edge = PredatorPerformFocusActionEdge(edge.active_id)

            new_list.append(edge)

        return new_list


class PredatorPerformFocusActionEdge(PerformFocusActionEdge):
    def transitionImpl(self, state):
        state.assignToken(self.active_id, 'focus')
        state.assignToken(self.active_id, 'focus')

rule_list = [PredatorRule]
