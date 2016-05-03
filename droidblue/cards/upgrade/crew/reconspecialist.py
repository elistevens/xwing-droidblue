from droidblue.defaults.actions import PerformFocusActionRule, PerformFocusActionEdge


class ReconSpecialistRule(PerformFocusActionRule):
    card_type = 'upgrade'
    card_name = 'reconspecialist'
    replacesRule_cls = PerformFocusActionRule

    def _getEdges(self, state):
        return [ReconSpecialistPerformFocusActionEdge(self.pilot_id)]


class ReconSpecialistPerformFocusActionEdge(PerformFocusActionEdge):
    def transitionImpl(self, state):
        state.assignToken(self.active_id, 'focus')
        state.assignToken(self.active_id, 'focus')
        super(ReconSpecialistPerformFocusActionEdge, self).transitionImpl(state)

rule_list = [ReconSpecialistRule]
