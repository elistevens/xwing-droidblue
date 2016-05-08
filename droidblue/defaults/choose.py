# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)

from droidblue.core.edge import Edge
from droidblue.core.rules import Rule
from droidblue.core.steps import Stepper

class ChooseActivePilotEdge(Edge):
    mandatory_bool = True
    stepper_func = None

    def __init__(self, active_id, order_tup):
        super(ChooseActivePilotEdge, self).__init__(active_id)
        self.order_tup = order_tup

    def transitionImpl(self, state):
        state.pushStepper(Stepper(self.stepper_func(), self.active_id))


class DialsChooseActivePilotEdge(ChooseActivePilotEdge):
    stepper_func = Stepper.steps_dial


class ActivationChooseActivePilotEdge(ChooseActivePilotEdge):
    stepper_func = Stepper.steps_activation


class CombatChooseActivePilotEdge(ChooseActivePilotEdge):
    stepper_func = Stepper.steps_combat


class ChooseActivePilotRule(Rule):
    isOncePerRound_bool = True
    step_str = None
    edge_cls = None

    def __init__(self, state, pilot_id):
        log.debug(state.pilot_count)
        log.debug(pilot_id)
        self.player_id = state._getRawStat(pilot_id, 'player_id')

        super(ChooseActivePilotRule, self).__init__(state, [(self.step_str,)], pilot_id)

    # # FIXME: I should be able to get rid of the chosen_XXX flags due to the
    # # opportunity handling code, but it breaks. Need to figure that out.
    # def isAvailable(self, state):
    #     return super(ChooseActivePilotRule, self).isAvailable(state) and \
    #         not state.getFlag(self.pilot_id, 'chosen_' + self.step_str)

    def _getEdges(self, state):
        order_tup = self.orderTuple(state)
        return [self.edge_cls(self.pilot_id, order_tup)]

    def filterEdges(self, edge_list, state):
        if edge_list:
            order_tup = min(edge.order_tup for edge in edge_list)
        else:
            order_tup = None

        return [edge for edge in edge_list if edge.order_tup == order_tup]


class DialsChooseActivePilotRule(ChooseActivePilotRule):
    step_str = 'dials'
    edge_cls = DialsChooseActivePilotEdge

    def orderTuple(self, state):
        return (self.player_id, self.pilot_id)


class ActivationChooseActivePilotRule(ChooseActivePilotRule):
    step_str = 'activation'
    edge_cls = ActivationChooseActivePilotEdge

    def orderTuple(self, state):
        return (state.getStat(self.pilot_id, 'ps'), self.player_id)


class CombatChooseActivePilotRule(ChooseActivePilotRule):
    step_str = 'combat'
    edge_cls = CombatChooseActivePilotEdge

    def orderTuple(self, state):
        return (-state.getStat(self.pilot_id, 'ps'), self.player_id)


rule_list = [DialsChooseActivePilotRule, ActivationChooseActivePilotRule, CombatChooseActivePilotRule]
