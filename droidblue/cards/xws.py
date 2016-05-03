import droidblue.cards.raw as raw
import droidblue.defaults.actions
import droidblue.defaults.attacks

# from droidblue.core.base import SmallBase, LargeBase

# subfaction2faction_dict = {
#     "Rebel Alliance": "Rebel",
#     "Resistance": "Rebel",
#     "Galactic Empire": "Imperial",
#     "First Order": "Imperial",
#     "Scum and Villainy": "Scum",
# }
from droidblue.util import canonicalize

attackIcon2rule_dict = {
    "xwing-miniatures-font-attack-frontback": droidblue.defaults.attacks.AttackPrimaryAuxBackRule,
    "xwing-miniatures-font-attack-180": droidblue.defaults.attacks.AttackPrimaryAuxSideRule,
    "xwing-miniatures-font-attack-turret": droidblue.defaults.attacks.AttackPrimaryTurretRule,
}
translate_dict = {
    'attack': 'atk',
    'agility': 'agi',
    'shields': 'shield_max',
    'hull': 'hull_max',
    'large': 'isLarge',
}

ship_dict = {}
for ship_str, raw_dict in raw.shipData_dict.iteritems():
    if raw_dict.get('huge', False):
        continue

    rule_list = []

    if 'attack_icon' in raw_dict:
        rule_list.append(attackIcon2rule_dict[raw_dict['attack_icon']])

    for action_str in raw_dict['actions']:
        rule_str = 'Perform{}ActionRule'.format(action_str.title().replace(' ', ''))
        rule_list.append(getattr(droidblue.defaults.actions, rule_str))

    stat_dict = {translate_dict.get(a, a): raw_dict[a] for a in ['attack', 'agility', 'hull', 'shields']}
    stat_dict['ionizedAt_count'] = 2 if raw_dict.get('large', False) else 1

    ship_dict[canonicalize(ship_str)] = {
        # 'base': LargeBase if raw_dict.get('large', False) else SmallBase,
        'rule_list': rule_list,
        'stat_dict': stat_dict,
        'maneuvers': raw_dict['maneuvers'],
    }

pilot_dict = {}
for raw_dict in raw.pilotData_list:
    if 'skip' in raw_dict:
        continue

    # print raw_dict.keys()
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
