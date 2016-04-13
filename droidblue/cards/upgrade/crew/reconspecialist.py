from droidblue.cards.generics import PerformFocusActionEdge
from droidblue.rules import ActiveAbilityRule
from droidblue.steps import Stepper


class ReconSpecialistRule(ActiveAbilityRule):
    card_type = 'upgrade'
    card_name = 'reconspecialist'

    def __init__(self, state, pilot_id):
        step_list = [Stepper.wildcard_key]
        super(ReconSpecialistRule, self).__init__(state, pilot_id, step_list)

    def filterEdges(self, edge_list, state):
        new_list = []
        for edge in edge_list:
            if type(edge) == PerformFocusActionEdge:
                edge = ReconSpecialistPerformFocusActionEdge(edge.active_id)

            new_list.append(edge)

        return new_list


class ReconSpecialistPerformFocusActionEdge(PerformFocusActionEdge):
    def transitionImpl(self, state):
        state.assignToken(self.active_id, 'focus')
        state.assignToken(self.active_id, 'focus')

rule_list = [ReconSpecialistRule]
