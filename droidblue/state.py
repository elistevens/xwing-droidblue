__author__ = 'elis'

# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)


from collections import deque

import numpy as np
from droidblue.steps import Stepper
from droidblue.edge import ChooseNoneEdge
from droidblue.cards import xws
from droidblue.base import LargeBase

game = object()

def importstr(module_str, from_=None):
    """
    >>> importstr('os')
    <module 'os' from '.../os.pyc'>
    >>> importstr('math', 'fabs')
    <built-in function fabs>
    """
    module = __import__(module_str)
    for sub_str in module_str.split('.')[1:]:
        module = getattr(module, sub_str)

    if from_:
        try:
            return getattr(module, from_)
        except:
            raise ImportError('{}.{}'.format(module_str, from_))
    return module

shipStatIndex_dict = {attr: i for i, attr in enumerate([
    # Stats:
    'atk',
    'agi',
    'hull_max',
    'shield_max',
    'ps',
    'points',
    
    # Tokens:
    # Note that crit tokens are just a handy reminder of the damage cards, 
    # not an actual in-game effect themselves.
    'shield',
    'focus',
    'evade',
    'cloak',
    'stress',
    'stress_afterCheckPilotStress',
    'ion',
    
    # Token caps:
    'evade_max',
    
    # Flags:
    'dialKnown',
    'weaponsDisabled',
    'weaponsDisabled_nextTurn',
    'performedGreenManeuver',

    'chosen_dials',
    'chosen_activation',
    'chosen_combat',

    # Hardcoded ones:
    #   ignoreStress
    #   grantsHalfMov
    #   totalHp
    #   currentHp
    #   damage
    #   ionizedAt_count
])}

# shipValueIndex_dict = {attr: i for i, attr in enumerate([
#     'x',
#     'y'
#     'heading',
# ])}


class Pilot(object):
    # _stat_set = {'atk', 'agi', 'ps', 'hull', 'shields'}
    # _token_set = {'focus', 'evade', 'extramunitions', 'shield'}
    def __init__(self,
                 state,
                 player_id, pilot_id,
                 faction_str, pilot_json):
        self.player_id = player_id
        self.pilot_id = pilot_id
        self.ship_str = pilot_json['ship']
        self.pilot_str = pilot_json['name']
        self.base = None
        self.maneuver = None

        self.damage_list = []
        self.targetLock_list = []

        # TODO
        state.setStat(self.pilot_id, 'points', pilot_json['points'])

        self.base = xws.ship_dict[self.ship_str]['base']()

        for xws_dict in [xws.ship_dict[self.ship_str], xws.pilot_dict[self.pilot_str]]:
            for stat, value in xws_dict.get('stat_dict', {}).iteritems():
                state.setStat(pilot_id, stat, value)

            for rule_cls in xws_dict.get('rule_list', []):
                log.debug(rule_cls)
                rule_cls(state, self.pilot_id)

        # Ship and pilot rules
        module_list = ['ship.' + pilot_json['ship'], 'pilot.{}.{}'.format(faction_str, pilot_json['name'])]
        for module_str in module_list:
            try:
                module = importstr('droidblue.{}'.format(module_str))
            except ImportError:
                if not '.ship.' in module_str:
                    log.warn("Module not found: {}".format(module_str))
                continue

            for stat, value in getattr(module, 'stat_dict', {}).iteritems():
                state.setStat(pilot_id, stat, value)

            for rule_cls in getattr(module, 'rule_list', []):
                rule_cls(state, self.pilot_id)

        module_list = []
        for slot_str, upgrade_list in pilot_json['upgrades'].iteritems():
            for upgrade_str in upgrade_list:
                module_list.append('upgrade.{}.{}'.format(slot_str, upgrade_str))

        upgrade_index = 0
        for module_str in module_list:
            try:
                module = importstr('droidblue.{}'.format(module_str))
            except ImportError:
                if not '.ship.' in module_str:
                    log.warn("Module not found: {}".format(module_str))
                continue

            for stat, value in getattr(module, 'stat_dict', {}).iteritems():
                state.setStat(pilot_id, stat, value)

            if '.upgrade.' in module_str:
                for rule_cls in getattr(module, 'rule_list', []):
                    rule_cls(state, self.pilot_id, upgrade_index)
                upgrade_index += 1
            else:
                for rule_cls in getattr(module, 'rule_list', []):
                    rule_cls(state, self.pilot_id)


