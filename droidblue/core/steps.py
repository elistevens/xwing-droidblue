import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

from collections import deque

class Stepper(object):
    def __init__(self, step_iter, active_id=None, attack_id=None, target_id=None):
        self.step_deq = deque(step_iter)
        self.step_tup = None
        self.count = None
        self.active_id = active_id
        self.attack_id = attack_id
        self.target_id = target_id

        assert len(self.step_deq) > 0

    def nextStep(self, state):
        if not self.step_deq:
            raise StopIteration()

        self.step_tup = self.step_deq.popleft()

        if isinstance(self.step_tup, str):
            self.step_tup = (self.step_tup,)

        log.debug("{}: {}, {}, {}".format(self.step_tup, self.active_id, self.attack_id, self.target_id))

        return self.step_tup

    @classmethod
    def steps_setup(cls):
        yield ('placeObstacles',)
        yield ('placeShips',)


    @classmethod
    def steps_round(cls, dials=False):
        # for se in _steps_beforeAfter():
        #     yield ('dials',) + se
        if dials:
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


    @classmethod
    def steps_dial(cls):
        yield ('setDial',)

    @classmethod
    def steps_activation(cls, isIonized=False):
        if not isIonized:
            for beforeAfter in _steps_beforeAfter():
                yield beforeAfter + ('revealDial',)

        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('performManeuver',)

        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('checkPilotStress',)

        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('performAction',)


    @classmethod
    def steps_combat(cls):
        yield ('chooseWeaponAndTarget',)

    @classmethod
    def steps_attack(cls):
        yield ('gatherExtraAttackDice',)
        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('rollAttack',)

        yield ('defenderModifyAttack',)
        yield ('attackerModifyAttack',)

        yield ('gatherExtraDefenseDice',)
        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('rollDefense',)

        yield ('attackerModifyDefense',)
        yield ('defenderModifyDefense',)

        for beforeAfter in _steps_beforeAfter():
            yield beforeAfter + ('compareResults',)


    @classmethod
    def steps_endphase(cls):
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
