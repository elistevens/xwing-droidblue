import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

from droidblue.core.rules import ActiveAbilityRule, ActiveAbilityRule, TargetAbilityRule
from droidblue.core.pilot import Pilot
from droidblue.core.edge import Edge, RandomEdge, SpendFocusTokenEdge, SpendEvadeTokenEdge
from droidblue.core.steps import steps_attack
from droidblue.core.dice import StateBackedAttackDicePool, StateBackedDefenseDicePool

class AttackRule(ActiveAbilityRule):
    def __init__(self, state, pilot_id):
        super(AttackRule, self).__init__(state, 'chooseWeaponAndTarget', pilot_id)

    def _getEdges(self, state):
        edge_list = []

        player_id = state.const._getRawStat(self.pilot_id, 'player_id')
        pilot_obj = state.pilots[self.pilot_id]
        for target_id, target_obj in enumerate(state.pilots):
            if state.const._getRawStat(target_id, 'player_id') != player_id:
                range_list = pilot_obj.getArcRanges(target_obj)
                range_int = range_list[self.arc_index]

                # log.debug("{} at {}: {}".format(self.pilot_id, target_id,range_list))

                if range_int in {1,2,3}:
                    edge_list.append(AttackPrimaryEdge(self.pilot_id, target_id, range_int))

        return edge_list

class AttackPrimaryForwardRule(AttackRule):
    card_type = 'generic'
    arc_index = Pilot.arcForward_index

class AttackPrimaryAuxBackRule(AttackRule):
    card_type = 'generic'
    arc_index = Pilot.arcBack_index


class AttackPrimaryAuxSideRule(AttackRule):
    card_type = 'generic'
    arc_index = Pilot.arcSide_index


class AttackTorpedoAuxBackRule(AttackRule):
    card_type = 'generic'
    arc_index = Pilot.arcBack_index


class AttackPrimaryTurretRule(AttackRule):
    card_type = 'generic'
    arc_index = Pilot.arcTurret_index


class AttackPrimaryEdge(Edge):
    # FIXME: not actually mandatory, but helps for simulation
    mandatoryIf_str = 'simplifyForTraining'

    def __init__(self, active_id, target_id, range_int):
        super(AttackPrimaryEdge, self).__init__(active_id)

        self.target_id = target_id
        self.range_int = range_int

    def transitionImpl(self, state):
        state.pushSteps(steps_attack(), self.active_id, self.target_id)

        # We can't use state.attackDice_pool yet, since we're still on the old
        # step, so state.active_id, etc. aren't correct yet. That will change
        # once state.nextStep gets called.
        attackDice_pool = StateBackedAttackDicePool(state, self.active_id)
        defenseDice_pool = StateBackedDefenseDicePool(state, self.target_id)

        attackDice_pool.reset()
        defenseDice_pool.reset()

        attackDice_pool.addDice(state.getStat(self.active_id, 'atk'))
        defenseDice_pool.addDice(state.getStat(self.target_id, 'agi'))

        if self.range_int == 1:
            attackDice_pool.addDice()

        if self.range_int == 3:
            defenseDice_pool.addDice()


# Spend focus
class SpendFocusTokenToModifyAttackDiceRule(ActiveAbilityRule):
    card_type = 'generic'

    def __init__(self, state, pilot_id):
        super(SpendFocusTokenToModifyAttackDiceRule, self).__init__(state, 'attackerModifyAttack', pilot_id)

    def _getEdges(self, state):
        if state.getToken(self.pilot_id, 'focus'):
            if state.getStat(self.pilot_id, 'rolled_f') \
                    or state.getStat(self.pilot_id, 'rerolled_f') \
                    or state.getStat(self.pilot_id, 'focusShenanigans'):
                return [SpendFocusTokenToModifyAttackDiceEdge(self.pilot_id)]

class SpendFocusTokenToModifyAttackDiceEdge(SpendFocusTokenEdge):
    def transitionImpl(self, state):
        super(SpendFocusTokenToModifyAttackDiceEdge, self).transitionImpl(state)
        state.attackDice_pool.modifyFaces('f', 'H', 99)


class SpendFocusTokenToModifyDefenseDiceRule(TargetAbilityRule):
    card_type = 'generic'

    def __init__(self, state, pilot_id):
        super(SpendFocusTokenToModifyDefenseDiceRule, self).__init__(state, 'defenderModifyDefense', pilot_id)

    def _getEdges(self, state):
        if state.getToken(self.pilot_id, 'focus'):
            if state.getStat(self.pilot_id, 'rolled_f') \
                    or state.getStat(self.pilot_id, 'rerolled_f') \
                    or state.getStat(self.pilot_id, 'focusShenanigans'):
                return [SpendFocusTokenToModifyDefenseDiceEdge(self.pilot_id)]

class SpendFocusTokenToModifyDefenseDiceEdge(SpendFocusTokenEdge):
    def transitionImpl(self, state):
        super(SpendFocusTokenToModifyDefenseDiceEdge, self).transitionImpl(state)
        state.defenseDice_pool.modifyFaces('f', 'E', 99)


