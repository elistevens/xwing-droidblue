from droidblue.core.edge import SpendFocusTokenEdge, SpendEvadeTokenEdge

from droidblue.core.rules import AttackAbilityRule, TargetAbilityRule


# Perform focus

# Perform evade

# Spend focus
class SpendFocusTokenToModifyAttackDiceRule(AttackAbilityRule):
    card_type = 'generic'

    def __init__(self, state, pilot_id):
        super(SpendFocusTokenToModifyAttackDiceRule, self).__init__(state, 'attackerModifyAttack', pilot_id)

    def _getEdges(self, state):
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
        return [SpendEvadeTokenToAddEvadeResultEdge(self.pilot_id)]

class SpendEvadeTokenToAddEvadeResultEdge(SpendEvadeTokenEdge):
    def transitionImpl(self, state):
        super(SpendEvadeTokenToAddEvadeResultEdge, self).transitionImpl(state)
        state.defenseDice_pool.addResult('E')


# Acquire Target Lock


rule_list = [
    SpendFocusTokenToModifyAttackDiceRule,
    SpendFocusTokenToModifyDefenseDiceRule,
    SpendEvadeTokenToAddEvadeResultRule,
]
