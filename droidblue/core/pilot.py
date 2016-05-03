import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)

import math

import droidblue.defaults
import droidblue.defaults.actions
import droidblue.defaults.attacks
import droidblue.defaults.choose
import droidblue.defaults.generics
import droidblue.defaults.maneuvers

from droidblue.cards import xws

from droidblue.core.base import Base
from droidblue.util import importstr


class Pilot(Base):
    def __init__(self, state, pilot_id):
        self.state = state
        self.pilot_id = pilot_id
        self.maneuver_tup = None

        state._setRawStat(pilot_id, 'shield', state.getStat(pilot_id, 'shield_max'))

        super(Pilot, self).__init__()


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
        self.state.position_array[self.pilot_id, 0] = value

    @property
    def y(self):
        return float(self.state.position_array[self.pilot_id, 1])
    @y.setter
    def y(self, value):
        self.state.position_array[self.pilot_id, 1] = value

    @property
    def heading_radians(self):
        return float(self.state.position_array[self.pilot_id, 2])
    @heading_radians.setter
    def heading_radians(self, value):
        self.state.position_array[self.pilot_id, 2] = value


    @classmethod
    def initRules(cls, const, pilot_id, upgrade_offset, faction_str, pilot_json):
        # Generic rules
        rule_list = []
        rule_list.extend(droidblue.defaults.actions.rule_list)
        rule_list.extend(droidblue.defaults.attacks.rule_list)
        rule_list.extend(droidblue.defaults.choose.rule_list)
        rule_list.extend(droidblue.defaults.generics.rule_list)
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
        upgrade_count = 0
        for slot_str, upgrade_list in pilot_json['upgrades'].iteritems():
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

        # This has to come late, since upgrades might change the value of
        # shield_max
        const._setRawStat(pilot_id, 'points', pilot_json['points'])
        const._setRawStat(pilot_id, 'upgrade_count', upgrade_count)

        return upgrade_count

    def toJson(self, state):
        stat_list = state.stat_list + state.const.stat_list

        j = {'ship': state.const.ship_list[self.pilot_id], 'pilot': state.const.pilot_list[self.pilot_id]}
        j['stats'] = {k: state.getStat(self.pilot_id, k) for k in state.const.stat_list}
        j['tokens'] = {k: state.getStat(self.pilot_id, k) for k in state.token_list}
        j['flags'] = {k: state.getStat(self.pilot_id, k) for k in state.flag_list}

        j['position'] = {
            'x': self.x,
            'y': self.y,
            'heading_radians': self.heading_radians,
            'heading_degrees': math.degrees(self.heading_radians),
        }

        return j
