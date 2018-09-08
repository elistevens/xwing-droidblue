import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

def steps_setup():
    yield 'placeObstacles'
    yield 'placeShips'


def steps_round(planning=True, activation=True, engagement=True, endphase=True):
    if planning:
        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + 'PlanningPhase'

    if activation:
        for beforeAfter in _steps_beforeAfter(decloak=True):
            yield beforeAfter + 'ActivationPhase'

    if engagement:
        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + 'EngagementPhase'

    if endphase:
        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + 'EndPhase'

def steps_activation(isIonized=False):
    if not isIonized:
        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + 'RevealDial'

    for beforeAfter in _steps_beforeAfter():
        yield beforeAfter + 'PerformManeuver'

    for beforeAfter in _steps_beforeAfter():
        yield beforeAfter + 'CheckPilotStress'

    for beforeAfter in _steps_beforeAfter():
        yield beforeAfter + 'PerformAction'


def steps_attack():
    substep_list = [
        # 'MeasureRange',
        'ChooseWeapon',
        'DeclareDefender',
        'PayCosts',

        'RollAttackDice',
        'DefenderModifiesAttack',
        'AttackerModifiesAttack',

        'RollDefenseDice',
        'AttackerModifiesDefense',
        'DefenderModifiesDefense',

        'CancelHits',
        'CancelCrits',
        'DetermineWetherAttackHits',

        'SufferHits',
        'SufferCrits',

        'ResolveAfterDefending',
        'ResolveAfterAttacking',
        'PerformBonusAttack',
    ]
    for substep_str in substep_list:
        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + substep_str


def steps_endphase():
    yield 'cleanup'


def _steps_beforeAfter(decloak=False):
    yield 'before'
    if decloak:
        yield 'decloak'
    yield 'do'
    yield 'after'

steps_str2id_dict = {}
steps_str2id_dict[None] = 9999
steps_str2id_dict['*'] = len(steps_str2id_dict)

for _step_gen in [steps_setup(), steps_round(True), steps_activation(), steps_attack(), steps_attack(), steps_endphase()]:
    for _step_str in _step_gen:
        steps_str2id_dict[_step_str] = len(steps_str2id_dict)

# steps_str2id_dict['doPerformAction'] = len(steps_str2id_dict)
steps_str2id_dict['dealtCrit'] = len(steps_str2id_dict)
steps_str2id_dict['dealtHit'] = len(steps_str2id_dict)

from droidblue.core.state import BoardState
for _token_str in BoardState.token_list:
    steps_str2id_dict['assign_{}'.format(_token_str)] = len(steps_str2id_dict)
    steps_str2id_dict['remove_{}'.format(_token_str)] = len(steps_str2id_dict)
    steps_str2id_dict['clear_{}'.format(_token_str)] = len(steps_str2id_dict)

for _flag_str in BoardState.flag_list:
    steps_str2id_dict['flag_{}'.format(_flag_str)] = len(steps_str2id_dict)
    steps_str2id_dict['unflag_{}'.format(_flag_str)] = len(steps_str2id_dict)


steps_str2id_dict['testing'] = len(steps_str2id_dict) + 9000

# for k,v in sorted(steps_str2id_dict.iteritems()):
#     print k, v

steps_id2str_dict = {v:k for k,v in steps_str2id_dict.iteritems()}

# for k,v in sorted(steps_id2str_dict.iteritems()):
#     print k, v

assert len(steps_str2id_dict) == len(steps_id2str_dict)
assert len(steps_str2id_dict) < 9000

    
