import copy
import simplejson as json

def swap(squad, pilot=None, noUpgrades=False, points=None):
    squad = copy.deepcopy(squad)

    total_points = 0

    for pilot_dict in squad['pilots']:
        if pilot:
            assert isinstance(pilot, str)
            pilot_dict['name'] = pilot

        if noUpgrades:
            pilot_dict['upgrades'] = {}

        if points:
            assert isinstance(points, int)
            pilot_dict['points'] = points

        total_points += pilot_dict['points']

    squad['points'] = total_points
    return squad

def _cleanup(s):
    d = json.loads(s)
    for key in ['vendor', 'description', 'version', 'name']:
        if key in d:
            del d[key]
    print json.dumps(d, indent=4)


tf_ept = {
    "faction": "imperial",
    "points": 15,
    "pilots": [
        {
            "ship": "tiefighter",
            "points": 15,
            "name": "blacksquadronpilot",
            "upgrades": {
                "ept": [
                    "crackshot"
                ]
            }
        }
    ],
}
tf_generic = swap(tf_ept, 'academypilot', True, 12)

tfo_ept = {
    "faction": "imperial",
    "points": 22,
    "pilots": [
        {
            "ship": "tiefofighter",
            "points": 22,
            "name": "omegasquadronpilot",
            "upgrades": {
                "ept": [
                    "juke"
                ],
                "tech": [
                    "commrelay"
                ]
            }
        }
    ]
}
tfo_generic = swap(tfo_ept, 'epsilonsquadronpilot', True, 15)

tint_ept = {
    "faction": "imperial",
    "points": 30,
    "pilots": [
        {
            "ship": "tieinterceptor",
            "points": 30,
            "name": "royalguardpilot",
            "upgrades": {
                "ept": [
                    "pushthelimit"
                ],
                "title": [
                    "royalguardtie"
                ],
                "mod": [
                    "autothrusters",
                    "stealthdevice"
                ]
            }
        }
    ]
}
tint_generic = swap(tint_ept, 'alphasquadronpilot', True, 18)

xwt70_ept = {
    "faction": "rebel",
    "points": 30,
    "pilots": [
        {
            "ship": "t70xwing",
            "points": 30,
            "name": "redsquadronveteran",
            "upgrades": {
                "ept": [
                    "predator"
                ],
                "amd": [
                    "r2astromech"
                ],
                "mod": [
                    "integratedastromech"
                ]
            }
        }
    ]
}
xwt70_generic = swap(tint_ept, 'bluesquadronnovice', True, 24)

awing_swarm = {
    "faction": "rebel",
    "points": 100,
    "pilots": [
        {
            "ship": "awing",
            "points": 25,
            "name": "greensquadronpilot",
            "upgrades": {
                "title": [
                    "awingtestpilot"
                ],
                "ept": [
                    "pushthelimit",
                    "predator"
                ],
                "mod": [
                    "autothrusters"
                ],
                "missile": [
                    "chardaanrefit"
                ]
            }
        },
        {
            "ship": "awing",
            "points": 25,
            "name": "greensquadronpilot",
            "upgrades": {
                "title": [
                    "awingtestpilot"
                ],
                "ept": [
                    "pushthelimit",
                    "predator"
                ],
                "mod": [
                    "autothrusters"
                ],
                "missile": [
                    "chardaanrefit"
                ]
            }
        },
        {
            "ship": "awing",
            "points": 25,
            "name": "greensquadronpilot",
            "upgrades": {
                "title": [
                    "awingtestpilot"
                ],
                "ept": [
                    "pushthelimit",
                    "predator"
                ],
                "mod": [
                    "autothrusters"
                ],
                "missile": [
                    "chardaanrefit"
                ]
            }
        },
        {
            "ship": "awing",
            "points": 25,
            "name": "greensquadronpilot",
            "upgrades": {
                "title": [
                    "awingtestpilot"
                ],
                "ept": [
                    "pushthelimit",
                    "predator"
                ],
                "mod": [
                    "autothrusters"
                ],
                "missile": [
                    "chardaanrefit"
                ]
            }
        }
    ]
}

howlcrack_swarm = {
    "faction": "imperial",
    "points": 100,
    "pilots": [
        {
            "ship": "tiefighter",
            "points": 19,
            "name": "howlrunner",
            "upgrades": {
                "ept": [
                    "crackshot"
                ]
            }
        },
        {
            "ship": "tiefighter",
            "points": 15,
            "name": "blacksquadronpilot",
            "upgrades": {
                "ept": [
                    "crackshot"
                ]
            }
        },
        {
            "ship": "tiefighter",
            "points": 15,
            "name": "blacksquadronpilot",
            "upgrades": {
                "ept": [
                    "crackshot"
                ]
            }
        },
        {
            "ship": "tiefighter",
            "points": 15,
            "name": "blacksquadronpilot",
            "upgrades": {
                "ept": [
                    "crackshot"
                ]
            }
        },
        {
            "ship": "tiefighter",
            "points": 15,
            "name": "blacksquadronpilot",
            "upgrades": {
                "ept": [
                    "crackshot"
                ]
            }
        },
        {
            "ship": "tiefofighter",
            "points": 21,
            "name": "zetaleader",
            "upgrades": {
                "ept": [
                    "crackshot"
                ]
            }
        }
    ]
}

yt1300_generic = {
    "faction": "rebel",
    "points": 27,
    "pilots": [
        {
            "ship": "yt1300",
            "points": 27,
            "name": "outerrimsmuggler"
        }
    ]
}
