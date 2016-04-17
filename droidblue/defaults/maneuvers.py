import itertools

from droidblue.rules import Rule, ActiveAbilityRule
from droidblue.edge import Edge
from droidblue.cards.xws import canonicalize, ship_dict

class SetDialRule(ActiveAbilityRule):
    maneuver_list = ['turnL', 'bankL', 'forward', 'bankR', 'turnR', 'kturn', 'sloopL', 'sloopR', 'trollL', 'trollR']
    notAvailable = 0
    white = 1
    green = 2
    red = 3

    def __init__(self, state, pilot_id):
        step_list = [('setDial',)]
        super(SetDialRule, self).__init__(state, pilot_id, step_list)

    def getEdges(self, state):
        if state.getStat(self.pilot_id, 'ionizedAt_count') <= state.getStat(self.pilot_id, 'ion'):
            return [SetDialEdge(self.pilot_id, self.white, 'forward', 1, known=True)]

        edge_list = []
        ship_str = state.pilots[self.pilot_id].ship_str
        for speed_int, color_list in enumerate(ship_dict[canonicalize(ship_str)]['maneuvers']):
            for color_int, type_str in itertools.izip(color_list, self.maneuver_list):
                if color_int == self.notAvailable:
                    continue

                # TODO: verify that there's no way to clear stress between dials and reveal
                if color_int == self.red and state.getStat(self.pilot_id, 'stress') > 0:
                    continue

                if speed_int == 0 and type_str == 'forward':
                    edge_list.append(SetDialEdge(self.pilot_id, color_int, 'stop'))
                else:
                    edge_list.append(SetDialEdge(self.pilot_id, color_int, type_str, speed_int))

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

class RevealDialRule(Rule):
    mandatory_bool = True
