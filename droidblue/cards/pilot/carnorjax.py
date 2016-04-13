from droidblue.cards.generics import PerformFocusActionEdge, PerformEvadeActionEdge
from droidblue.edge import SpendFocusTokenEdge, SpendEvadeTokenEdge
from droidblue.rules import Rule
from droidblue.steps import Stepper


class CarnorJaxRule(Rule):
    card_type = 'pilot'
    card_name = 'carnorjax'
    focusEvadeTypes_tup = (PerformFocusActionEdge, PerformEvadeActionEdge, SpendFocusTokenEdge, SpendEvadeTokenEdge)

    def __init__(self, state, pilot_id):
        step_list = [Stepper.wildcard_key]
        super(CarnorJaxRule, self).__init__(state, pilot_id, step_list)

    def isAvailable(self, state):
        return super(CarnorJaxRule, self).isAvailable(state) and \
               state.range(self.pilot_id, state.active_id) == 1

    def filterEdges(self, edge_list, state):
        return [edge for edge in edge_list if not isinstance(edge, self.focusEvadeTypes_tup)]

rule_list = [CarnorJaxRule]
