from droidblue.rules import AttackAbilityRule, TargetAbilityRule

class OmegaLeaderAttackRule(AttackAbilityRule):
    card_type = 'pilot'
    card_name = 'omegaleader'

    def __init__(self, state, pilot_id):
        step_list = [('defenderModifyDefense',)]
        super(OmegaLeaderAttackRule, self).__init__(state, pilot_id, step_list)

    def isAvailable(self, state):
        return super(OmegaLeaderAttackRule, self).isAvailable(state) and \
            state.hasTargetLock(state.attack_id, state.target_id)

    def filterEdges(self, edge_list, state):
        return []

class OmegaLeaderDefendRule(TargetAbilityRule):
    card_type = 'pilot'
    card_name = 'omegaleader'

    def __init__(self, state, pilot_id):
        step_list = [('attackerModifyAttack',)]
        super(OmegaLeaderDefendRule, self).__init__(state, pilot_id, step_list)

    def isAvailable(self, state):
        return super(OmegaLeaderDefendRule, self).isAvailable(state) and \
            state.hasTargetLock(state.target_id, state.attack_id)

    def filterEdges(self, edge_list, state):
        # TODO: properly handle defensive palpatine
        return []

rule_list = [OmegaLeaderAttackRule, OmegaLeaderDefendRule]
