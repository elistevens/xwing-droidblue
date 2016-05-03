from droidblue.core.rules import ActiveAbilityRule


class AttackRule(ActiveAbilityRule):
    def __init__(self, state, pilot_id):
        super(AttackRule, self).__init__(state, pilot_id, 'chooseWeaponAndTarget')


class AttackPrimaryArcRule(AttackRule):
    card_type = 'generic'


class AttackPrimaryAuxBackRule(AttackRule):
    card_type = 'generic'


class AttackPrimaryAuxSideRule(AttackRule):
    card_type = 'generic'


class AttackTorpedoAuxBackRule(AttackRule):
    card_type = 'generic'


class AttackPrimaryTurretRule(AttackRule):
    card_type = 'generic'


rule_list = [
    # AttackPrimaryArcRule,
]
