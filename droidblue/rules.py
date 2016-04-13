__author__ = 'elis'

import functools


@functools.total_ordering
class Rule(object):
    priority = 10
    card_type = None
    card_name = None
    isStatRule_bool = False


    def __init__(self, state, pilot_id, step_list):
        self.pilot_id = pilot_id

        for step_tup in step_list:
            state.addEdgeRule(self, step_tup)

    def _sortKey(self):
        return (self.priority, self.pilot_id, str(type(self)))

    def __lt__(self, other):
        return self._sortKey() < other._sortKey()

    def __eq__(self, other):
        return id(self) == id(other)

    def isAlive(self, state):
        return state.isAlive(self.pilot_id)

    def isAvailable(self, state):
        return True

    def getEdges(self, state):
        return []

    def filterEdges(self, edge_list, state):
        return edge_list


class ActiveAbilityRule(Rule):
    def __init__(self, state, pilot_id, step_list):
        step_list = [step_tup + ('active', pilot_id) for step_tup in step_list]
        super(ActiveAbilityRule, self).__init__(pilot_id, step_list)

class AttackAbilityRule(Rule):
    """Note that this is a "when attacking" ability, not the actual attack."""
    def __init__(self, state, pilot_id, step_list):
        step_list = [step_tup + ('attack', pilot_id) for step_tup in step_list]
        super(AttackAbilityRule, self).__init__(pilot_id, step_list)

class TargetAbilityRule(Rule):
    def __init__(self, state, pilot_id, step_list):
        step_list = [step_tup + ('target', pilot_id) for step_tup in step_list]
        super(TargetAbilityRule, self).__init__(pilot_id, step_list)

class PerformActionRule(ActiveAbilityRule):
    def __init__(self, state, pilot_id):
        step_list = [('performAction',)]
        super(PerformActionRule, self).__init__(pilot_id, step_list)

    def isAvailable(self, state):
        ship = state.ship[self.pilot_id]
        return super(PerformActionRule, self).isAvailable(state) and \
            (ship.hasFlag('ignoreStress') or ship.numTokens('stress') == 0)


class AttackRule(Rule):
    pass




