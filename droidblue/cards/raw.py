import simplejson as json
shipData_dict = json.loads("""
{
    "X-Wing": {
        "name": "X-Wing",
        "factions": [
            "Rebel Alliance"
        ],
        "attack": 3,
        "agility": 2,
        "hull": 3,
        "shields": 2,
        "actions": [
            "Focus",
            "Target Lock"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                2,
                2,
                2,
                0,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                1,
                1,
                1,
                1,
                1,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ]
        ]
    },
    "Y-Wing": {
        "name": "Y-Wing",
        "factions": [
            "Rebel Alliance",
            "Scum and Villainy"
        ],
        "attack": 2,
        "agility": 1,
        "hull": 5,
        "shields": 3,
        "actions": [
            "Focus",
            "Target Lock"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                2,
                1,
                0,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                3,
                1,
                1,
                1,
                3,
                0
            ],
            [
                0,
                0,
                3,
                0,
                0,
                3
            ]
        ]
    },
    "A-Wing": {
        "name": "A-Wing",
        "factions": [
            "Rebel Alliance"
        ],
        "attack": 2,
        "agility": 3,
        "hull": 2,
        "shields": 2,
        "actions": [
            "Focus",
            "Target Lock",
            "Boost",
            "Evade"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                0,
                0,
                0,
                1,
                0
            ],
            [
                2,
                2,
                2,
                2,
                2,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                3
            ],
            [
                0,
                0,
                2,
                0,
                0,
                0
            ],
            [
                0,
                0,
                2,
                0,
                0,
                3
            ]
        ]
    },
    "YT-1300": {
        "name": "YT-1300",
        "factions": [
            "Rebel Alliance"
        ],
        "attack": 2,
        "agility": 1,
        "hull": 6,
        "shields": 4,
        "actions": [
            "Focus",
            "Target Lock"
        ],
        "attack_icon": "xwing-miniatures-font-attack-turret",
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ]
        ],
        "large": true
    },
    "TIE Fighter": {
        "name": "TIE Fighter",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 2,
        "agility": 3,
        "hull": 3,
        "shields": 0,
        "actions": [
            "Focus",
            "Barrel Roll",
            "Evade"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                0,
                0,
                0,
                1,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "TIE Advanced": {
        "name": "TIE Advanced",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 2,
        "agility": 3,
        "hull": 3,
        "shields": 2,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll",
            "Evade"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                2,
                0,
                2,
                0,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "TIE Interceptor": {
        "name": "TIE Interceptor",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 3,
        "agility": 3,
        "hull": 3,
        "shields": 0,
        "actions": [
            "Focus",
            "Barrel Roll",
            "Boost",
            "Evade"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                0,
                0,
                0,
                1,
                0
            ],
            [
                2,
                2,
                2,
                2,
                2,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                3
            ],
            [
                0,
                0,
                2,
                0,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ]
        ]
    },
    "Firespray-31": {
        "name": "Firespray-31",
        "factions": [
            "Galactic Empire",
            "Scum and Villainy"
        ],
        "attack": 3,
        "agility": 2,
        "hull": 6,
        "shields": 4,
        "actions": [
            "Focus",
            "Target Lock",
            "Evade"
        ],
        "attack_icon": "xwing-miniatures-font-attack-frontback",
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                2,
                2,
                2,
                0,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                1,
                1,
                1,
                1,
                1,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ]
        ],
        "large": true
    },
    "HWK-290": {
        "name": "HWK-290",
        "factions": [
            "Rebel Alliance",
            "Scum and Villainy"
        ],
        "attack": 1,
        "agility": 2,
        "hull": 4,
        "shields": 1,
        "actions": [
            "Focus",
            "Target Lock"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                2,
                2,
                2,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1
            ],
            [
                0,
                3,
                1,
                3,
                0
            ],
            [
                0,
                0,
                3,
                0,
                0
            ]
        ]
    },
    "Lambda-Class Shuttle": {
        "name": "Lambda-Class Shuttle",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 3,
        "agility": 1,
        "hull": 5,
        "shields": 5,
        "actions": [
            "Focus",
            "Target Lock"
        ],
        "maneuvers": [
            [
                0,
                0,
                3,
                0,
                0
            ],
            [
                0,
                2,
                2,
                2,
                0
            ],
            [
                3,
                1,
                2,
                1,
                3
            ],
            [
                0,
                3,
                1,
                3,
                0
            ]
        ],
        "large": true
    },
    "B-Wing": {
        "name": "B-Wing",
        "factions": [
            "Rebel Alliance"
        ],
        "attack": 3,
        "agility": 1,
        "hull": 3,
        "shields": 5,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                3,
                2,
                2,
                2,
                3,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                3
            ],
            [
                0,
                3,
                1,
                3,
                0,
                0
            ],
            [
                0,
                0,
                3,
                0,
                0,
                0
            ]
        ]
    },
    "TIE Bomber": {
        "name": "TIE Bomber",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 2,
        "agility": 2,
        "hull": 6,
        "shields": 0,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                2,
                1,
                0,
                0
            ],
            [
                3,
                2,
                2,
                2,
                3,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ],
            [
                0,
                0,
                0,
                0,
                0,
                3
            ]
        ]
    },
    "GR-75 Medium Transport": {
        "name": "GR-75 Medium Transport",
        "factions": [
            "Rebel Alliance"
        ],
        "energy": 4,
        "agility": 0,
        "hull": 8,
        "shields": 4,
        "actions": [
            "Recover",
            "Reinforce",
            "Coordinate",
            "Jam"
        ],
        "huge": true,
        "epic_points": 2,
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "Z-95 Headhunter": {
        "name": "Z-95 Headhunter",
        "factions": [
            "Rebel Alliance",
            "Scum and Villainy"
        ],
        "attack": 2,
        "agility": 2,
        "hull": 2,
        "shields": 2,
        "actions": [
            "Focus",
            "Target Lock"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                2,
                1,
                0,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0
            ],
            [
                1,
                1,
                1,
                1,
                1,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "TIE Defender": {
        "name": "TIE Defender",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 3,
        "agility": 3,
        "hull": 3,
        "shields": 3,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                3,
                1,
                0,
                1,
                3,
                0
            ],
            [
                3,
                1,
                2,
                1,
                3,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                0,
                0,
                2,
                0,
                0,
                1
            ],
            [
                0,
                0,
                2,
                0,
                0,
                0
            ]
        ]
    },
    "E-Wing": {
        "name": "E-Wing",
        "factions": [
            "Rebel Alliance"
        ],
        "attack": 3,
        "agility": 3,
        "hull": 2,
        "shields": 3,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll",
            "Evade"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                2,
                1,
                0,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "TIE Phantom": {
        "name": "TIE Phantom",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 4,
        "agility": 2,
        "hull": 2,
        "shields": 2,
        "actions": [
            "Focus",
            "Barrel Roll",
            "Evade",
            "Cloak"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                0,
                0,
                0,
                1,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ]
        ]
    },
    "CR90 Corvette (Fore)": {
        "name": "CR90 Corvette (Fore)",
        "factions": [
            "Rebel Alliance"
        ],
        "attack": 4,
        "agility": 0,
        "hull": 8,
        "shields": 5,
        "actions": [
            "Coordinate",
            "Target Lock"
        ],
        "huge": true,
        "epic_points": 1.5,
        "attack_icon": "xwing-miniatures-font-attack-turret",
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                0,
                1,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ],
        "multisection": [
            "cr90corvetteaft"
        ],
        "canonical_name": "cr90corvette"
    },
    "CR90 Corvette (Aft)": {
        "name": "CR90 Corvette (Aft)",
        "factions": [
            "Rebel Alliance"
        ],
        "energy": 5,
        "agility": 0,
        "hull": 8,
        "shields": 3,
        "actions": [
            "Reinforce",
            "Recover"
        ],
        "huge": true,
        "epic_points": 1.5,
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                0,
                1,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ],
        "multisection": [
            "cr90corvettefore"
        ],
        "canonical_name": "cr90corvette"
    },
    "YT-2400": {
        "name": "YT-2400",
        "canonical_name": "yt2400freighter",
        "factions": [
            "Rebel Alliance"
        ],
        "attack": 2,
        "agility": 2,
        "hull": 5,
        "shields": 5,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll"
        ],
        "large": true,
        "attack_icon": "xwing-miniatures-font-attack-turret",
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                1,
                1,
                1,
                1,
                1,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ]
        ]
    },
    "VT-49 Decimator": {
        "name": "VT-49 Decimator",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 3,
        "agility": 0,
        "hull": 12,
        "shields": 4,
        "actions": [
            "Focus",
            "Target Lock"
        ],
        "large": true,
        "attack_icon": "xwing-miniatures-font-attack-turret",
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "StarViper": {
        "name": "StarViper",
        "factions": [
            "Scum and Villainy"
        ],
        "attack": 3,
        "agility": 3,
        "hull": 4,
        "shields": 1,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll",
            "Boost"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0,
                0,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0,
                0,
                0
            ],
            [
                0,
                1,
                2,
                1,
                0,
                0,
                3,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0
            ]
        ]
    },
    "M3-A Interceptor": {
        "name": "M3-A Interceptor",
        "factions": [
            "Scum and Villainy"
        ],
        "attack": 2,
        "agility": 3,
        "hull": 2,
        "shields": 1,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll",
            "Evade"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                2,
                0,
                2,
                1,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0
            ],
            [
                0,
                1,
                2,
                1,
                0,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ],
            [
                0,
                0,
                0,
                0,
                0,
                3
            ]
        ]
    },
    "Aggressor": {
        "name": "Aggressor",
        "factions": [
            "Scum and Villainy"
        ],
        "attack": 3,
        "agility": 3,
        "hull": 4,
        "shields": 4,
        "actions": [
            "Focus",
            "Target Lock",
            "Boost",
            "Evade"
        ],
        "large": true,
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0,
                0,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0,
                0,
                0
            ],
            [
                0,
                2,
                2,
                2,
                0,
                0,
                3,
                3
            ],
            [
                0,
                0,
                0,
                0,
                0,
                3,
                0,
                0
            ]
        ]
    },
    "Raider-class Corvette (Fore)": {
        "name": "Raider-class Corvette (Fore)",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 4,
        "agility": 0,
        "hull": 8,
        "shields": 6,
        "actions": [
            "Recover",
            "Reinforce"
        ],
        "huge": true,
        "epic_points": 1.5,
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "Raider-class Corvette (Aft)": {
        "name": "Raider-class Corvette (Aft)",
        "factions": [
            "Galactic Empire"
        ],
        "energy": 6,
        "agility": 0,
        "hull": 8,
        "shields": 4,
        "actions": [
            "Coordinate",
            "Target Lock"
        ],
        "huge": true,
        "epic_points": 1.5,
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "YV-666": {
        "name": "YV-666",
        "factions": [
            "Scum and Villainy"
        ],
        "attack": 3,
        "agility": 1,
        "hull": 6,
        "shields": 6,
        "large": true,
        "actions": [
            "Focus",
            "Target Lock"
        ],
        "attack_icon": "xwing-miniatures-font-attack-180",
        "maneuvers": [
            [
                0,
                0,
                3,
                0,
                0,
                0
            ],
            [
                0,
                2,
                2,
                2,
                0,
                0
            ],
            [
                3,
                1,
                2,
                1,
                3,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "Kihraxz Fighter": {
        "name": "Kihraxz Fighter",
        "factions": [
            "Scum and Villainy"
        ],
        "attack": 3,
        "agility": 2,
        "hull": 4,
        "shields": 1,
        "actions": [
            "Focus",
            "Target Lock"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                2,
                0,
                2,
                1,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ],
            [
                0,
                0,
                0,
                0,
                0,
                3
            ]
        ]
    },
    "K-Wing": {
        "name": "K-Wing",
        "factions": [
            "Rebel Alliance"
        ],
        "attack": 2,
        "agility": 1,
        "hull": 5,
        "shields": 4,
        "actions": [
            "Focus",
            "Target Lock",
            "SLAM"
        ],
        "attack_icon": "xwing-miniatures-font-attack-turret",
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                2,
                2,
                2,
                0,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ]
        ]
    },
    "TIE Punisher": {
        "name": "TIE Punisher",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 2,
        "agility": 1,
        "hull": 6,
        "shields": 3,
        "actions": [
            "Focus",
            "Target Lock",
            "Boost"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                2,
                2,
                2,
                0,
                0
            ],
            [
                3,
                1,
                2,
                1,
                3,
                0
            ],
            [
                1,
                1,
                1,
                1,
                1,
                0
            ],
            [
                0,
                0,
                0,
                0,
                0,
                3
            ]
        ]
    },
    "Gozanti-class Cruiser": {
        "name": "Gozanti-class Cruiser",
        "factions": [
            "Galactic Empire"
        ],
        "energy": 4,
        "agility": 0,
        "hull": 9,
        "shields": 5,
        "huge": true,
        "epic_points": 2,
        "actions": [
            "Recover",
            "Reinforce",
            "Coordinate",
            "Target Lock"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "VCX-100": {
        "name": "VCX-100",
        "factions": [
            "Rebel Alliance"
        ],
        "attack": 4,
        "agility": 0,
        "hull": 10,
        "shields": 6,
        "large": true,
        "actions": [
            "Focus",
            "Target Lock",
            "Evade"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                3,
                1,
                2,
                1,
                3,
                0
            ],
            [
                1,
                2,
                2,
                2,
                1,
                0
            ],
            [
                3,
                1,
                1,
                1,
                3,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ],
            [
                0,
                0,
                0,
                0,
                0,
                3
            ]
        ]
    },
    "Attack Shuttle": {
        "name": "Attack Shuttle",
        "factions": [
            "Rebel Alliance"
        ],
        "attack": 3,
        "agility": 2,
        "hull": 2,
        "shields": 2,
        "actions": [
            "Focus",
            "Barrel Roll",
            "Evade"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                3,
                2,
                2,
                2,
                3,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                3,
                1,
                1,
                1,
                3,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ]
        ]
    },
    "TIE Advanced Prototype": {
        "name": "TIE Advanced Prototype",
        "canonical_name": "tieadvprototype",
        "factions": [
            "Galactic Empire"
        ],
        "attack": 2,
        "agility": 3,
        "hull": 2,
        "shields": 2,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll",
            "Boost"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                2,
                2,
                0,
                2,
                2,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                0,
                0,
                2,
                0,
                0,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0
            ]
        ]
    },
    "G-1A Starfighter": {
        "name": "G-1A Starfighter",
        "factions": [
            "Scum and Villainy"
        ],
        "attack": 3,
        "agility": 1,
        "hull": 4,
        "shields": 4,
        "actions": [
            "Focus",
            "Target Lock",
            "Evade"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                3,
                2,
                2,
                2,
                3,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0
            ],
            [
                0,
                3,
                2,
                3,
                0,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3
            ]
        ]
    },
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
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                2,
                2,
                2,
                1,
                1,
                0,
                0,
                0
            ],
            [
                2,
                2,
                2,
                1,
                1,
                0,
                1,
                3
            ],
            [
                0,
                1,
                1,
                1,
                0,
                0,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3,
                0,
                0
            ]
        ]
    },
    "T-70 X-Wing": {
        "name": "T-70 X-Wing",
        "factions": [
            "Resistance"
        ],
        "attack": 3,
        "agility": 2,
        "hull": 3,
        "shields": 3,
        "actions": [
            "Focus",
            "Target Lock",
            "Boost"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                0,
                2,
                2,
                2,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0,
                0,
                0,
                3,
                3
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3,
                0,
                0,
                0,
                0
            ]
        ]
    },
    "TIE/fo Fighter": {
        "name": "TIE/fo Fighter",
        "factions": [
            "First Order"
        ],
        "attack": 2,
        "agility": 3,
        "hull": 3,
        "shields": 1,
        "actions": [
            "Focus",
            "Target Lock",
            "Barrel Roll",
            "Evade"
        ],
        "maneuvers": [
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [
                1,
                0,
                0,
                0,
                1,
                0,
                0,
                0
            ],
            [
                2,
                2,
                2,
                2,
                2,
                0,
                3,
                3
            ],
            [
                1,
                1,
                2,
                1,
                1,
                0,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                3,
                0,
                0
            ],
            [
                0,
                0,
                1,
                0,
                0,
                0,
                0,
                0
            ]
        ]
    }
}
""")

