import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

__author__ = 'elis'

import collections
import functools
import re

OpportunityTuple = collections.namedtuple('OpportunityTuple', ['step', 'count', 'rule', 'pilot_id', 'upgrade_id'])
default_oppKey = OpportunityTuple(None, None, None, None, None)

RuleKeyTuple = collections.namedtuple('RuleKeyTuple', ['step', 'active_id', 'target_id'])
default_ruleKey = RuleKeyTuple(None, None, None)


@functools.total_ordering
class Rule(object):
    wildcard_key = ('*',)
    priority = 50
    card_type = None
    card_name = None
    isStatRule_bool = False
    replacesRule_cls = None

    isOncePerGame_bool = False
    isOncePerRound_bool = False


    def __init__(self, state, key_list, pilot_id, upgrade_id=None):
        from droidblue.core.steps import steps_str2id_dict

        assert isinstance(key_list, list)
        assert isinstance(pilot_id, int)
        assert isinstance(upgrade_id, (int, type(None)))

        self.rule_id = state.getRuleId()
        self.pilot_id = pilot_id
        self.upgrade_id = upgrade_id
        self.player_id = state.getStat(pilot_id, 'player_id')
        # self.opportunity_key = "{}:{}:{}".format(type(self).__name__, id(self), pilot_id)
        # if upgrade_id is not None:
        #     self.opportunity_key += "-{}".format(upgrade_id)

        for attr in dir(self):
            if attr.startswith('getStat_'):
                key = attr.split('_', 1)[1]
                state.addStatRule(self, key)

        for key in key_list:
            assert isinstance(key, RuleKeyTuple)
            assert key.step in steps_str2id_dict
            state.addEdgeRule(self, key.step, key.active_id, key.target_id)

    def __repr__(self):
        extra_str = ', '.join(['{}:{!r}'.format(k, v) for k, v in sorted(self.__dict__.iteritems())])
        r = super(Rule, self).__repr__()
        r = re.sub(r'\<droidblue\.([a-z]+\.)+', '<', r)
        return r.replace('>', ' {}>'.format(extra_str))

    def _sortKey(self):
        return (self.priority, self.pilot_id, self.opportunity_key)

    def __lt__(self, other):
        try:
            return self._sortKey() < other._sortKey()
        except:
            return True

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # @property
    # def opportunity_list(self):
    #     return ('rule', self.pilot_id, type(self))

    def isAvailable(self, state):
        return True

    def getOpportunityKeys(self, state):
        opportunity_key = default_oppKey._replace(
            rule=type(self).__name__,
            pilot_id=self.pilot_id,
            upgrade_id=self.upgrade_id if self.upgrade_id is not None else 9999)

        if not self.isOncePerRound_bool:
            opportunity_key = opportunity_key._replace(**state.getStepOpportunityKeys())

        return [opportunity_key]

    @classmethod
    def getPassOpportunityKey(cls, state, player_id):
        opportunity_dict = {
            'step': None,
            'count': 9999,
            'rule': -1,  # Pass
            'pilot_id': player_id,
            'upgrade_id': 9999,
        }
        opportunity_dict.update(state.getStepOpportunityKeys())

        return OpportunityTuple(**opportunity_dict)


    def getEdges(self, state):
        if self.isOncePerGame_bool and state.getUpgradeStat(self.pilot_id, self.upgrade_id, 'token') == 0:
            return []

        if state.hasOpportunityBeenUsed(self.getPassOpportunityKey(state, self.player_id)):
            return []

        # if self.getPassOpportunityKey(state) in state.usedOpportunity_set:
        #     return []

        opportunity_list = self.getOpportunityKeys(state)

        # log.info('===============================')
        # log.info(opportunity_list)
        # log.info(sorted(state.usedOpportunity_set))

        for opportunity_key in opportunity_list:
            if state.hasOpportunityBeenUsed(opportunity_key):
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
            # else:
            #     log.debug("{} filtering {}".format(str(type(self)), edge))
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
        key_list = [default_ruleKey._replace(step=key_str, active_id=pilot_id) for key_str in _str2list(key_list)]
        super(ActiveAbilityRule, self).__init__(state, key_list, pilot_id, upgrade_id=None)


class TargetAbilityRule(Rule):
    def __init__(self, state, key_list, pilot_id, upgrade_id=None):
        key_list = [default_ruleKey._replace(step=key_str, target_id=pilot_id) for key_str in _str2list(key_list)]
        super(TargetAbilityRule, self).__init__(state, key_list, pilot_id, upgrade_id=None)


