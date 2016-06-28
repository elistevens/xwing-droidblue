import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)

import itertools
import math

import numpy as np

from droidblue.core.base import Base
from droidblue.util import importstr


class Pilot(Base):
    def __init__(self, state, pilot_id):
        self.state = state
        self.pilot_id = pilot_id

    @property
    def ship_str(self):
        return self.state.const.ship_list[self.pilot_id]

    @property
    def pilot_str(self):
        return self.state.const.pilot_list[self.pilot_id]

    @property
    def isLarge(self):
        return self.state.const._getRawStat(self.pilot_id, 'isLarge')

    @property
    def width(self):
        return self._widths[self.isLarge]

    @property
    def x(self):
        return float(self.state.position_array[self.pilot_id, 0])
    @x.setter
    def x(self, value):
        self.state.position_array = np.copy(self.state.position_array)
        self.state.position_array[self.pilot_id, 0] = value

    @property
    def dx(self):
        return float(self.state.position_array[self.pilot_id, 1])
    @dx.setter
    def dx(self, value):
        self.state.position_array = np.copy(self.state.position_array)
        self.state.position_array[self.pilot_id, 1] = value

    @property
    def y(self):
        return float(self.state.position_array[self.pilot_id, 2])
    @y.setter
    def y(self, value):
        self.state.position_array = np.copy(self.state.position_array)
        self.state.position_array[self.pilot_id, 2] = value

    @property
    def dy(self):
        return float(self.state.position_array[self.pilot_id, 3])
    @dy.setter
    def dy(self, value):
        self.state.position_array = np.copy(self.state.position_array)
        self.state.position_array[self.pilot_id, 3] = value

    @property
    def heading_radians(self):
        return float(self.state.position_array[self.pilot_id, 4])
    @heading_radians.setter
    def heading_radians(self, value):
        self.state.position_array = np.copy(self.state.position_array)
        self.state.position_array[self.pilot_id, 4] = value

    @property
    def maneuver_tup(self):
        return self.state.maneuver_list[self.pilot_id]
    @maneuver_tup.setter
    def maneuver_tup(self, value):
        self.state.maneuver_list[self.pilot_id] = value

    @classmethod
    def initRules(cls, const, pilot_id, upgrade_offset, faction_str, pilot_json):
        import droidblue.defaults.actions
        import droidblue.defaults.attacks
        import droidblue.defaults.choose
        import droidblue.defaults.maneuvers
        from droidblue.cards import xws

        # Generic rules
        rule_list = []
        rule_list.extend(droidblue.defaults.actions.rule_list)
        rule_list.extend(droidblue.defaults.attacks.rule_list)
        rule_list.extend(droidblue.defaults.choose.rule_list)
        rule_list.extend(droidblue.defaults.maneuvers.rule_list)

        for xws_dict in [xws.ship_dict[pilot_json['ship']], xws.pilot_dict[pilot_json['name']]]:
            for stat, value in xws_dict.get('stat_dict', {}).iteritems():
                log.debug("pilot_id {}, {}: {}".format(pilot_id, stat, value))
                const._setRawStat(pilot_id, stat, value)

            rule_list.extend(xws_dict.get('rule_list', []))

        # Ship and pilot rules
        module_list = ['ship.' + pilot_json['ship'], 'pilot.{}.{}'.format(faction_str, pilot_json['name'])]
        for module_str in module_list:
            try:
                module = importstr('droidblue.cards.{}'.format(module_str))
            except ImportError:
                if '.ship.' not in module_str:
                    log.warn("Module not found: {}".format(module_str))
                continue

            for stat, value in getattr(module, 'stat_dict', {}).iteritems():
                const._setRawStat(pilot_id, stat, value)

            rule_list.extend(getattr(module, 'rule_list', []))

        for rule_cls in rule_list:
            log.debug(rule_cls)
            rule_cls(const, pilot_id)

        # Can't fold in the upgrade rules to the above, since we need to check
        # the cards for discard, etc.
        # We need one "upgrade" to represent the pilot card, for things
        # like "no more pilot ability" crits and once-per-game effects.
        upgrade_count = 1
        for slot_str, upgrade_list in pilot_json.get('upgrades', {}).iteritems():
            for upgrade_str in upgrade_list:
                module_str = 'droidblue.upgrade.{}.{}'.format(slot_str, upgrade_str)

                try:
                    module = importstr('droidblue.{}'.format(module_str))
                except ImportError:
                    log.warn("Module not found: {}".format(module_str))
                    continue

                for rule_cls in getattr(module, 'rule_list', []):
                    rule_cls(const, pilot_id, upgrade_offset + upgrade_count)
                upgrade_count += 1

        const._setRawStat(pilot_id, 'points', pilot_json['points'])
        const._setRawStat(pilot_id, 'upgrade_count', upgrade_count)

        return upgrade_count

    def toJson(self, state):
        state = self.state
        stat_list = state.stat_list + state.const.stat_list

        j = {'ship': state.const.ship_list[self.pilot_id], 'pilot': state.const.pilot_list[self.pilot_id]}
        j['stats'] = {k: state.getStat(self.pilot_id, k) for k in state.const.stat_list}
        j['tokens'] = {k: state.getStat(self.pilot_id, k) for k in state.token_list}
        j['flags'] = {k: state.getStat(self.pilot_id, k) for k in state.flag_list}
        j['damage'] = [int(n) for n in state.damage_array[self.pilot_id] if n]

        j['position'] = {
            'x': self.x,
            'y': self.y,
            'heading_radians': self.heading_radians,
            'heading_degrees': math.degrees(self.heading_radians),
        }

        return j

    def phase1_toNeuralNetInput(self):
        from droidblue.cards import xws
        skip_set = {
            'player_id',
            'upgrade_count',
            'upgrade_offset',
            'simplifyForTraining',
        }

        state = self.state
        pilot_id = self.pilot_id
        stat_list = self.state.const.stat_list + self.state.token_list # + self.state.flag_list # + self.state.targetLock_list

        value_list = []
        value_list.extend(self.toBits(state.getStat(self.pilot_id, 'player_id'), 2))

        for stat_str in self.state.const.stat_list:
            if stat_str not in skip_set:
                value_list.append(state.getStat(pilot_id, stat_str))
        for stat_str in self.state.token_list:
            if stat_str not in skip_set:
                value_list.append(state.getToken(pilot_id, stat_str))

        #value_list.extend(self.toBits(state.getTargetLock1(), 8))
        #value_list.extend(self.toBits(state.getTargetLock2(), 8))

        value_list.append(self.x)
        value_list.append(self.y)
        value_list.append(self.heading_degrees)

        value_list.extend(self.toBits(self.ship_str, sorted(xws.ship_dict.keys())))
        value_list.extend(self.toBits(self.pilot_str, sorted(xws.ship_dict[self.ship_str]['pilots'].keys()), xws.pilots_max))

        return np.array(value_list, dtype=np.float32)

    def phase1_toNeuralNetOutput(self):
        arcType_list = ['Front', 'Side', 'Back', 'Turret']
        pilot_score = 0
        other_score = 0
        pilot_focus = self.state.getToken(self.pilot_id, 'focus')
        pilot_evade = self.state.getToken(self.pilot_id, 'evade')
        pilot_points = self.state.getStat(self.pilot_id, 'points')

        for other_id in range(self.state.const.pilot_count):
            if other_id != self.pilot_id:
                other_pilot = Pilot(self.state, other_id)
                other_focus = self.state.getToken(other_id, 'focus')
                other_evade = self.state.getToken(other_id, 'evade')
                other_points = self.state.getStat(other_id, 'points')
                
                otherRange_list = other_pilot.getArcRanges(self)
                other_red = 0
                other_green = self.state.getStat(other_id, 'agi')

                pilotRange_list = self.getArcRanges(other_pilot)
                pilot_red = 0
                pilot_green = self.state.getStat(self.pilot_id, 'agi')
                
                for i, arcType_str in enumerate(arcType_list):

                    # print otherRange_list
                    range_int = otherRange_list[i]
                    if range_int in {1, 2, 3}:
                        other_red = max(other_red, self.state.getStat(other_id, 'dice{}ArcRange{}'.format(arcType_str, range_int)))
                        # print other_red
                        
                    range_int = pilotRange_list[i]
                    if range_int in {1, 2, 3}:
                        pilot_red = max(pilot_red, self.state.getStat(self.pilot_id, 'dice{}ArcRange{}'.format(arcType_str, range_int)))
                        # print pilot_red

                if other_focus:
                    other_red *= 0.75
                else:
                    other_red *= 0.5
                    
                if pilot_focus:
                    pilot_red *= 0.75
                else:
                    pilot_red *= 0.5

                # print pilot_score, pilot_red, other_green, other_evade, other_points
                    
                pilot_score = max(pilot_score, max(0, pilot_red - other_green * 0.3 - other_evade) * other_points)
                other_score -= max(0, other_red - pilot_green * 0.3 - pilot_evade) * pilot_points

        # print
        return pilot_score - other_score  



    def toBits(self, item, options, max_count=0):
        if isinstance(options, list):
            index = options.index(item)
            options = len(options)
        else:
            index = int(item)
            options = int(options)

        bit_list = [0] * max(options, max_count)

        if index >= 0:
            bit_list[index] = 1

        return bit_list
