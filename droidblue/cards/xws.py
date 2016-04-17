import re

import droidblue.cards.raw as raw
import droidblue.defaults.generics
from droidblue.base import SmallBase, LargeBase

subfaction2faction_dict = {
    "Rebel Alliance": "Rebel",
    "Resistance": "Rebel",
    "Galactic Empire": "Imperial",
    "First Order": "Imperial",
    "Scum and Villainy": "Scum",
}

canonicalizationExceptions_dict = {
    "Astromech Droid": "amd",
    "Salvaged Astromech Droid": "samd",
    "Elite Pilot Talent": "ept",
    "Modification": "mod",
}

def canonicalize(name):
    if name in canonicalizationExceptions_dict:
        return canonicalizationExceptions_dict[name]

    return re.sub('[^a-z0-9]', '', name.lower())

attackIcon2rule_dict = {
    "xwing-miniatures-font-attack-frontback": droidblue.defaults.generics.AttackPrimaryAuxBackRule,
    "xwing-miniatures-font-attack-180": droidblue.defaults.generics.AttackPrimaryAuxSideRule,
    "xwing-miniatures-font-attack-turret": droidblue.defaults.generics.AttackPrimaryTurretRule,
}
translate_dict = {
    'attack': 'atk',
    'agility': 'agi',
    'shields': 'shield_max',
    'hull': 'hull_max',
}

ship_dict = {}
for ship_str, raw_dict in raw.shipData_dict.iteritems():
    if raw_dict.get('huge', False):
        continue

    rule_list = [droidblue.defaults.generics.AttackPrimaryArcRule]
    if 'attack_icon' in raw_dict:
        rule_list.append(attackIcon2rule_dict[raw_dict['attack_icon']])

    for action_str in raw_dict['actions']:
        rule_str = 'Perform{}ActionRule'.format(action_str.title().replace(' ', ''))
        rule_list.append(getattr(droidblue.defaults.generics, rule_str))

    stat_dict = {translate_dict.get(a, a): raw_dict[a] for a in ['attack', 'agility', 'hull', 'shields']}

    ship_dict[canonicalize(ship_str)] = {
        'base': LargeBase if raw_dict.get('large', False) else SmallBase,
        'rule_list': rule_list,
        'stat_dict': stat_dict,
        'maneuvers': raw_dict['maneuvers'],
    }

pilot_dict = {}
for raw_dict in raw.pilotData_list:
    if 'skip' in raw_dict:
        continue

    print raw_dict.keys()
    pilot_dict[canonicalize(raw_dict['name'])] = {
        'stats': {'ps': raw_dict['skill']},
    }

"""
    "JumpMaster 5000": {
        "name": "JumpMaster 5000",
        "factions": [
            "Scum and Villainy"
        ],
        "large": true,
        "attack": 2,
        "agility": 2,
        "hull": 5,
        "shields": 4,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll"
        ],
        "attack_icon": "xwing-miniatures-font-attack-turret",
        "maneuvers": [
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 2, 2, 2, 1, 1, 0, 0, 0 ],
            [ 2, 2, 2, 1, 1, 0, 1, 3 ],
            [ 0, 1, 1, 1, 0, 0, 0, 0 ],
            [ 0, 0, 1, 0, 0, 3, 0, 0 ]
        ]
    },
...
    {
        "name": "\"Fel's Wrath\"",
        "faction": "Galactic Empire",
        "id": 26,
        "unique": true,
        "ship": "TIE Interceptor",
        "skill": 5,
        "points": 23,
        "slots": []
    },
"""