class BoardState(object):
    def __init__(self, squads_list):
        """
        BoardStateNode.__init__ is only called at the start of the game.
        All other instances are created by deepcopying the previous state, then
        applying the edge.transformImpl function.
        """

        self._stepper_stack = []

        self.edgeRules_dict = {}
        self.statRules_dict = {}

        self.fastforward_list = []
        self.edge_list = None
        self.activePlayer_id = None
        # self.slop = None

        self.attackDice_pool = None
        self.defenseDice_pool = None

        self.player_count = len(squads_list)
        self.pilots = []

        pilot_count = 0
        for player_id, squad_json in enumerate(squads_list):
            pilot_count += len(squad_json['pilots'])
        self.stat_array = np.zeros((pilot_count, len(shipStatIndex_dict)), np.int8)

        for player_id, squad_json in enumerate(squads_list):
            for pilot_json in squad_json['pilots']:
                print type(pilot_json), pilot_json
                self.pilots.append(Pilot(self, player_id, len(self.pilots), squad_json['faction'], pilot_json))

    # Stats (int8)
    def getRawStat(self, pilot_id, stat_key):
        if stat_key in shipStatIndex_dict:
            return int(self.stat_array[pilot_id, shipStatIndex_dict[stat_key]])

        if stat_key == 'ignoreStress':
            return False

        if stat_key == 'grantsHalfMov':
            return int(type(self.pilots[pilot_id].base) == LargeBase)

        if stat_key == 'totalHp':
            return int(self.getStat(pilot_id, 'hull_max') + self.getStat(pilot_id, 'shield_max'))

        if stat_key == 'currentHp':
            hull_int = self.getStat(pilot_id, 'hull_max')
            hull_int -= self.getStat(pilot_id, 'damage')
            return int(hull_int + self.getStat(pilot_id, 'shield'))

        if stat_key == 'damage':
            return len(self.pilots[pilot_id].damage_list)

        if stat_key == 'ionizedAt_count':
            return 2 if type(self.pilots[pilot_id].base) == LargeBase else 1

    def setStat(self, pilot_id, stat_key, value):
        stat_ndx = shipStatIndex_dict[stat_key]
        if stat_key + '_max' in shipStatIndex_dict:
            max_ndx = shipStatIndex_dict[stat_key + '_max']
            stat_max = self.stat_array[pilot_id, max_ndx]
        else:
            stat_max = 99
            
        self.stat_array[pilot_id, shipStatIndex_dict[stat_key]] = min(value, stat_max)

    def incStat(self, pilot_id, stat_key):
        stat_ndx = shipStatIndex_dict[stat_key]
        if stat_key + '_max' in shipStatIndex_dict:
            max_ndx = shipStatIndex_dict[stat_key + '_max']
            stat_max = self.stat_array[pilot_id, max_ndx]
        else:
            stat_max = 99
            
        if self.stat_array[pilot_id, stat_ndx] < stat_max:
            self.stat_array[pilot_id, stat_ndx] += 1
            
    def decStat(self, pilot_id, stat_key):
        stat_ndx = shipStatIndex_dict[stat_key]
        if self.stat_array[pilot_id, stat_ndx] > 0:
            self.stat_array[pilot_id, stat_ndx] -= 1

    # # Values (float32)
    # def getValue(self, pilot_id, value_key):
    #     return int(self.value_array[pilot_id, shipValueIndex_dict[value_key]])
    #
    # def setValue(self, pilot_id, value_key, value):
    #     self.value_array[pilot_id, shipValueIndex_dict[value_key]] = value

    # Tokens, a special kind of stat
    def assignToken(self, pilot_id, token_str):
        self.incStat(pilot_id, token_str)
        self.pushStepper(Stepper(['assign_{}'.format(token_str)], active_id=pilot_id))

    def removeToken(self, pilot_id, token_str):
        self.decStat(pilot_id, token_str)
        self.pushStepper(Stepper(['remove_{}'.format(token_str)], active_id=pilot_id))

    def clearToken(self, pilot_id, token_str):
        self.setStat(pilot_id, token_str, 0)
        self.pushStepper(Stepper(['clear_{}'.format(token_str)], active_id=pilot_id))

    # # Score
    # def computeCurrentScore(self, score_cls):
    #     self.currentScore_list = [score_cls(self, player_id) for player_id in range(self.player_count)]
    #
    # def computeLookaheadScore(self, score_cls, depth=0, slop=None):
    #     if depth <= 0:
    #         return self.computeCurrentScore(score_cls)
    #
    #     self.slop = slop
    #     for edge in self.edge_list:
    #         edge.computeScore(score_cls, self, depth-1)

    # Rules
    def addEdgeRule(self, rule, step_tup):
        self.edgeRules_dict.setdefault(step_tup, []).append(rule)

    def addStatRule(self, rule, key_tup):
        self.statRules_dict.setdefault(key_tup, []).append(rule)

    def getStat(self, pilot_id, stat_key):
        result = self.getRawStat(pilot_id, stat_key)

        rule_list = []
        for key_tup in [(stat_key,), (stat_key, pilot_id)]:
            rule_list.extend(self.statRules_dict.get(key_tup, []))

        rule_list = sorted([rule for rule in rule_list if rule.isAvailable(self)])

        for rule in rule_list:
            result = getattr(rule, stat_key, lambda s, r: r)(self, result)

        return result

    def getEdges(self):
        while True:
            self.edge_list = self._getEdges()

            if len(self.edge_list) == 0:
                self.nextStep()

            elif len(self.edge_list) == 1:
                only_edge = self.edge_list.pop()
                self.fastforward_list.append(only_edge)
                only_edge.transitionImpl(self)

            else:
                break

        self.activePlayer_id = self.pilots[self.edge_list[0].active_id].player_id
        for edge in self.edge_list:
            assert self.pilots[edge.active_id].player_id == self.activePlayer_id


    def _getEdges(self):
        key = self.step
        base_list = [Stepper.wildcard_key, key]
        step_list = []

        for step in base_list:
            step_list.append(step)
            if self.active_id is not None:
                step_list.append(step + ('active', self.active_id))
            if self.attack_id is not None:
                step_list.append(step + ('attack', self.attack_id))
            if self.target_id is not None:
                step_list.append(step + ('target', self.target_id))

        rule_list = []
        for step_tup in step_list:
            rule_list.extend(self.edgeRules_dict.get(step_tup, []))

        rule_list = sorted([rule for rule in rule_list if rule.isAvailable(self)])

        edge_list = []
        for rule in rule_list:
            edge_list.extend(rule.getEdges(self))

        # Has to be a separate loop so that filtering can see the full edge set, not just the incremental results.
        for rule in rule_list:
            edge_list = rule.filterEdges(edge_list, self)

        hasMandatory_bool = False
        for edge in edge_list:
            if edge.mandatory_bool:
                hasMandatory_bool = True

        if not hasMandatory_bool:
            edge_list.append(ChooseNoneEdge(edge_list[0].active_id))

        return edge_list








    # Stepper stuff
    def pushStepper(self, stepper):
        self._stepper_stack.append(deque([stepper]))

    def appendStepper(self, stepper):
        self._stepper_stack[-1].append(stepper)

    def nextStep(self):
        if self._stepper_stack and not self._stepper_stack[-1]:
            self._stepper_stack.pop()

        if not self._stepper_stack:
            self.pushStepper(Stepper(Stepper.steps_round(self.player_count)))

        try:
            self._stepper_stack[-1][0].nextStep()

        except StopIteration:
            self._stepper_stack[-1].popleft()
            self.nextStep()

    @property
    def step(self):
        return self._stepper_stack[-1][0].step_tup

    @property
    def active_id(self):
        return self._stepper_stack[-1][0].active_id
    @active_id.setter
    def active_id(self, value):
        assert self._stepper_stack[-1][0].active_id == None
        self._stepper_stack[-1][0].active_id = value

    @property
    def attack_id(self):
        return self._stepper_stack[-1][0].attack_id
    @attack_id.setter
    def attack_id(self, value):
        assert self._stepper_stack[-1][0].attack_id == None
        self._stepper_stack[-1][0].attack_id = value

    @property
    def target_id(self):
        return self._stepper_stack[-1][0].target_id
    @target_id.setter
    def target_id(self, value):
        assert self._stepper_stack[-1][0].target_id == None
        self._stepper_stack[-1][0].target_id = value
