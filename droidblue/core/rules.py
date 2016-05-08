import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

__author__ = 'elis'

import functools
import re

@functools.total_ordering
class Rule(object):
    wildcard_key = ('*',)
    priority = 10
    card_type = None
    card_name = None
    isStatRule_bool = False
    replacesRule_cls = None

    isOncePerGame_bool = False
    isOncePerRound_bool = False


    def __init__(self, state, key_list, pilot_id, upgrade_id=None):
        assert isinstance(key_list, list)
        assert isinstance(pilot_id, int)
        assert isinstance(upgrade_id, (int, type(None)))

        self.opportunity_key = "{}:{}:{}".format(type(self).__name__, id(self), pilot_id)
        self.pilot_id = pilot_id
        self.upgrade_id = upgrade_id

        for key_tup in key_list:
            assert isinstance(key_tup, tuple)
            
            if self.isStatRule_bool:
                state.addStatRule(self, key_tup)
            else:
                state.addEdgeRule(self, key_tup)

    def __repr__(self):
        extra_str = ', '.join(['{}:{!r}'.format(k, v) for k, v in sorted(self.__dict__.iteritems())])
        r = super(Rule, self).__repr__()
        r = re.sub(r'\<droidblue\.([a-z]+\.)+', '<', r)
        return r.replace('>', ' {}>'.format(extra_str))

    def _sortKey(self):
        return (self.priority, self.pilot_id, str(type(self)))

    def __lt__(self, other):
        try:
            return self._sortKey() < other._sortKey()
        except:
            return True

    def __eq__(self, other):
        return id(self) == id(other)

    # @property
    # def opportunity_list(self):
    #     return ('rule', self.pilot_id, type(self))

    def isAvailable(self, state):
        return True

    def getOpportunityKey(self, state):
        opportunity_key = (self.opportunity_key,)
        if not self.isOncePerRound_bool:
            opportunity_key += state.getOpportunityStepKey()

        return [opportunity_key]

    def getPassOpportunityKey(self, state):
        player_id = state.getStat(self.pilot_id, 'player_id')
        opportunity_key = ('pass', player_id)

        return opportunity_key + state.getOpportunityStepKey()

    def getEdges(self, state):
        if self.isOncePerGame_bool and state.getUpgradeStat(self.pilot_id, self.upgrade_id, 'token') == 0:
            return []

        if self.getPassOpportunityKey(state) in state.usedOpportunity_set:
            return []

        opportunity_list = self.getOpportunityKey(state)

        # log.info('===============================')
        # log.info(opportunity_list)
        # log.info(sorted(state.usedOpportunity_set))

        for opportunity_key in opportunity_list:
            if opportunity_key in state.usedOpportunity_set:
                return []

        edge_list = self._getEdges(state) or []

        for edge in edge_list:
            assert edge.opportunity_list is None
            edge.opportunity_list = opportunity_list

        return edge_list

    def _getEdges(self, state):
        return []

    def filterEdges(self, edge_list, state):
        filtered_list = []
        for edge in edge_list:
            if self.filterEdge(edge, state):
                filtered_list.append(edge)
            else:
                log.debug("{} filtering {}".format(str(type(self)), edge))
        return filtered_list

    def filterEdge(self, edge, state):
        return True


def _str2list(item):
    if isinstance(item, str):
        return [item]
    elif isinstance(item, list):
        return item
    raise TypeError(str(type(item)))

def _str2tup(item):
    if isinstance(item, str):
        return (item,)
    elif isinstance(item, tuple):
        return item
    raise TypeError(str(type(item)))

class ActiveAbilityRule(Rule):
    def __init__(self, state, key_list, pilot_id, upgrade_id=None):
        key_list = [_str2tup(key_tup) + ('active', pilot_id) for key_tup in _str2list(key_list)]
        super(ActiveAbilityRule, self).__init__(state, key_list, pilot_id, upgrade_id=None)

class AttackAbilityRule(Rule):
    """Note that this is a "when attacking" ability, not the actual attack."""
    def __init__(self, state, key_list, pilot_id, upgrade_id=None):
        key_list = [_str2tup(key_tup) + ('attack', pilot_id) for key_tup in _str2list(key_list)]
        super(AttackAbilityRule, self).__init__(state, key_list, pilot_id, upgrade_id=None)

class TargetAbilityRule(Rule):
    def __init__(self, state, key_list, pilot_id, upgrade_id=None):
        key_list = [_str2tup(key_tup) + ('target', pilot_id) for key_tup in _str2list(key_list)]
        super(TargetAbilityRule, self).__init__(state, key_list, pilot_id, upgrade_id=None)


