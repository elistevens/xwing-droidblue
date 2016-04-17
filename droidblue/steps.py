class Stepper(object):
    wildcard_key = ('*',)

    def __init__(self, step_iter, active_id=None, attack_id=None, target_id=None):
        self.step_iter = step_iter
        self.step_tup = None
        self.active_id = active_id
        self.attack_id = attack_id
        self.target_id = target_id

    def nextStep(self, state):
        self.step_tup = self.step_iter.next()


    @staticmethod
    def steps_round():
        # for se in _steps_beforeAfter():
        #     yield ('dials',) + se
        yield ('dials',)

        for beforeAfter in _steps_beforeAfter(decloak=True):
            yield beforeAfter + ('activation',)
            # for psinit in _steps_ps_init(player_count):
            #     yield beforeAfter + ('activation',) + psinit + ('chooseActivationShip',)

        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('combat',)
            # for psinit in _steps_ps_init(player_count, reverse=True):
            #     yield beforeAfter + ('combat',) + psinit + ('chooseCombatShip',)

        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('endphase',)
            # for psinit in _steps_ps_init(player_count, reverse=True):
            #     yield beforeAfter + ('endphase',) + psinit + ('chooseEndShip',)


    @staticmethod
    def steps_dial():
        yield ('setDial',)

    @staticmethod
    def steps_activation(isIonized=False):
        if not isIonized:
            for beforeAfter in _steps_beforeAfter():
                yield beforeAfter + ('revealDial',)

        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('moveShip',)

        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('checkPilotStress',)

        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('action',)


    @staticmethod
    def steps_combat(chooseTarget=True):
        if chooseTarget:
            yield ('chooseWeaponAndTarget',)

        yield ('gatherAttackDice',)
        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('rollAttack',)

        yield ('defenderModifyAttack',)
        yield ('attackerModifyAttack',)

        yield ('gatherDefenseDice',)
        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('rollDefense',)

        yield ('attackerModifyDefense',)
        yield ('defenderModifyDefense',)

        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('compareResults',)


    @staticmethod
    def steps_endphase():
        yield ('cleanup',)



# def _steps_init(player_count):
#     for init in range(player_count):
#         yield (init,)
#
# # Need to change this up to instead just be the groups of pilots by PS
# # can't hook into steps the current way
# def _steps_ps_init(player_count, reverse=False):
#     for ps in sorted(range(13), reverse=reverse):
#         for init in _steps_init(player_count):
#             yield (ps,) + init


def _steps_beforeAfter(decloak=False):
    yield ('before',)
    if decloak:
        yield ('decloak',)
    # yield ('perform',)
    yield tuple()
    yield ('after',)