# Spend evade
class SpendEvadeTokenToAddEvadeResultRule(TargetAbilityRule):
    card_type = 'generic'

    def __init__(self, state, pilot_id):
        super(SpendEvadeTokenToAddEvadeResultRule, self).__init__(state, 'defenderModifyDefense', pilot_id)

    def _getEdges(self, state):
        if state.getToken(self.pilot_id, 'evade'):
            return [SpendEvadeTokenToAddEvadeResultEdge(self.pilot_id)]

class SpendEvadeTokenToAddEvadeResultEdge(SpendEvadeTokenEdge):
    def transitionImpl(self, state):
        super(SpendEvadeTokenToAddEvadeResultEdge, self).transitionImpl(state)
        state.defenseDice_pool.addResults('E')


# Acquire Target Lock

# Roll Dice
class RollAttackRule(ActiveAbilityRule):
    card_type = 'generic'

    def __init__(self, state, pilot_id):
        super(RollAttackRule, self).__init__(state, 'doRollAttack', pilot_id)

    def _getEdges(self, state):
        roll_edge = RollAttackEdge(self.pilot_id)
        # log.debug(state._step)
        prob_dict = state.attackDice_pool.rollDice()

        # log.info(prob_dict)

        for faces, prob_frac in prob_dict.iteritems():
            subedge = SetRollAttackEdge(self.pilot_id, faces)
            roll_edge.addOutcome(faces, subedge, weight=prob_frac)

        return [roll_edge]

class RollAttackEdge(RandomEdge):
    mandatory_bool = True

class SetRollAttackEdge(Edge):
    mandatory_bool = True

    def __init__(self, active_id, rolled_faces):
        super(SetRollAttackEdge, self).__init__(active_id)
        self.rolled_faces = rolled_faces

    def transitionImpl(self, state):
        state.attackDice_pool.setRoll(self.rolled_faces)


class RollDefenseRule(TargetAbilityRule):
    card_type = 'generic'

    def __init__(self, state, pilot_id):
        super(RollDefenseRule, self).__init__(state, 'doRollDefense', pilot_id)

    def _getEdges(self, state):
        roll_edge = RollDefenseEdge(self.pilot_id)
        prob_dict = state.defenseDice_pool.rollDice()

        for faces, prob_frac in prob_dict.iteritems():
            subedge = SetRollDefenseEdge(self.pilot_id, faces)
            roll_edge.addOutcome(faces, subedge, weight=prob_frac)

        return [roll_edge]

class RollDefenseEdge(RandomEdge):
    mandatory_bool = True

class SetRollDefenseEdge(Edge):
    mandatory_bool = True

    def __init__(self, active_id, rolled_faces):
        super(SetRollDefenseEdge, self).__init__(active_id)
        self.rolled_faces = rolled_faces

    def transitionImpl(self, state):
        state.defenseDice_pool.setRoll(self.rolled_faces)


# Compare Results
class CompareResultsRule(TargetAbilityRule):
    card_type = 'generic'

    def __init__(self, state, pilot_id):
        super(CompareResultsRule, self).__init__(state, 'doCompareResults', pilot_id)

    def _getEdges(self, state):
        return [CompareResultsEdge(self.pilot_id)]

class CompareResultsEdge(Edge):
    mandatory_bool = True

    def transitionImpl(self, state):
        # super(CompareResultsEdge, self).transitionImpl(state)
        hit_count = 0
        crit_count = 0
        evade_count = 0

        # log.info(state.attackDice_pool.getResults())
        # log.info(state.defenseDice_pool.getResults())

        for face in state.attackDice_pool.getResults():
            if face == 'C':
                crit_count += 1
            elif face == 'H':
                hit_count += 1

        for face in state.defenseDice_pool.getResults():
            if face == 'E':
                evade_count += 1

        # log.info("{}C + {}H vs. {}E".format(crit_count, hit_count, evade_count))

        while hit_count and evade_count:
            hit_count -= 1
            evade_count -= 1

        while crit_count and evade_count:
            crit_count -= 1
            evade_count -= 1

        while hit_count and state.getToken(state.target_id, 'shield'):
            hit_count -= 1
            state.removeToken(state.target_id, 'shield')

        while crit_count and state.getToken(state.target_id, 'shield'):
            crit_count -= 1
            state.removeToken(state.target_id, 'shield')

        while hit_count:
            hit_count -= 1
            state.dealDamage(state.target_id, faceup=False)

        while crit_count:
            crit_count -= 1
            state.dealDamage(state.target_id, faceup=True)

rule_list = [
    SpendFocusTokenToModifyAttackDiceRule,
    SpendFocusTokenToModifyDefenseDiceRule,
    SpendEvadeTokenToAddEvadeResultRule,
    RollAttackRule,
    RollDefenseRule,
    CompareResultsRule,
]
