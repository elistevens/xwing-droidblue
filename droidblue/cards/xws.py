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
    "xwing-miniatures-font-attack-frontback": [droidblue.defaults.attacks.AttackPrimaryAuxBackRule, droidblue.defaults.attacks.AttackPrimaryForwardRule],
    "xwing-miniatures-font-attack-180": [droidblue.defaults.attacks.AttackPrimaryAuxSideRule],
    "xwing-miniatures-font-attack-turret": [droidblue.defaults.attacks.AttackPrimaryTurretRule],
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
        rule_list.extend(attackIcon2rule_dict[raw_dict['attack_icon']])
    else:
        rule_list.append(droidblue.defaults.attacks.AttackPrimaryForwardRule)

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

    try:
        ship_dict[canonicalize(raw_dict['ship'])].setdefault('pilots', {})[canonicalize(raw_dict['name'])] = {
            'stats': {
                'ps': raw_dict['skill'],
                'unique': raw_dict.get('unique', False),
            },
        }
    except:
        print raw_dict

pilots_max = max(len(s['pilots']) for s in ship_dict.values())

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

('aggressor', 6) ['ig88a', 'ig88c', 'ig88b', 'ig88d']
('tiefighter', 5) ['wingedgundark', 'nightbeast']
('tiefighter', 6) ['darkcurse', 'backstabber', 'youngster']
('tiefighter', 7) ['maulermithel', 'scourge']
('tiefofighter', 7) ['omegaace', 'zetaleader']
('tieinterceptor', 5) ['felswrath', 'lieutenantlorrir']
('tieinterceptor', 7) ['turrphennir', 'tetrancowall']
('xwing', 5) ['biggsdarklighter', 'hobbieklivian']
('xwing', 8) ['wesjanson', 'lukeskywalker']

('tiedefender', 6) ['glaivesqua', 'colonelvessery']
('tiefighter', 3) ['obsidiansquadronpilot', 'chaser']
('tiefighter', 4) ['blacksquadronpilot', 'wampa']
('tiefofighter', 4) ['epsilonace', 'omegasquadronpilot']
('tieinterceptor', 6) ['kirkanos', 'royalguardpilot']


('firespray31', 5) ['mandalorianmercenary', 'krassistrelix']
('firespray31', 7) ['kathscarlet', 'kathscarletscum']
('firespray31', 8) ['bobafett', 'bobafettscum']
('ywing', 2) ['goldsquadronpilot', 'syndicatethug']
('ywing', 4) ['graysquadronpilot', 'hiredgun']

"""
