__author__ = 'elis'

import collections
import functools
import re

from typing import NewType, Optional, Dict, List, Tuple

import numpy as np

from .node import StateAbc, PilotId

from ..logging_config import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)


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


    def __init__(self, state: 'RuleState', key_list: List[RuleKeyTuple], pilot_id, upgrade_id=None):
        # from droidblue.core.steps import steps_str2id_dict

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
            # assert key.step in steps_str2id_dict
            state.addEdgeRule(self, key.step, key.active_id, key.target_id)

    def __repr__(self):
        extra_str = ', '.join(['{}:{!r}'.format(k, v) for k, v in sorted(self.__dict__.items())])
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
        return type(self) == type(other) and self.__dict__ == other.__dict__

    # @property
    # def opportunity_list(self):
    #     return ('rule', self.pilot_id, type(self))

    def isAvailable(self, state: 'RuleState'):
        return True

    def getOpportunityKeys(self, state: 'RuleState'):
        opportunity_key = default_oppKey._replace(
            rule=type(self).__name__,
            pilot_id=self.pilot_id,
            upgrade_id=self.upgrade_id if self.upgrade_id is not None else 9999)

        if not self.isOncePerRound_bool:
            opportunity_key = opportunity_key._replace(**state.getStepOpportunityKeys())

        return [opportunity_key]

    @classmethod
    def getPassOpportunityKey(cls, state: 'RuleState', player_id):
        opportunity_dict = {
            'step': None,
            'count': 9999,
            'rule': -1,  # Pass
            'pilot_id': player_id,
            'upgrade_id': 9999,
        }
        opportunity_dict.update(state.getStepOpportunityKeys())

        return OpportunityTuple(**opportunity_dict)


    def getEdges(self, state: 'RuleState'):
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

    def _getEdges(self, state: 'RuleState'):
        return []

    def filterEdges(self, edge_list, state: 'RuleState'):
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
    def __init__(self, state: 'RuleState', key_list, pilot_id, upgrade_id=None):
        key_list = [default_ruleKey._replace(step=key_str, active_id=pilot_id) for key_str in _str2list(key_list)]
        super(ActiveAbilityRule, self).__init__(state, key_list, pilot_id, upgrade_id=None)


class TargetAbilityRule(Rule):
    def __init__(self, state: 'RuleState', key_list, pilot_id, upgrade_id=None):
        key_list = [default_ruleKey._replace(step=key_str, target_id=pilot_id) for key_str in _str2list(key_list)]
        super(TargetAbilityRule, self).__init__(state, key_list, pilot_id, upgrade_id=None)




class RuleState(StateAbc):
    # cloneKeep_set = set('constant_info')

    stat_list = []
    stat_set = set(stat_list)
    statIndex_dict = {}

    def __init__(self, readonly, pilot_count):
        super().__init__(readonly=readonly)

        self.edgeRules_dict = {}
        self.statRules_dict = {}

        if len(self.stat_list):
            self.stat_array = np.zeros((pilot_count, len(self.stat_list)), np.int8)
        else:
            self.stat_array = None

    # Rules
    def addEdgeRule(self, rule: Rule, step: tuple, active_id: Optional[PilotId], target_id: Optional[PilotId]):
        rule_sublist = self.edgeRules_dict.setdefault(step, [[], {}, {}])

        if active_id is not None:
            assert target_id is None
            rule_sublist[1].setdefault(active_id, []).append(rule)
        elif target_id is not None:
            assert active_id is None
            rule_sublist[2].setdefault(target_id, []).append(rule)
        else:
            rule_sublist[0].append(rule)

    def getEdgeRules(self, step, active_id: PilotId, target_id: PilotId):
        # Returns all rules, but subclasses are free to filter first
        rule_list = []

        # This function is a hotspot, and these two ifs are a huge speedup
        if self.edgeRules_dict:
            for step_str in [Rule.wildcard_key, step]:
                if step_str in self.edgeRules_dict:
                    rule_sublist = self.edgeRules_dict[step_str]
                    rule_list.extend(rule_sublist[0])

                    if active_id in rule_sublist[1]:
                        rule_list.extend(rule_sublist[1][active_id])

                    if target_id in rule_sublist[2]:
                        rule_list.extend(rule_sublist[2][target_id])

        return rule_list

    def addStatRule(self, rule, stat_key):
        self.statRules_dict.setdefault(stat_key, []).append(rule)

    def getStatRules(self, key_list):
        # Returns all rules, but subclasses are free to filter first
        rule_list = []
        for stat_key in key_list:
            rule_list.extend(self.statRules_dict.get(stat_key, []))
        return rule_list

    # Stats, which includes the raw storage for tokens and flags
    def getStat(self, pilot_id: PilotId, stat_key):
        result = self._getRawStat(pilot_id, stat_key)
        for rule in self.getStatRules([stat_key]):
            result = getattr(rule, 'getStat_' + stat_key, lambda state, result: result)(self, result)

        return result

    def _getRawStat(self, pilot_id: PilotId, stat_key):
        return int(self.stat_array[pilot_id, self.statIndex_dict[stat_key]])

    def _setRawStat(self, pilot_id: PilotId, stat_key, value):
        # log.info(self.statIndex_dict)
        self.stat_array[pilot_id: PilotId, self.statIndex_dict[stat_key]] = value


    # Edges
    def _getEdges(self, step, active_id: PilotId, target_id: PilotId):
        rule_list = self.getEdgeRules(step, active_id, target_id)
        edge_list = []
        for rule in rule_list:
            edge_list.extend(rule.getOutgoingEdges(self))
            # log.debug("{}: {}".format(rule, edge_list))

        # Has to be a separate loop from the above so that filtering can see
        # the full edge set, not just the incremental results.
        for rule in rule_list:
            edge_list = rule.filterEdges(edge_list, self)

        # log.info(edge_list)

        return edge_list


