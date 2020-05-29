import glob
import json
import os

from typing import NewType, Optional, Dict, List, Tuple

from droidblue.util import importstr, canonicalize
from droidblue.core.rules import Rule

with open(os.path.join(os.path.dirname(__file__), 'onehot.json')) as fp:
    try:
        xws2onehot_dict = json.load(fp)
    except:
        xws2onehot_dict = {'pilot':{}, 'upgrade': {}}
xws2onehot_dirty_bool = False

from ..logging_config import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARN)
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)

xws2json_dict = {}



for json_path in glob.glob(os.path.join(os.path.join(os.path.dirname(__file__), 'xwing-data2/data/pilots/*/*.json'))):
    with open(json_path) as fp:
        ship_dict = json.load(fp)

    pilot_list = ship_dict.pop('pilots')

    for pilot_dict in pilot_list:
        combined_dict = {}
        combined_dict.update(ship_dict)
        combined_dict.update(pilot_dict) # important this comes last to overwrite stuff
        pilot_dict['ship_name'] = ship_dict['name']
        pilot_dict['ship_xws'] = ship_dict['xws']

        assert combined_dict['xws'] not in xws2json_dict, combined_dict['xws']
        xws2json_dict[combined_dict['xws']] = combined_dict

        if 'ability' in pilot_dict:
            if pilot_dict['xws'] not in xws2onehot_dict:
                xws2onehot_dict['pilot'][pilot_dict['xws']] = len(xws2onehot_dict['pilot'])
                xws2onehot_dirty_bool = True

            import_path = 'droidblue.cards.pilot.{}.{}'.format(
                ship_dict['xws'].replace('-', '_'),
                pilot_dict['xws'].replace('-', '_'),
            )
            try:
                importstr(import_path)
            except ImportError as e:
                log.debug("Missing pilot: {}".format(import_path))

        if 'shipAbility' in pilot_dict:
            ability_xws = canonicalize(pilot_dict['shipAbility']['name'].replace('-', ''))

            if ability_xws not in xws2onehot_dict:
                xws2onehot_dict['pilot'][ability_xws] = len(xws2onehot_dict['pilot'])
                xws2onehot_dirty_bool = True

            import_path = 'droidblue.cards.pilot.{}.{}'.format(
                ship_dict['xws'].replace('-', '_'),
                ability_xws,
            )
            try:
                importstr(import_path)
            except ImportError as e:
                log.debug("Missing ship ability: {}".format(import_path))

    # faction_str = ship_dict.pop('faction')
    #
    # assert ship_dict['xws'] not in xws2json_dict, ship_dict['xws']
    # xws2json_dict[ship_dict['xws']] = ship_dict

for json_path in glob.glob(os.path.join(os.path.join(os.path.dirname(__file__), 'xwing-data2/data/upgrades/*.json'))):
    with open(json_path) as fp:
        upgrade_list = json.load(fp)

    for upgrade_dict in upgrade_list:
        xws2json_dict[upgrade_dict['xws']] = upgrade_dict

        if upgrade_dict['xws'] not in xws2onehot_dict:
            xws2onehot_dict['upgrade'][upgrade_dict['xws']] = len(xws2onehot_dict['upgrade'])
            xws2onehot_dirty_bool = True

        import_path = 'droidblue.cards.upgrade.{}.{}'.format(
            canonicalize(upgrade_dict['sides'][0]['type']),
            upgrade_dict['xws'].replace('-', '_'),
        )
        try:
            importstr(import_path)
        except ImportError as e:
            log.debug("Missing upgrade: {}".format(import_path))

if xws2onehot_dirty_bool:
    with open(os.path.join(os.path.dirname(__file__), 'onehot.json'), 'w') as fp:
        log.warning("Updating {}, {} pilots, {} upgrades".format(
            os.path.join(os.path.dirname(__file__), 'onehot.json'),
            len(xws2onehot_dict['pilot']),
            len(xws2onehot_dict['upgrade']),
        ))
        json.dump(xws2onehot_dict, fp, sort_keys=True, indent=2)

xws2cls_dict: Dict[str, List[type]] = {}

class XwsCard:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        xws_id = getattr(cls, 'xws_id', cls.__name__.lower())
        xws2cls_dict.setdefault(xws_id, []).append(cls)

class Pilot:
    @classmethod
    def fromXws(cls, pilot_xws: str, upgrade_list: List[str]):
        import droidblue.defaults.actions
        import droidblue.defaults.attacks
        import droidblue.defaults.choose
        import droidblue.defaults.maneuvers

        pilot_dict = xws2json_dict[pilot_xws]

        rule_list: List[type] = []
        rule_list.extend(droidblue.defaults.actions.rule_list)
        rule_list.extend(droidblue.defaults.attacks.rule_list)
        rule_list.extend(droidblue.defaults.choose.rule_list)
        rule_list.extend(droidblue.defaults.maneuvers.rule_list)

        if 'ability' in pilot_dict:
            if pilot_xws not in xws2cls_dict:
                log.warning("Skipping pilot ability: {}".format(pilot_xws))
            else:
                rule_list.extend(xws2cls_dict[pilot_xws])

        if 'shipAbility' in pilot_dict:
            shipAbility_xws = canonicalize(pilot_dict['shipAbility']['name'])
            if shipAbility_xws not in xws2cls_dict:
                log.warning("Skipping ship ability: {} ({})".format(shipAbility_xws, pilot_dict['ship_name']))
            else:
                rule_list.extend(xws2cls_dict[shipAbility_xws])

        for upgrade_xws in upgrade_list:
            if upgrade_xws not in xws2cls_dict:
                log.warning("Skipping upgrade: {}".format(upgrade_xws))
            else:
                rule_list.extend(xws2cls_dict[upgrade_xws])

        return cls(pilot_dict, rule_list)

    def __init__(self, pilot_dict, rule_list):
        pass

    @classmethod
    def initRules(cls, const: ConstantState, pilot_id: PilotId, faction_str: str, pilot_json: Dict):
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
