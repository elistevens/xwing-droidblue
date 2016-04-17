from droidblue.edge import Edge
from droidblue.rules import Rule
from droidblue.steps import Stepper


class ChooseActivePilotRule(Rule):
    chosen_str = None
    edge_cls = None

    def __init__(self, state, pilot_id, step_list):
        self.player_id = state.pilots[pilot_id].player_id

        super(ChooseActivePilotRule, self).__init__(state, pilot_id, step_list)

    def getEdges(self, state):
        edge_list = []
        if not state.getStat(self.pilot_id, 'chosen_' + self.chosen_str):
            edge_list.append(self.edge_cls(self.pilot_id))
        return edge_list

    def filterEdges(self, edge_list, state):
        new_list = []
        for edge in edge_list:
            if edge.active_id <= self.player_id and self.filterSecondary(state, edge):
                new_list.append(edge)

        return new_list


class DialsChooseActivePilotRule(ChooseActivePilotRule):
    chosen_str = 'dials'
    edge_cls = DialsChooseActivePilotEdge

    def filterSecondary(self, state, edge):
        return self.pilot_id <= edge.active_id


class ActivationChooseActivePilotRule(ChooseActivePilotRule):
    chosen_str = 'activation'
    edge_cls = ActivationChooseActivePilotEdge

    def filterSecondary(self, state, edge):
        return state.getStat(self.pilot_id, 'ps') <= state.getStat(edge.active_id, 'ps')


class CombatChooseActivePilotRule(ChooseActivePilotRule):
    chosen_str = 'combat'
    edge_cls = CombatChooseActivePilotEdge

    def filterSecondary(self, state, edge):
        return state.getStat(self.pilot_id, 'ps') >= state.getStat(edge.active_id, 'ps')


class ChooseActivePilotEdge(Edge):
    mandatory_bool = True
    chosen_str = None
    stepper_func = None

    def transitionImpl(self, state):
        state.setState(self.active_id, 'chosen_' + self.chosen_str, 1)
        state.pushStepper(Stepper(self.stepper_func(), self.active_id))


class DialsChooseActivePilotEdge(Edge):
    chosen_str = 'dials'
    stepper_func = Stepper.steps_dial


class ActivationChooseActivePilotEdge(Edge):
    chosen_str = 'activation'
    stepper_func = Stepper.steps_activation


class CombatChooseActivePilotEdge(Edge):
    chosen_str = 'combat'
    stepper_func = Stepper.steps_combat
