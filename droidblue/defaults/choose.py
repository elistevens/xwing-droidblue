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
    chosen_str = None
    stepper_func = None

    def __init__(self, active_id, order_tup):
        super(ChooseActivePilotEdge, self).__init__(active_id)
        self.order_tup = order_tup

    def transitionImpl(self, state):
        log.debug("Choosing {} for {}".format(self.active_id, self.chosen_str))
        state.setFlag(self.active_id, 'chosen_' + self.chosen_str)
        state.pushStepper(Stepper(self.stepper_func(), self.active_id))


class DialsChooseActivePilotEdge(ChooseActivePilotEdge):
    chosen_str = 'dials'
    stepper_func = Stepper.steps_dial


class ActivationChooseActivePilotEdge(ChooseActivePilotEdge):
    chosen_str = 'activation'
    stepper_func = Stepper.steps_activation


class CombatChooseActivePilotEdge(ChooseActivePilotEdge):
    chosen_str = 'combat'
    stepper_func = Stepper.steps_combat


class ChooseActivePilotRule(Rule):
    isOncePerRound_bool = True
    chosen_str = None
    edge_cls = None

    def __init__(self, state, pilot_id):
        log.debug(state.pilot_count)
        log.debug(pilot_id)
        self.player_id = state._getRawStat(pilot_id, 'player_id')

        super(ChooseActivePilotRule, self).__init__(state, [(self.chosen_str,)], pilot_id)

    # FIXME: I should be able to get rid of the chosen_XXX flags due to the
    # opportunity handling code, but it breaks. Need to figure that out.
    def isAvailable(self, state):
        return super(ChooseActivePilotRule, self).isAvailable(state) and \
            not state.getFlag(self.pilot_id, 'chosen_' + self.chosen_str)

    def _getEdges(self, state):
        order_tup = self.orderTuple(state)
        return [self.edge_cls(self.pilot_id, order_tup)]

    def filterEdges(self, edge_list, state):
        order_tup = min(edge.order_tup for edge in edge_list)
        return [edge for edge in edge_list if edge.order_tup == order_tup]


class DialsChooseActivePilotRule(ChooseActivePilotRule):
    chosen_str = 'dials'
    edge_cls = DialsChooseActivePilotEdge

    def orderTuple(self, state):
        return (self.player_id, self.pilot_id)


class ActivationChooseActivePilotRule(ChooseActivePilotRule):
    chosen_str = 'activation'
    edge_cls = ActivationChooseActivePilotEdge

    def orderTuple(self, state):
        return (state.getStat(self.pilot_id, 'ps'), self.player_id)


class CombatChooseActivePilotRule(ChooseActivePilotRule):
    chosen_str = 'combat'
    edge_cls = CombatChooseActivePilotEdge

    def orderTuple(self, state):
        return (-state.getStat(self.pilot_id, 'ps'), self.player_id)


rule_list = [DialsChooseActivePilotRule, ActivationChooseActivePilotRule, CombatChooseActivePilotRule]
