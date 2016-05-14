import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)

import itertools

from droidblue.core.edge import Edge
from droidblue.core.steps import Stepper

from droidblue.cards.xws import ship_dict
from droidblue.core.rules import ActiveAbilityRule
from droidblue.util import canonicalize


class SetDialRule(ActiveAbilityRule):
    maneuver_list = ['turnL', 'bankL', 'forward', 'bankR', 'turnR', 'kturn', 'sloopL', 'sloopR', 'trollL', 'trollR']
    notAvailable = 0
    white = 1
    green = 2
    red = 3

    def __init__(self, state, pilot_id):
        super(SetDialRule, self).__init__(state, 'setDial', pilot_id)

    def isAvailable(self, state):
        return super(SetDialRule, self).isAvailable(state) and \
            not state.pilots[self.pilot_id].maneuver_tup

    def _getEdges(self, state):
        if state.getStat(self.pilot_id, 'ionizedAt_count') <= state.getToken(self.pilot_id, 'ion'):
            return [SetDialEdge(self.pilot_id, self.white, 'forward', 1, known=True)]

        edge_list = []
        ship_str = state.const.ship_list[self.pilot_id]
        for speed_int, color_list in enumerate(ship_dict[canonicalize(ship_str)]['maneuvers']):
            for color_int, type_str in itertools.izip(color_list, self.maneuver_list):
                if color_int == self.notAvailable:
                    continue

                # TODO: verify that there's no way to clear stress between dials and reveal
                if color_int == self.red and state.getToken(self.pilot_id, 'stress') > 0:
                    continue

                if speed_int == 0 and type_str == 'forward':
                    edge_list.append(SetDialEdge(self.pilot_id, color_int, 'stop'))
                else:
                    edge_list.append(SetDialEdge(self.pilot_id, color_int, type_str, speed_int))

        # return edge_list[:5]
        return edge_list


class SetDialEdge(Edge):
    mandatory_bool = True
    
    def __init__(self, pilot_id, color_int, type_str, speed_int=None, known=False):
        super(SetDialEdge, self).__init__(pilot_id)
        
        self.color_int = color_int
        self.type_str = type_str
        self.speed_int = speed_int
        self.maneuver_str = '{}{}'.format(type_str, speed_int or '')
        self.known = known

    def transitionImpl(self, state):
        state.pilots[self.active_id].maneuver_tup = (self.maneuver_str, self.color_int)


class RevealDialRule(ActiveAbilityRule):
    def __init__(self, state, pilot_id):
        super(RevealDialRule, self).__init__(state, 'revealDial', pilot_id)

    def _getEdges(self, state):
        if not state.getFlag(self.pilot_id, 'dialKnown'):
            return [RevealDialEdge(self.pilot_id)]
        return []


class RevealDialEdge(Edge):
    mandatory_bool = True

    def transitionImpl(self, state):
        state.setFlag(self.active_id, 'dialKnown')
        # state.pushStepper(Stepper(['dialRevealed'], self.active_id))


class PerformManeuverRule(ActiveAbilityRule):
    mandatory_bool = True

    def __init__(self, state, pilot_id):
        super(PerformManeuverRule, self).__init__(state, 'performManeuver', pilot_id)

    def _getEdges(self, state):
        return [PerformManeuverEdge(self.pilot_id)]

class PerformManeuverEdge(Edge):
    mandatory_bool = True

    def transitionImpl(self, state):
        pilot_obj = state.pilots[self.active_id]
        maneuver_str, color_int = pilot_obj.maneuver_tup

        if color_int == SetDialRule.red and state.getToken(self.active_id, 'stress') > 0:
            # FIXME: this needs to be implemented
            state.assignToken(self.active_id, 'stress')
            # state.pushStepper(Stepper(['opponentPickDial'], self.active_id))
            # return

        elif color_int == SetDialRule.red:
            state.assignToken(self.active_id, 'stress')
        elif color_int == SetDialRule.green:
            state.setFlag(self.active_id, 'checkPilotStress:green')

        # log.info("{}: {}".format(self.active_id, maneuver_str))
        pilot_obj.performManeuver(maneuver_str)

rule_list = [SetDialRule, RevealDialRule, PerformManeuverRule]
