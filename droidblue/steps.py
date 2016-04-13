class Stepper(object):
    wildcard_key = ('*',)

    def __init__(self, step_iter, active_id=None, attack_id=None, target_id=None):
        self.step_iter = step_iter
        self.step_tup = None
        self.active_id = active_id
        self.attack_id = attack_id
        self.target_id = target_id

    def nextStep(self):
        self.step_tup = self.step_iter.next()


    @staticmethod
    def steps_round(player_count):
        for se in _steps_startEnd():
            yield ('setDials',) + se

        for se in _steps_startEnd(decloak=True):
            for psinit in _steps_ps_init(player_count):
                yield ('activation',) + se + psinit + ('chooseActivationShip',)

        for se in _steps_startEnd():
            for psinit in _steps_ps_init(player_count, reverse=True):
                yield ('combat',) + se + psinit + ('chooseCombatShip',)

        for se in _steps_startEnd():
            for psinit in _steps_ps_init(player_count, reverse=True):
                yield ('endphase',) + se + psinit + ('chooseEndShip',)


    @staticmethod
    def steps_activation():
        for order in _steps_startEnd():
            yield ('revealDial',) + order

        for order in _steps_startEnd():
            yield ('maneuver',) + order

        for order in _steps_startEnd():
            yield ('action',) + order


    @staticmethod
    def steps_combat():
        yield ('chooseTarget',)

        for se in _steps_startEnd():
            yield ('rollAttack',) + se

        yield ('defenderModifyAttack',)
        yield ('attackerModifyAttack',)

        for se in _steps_startEnd():
            yield ('rollDefense',) + se

        yield ('attackerModifyDefense',)
        yield ('defenderModifyDefense',)

        for se in _steps_startEnd():
            yield ('compareResults',) + se


    @staticmethod
    def steps_endphase():
        yield ('cleanup',)


    # @staticmethod
    # def steps_spendToken(token_str):
    #     def _steps_spendToken_closure():
    #         for order in _steps_startEnd():
    #             yield (
    #                   'spend{}'.format(token_str.title().replace(' ', '')),) + order
    #
    #     return _steps_spendToken_closure


def _steps_init(player_count):
    for init in range(player_count):
        yield (init,)


def _steps_ps_init(player_count, reverse=False):
    for ps in sorted(range(13), reverse=reverse):
        for init in _steps_init(player_count):
            yield (ps,) + init


def _steps_startEnd(decloak=False):
    yield ('start',)
    if decloak:
        yield ('decloak',)
    yield ('perform',)
    yield ('end',)