pilotData_dict = json.loads("""
[
    {
        "name": "Wedge Antilles",
        "faction": "Rebel Alliance",
        "id": 0,
        "unique": true,
        "ship": "X-Wing",
        "skill": 9,
        "points": 29,
        "slots": [
            "Elite",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Garven Dreis",
        "faction": "Rebel Alliance",
        "id": 1,
        "unique": true,
        "ship": "X-Wing",
        "skill": 6,
        "points": 26,
        "slots": [
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Red Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 2,
        "ship": "X-Wing",
        "skill": 4,
        "points": 23,
        "slots": [
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Rookie Pilot",
        "faction": "Rebel Alliance",
        "id": 3,
        "ship": "X-Wing",
        "skill": 2,
        "points": 21,
        "slots": [
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Biggs Darklighter",
        "faction": "Rebel Alliance",
        "id": 4,
        "unique": true,
        "ship": "X-Wing",
        "skill": 5,
        "points": 25,
        "slots": [
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Luke Skywalker",
        "faction": "Rebel Alliance",
        "id": 5,
        "unique": true,
        "ship": "X-Wing",
        "skill": 8,
        "points": 28,
        "slots": [
            "Elite",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Gray Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 6,
        "ship": "Y-Wing",
        "skill": 4,
        "points": 20,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "\"Dutch\" Vander",
        "faction": "Rebel Alliance",
        "id": 7,
        "unique": true,
        "ship": "Y-Wing",
        "skill": 6,
        "points": 23,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Horton Salm",
        "faction": "Rebel Alliance",
        "id": 8,
        "unique": true,
        "ship": "Y-Wing",
        "skill": 8,
        "points": 25,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Gold Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 9,
        "ship": "Y-Wing",
        "skill": 2,
        "points": 18,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Academy Pilot",
        "faction": "Galactic Empire",
        "id": 10,
        "ship": "TIE Fighter",
        "skill": 1,
        "points": 12,
        "slots": []
    },
    {
        "name": "Obsidian Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 11,
        "ship": "TIE Fighter",
        "skill": 3,
        "points": 13,
        "slots": []
    },
    {
        "name": "Black Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 12,
        "ship": "TIE Fighter",
        "skill": 4,
        "points": 14,
        "slots": [
            "Elite"
        ]
    },
    {
        "name": "\"Winged Gundark\"",
        "faction": "Galactic Empire",
        "id": 13,
        "unique": true,
        "ship": "TIE Fighter",
        "skill": 5,
        "points": 15,
        "slots": []
    },
    {
        "name": "\"Night Beast\"",
        "faction": "Galactic Empire",
        "id": 14,
        "unique": true,
        "ship": "TIE Fighter",
        "skill": 5,
        "points": 15,
        "slots": []
    },
    {
        "name": "\"Backstabber\"",
        "faction": "Galactic Empire",
        "id": 15,
        "unique": true,
        "ship": "TIE Fighter",
        "skill": 6,
        "points": 16,
        "slots": []
    },
    {
        "name": "\"Dark Curse\"",
        "faction": "Galactic Empire",
        "id": 16,
        "unique": true,
        "ship": "TIE Fighter",
        "skill": 6,
        "points": 16,
        "slots": []
    },
    {
        "name": "\"Mauler Mithel\"",
        "faction": "Galactic Empire",
        "id": 17,
        "unique": true,
        "ship": "TIE Fighter",
        "skill": 7,
        "points": 17,
        "slots": [
            "Elite"
        ]
    },
    {
        "name": "\"Howlrunner\"",
        "faction": "Galactic Empire",
        "id": 18,
        "unique": true,
        "ship": "TIE Fighter",
        "skill": 8,
        "points": 18,
        "slots": [
            "Elite"
        ]
    },
    {
        "name": "Maarek Stele",
        "faction": "Galactic Empire",
        "id": 19,
        "unique": true,
        "ship": "TIE Advanced",
        "skill": 7,
        "points": 27,
        "slots": [
            "Elite",
            "Missile"
        ]
    },
    {
        "name": "Tempest Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 20,
        "ship": "TIE Advanced",
        "skill": 2,
        "points": 21,
        "slots": [
            "Missile"
        ]
    },
    {
        "name": "Storm Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 21,
        "ship": "TIE Advanced",
        "skill": 4,
        "points": 23,
        "slots": [
            "Missile"
        ]
    },
    {
        "name": "Darth Vader",
        "faction": "Galactic Empire",
        "id": 22,
        "unique": true,
        "ship": "TIE Advanced",
        "skill": 9,
        "points": 29,
        "slots": [
            "Elite",
            "Missile"
        ]
    },
    {
        "name": "Alpha Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 23,
        "ship": "TIE Interceptor",
        "skill": 1,
        "points": 18,
        "slots": []
    },
    {
        "name": "Avenger Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 24,
        "ship": "TIE Interceptor",
        "skill": 3,
        "points": 20,
        "slots": []
    },
    {
        "name": "Saber Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 25,
        "ship": "TIE Interceptor",
        "skill": 4,
        "points": 21,
        "slots": [
            "Elite"
        ]
    },
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
    {
        "name": "Turr Phennir",
        "faction": "Galactic Empire",
        "id": 27,
        "unique": true,
        "ship": "TIE Interceptor",
        "skill": 7,
        "points": 25,
        "slots": [
            "Elite"
        ]
    },
    {
        "name": "Soontir Fel",
        "faction": "Galactic Empire",
        "id": 28,
        "unique": true,
        "ship": "TIE Interceptor",
        "skill": 9,
        "points": 27,
        "slots": [
            "Elite"
        ]
    },
    {
        "name": "Tycho Celchu",
        "faction": "Rebel Alliance",
        "id": 29,
        "unique": true,
        "ship": "A-Wing",
        "skill": 8,
        "points": 26,
        "slots": [
            "Elite",
            "Missile"
        ]
    },
    {
        "name": "Arvel Crynyd",
        "faction": "Rebel Alliance",
        "id": 30,
        "unique": true,
        "ship": "A-Wing",
        "skill": 6,
        "points": 23,
        "slots": [
            "Missile"
        ]
    },
    {
        "name": "Green Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 31,
        "ship": "A-Wing",
        "skill": 3,
        "points": 19,
        "slots": [
            "Elite",
            "Missile"
        ]
    },
    {
        "name": "Prototype Pilot",
        "faction": "Rebel Alliance",
        "id": 32,
        "ship": "A-Wing",
        "skill": 1,
        "points": 17,
        "slots": [
            "Missile"
        ]
    },
    {
        "name": "Outer Rim Smuggler",
        "faction": "Rebel Alliance",
        "id": 33,
        "ship": "YT-1300",
        "skill": 1,
        "points": 27,
        "slots": [
            "Crew",
            "Crew"
        ]
    },
    {
        "name": "Chewbacca",
        "faction": "Rebel Alliance",
        "id": 34,
        "unique": true,
        "ship": "YT-1300",
        "skill": 5,
        "points": 42,
        "slots": [
            "Elite",
            "Missile",
            "Crew",
            "Crew"
        ],
        "ship_override": {
            "attack": 3,
            "agility": 1,
            "hull": 8,
            "shields": 5
        }
    },
    {
        "name": "Lando Calrissian",
        "faction": "Rebel Alliance",
        "id": 35,
        "unique": true,
        "ship": "YT-1300",
        "skill": 7,
        "points": 44,
        "slots": [
            "Elite",
            "Missile",
            "Crew",
            "Crew"
        ],
        "ship_override": {
            "attack": 3,
            "agility": 1,
            "hull": 8,
            "shields": 5
        }
    },
    {
        "name": "Han Solo",
        "faction": "Rebel Alliance",
        "id": 36,
        "unique": true,
        "ship": "YT-1300",
        "skill": 9,
        "points": 46,
        "slots": [
            "Elite",
            "Missile",
            "Crew",
            "Crew"
        ],
        "ship_override": {
            "attack": 3,
            "agility": 1,
            "hull": 8,
            "shields": 5
        }
    },
    {
        "name": "Kath Scarlet",
        "faction": "Galactic Empire",
        "id": 37,
        "unique": true,
        "ship": "Firespray-31",
        "skill": 7,
        "points": 38,
        "slots": [
            "Elite",
            "Cannon",
            "Bomb",
            "Crew",
            "Missile"
        ]
    },
    {
        "name": "Boba Fett",
        "faction": "Galactic Empire",
        "id": 38,
        "unique": true,
        "ship": "Firespray-31",
        "skill": 8,
        "points": 39,
        "slots": [
            "Elite",
            "Cannon",
            "Bomb",
            "Crew",
            "Missile"
        ]
    },
    {
        "name": "Krassis Trelix",
        "faction": "Galactic Empire",
        "id": 39,
        "unique": true,
        "ship": "Firespray-31",
        "skill": 5,
        "points": 36,
        "slots": [
            "Cannon",
            "Bomb",
            "Crew",
            "Missile"
        ]
    },
    {
        "name": "Bounty Hunter",
        "faction": "Galactic Empire",
        "id": 40,
        "ship": "Firespray-31",
        "skill": 3,
        "points": 33,
        "slots": [
            "Cannon",
            "Bomb",
            "Crew",
            "Missile"
        ]
    },
    {
        "name": "Ten Numb",
        "faction": "Rebel Alliance",
        "id": 41,
        "unique": true,
        "ship": "B-Wing",
        "skill": 8,
        "points": 31,
        "slots": [
            "Elite",
            "System",
            "Cannon",
            "Torpedo",
            "Torpedo"
        ]
    },
    {
        "name": "Ibtisam",
        "faction": "Rebel Alliance",
        "id": 42,
        "unique": true,
        "ship": "B-Wing",
        "skill": 6,
        "points": 28,
        "slots": [
            "Elite",
            "System",
            "Cannon",
            "Torpedo",
            "Torpedo"
        ]
    },
    {
        "name": "Dagger Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 43,
        "ship": "B-Wing",
        "skill": 4,
        "points": 24,
        "slots": [
            "System",
            "Cannon",
            "Torpedo",
            "Torpedo"
        ]
    },
    {
        "name": "Blue Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 44,
        "ship": "B-Wing",
        "skill": 2,
        "points": 22,
        "slots": [
            "System",
            "Cannon",
            "Torpedo",
            "Torpedo"
        ]
    },
    {
        "name": "Rebel Operative",
        "faction": "Rebel Alliance",
        "id": 45,
        "ship": "HWK-290",
        "skill": 2,
        "points": 16,
        "slots": [
            "Turret",
            "Crew"
        ]
    },
    {
        "name": "Roark Garnet",
        "faction": "Rebel Alliance",
        "id": 46,
        "unique": true,
        "ship": "HWK-290",
        "skill": 4,
        "points": 19,
        "slots": [
            "Turret",
            "Crew"
        ]
    },
    {
        "name": "Kyle Katarn",
        "faction": "Rebel Alliance",
        "id": 47,
        "unique": true,
        "ship": "HWK-290",
        "skill": 6,
        "points": 21,
        "slots": [
            "Elite",
            "Turret",
            "Crew"
        ]
    },
    {
        "name": "Jan Ors",
        "faction": "Rebel Alliance",
        "id": 48,
        "unique": true,
        "ship": "HWK-290",
        "skill": 8,
        "points": 25,
        "slots": [
            "Elite",
            "Turret",
            "Crew"
        ]
    },
    {
        "name": "Scimitar Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 49,
        "ship": "TIE Bomber",
        "skill": 2,
        "points": 16,
        "slots": [
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb"
        ]
    },
    {
        "name": "Gamma Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 50,
        "ship": "TIE Bomber",
        "skill": 4,
        "points": 18,
        "slots": [
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb"
        ]
    },
    {
        "name": "Captain Jonus",
        "faction": "Galactic Empire",
        "id": 51,
        "unique": true,
        "ship": "TIE Bomber",
        "skill": 6,
        "points": 22,
        "slots": [
            "Elite",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb"
        ]
    },
    {
        "name": "Major Rhymer",
        "faction": "Galactic Empire",
        "id": 52,
        "unique": true,
        "ship": "TIE Bomber",
        "skill": 7,
        "points": 26,
        "slots": [
            "Elite",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb"
        ]
    },
    {
        "name": "Captain Kagi",
        "faction": "Galactic Empire",
        "id": 53,
        "unique": true,
        "ship": "Lambda-Class Shuttle",
        "skill": 8,
        "points": 27,
        "slots": [
            "System",
            "Cannon",
            "Crew",
            "Crew"
        ]
    },
    {
        "name": "Colonel Jendon",
        "faction": "Galactic Empire",
        "id": 54,
        "unique": true,
        "ship": "Lambda-Class Shuttle",
        "skill": 6,
        "points": 26,
        "slots": [
            "System",
            "Cannon",
            "Crew",
            "Crew"
        ]
    },
    {
        "name": "Captain Yorr",
        "faction": "Galactic Empire",
        "id": 55,
        "unique": true,
        "ship": "Lambda-Class Shuttle",
        "skill": 4,
        "points": 24,
        "slots": [
            "System",
            "Cannon",
            "Crew",
            "Crew"
        ]
    },
    {
        "name": "Omicron Group Pilot",
        "faction": "Galactic Empire",
        "id": 56,
        "ship": "Lambda-Class Shuttle",
        "skill": 2,
        "points": 21,
        "slots": [
            "System",
            "Cannon",
            "Crew",
            "Crew"
        ]
    },
    {
        "name": "Lieutenant Lorrir",
        "faction": "Galactic Empire",
        "id": 57,
        "unique": true,
        "ship": "TIE Interceptor",
        "skill": 5,
        "points": 23,
        "slots": []
    },
    {
        "name": "Royal Guard Pilot",
        "faction": "Galactic Empire",
        "id": 58,
        "ship": "TIE Interceptor",
        "skill": 6,
        "points": 22,
        "slots": [
            "Elite"
        ]
    },
    {
        "name": "Tetran Cowall",
        "faction": "Galactic Empire",
        "id": 59,
        "unique": true,
        "ship": "TIE Interceptor",
        "skill": 7,
        "points": 24,
        "slots": [
            "Elite"
        ]
    },
    {
        "name": "I messed up this pilot, sorry",
        "id": 60,
        "skip": true
    },
    {
        "name": "Kir Kanos",
        "faction": "Galactic Empire",
        "id": 61,
        "unique": true,
        "ship": "TIE Interceptor",
        "skill": 6,
        "points": 24,
        "slots": []
    },
    {
        "name": "Carnor Jax",
        "faction": "Galactic Empire",
        "id": 62,
        "unique": true,
        "ship": "TIE Interceptor",
        "skill": 8,
        "points": 26,
        "slots": [
            "Elite"
        ]
    },
    {
        "name": "GR-75 Medium Transport",
        "faction": "Rebel Alliance",
        "id": 63,
        "epic": true,
        "ship": "GR-75 Medium Transport",
        "skill": 3,
        "points": 30,
        "slots": [
            "Crew",
            "Crew",
            "Cargo",
            "Cargo",
            "Cargo"
        ]
    },
    {
        "name": "Bandit Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 64,
        "ship": "Z-95 Headhunter",
        "skill": 2,
        "points": 12,
        "slots": [
            "Missile"
        ]
    },
    {
        "name": "Tala Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 65,
        "ship": "Z-95 Headhunter",
        "skill": 4,
        "points": 13,
        "slots": [
            "Missile"
        ]
    },
    {
        "name": "Lieutenant Blount",
        "faction": "Rebel Alliance",
        "id": 66,
        "unique": true,
        "ship": "Z-95 Headhunter",
        "skill": 6,
        "points": 17,
        "slots": [
            "Elite",
            "Missile"
        ]
    },
    {
        "name": "Airen Cracken",
        "faction": "Rebel Alliance",
        "id": 67,
        "unique": true,
        "ship": "Z-95 Headhunter",
        "skill": 8,
        "points": 19,
        "slots": [
            "Elite",
            "Missile"
        ]
    },
    {
        "name": "Delta Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 68,
        "ship": "TIE Defender",
        "skill": 1,
        "points": 30,
        "slots": [
            "Cannon",
            "Missile"
        ]
    },
    {
        "name": "Onyx Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 69,
        "ship": "TIE Defender",
        "skill": 3,
        "points": 32,
        "slots": [
            "Cannon",
            "Missile"
        ]
    },
    {
        "name": "Colonel Vessery",
        "faction": "Galactic Empire",
        "id": 70,
        "unique": true,
        "ship": "TIE Defender",
        "skill": 6,
        "points": 35,
        "slots": [
            "Elite",
            "Cannon",
            "Missile"
        ]
    },
    {
        "name": "Rexler Brath",
        "faction": "Galactic Empire",
        "id": 71,
        "unique": true,
        "ship": "TIE Defender",
        "skill": 8,
        "points": 37,
        "slots": [
            "Elite",
            "Cannon",
            "Missile"
        ]
    },
    {
        "name": "Knave Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 72,
        "ship": "E-Wing",
        "skill": 1,
        "points": 27,
        "slots": [
            "System",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Blackmoon Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 73,
        "ship": "E-Wing",
        "skill": 3,
        "points": 29,
        "slots": [
            "System",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Etahn A'baht",
        "faction": "Rebel Alliance",
        "id": 74,
        "unique": true,
        "ship": "E-Wing",
        "skill": 5,
        "points": 32,
        "slots": [
            "Elite",
            "System",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Corran Horn",
        "faction": "Rebel Alliance",
        "id": 75,
        "unique": true,
        "ship": "E-Wing",
        "skill": 8,
        "points": 35,
        "slots": [
            "Elite",
            "System",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Sigma Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 76,
        "ship": "TIE Phantom",
        "skill": 3,
        "points": 25,
        "slots": [
            "System",
            "Crew"
        ]
    },
    {
        "name": "Shadow Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 77,
        "ship": "TIE Phantom",
        "skill": 5,
        "points": 27,
        "slots": [
            "System",
            "Crew"
        ]
    },
    {
        "name": "\"Echo\"",
        "faction": "Galactic Empire",
        "id": 78,
        "unique": true,
        "ship": "TIE Phantom",
        "skill": 6,
        "points": 30,
        "slots": [
            "Elite",
            "System",
            "Crew"
        ]
    },
    {
        "name": "\"Whisper\"",
        "faction": "Galactic Empire",
        "id": 79,
        "unique": true,
        "ship": "TIE Phantom",
        "skill": 7,
        "points": 32,
        "slots": [
            "Elite",
            "System",
            "Crew"
        ]
    },
    {
        "name": "CR90 Corvette (Fore)",
        "faction": "Rebel Alliance",
        "id": 80,
        "epic": true,
        "ship": "CR90 Corvette (Fore)",
        "skill": 4,
        "points": 50,
        "slots": [
            "Crew",
            "Hardpoint",
            "Hardpoint",
            "Team",
            "Team",
            "Cargo"
        ]
    },
    {
        "name": "CR90 Corvette (Aft)",
        "faction": "Rebel Alliance",
        "id": 81,
        "epic": true,
        "ship": "CR90 Corvette (Aft)",
        "skill": 4,
        "points": 40,
        "slots": [
            "Crew",
            "Hardpoint",
            "Team",
            "Cargo"
        ]
    },
    {
        "name": "Wes Janson",
        "faction": "Rebel Alliance",
        "id": 82,
        "unique": true,
        "ship": "X-Wing",
        "skill": 8,
        "points": 29,
        "slots": [
            "Elite",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Jek Porkins",
        "faction": "Rebel Alliance",
        "id": 83,
        "unique": true,
        "ship": "X-Wing",
        "skill": 7,
        "points": 26,
        "slots": [
            "Elite",
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "\"Hobbie\" Klivian",
        "faction": "Rebel Alliance",
        "id": 84,
        "unique": true,
        "ship": "X-Wing",
        "skill": 5,
        "points": 25,
        "slots": [
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Tarn Mison",
        "faction": "Rebel Alliance",
        "id": 85,
        "unique": true,
        "ship": "X-Wing",
        "skill": 3,
        "points": 23,
        "slots": [
            "Torpedo",
            "Astromech"
        ]
    },
    {
        "name": "Jake Farrell",
        "faction": "Rebel Alliance",
        "id": 86,
        "unique": true,
        "ship": "A-Wing",
        "skill": 7,
        "points": 24,
        "slots": [
            "Elite",
            "Missile"
        ]
    },
    {
        "name": "Gemmer Sojan",
        "faction": "Rebel Alliance",
        "id": 87,
        "unique": true,
        "ship": "A-Wing",
        "skill": 5,
        "points": 22,
        "slots": [
            "Missile"
        ]
    },
    {
        "name": "Keyan Farlander",
        "faction": "Rebel Alliance",
        "id": 88,
        "unique": true,
        "ship": "B-Wing",
        "skill": 7,
        "points": 29,
        "slots": [
            "Elite",
            "System",
            "Cannon",
            "Torpedo",
            "Torpedo"
        ]
    },
    {
        "name": "Nera Dantels",
        "faction": "Rebel Alliance",
        "id": 89,
        "unique": true,
        "ship": "B-Wing",
        "skill": 5,
        "points": 26,
        "slots": [
            "Elite",
            "System",
            "Cannon",
            "Torpedo",
            "Torpedo"
        ]
    },
    {
        "name": "CR90 Corvette (Crippled Fore)",
        "skip": true,
        "faction": "Rebel Alliance",
        "id": 90,
        "ship": "CR90 Corvette (Fore)",
        "skill": 4,
        "points": 0,
        "epic": true,
        "slots": [
            "Crew"
        ],
        "ship_override": {
            "attack": 2,
            "agility": 0,
            "hull": 0,
            "shields": 0,
            "actions": []
        }
    },
    {
        "name": "CR90 Corvette (Crippled Aft)",
        "skip": true,
        "faction": "Rebel Alliance",
        "id": 91,
        "ship": "CR90 Corvette (Aft)",
        "skill": 4,
        "points": 0,
        "epic": true,
        "slots": [
            "Cargo"
        ],
        "ship_override": {
            "energy": 1,
            "agility": 0,
            "hull": 0,
            "shields": 0,
            "actions": []
        }
    },
    {
        "name": "Wild Space Fringer",
        "faction": "Rebel Alliance",
        "id": 92,
        "ship": "YT-2400",
        "skill": 2,
        "points": 30,
        "slots": [
            "Cannon",
            "Missile",
            "Crew"
        ]
    },
    {
        "name": "Eaden Vrill",
        "faction": "Rebel Alliance",
        "id": 93,
        "ship": "YT-2400",
        "unique": true,
        "skill": 3,
        "points": 32,
        "slots": [
            "Cannon",
            "Missile",
            "Crew"
        ]
    },
    {
        "name": "\"Leebo\"",
        "faction": "Rebel Alliance",
        "id": 94,
        "ship": "YT-2400",
        "unique": true,
        "skill": 5,
        "points": 34,
        "slots": [
            "Elite",
            "Cannon",
            "Missile",
            "Crew"
        ]
    },
    {
        "name": "Dash Rendar",
        "faction": "Rebel Alliance",
        "id": 95,
        "ship": "YT-2400",
        "unique": true,
        "skill": 7,
        "points": 36,
        "slots": [
            "Elite",
            "Cannon",
            "Missile",
            "Crew"
        ]
    },
    {
        "name": "Patrol Leader",
        "faction": "Galactic Empire",
        "id": 96,
        "ship": "VT-49 Decimator",
        "skill": 3,
        "points": 40,
        "slots": [
            "Torpedo",
            "Crew",
            "Crew",
            "Crew",
            "Bomb"
        ]
    },
    {
        "name": "Captain Oicunn",
        "faction": "Galactic Empire",
        "id": 97,
        "ship": "VT-49 Decimator",
        "skill": 4,
        "points": 42,
        "unique": true,
        "slots": [
            "Elite",
            "Torpedo",
            "Crew",
            "Crew",
            "Crew",
            "Bomb"
        ]
    },
    {
        "name": "Commander Kenkirk",
        "faction": "Galactic Empire",
        "id": 98,
        "ship": "VT-49 Decimator",
        "skill": 6,
        "points": 44,
        "unique": true,
        "slots": [
            "Elite",
            "Torpedo",
            "Crew",
            "Crew",
            "Crew",
            "Bomb"
        ]
    },
    {
        "name": "Rear Admiral Chiraneau",
        "faction": "Galactic Empire",
        "id": 99,
        "ship": "VT-49 Decimator",
        "skill": 8,
        "points": 46,
        "unique": true,
        "slots": [
            "Elite",
            "Torpedo",
            "Crew",
            "Crew",
            "Crew",
            "Bomb"
        ]
    },
    {
        "name": "Prince Xizor",
        "faction": "Scum and Villainy",
        "id": 100,
        "unique": true,
        "ship": "StarViper",
        "skill": 7,
        "points": 31,
        "slots": [
            "Elite",
            "Torpedo"
        ]
    },
    {
        "name": "Guri",
        "faction": "Scum and Villainy",
        "id": 101,
        "unique": true,
        "ship": "StarViper",
        "skill": 5,
        "points": 30,
        "slots": [
            "Elite",
            "Torpedo"
        ]
    },
    {
        "name": "Black Sun Vigo",
        "faction": "Scum and Villainy",
        "id": 102,
        "ship": "StarViper",
        "skill": 3,
        "points": 27,
        "slots": [
            "Torpedo"
        ]
    },
    {
        "name": "Black Sun Enforcer",
        "faction": "Scum and Villainy",
        "id": 103,
        "ship": "StarViper",
        "skill": 1,
        "points": 25,
        "slots": [
            "Torpedo"
        ]
    },
    {
        "name": "Serissu",
        "faction": "Scum and Villainy",
        "id": 104,
        "ship": "M3-A Interceptor",
        "skill": 8,
        "points": 20,
        "unique": true,
        "slots": [
            "Elite"
        ]
    },
    {
        "name": "Laetin A'shera",
        "faction": "Scum and Villainy",
        "id": 105,
        "ship": "M3-A Interceptor",
        "skill": 6,
        "points": 18,
        "unique": true,
        "slots": []
    },
    {
        "name": "Tansarii Point Veteran",
        "faction": "Scum and Villainy",
        "id": 106,
        "ship": "M3-A Interceptor",
        "skill": 5,
        "points": 17,
        "slots": [
            "Elite"
        ]
    },
    {
        "name": "Cartel Spacer",
        "faction": "Scum and Villainy",
        "id": 107,
        "ship": "M3-A Interceptor",
        "skill": 2,
        "points": 14,
        "slots": []
    },
    {
        "name": "IG-88A",
        "faction": "Scum and Villainy",
        "id": 108,
        "unique": true,
        "ship": "Aggressor",
        "skill": 6,
        "points": 36,
        "slots": [
            "Elite",
            "System",
            "Cannon",
            "Cannon",
            "Bomb",
            "Illicit"
        ]
    },
    {
        "name": "IG-88B",
        "faction": "Scum and Villainy",
        "id": 109,
        "unique": true,
        "ship": "Aggressor",
        "skill": 6,
        "points": 36,
        "slots": [
            "Elite",
            "System",
            "Cannon",
            "Cannon",
            "Bomb",
            "Illicit"
        ]
    },
    {
        "name": "IG-88C",
        "faction": "Scum and Villainy",
        "id": 110,
        "unique": true,
        "ship": "Aggressor",
        "skill": 6,
        "points": 36,
        "slots": [
            "Elite",
            "System",
            "Cannon",
            "Cannon",
            "Bomb",
            "Illicit"
        ]
    },
    {
        "name": "IG-88D",
        "faction": "Scum and Villainy",
        "id": 111,
        "unique": true,
        "ship": "Aggressor",
        "skill": 6,
        "points": 36,
        "slots": [
            "Elite",
            "System",
            "Cannon",
            "Cannon",
            "Bomb",
            "Illicit"
        ]
    },
    {
        "name": "N'Dru Suhlak",
        "unique": true,
        "faction": "Scum and Villainy",
        "id": 112,
        "ship": "Z-95 Headhunter",
        "skill": 7,
        "points": 17,
        "slots": [
            "Elite",
            "Missile",
            "Illicit"
        ]
    },
    {
        "name": "Kaa'To Leeachos",
        "unique": true,
        "faction": "Scum and Villainy",
        "id": 113,
        "ship": "Z-95 Headhunter",
        "skill": 5,
        "points": 15,
        "slots": [
            "Elite",
            "Missile",
            "Illicit"
        ]
    },
    {
        "name": "Black Sun Soldier",
        "faction": "Scum and Villainy",
        "id": 114,
        "ship": "Z-95 Headhunter",
        "skill": 3,
        "points": 13,
        "slots": [
            "Missile",
            "Illicit"
        ]
    },
    {
        "name": "Binayre Pirate",
        "faction": "Scum and Villainy",
        "id": 115,
        "ship": "Z-95 Headhunter",
        "skill": 1,
        "points": 12,
        "slots": [
            "Missile",
            "Illicit"
        ]
    },
    {
        "name": "Boba Fett (Scum)",
        "canonical_name": "bobafett",
        "faction": "Scum and Villainy",
        "id": 116,
        "ship": "Firespray-31",
        "skill": 8,
        "points": 39,
        "unique": true,
        "slots": [
            "Elite",
            "Cannon",
            "Bomb",
            "Crew",
            "Missile",
            "Illicit"
        ]
    },
    {
        "name": "Kath Scarlet (Scum)",
        "canonical_name": "kathscarlet",
        "unique": true,
        "faction": "Scum and Villainy",
        "id": 117,
        "ship": "Firespray-31",
        "skill": 7,
        "points": 38,
        "slots": [
            "Elite",
            "Cannon",
            "Bomb",
            "Crew",
            "Missile",
            "Illicit"
        ]
    },
    {
        "name": "Emon Azzameen",
        "unique": true,
        "faction": "Scum and Villainy",
        "id": 118,
        "ship": "Firespray-31",
        "skill": 6,
        "points": 36,
        "slots": [
            "Cannon",
            "Bomb",
            "Crew",
            "Missile",
            "Illicit"
        ]
    },
    {
        "name": "Mandalorian Mercenary",
        "faction": "Scum and Villainy",
        "id": 119,
        "ship": "Firespray-31",
        "skill": 5,
        "points": 35,
        "slots": [
            "Elite",
            "Cannon",
            "Bomb",
            "Crew",
            "Missile",
            "Illicit"
        ]
    },
    {
        "name": "Kavil",
        "unique": true,
        "faction": "Scum and Villainy",
        "id": 120,
        "ship": "Y-Wing",
        "skill": 7,
        "points": 24,
        "slots": [
            "Elite",
            "Turret",
            "Torpedo",
            "Torpedo",
            "Salvaged Astromech"
        ]
    },
    {
        "name": "Drea Renthal",
        "unique": true,
        "faction": "Scum and Villainy",
        "id": 121,
        "ship": "Y-Wing",
        "skill": 5,
        "points": 22,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Salvaged Astromech"
        ]
    },
    {
        "name": "Hired Gun",
        "faction": "Scum and Villainy",
        "id": 122,
        "ship": "Y-Wing",
        "skill": 4,
        "points": 20,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Salvaged Astromech"
        ]
    },
    {
        "name": "Syndicate Thug",
        "faction": "Scum and Villainy",
        "id": 123,
        "ship": "Y-Wing",
        "skill": 2,
        "points": 18,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Salvaged Astromech"
        ]
    },
    {
        "name": "Dace Bonearm",
        "unique": true,
        "faction": "Scum and Villainy",
        "id": 124,
        "ship": "HWK-290",
        "skill": 7,
        "points": 23,
        "slots": [
            "Elite",
            "Turret",
            "Crew",
            "Illicit"
        ]
    },
    {
        "name": "Palob Godalhi",
        "unique": true,
        "faction": "Scum and Villainy",
        "id": 125,
        "ship": "HWK-290",
        "skill": 5,
        "points": 20,
        "slots": [
            "Elite",
            "Turret",
            "Crew",
            "Illicit"
        ]
    },
    {
        "name": "Torkil Mux",
        "unique": true,
        "faction": "Scum and Villainy",
        "id": 126,
        "ship": "HWK-290",
        "skill": 3,
        "points": 19,
        "slots": [
            "Turret",
            "Crew",
            "Illicit"
        ]
    },
    {
        "name": "Spice Runner",
        "faction": "Scum and Villainy",
        "id": 127,
        "ship": "HWK-290",
        "skill": 1,
        "points": 16,
        "slots": [
            "Turret",
            "Crew",
            "Illicit"
        ]
    },
    {
        "name": "Commander Alozen",
        "faction": "Galactic Empire",
        "id": 128,
        "ship": "TIE Advanced",
        "unique": true,
        "skill": 5,
        "points": 25,
        "slots": [
            "Elite",
            "Missile"
        ]
    },
    {
        "name": "Raider-class Corvette (Fore)",
        "faction": "Galactic Empire",
        "id": 129,
        "ship": "Raider-class Corvette (Fore)",
        "skill": 4,
        "points": 50,
        "epic": true,
        "slots": [
            "Hardpoint",
            "Team",
            "Cargo"
        ]
    },
    {
        "name": "Raider-class Corvette (Aft)",
        "faction": "Galactic Empire",
        "id": 130,
        "ship": "Raider-class Corvette (Aft)",
        "skill": 4,
        "points": 50,
        "epic": true,
        "slots": [
            "Crew",
            "Crew",
            "Hardpoint",
            "Hardpoint",
            "Team",
            "Team",
            "Cargo"
        ]
    },
    {
        "name": "Bossk",
        "faction": "Scum and Villainy",
        "id": 131,
        "ship": "YV-666",
        "unique": true,
        "skill": 7,
        "points": 35,
        "slots": [
            "Elite",
            "Cannon",
            "Missile",
            "Crew",
            "Crew",
            "Crew",
            "Illicit"
        ]
    },
    {
        "name": "Moralo Eval",
        "faction": "Scum and Villainy",
        "id": 132,
        "ship": "YV-666",
        "unique": true,
        "skill": 6,
        "points": 34,
        "slots": [
            "Cannon",
            "Missile",
            "Crew",
            "Crew",
            "Crew",
            "Illicit"
        ]
    },
    {
        "name": "Latts Razzi",
        "faction": "Scum and Villainy",
        "id": 133,
        "ship": "YV-666",
        "unique": true,
        "skill": 5,
        "points": 33,
        "slots": [
            "Cannon",
            "Missile",
            "Crew",
            "Crew",
            "Crew",
            "Illicit"
        ]
    },
    {
        "name": "Trandoshan Slaver",
        "faction": "Scum and Villainy",
        "id": 134,
        "ship": "YV-666",
        "skill": 2,
        "points": 29,
        "slots": [
            "Cannon",
            "Missile",
            "Crew",
            "Crew",
            "Crew",
            "Illicit"
        ]
    },
    {
        "name": "Talonbane Cobra",
        "unique": true,
        "id": 135,
        "faction": "Scum and Villainy",
        "ship": "Kihraxz Fighter",
        "skill": 9,
        "slots": [
            "Elite",
            "Missile",
            "Illicit"
        ],
        "points": 28
    },
    {
        "name": "Graz the Hunter",
        "unique": true,
        "id": 136,
        "faction": "Scum and Villainy",
        "ship": "Kihraxz Fighter",
        "skill": 6,
        "slots": [
            "Missile",
            "Illicit"
        ],
        "points": 25
    },
    {
        "name": "Black Sun Ace",
        "faction": "Scum and Villainy",
        "id": 137,
        "ship": "Kihraxz Fighter",
        "skill": 5,
        "slots": [
            "Elite",
            "Missile",
            "Illicit"
        ],
        "points": 23
    },
    {
        "name": "Cartel Marauder",
        "faction": "Scum and Villainy",
        "id": 138,
        "ship": "Kihraxz Fighter",
        "skill": 2,
        "slots": [
            "Missile",
            "Illicit"
        ],
        "points": 20
    },
    {
        "name": "Miranda Doni",
        "unique": true,
        "id": 139,
        "faction": "Rebel Alliance",
        "ship": "K-Wing",
        "skill": 8,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Crew",
            "Bomb",
            "Bomb"
        ],
        "points": 29
    },
    {
        "name": "Esege Tuketu",
        "unique": true,
        "id": 140,
        "faction": "Rebel Alliance",
        "ship": "K-Wing",
        "skill": 6,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Crew",
            "Bomb",
            "Bomb"
        ],
        "points": 28
    },
    {
        "name": "Guardian Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 141,
        "ship": "K-Wing",
        "skill": 4,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Crew",
            "Bomb",
            "Bomb"
        ],
        "points": 25
    },
    {
        "name": "Warden Squadron Pilot",
        "faction": "Rebel Alliance",
        "id": 142,
        "ship": "K-Wing",
        "skill": 2,
        "slots": [
            "Turret",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Crew",
            "Bomb",
            "Bomb"
        ],
        "points": 23
    },
    {
        "name": "\"Redline\"",
        "unique": true,
        "id": 143,
        "faction": "Galactic Empire",
        "ship": "TIE Punisher",
        "skill": 7,
        "slots": [
            "System",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb",
            "Bomb"
        ],
        "points": 27
    },
    {
        "name": "\"Deathrain\"",
        "unique": true,
        "id": 144,
        "faction": "Galactic Empire",
        "ship": "TIE Punisher",
        "skill": 6,
        "slots": [
            "System",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb",
            "Bomb"
        ],
        "points": 26
    },
    {
        "name": "Black Eight Squadron Pilot",
        "canonical_name": "blackeightsqpilot",
        "faction": "Galactic Empire",
        "id": 145,
        "ship": "TIE Punisher",
        "skill": 4,
        "slots": [
            "System",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb",
            "Bomb"
        ],
        "points": 23
    },
    {
        "name": "Cutlass Squadron Pilot",
        "faction": "Galactic Empire",
        "id": 146,
        "ship": "TIE Punisher",
        "skill": 2,
        "slots": [
            "System",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb",
            "Bomb"
        ],
        "points": 21
    },
    {
        "name": "Juno Eclipse",
        "id": 147,
        "faction": "Galactic Empire",
        "ship": "TIE Advanced",
        "unique": true,
        "skill": 8,
        "points": 28,
        "slots": [
            "Elite",
            "Missile"
        ]
    },
    {
        "name": "Zertik Strom",
        "id": 148,
        "faction": "Galactic Empire",
        "ship": "TIE Advanced",
        "unique": true,
        "skill": 6,
        "points": 26,
        "slots": [
            "Elite",
            "Missile"
        ]
    },
    {
        "name": "Lieutenant Colzet",
        "id": 149,
        "faction": "Galactic Empire",
        "ship": "TIE Advanced",
        "unique": true,
        "skill": 3,
        "points": 23,
        "slots": [
            "Missile"
        ]
    },
    {
        "name": "Gozanti-class Cruiser",
        "id": 150,
        "faction": "Galactic Empire",
        "ship": "Gozanti-class Cruiser",
        "skill": 2,
        "slots": [
            "Crew",
            "Crew",
            "Hardpoint",
            "Team",
            "Cargo",
            "Cargo"
        ],
        "points": 40
    },
    {
        "name": "\"Scourge\"",
        "id": 151,
        "unique": true,
        "faction": "Galactic Empire",
        "ship": "TIE Fighter",
        "skill": 7,
        "slots": [
            "Elite"
        ],
        "points": 17
    },
    {
        "name": "\"Youngster\"",
        "id": 152,
        "unique": true,
        "faction": "Galactic Empire",
        "ship": "TIE Fighter",
        "skill": 6,
        "slots": [
            "Elite"
        ],
        "points": 15
    },
    {
        "name": "\"Wampa\"",
        "id": 153,
        "unique": true,
        "faction": "Galactic Empire",
        "ship": "TIE Fighter",
        "skill": 4,
        "slots": [],
        "points": 14
    },
    {
        "name": "\"Chaser\"",
        "id": 154,
        "unique": true,
        "faction": "Galactic Empire",
        "ship": "TIE Fighter",
        "skill": 3,
        "slots": [],
        "points": 14
    },
    {
        "name": "Hera Syndulla",
        "id": 155,
        "unique": true,
        "faction": "Rebel Alliance",
        "ship": "VCX-100",
        "skill": 7,
        "slots": [
            "System",
            "Turret",
            "Torpedo",
            "Torpedo",
            "Crew",
            "Crew"
        ],
        "points": 40
    },
    {
        "name": "Kanan Jarrus",
        "id": 156,
        "unique": true,
        "faction": "Rebel Alliance",
        "ship": "VCX-100",
        "skill": 5,
        "slots": [
            "System",
            "Turret",
            "Torpedo",
            "Torpedo",
            "Crew",
            "Crew"
        ],
        "points": 38
    },
    {
        "name": "\"Chopper\"",
        "id": 157,
        "unique": true,
        "faction": "Rebel Alliance",
        "ship": "VCX-100",
        "skill": 4,
        "slots": [
            "System",
            "Turret",
            "Torpedo",
            "Torpedo",
            "Crew",
            "Crew"
        ],
        "points": 37
    },
    {
        "name": "Lothal Rebel",
        "id": 158,
        "faction": "Rebel Alliance",
        "ship": "VCX-100",
        "skill": 3,
        "slots": [
            "System",
            "Turret",
            "Torpedo",
            "Torpedo",
            "Crew",
            "Crew"
        ],
        "points": 35
    },
    {
        "name": "Hera Syndulla (Attack Shuttle)",
        "id": 159,
        "canonical_name": "herasyndulla",
        "unique": true,
        "faction": "Rebel Alliance",
        "ship": "Attack Shuttle",
        "skill": 7,
        "slots": [
            "Elite",
            "Turret",
            "Crew"
        ],
        "points": 22
    },
    {
        "name": "Sabine Wren",
        "id": 160,
        "unique": true,
        "faction": "Rebel Alliance",
        "ship": "Attack Shuttle",
        "skill": 5,
        "slots": [
            "Elite",
            "Turret",
            "Crew"
        ],
        "points": 21
    },
    {
        "name": "Ezra Bridger",
        "id": 161,
        "unique": true,
        "faction": "Rebel Alliance",
        "ship": "Attack Shuttle",
        "skill": 4,
        "slots": [
            "Elite",
            "Turret",
            "Crew"
        ],
        "points": 20
    },
    {
        "name": "\"Zeb\" Orrelios",
        "id": 162,
        "unique": true,
        "faction": "Rebel Alliance",
        "ship": "Attack Shuttle",
        "skill": 3,
        "slots": [
            "Turret",
            "Crew"
        ],
        "points": 18
    },
    {
        "name": "The Inquisitor",
        "id": 163,
        "unique": true,
        "faction": "Galactic Empire",
        "ship": "TIE Advanced Prototype",
        "skill": 8,
        "slots": [
            "Elite",
            "Missile"
        ],
        "points": 25
    },
    {
        "name": "Valen Rudor",
        "id": 164,
        "unique": true,
        "faction": "Galactic Empire",
        "ship": "TIE Advanced Prototype",
        "skill": 6,
        "slots": [
            "Elite",
            "Missile"
        ],
        "points": 22
    },
    {
        "name": "Baron of the Empire",
        "id": 165,
        "faction": "Galactic Empire",
        "ship": "TIE Advanced Prototype",
        "skill": 4,
        "slots": [
            "Elite",
            "Missile"
        ],
        "points": 19
    },
    {
        "name": "Sienar Test Pilot",
        "id": 166,
        "faction": "Galactic Empire",
        "ship": "TIE Advanced Prototype",
        "skill": 2,
        "slots": [
            "Missile"
        ],
        "points": 16
    },
    {
        "name": "Zuckuss",
        "id": 167,
        "unique": true,
        "faction": "Scum and Villainy",
        "ship": "G-1A Starfighter",
        "skill": 7,
        "slots": [
            "Elite",
            "Crew",
            "System",
            "Illicit"
        ],
        "points": 28
    },
    {
        "name": "4-LOM",
        "id": 168,
        "unique": true,
        "faction": "Scum and Villainy",
        "ship": "G-1A Starfighter",
        "skill": 6,
        "slots": [
            "Elite",
            "Crew",
            "System",
            "Illicit"
        ],
        "points": 27
    },
    {
        "name": "Gand Findsman",
        "id": 169,
        "faction": "Scum and Villainy",
        "ship": "G-1A Starfighter",
        "skill": 5,
        "slots": [
            "Elite",
            "Crew",
            "System",
            "Illicit"
        ],
        "points": 25
    },
    {
        "name": "Ruthless Freelancer",
        "id": 170,
        "faction": "Scum and Villainy",
        "ship": "G-1A Starfighter",
        "skill": 3,
        "slots": [
            "Crew",
            "System",
            "Illicit"
        ],
        "points": 23
    },
    {
        "name": "Dengar",
        "id": 171,
        "unique": true,
        "faction": "Scum and Villainy",
        "ship": "JumpMaster 5000",
        "skill": 9,
        "slots": [
            "Elite",
            "Torpedo",
            "Torpedo",
            "Crew",
            "Salvaged Astromech",
            "Illicit"
        ],
        "points": 33
    },
    {
        "name": "Tel Trevura",
        "id": 172,
        "unique": true,
        "faction": "Scum and Villainy",
        "ship": "JumpMaster 5000",
        "skill": 7,
        "slots": [
            "Elite",
            "Torpedo",
            "Torpedo",
            "Crew",
            "Salvaged Astromech",
            "Illicit"
        ],
        "points": 30
    },
    {
        "name": "Manaroo",
        "id": 173,
        "unique": true,
        "faction": "Scum and Villainy",
        "ship": "JumpMaster 5000",
        "skill": 4,
        "slots": [
            "Elite",
            "Torpedo",
            "Torpedo",
            "Crew",
            "Salvaged Astromech",
            "Illicit"
        ],
        "points": 27
    },
    {
        "name": "Contracted Scout",
        "id": 174,
        "faction": "Scum and Villainy",
        "ship": "JumpMaster 5000",
        "skill": 3,
        "slots": [
            "Elite",
            "Torpedo",
            "Torpedo",
            "Crew",
            "Salvaged Astromech",
            "Illicit"
        ],
        "points": 25
    },
    {
        "name": "Poe Dameron",
        "id": 175,
        "unique": true,
        "faction": "Resistance",
        "ship": "T-70 X-Wing",
        "skill": 8,
        "slots": [
            "Elite",
            "Torpedo",
            "Astromech",
            "Tech"
        ],
        "points": 31
    },
    {
        "name": "\"Blue Ace\"",
        "id": 176,
        "unique": true,
        "faction": "Resistance",
        "ship": "T-70 X-Wing",
        "skill": 5,
        "slots": [
            "Torpedo",
            "Astromech",
            "Tech"
        ],
        "points": 27
    },
    {
        "name": "Red Squadron Veteran",
        "id": 177,
        "faction": "Resistance",
        "ship": "T-70 X-Wing",
        "skill": 4,
        "slots": [
            "Elite",
            "Torpedo",
            "Astromech",
            "Tech"
        ],
        "points": 26
    },
    {
        "name": "Blue Squadron Novice",
        "id": 178,
        "faction": "Resistance",
        "ship": "T-70 X-Wing",
        "skill": 2,
        "slots": [
            "Torpedo",
            "Astromech",
            "Tech"
        ],
        "points": 24
    },
    {
        "name": "\"Omega Ace\"",
        "id": 179,
        "unique": true,
        "faction": "First Order",
        "ship": "TIE/fo Fighter",
        "skill": 7,
        "slots": [
            "Elite",
            "Tech"
        ],
        "points": 20
    },
    {
        "name": "\"Epsilon Leader\"",
        "id": 180,
        "unique": true,
        "faction": "First Order",
        "ship": "TIE/fo Fighter",
        "skill": 6,
        "slots": [
            "Tech"
        ],
        "points": 19
    },
    {
        "name": "\"Zeta Ace\"",
        "id": 181,
        "unique": true,
        "faction": "First Order",
        "ship": "TIE/fo Fighter",
        "skill": 5,
        "slots": [
            "Elite",
            "Tech"
        ],
        "points": 18
    },
    {
        "name": "Omega Squadron Pilot",
        "id": 182,
        "faction": "First Order",
        "ship": "TIE/fo Fighter",
        "skill": 4,
        "slots": [
            "Elite",
            "Tech"
        ],
        "points": 17
    },
    {
        "name": "Zeta Squadron Pilot",
        "id": 183,
        "faction": "First Order",
        "ship": "TIE/fo Fighter",
        "skill": 3,
        "slots": [
            "Tech"
        ],
        "points": 16
    },
    {
        "name": "Epsilon Squadron Pilot",
        "id": 184,
        "faction": "First Order",
        "ship": "TIE/fo Fighter",
        "skill": 1,
        "slots": [
            "Tech"
        ],
        "points": 15
    },
    {
        "name": "Ello Asty",
        "id": 185,
        "unique": true,
        "faction": "Resistance",
        "ship": "T-70 X-Wing",
        "skill": 7,
        "slots": [
            "Elite",
            "Torpedo",
            "Astromech",
            "Tech"
        ],
        "points": 30
    },
    {
        "name": "\"Red Ace\"",
        "id": 186,
        "unique": true,
        "faction": "Resistance",
        "ship": "T-70 X-Wing",
        "skill": 6,
        "slots": [
            "Torpedo",
            "Astromech",
            "Tech"
        ],
        "points": 29
    },
    {
        "name": "\"Omega Leader\"",
        "id": 187,
        "unique": true,
        "faction": "First Order",
        "ship": "TIE/fo Fighter",
        "skill": 8,
        "slots": [
            "Elite",
            "Tech"
        ],
        "points": 21
    },
    {
        "name": "\"Zeta Leader\"",
        "id": 188,
        "unique": true,
        "faction": "First Order",
        "ship": "TIE/fo Fighter",
        "skill": 7,
        "slots": [
            "Elite",
            "Tech"
        ],
        "points": 20
    },
    {
        "name": "\"Epsilon Ace\"",
        "id": 189,
        "unique": true,
        "faction": "First Order",
        "ship": "TIE/fo Fighter",
        "skill": 4,
        "slots": [
            "Tech"
        ],
        "points": 17
    },
    {
        "name": "Tomax Bren",
        "id": 190,
        "unique": true,
        "faction": "Galactic Empire",
        "ship": "TIE Bomber",
        "skill": 8,
        "slots": [
            "Elite",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb"
        ],
        "points": 24
    },
    {
        "name": "Gamma Squadron Veteran",
        "id": 191,
        "faction": "Galactic Empire",
        "ship": "TIE Bomber",
        "skill": 5,
        "slots": [
            "Elite",
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb"
        ],
        "points": 19
    },
    {
        "name": "\"Dea???\"",
        "id": 192,
        "unique": true,
        "faction": "Galactic Empire",
        "ship": "TIE Bomber",
        "skill": 3,
        "slots": [
            "Torpedo",
            "Torpedo",
            "Missile",
            "Missile",
            "Bomb"
        ],
        "points": 100
    },
    {
        "name": "Maarek Stele (TIE Defender)",
        "canonical_name": "maarekstele",
        "id": 193,
        "unique": true,
        "faction": "Galactic Empire",
        "ship": "TIE Defender",
        "skill": 7,
        "slots": [
            "Cannon",
            "Missile"
        ],
        "points": 100
    },
    {
        "name": "Glaive Squa???",
        "id": 194,
        "faction": "Galactic Empire",
        "ship": "TIE Defender",
        "skill": 6,
        "slots": [
            "Cannon",
            "Missile"
        ],
        "points": 100
    },
    {
        "name": "Count???",
        "id": 195,
        "unique": true,
        "faction": "Galactic Empire",
        "ship": "TIE Defender",
        "skill": 5,
        "slots": [
            "Cannon",
            "Missile"
        ],
        "points": 100
    }
]
""")
