from droidblue.rules import AttackRule, PerformActionRule
from droidblue.edge import Edge, SpendFocusTokenEdge, SpendEvadeTokenEdge

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


# Perform focus
class PerformFocusActionRule(PerformActionRule):
    card_type = 'generic'

    def getEdges(self, state):
        return [PerformFocusActionEdge(self.pilot_id)]

class PerformFocusActionEdge(Edge):
    def transitionImpl(self, state):
        state.ship[self.active_id].assignToken(state, 'focus')

# Perform evade
class PerformEvadeActionRule(PerformActionRule):
    card_type = 'generic'

    def getEdges(self, state):
        return [PerformEvadeActionEdge(self.pilot_id)]

class PerformEvadeActionEdge(Edge):
    def transitionImpl(self, state):
        state.ship[self.active_id].assignToken(state, 'evade')

# Spend focus
class SpendFocusTokenToModifyAttackDiceEdge(SpendFocusTokenEdge):
    def transitionImpl(self, state):
        super(SpendFocusTokenToModifyAttackDiceEdge, self).transitionImpl(state)
        state.attackDice_pool.modifyFaces('f', 'H', 99)


class SpendFocusTokenToModifyDefenseDiceEdge(SpendFocusTokenEdge):
    def transitionImpl(self, state):
        super(SpendFocusTokenToModifyDefenseDiceEdge, self).transitionImpl(state)
        state.defenseDice_pool.modifyFaces('f', 'E', 99)

# Spend evade
class SpendEvadeTokenToAddEvadeResultEdge(SpendEvadeTokenEdge):
    def transitionImpl(self, state):
        super(SpendEvadeTokenToAddEvadeResultEdge, self).transitionImpl(state)
        state.defenseDice_pool.addResult('E')

# Acquire Target Lock
class PerformTargetLockActionRule(PerformActionRule):
    card_type = 'generic'

    def getEdges(self, state):
        edge_list = [PerformTargetLockActionEdge(self.pilot_id)]
        return edge_list

class PerformTargetLockActionEdge(Edge):
    def transitionImpl(self, state):
        state.ship[self.active_id].acquireTargetLock(state, 'focus')

class PerformBarrelRollActionRule(PerformActionRule):
    card_type = 'generic'

class PerformBoostActionRule(PerformActionRule):
    card_type = 'generic'

class PerformCloakActionRule(PerformActionRule):
    card_type = 'generic'

class PerformSlamActionRule(PerformActionRule):
    card_type = 'generic'
