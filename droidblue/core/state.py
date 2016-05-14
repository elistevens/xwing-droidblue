from droidblue.core.pilot import Pilot

__author__ = 'elis'

# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
# log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)

import copy
import uuid

from collections import deque

import numpy as np

from droidblue.core.edge import ChoosePassEdge
from droidblue.core.steps import Stepper
from droidblue.core.rules import Rule
from droidblue.core.dice import StateBackedAttackDicePool, StateBackedDefenseDicePool

class StateBase(object):
    stat_list = []
    stat_set = set(stat_list)
    statIndex_dict = {}

    def __init__(self, pilot_count):
        self.edgeRules_dict = {}
        self.statRules_dict = {}

        if len(self.stat_list):
            self.stat_array = np.zeros((pilot_count, len(self.stat_list)), np.int8)
        else:
            self.stat_array = None


    # Rules
    def addEdgeRule(self, rule, key_tup):
        self.edgeRules_dict.setdefault(key_tup, []).append(rule)

    def getEdgeRules(self, key_list):
        # Returns all rules, but subclasses are free to filter first
        rule_list = []
        for key_tup in key_list:
            rule_list.extend(self.edgeRules_dict.get(key_tup, []))
        return rule_list

    def addStatRule(self, rule, stat_key):
        self.statRules_dict.setdefault(stat_key, []).append(rule)

    def getStatRules(self, key_list):
        # Returns all rules, but subclasses are free to filter first
        rule_list = []
        for key_tup in key_list:
            rule_list.extend(self.statRules_dict.get(key_tup, []))
        return rule_list

    # Stats, which includes the raw storage for tokens and flags
    def _getStat(self, pilot_id, stat_key):
        result = self._getRawStat(pilot_id, stat_key)
        for rule in self.getStatRules([stat_key]):
            result = getattr(rule, stat_key, lambda s, r: r)(self, result)

        return result

    def _getRawStat(self, pilot_id, stat_key):
        return int(self.stat_array[pilot_id, self.statIndex_dict[stat_key]])

    def _setRawStat(self, pilot_id, stat_key, value):
        # log.info(self.statIndex_dict)
        self.stat_array[pilot_id, self.statIndex_dict[stat_key]] = value


    # Edges
    def _getEdges(self, key_list):
        rule_list = self.getEdgeRules(key_list)
        edge_list = []
        for rule in rule_list:
            edge_list.extend(rule.getEdges(self))
            # log.debug("{}: {}".format(rule, edge_list))

        # Has to be a separate loop from the above so that filtering can see
        # the full edge set, not just the incremental results.
        for rule in rule_list:
            edge_list = rule.filterEdges(edge_list, self)

        # log.info(edge_list)

        return edge_list


class ConstantState(StateBase):
    """
    Responsible for global game state (rules for pilots and upgrades, point
    values, etc.). Nothing on this class will change after players select
    and/or reveal the lists that they plan on flying.
    """
    id2obj_dict = {}

    @classmethod
    def getInst(cls, const_id):
        return cls.id2obj_dict[const_id]

    stat_list = [
        'player_id',
        'points',
        'ps',
        'atk',
        'agi',
        'shield_max',
        'hull_max',
        'isLarge',
        'ionizedAt_count',
        'upgrade_count',
        'upgrade_offset',
    ]
    stat_set = set(stat_list)
    statIndex_dict = {k: i for i, k in enumerate(stat_list)}

    def __init__(self, squads_list):
        # Register ID in global cache
        self.const_id = str(uuid.uuid4()) # FIXME: make this something similar, but easier to read
        self.id2obj_dict[self.const_id] = self

        self.player_count = len(squads_list)
        self.pilot_count = 0
        self.upgrade_count = 0
        self.ship_list = []
        self.pilot_list = []

        for player_id, squad_json in enumerate(squads_list):
            self.pilot_count += len(squad_json['pilots'])

        super(ConstantState, self).__init__(self.pilot_count)

        pilot_id = 0
        for player_id, squad_json in enumerate(squads_list):
            for pilot_json in squad_json['pilots']:
                self._setRawStat(pilot_id, 'player_id', player_id)
                self._setRawStat(pilot_id, 'upgrade_offset', self.upgrade_count)
                self.upgrade_count += Pilot.initRules(self, pilot_id, self.upgrade_count, squad_json['faction'], pilot_json)

                self.ship_list.append(pilot_json['ship'])
                self.pilot_list.append(pilot_json['name'])

                pilot_id += 1


class BoardState(StateBase):
    """
    Responsible for the state of the board as play progresses.

    Gameplay is represented as a DAG with the BoardState instances as nodes,
    and Edge instances as the edges (shocking). Each edge is capable of
    mutating the parent state into the child state (adding tokens, moving
    ships, etc.).

    Each edge is a choice that a player makes (though sometimes they're choices
    with only one option; see the fastforward_list).
    """
    token_list = [
        # Note that crit tokens are just a handy reminder of the damage cards,
        # not an actual in-game effect themselves.
        'shield',
        'focus',
        'evade',
        'cloak',
        'stress',
        'ion',
    ]
    token_set = set(token_list)
    flag_list = [
        'dialKnown',
        'weaponsDisabled',
        'nextRound:weaponsDisabled',
        'checkPilotStress:stress',
        'checkPilotStress:green',
        'isDestroyed',

        # 'chosen_dials',
        # 'chosen_activation',
        # 'chosen_combat',
    ]
    flag_set = set(flag_list)
    targetLock_list = [
        '0',
        '1',
    ]
    targetLock_set = set(targetLock_list)

    dice_list = [
        'dice_count',
        'rolled_C',
        'rolled_E',
        'rolled_H',
        'rolled_f',
        'rolled_x',

        'rerolled_C',
        'rerolled_E',
        'rerolled_H',
        'rerolled_f',
        'rerolled_x',
    ]
    dice_set = set(dice_list)


    stat_list = token_list + flag_list + targetLock_list + dice_list
    stat_set = set(stat_list)
    statIndex_dict = {k: i for i, k in enumerate(stat_list)}

    upgrade_list = [
        'isDiscarded',
        'extraMunitions',
        'token',
    ]
    upgrade_set = set(upgrade_list)
    upgradeIndex_dict = {k: i for i, k in enumerate(upgrade_list)}

    @property
    def const(self):
        return ConstantState.getInst(self.const_id)

    def __init__(self, const_id):
        """
        BoardStateNode.__init__ is only called at the start of the game.
        All other instances are created by deepcopying the previous state, then
        applying the edge.transformImpl function.
        """
        self.const_id = const_id
        super(BoardState, self).__init__(self.const.pilot_count)

        self.pickle_str = None


        self.fastforward_list = []
        self.edge_list = None
        self.usedOpportunity_set = set()
        self.playerWithInit_id = 999 # Inf, essentially

        # self.attackDice_pool = None
        # self.defenseDice_pool = None

        self.upgrade_array = np.zeros((self.const.upgrade_count, 2), np.int8)
        self.position_array = np.zeros((self.const.pilot_count, 5), np.float32)
        self.maneuver_list = [None] * self.const.pilot_count
        # self.pilots = []

        hull_max = 1
        for pilot_id in range(self.const.pilot_count):
            hull_max = max(hull_max, self.getStat(pilot_id, 'hull_max'))
            self._setRawStat(pilot_id, 'shield', self.getStat(pilot_id, 'shield_max'))
            # self.pilots.append(Pilot(self, pilot_id))

        self.damage_array = np.zeros((self.const.pilot_count, hull_max), np.int8)

        self._stepper_stack = []
        self._stepper_index = 0
        self._stepper_count = 0
        self.pushStepper(Stepper(Stepper.steps_setup()))


    # Rules
    def getEdgeRules(self, key_list):
        # Here we collect rules for both global game state, as well as local
        # board state, check to make sure that those rules are active, and pass
        # them along.
        rule_list = super(BoardState, self).getEdgeRules(key_list)
        rule_list.extend(self.const.getEdgeRules(key_list))

        replaced_set = set(rule.replacesRule_cls for rule in rule_list if rule.replacesRule_cls)
        rule_list = sorted([rule for rule in rule_list if type(rule) not in replaced_set])
        rule_list = sorted([rule for rule in rule_list if rule.isAvailable(self)])

        return rule_list

    def getStatRules(self, key_list):
        # Here we collect rules for both global game state, as well as local
        # board state, check to make sure that those rules are active, and pass
        # them along.
        rule_list = super(BoardState, self).getStatRules(key_list)
        rule_list.extend(self.const.getStatRules(key_list))

        replaced_set = set(rule.replacesRule_cls for rule in rule_list if rule.replacesRule_cls)
        rule_list = sorted([rule for rule in rule_list if type(rule) not in replaced_set])
        rule_list = sorted([rule for rule in rule_list if rule.isAvailable(self)])

        return rule_list

    # Stats
    def getStat(self, pilot_id, stat_key):
        return self._getStat(pilot_id, stat_key)

    def _getRawStat(self, pilot_id, stat_key):
        try:
            return super(BoardState, self)._getRawStat(pilot_id, stat_key)
        except KeyError:
            pass

        try:
            return self.const._getRawStat(pilot_id, stat_key)
        except KeyError:
            pass

        if stat_key.endswith('_max'):
            return 99

        if stat_key == 'grantsHalfMov':
            return int(self.const._getRawStat(pilot_id, 'isLarge'))

        if stat_key == 'ionizedAt_count':
            return 2 if self.const._getRawStat(pilot_id, 'isLarge') else 1

        if stat_key == 'totalHp':
            return int(self._getStat(pilot_id, 'hull_max') + self._getStat(pilot_id, 'shield_max'))

        if stat_key == 'currentHp':
            hull_int = self._getStat(pilot_id, 'hull_max')
            hull_int -= self._getStat(pilot_id, 'damage')
            return int(hull_int + self._getStat(pilot_id, 'shield'))

        if stat_key == 'damage':
            return int(np.sum(self.damage_array[pilot_id] != 0) + np.sum(self.damage_array[pilot_id] == 2))

        return 0

    # Edges
    def getEdges(self, fastforward_bool=True):
        # while True:
        for _ in range(100):
            # Make sure we're using the deepest stepper
            if self._stepper_index >= len(self._stepper_stack):
                self._stepper_index = len(self._stepper_stack) - 1

            if self._stepper_index < len(self._stepper_stack) - 1:
                self._stepper_index = len(self._stepper_stack) - 1

            if self.step is None:
                self.nextStep()

            base_list = [Rule.wildcard_key, self.step]
            key_list = []

            for step in base_list:
                if not isinstance(step, tuple):
                    step = (step,)

                key_list.append(step)
                if self.active_id is not None:
                    key_list.append(step + ('active', self.active_id))
                if self.attack_id is not None:
                    key_list.append(step + ('attack', self.attack_id))
                if self.target_id is not None:
                    key_list.append(step + ('target', self.target_id))

            edge_list = self._getEdges(key_list)

            # Restrict to player with the best init
            self.playerWithInit_id = 999 # Inf, essentially
            self.edge_list = []
            for edge in edge_list:
                player_id = self.getStat(edge.active_id, 'player_id')

                if player_id < self.playerWithInit_id:
                    self.edge_list = [edge]
                    self.playerWithInit_id = player_id
                elif player_id == self.playerWithInit_id:
                    self.edge_list.append(edge)

            # Provide option to pass
            if self.edge_list and not any(edge.mandatory_bool for edge in self.edge_list):
                pilot_id = self.edge_list[0].active_id
                player_id = self.getStat(pilot_id, 'player_id')
                opportunity_key = ('pass', player_id) + self.getOpportunityStepKey()
                self.edge_list.append(ChoosePassEdge(pilot_id, [opportunity_key]))

            if fastforward_bool:
                # Next/Fastforward if nothing interesting to choose from
                if len(self.edge_list) == 0:
                    self.nextStep()

                elif len(self.edge_list) == 1:
                    only_edge = self.edge_list.pop()
                    self.fastforward_list.append(only_edge)
                    # log.info("Fastforward {}: {}".format(fastforward_bool, only_edge))
                    only_edge.getExactState(self, doCopy=False)
                    self.nextStep()

                else:
                    break
            else:
                break

        self.edge_list.sort()
        return self.edge_list


    # Tokens, a special kind of stat
    def getToken(self, pilot_id, token_str):
        assert token_str in self.token_set
        return self._getStat(pilot_id, token_str)

    def assignToken(self, pilot_id, token_str):
        assert token_str in self.token_set
        token_count = self._getStat(pilot_id, token_str)
        if token_count < 99:
            self._setRawStat(pilot_id, token_str, token_count + 1)
        self.pushStepper(Stepper(['assign_{}'.format(token_str)], active_id=pilot_id))

    def removeToken(self, pilot_id, token_str):
        assert token_str in self.token_set
        token_count = self._getStat(pilot_id, token_str)
        assert token_count > 0

        self._setRawStat(pilot_id, token_str, token_count - 1)
        self.pushStepper(Stepper(['remove_{}'.format(token_str)], active_id=pilot_id))

    def clearToken(self, pilot_id, token_str):
        assert token_str in self.token_set
        token_count = self._getStat(pilot_id, token_str)
        if token_count > 0:
            self._setRawStat(pilot_id, token_str, 0)
            self.pushStepper(Stepper(['clear_{}'.format(token_str)], active_id=pilot_id))

    # Flags, a special kind of stat
    def getFlag(self, pilot_id, flag_str):
        assert flag_str in self.flag_set
        return bool(self._getStat(pilot_id, flag_str))

    def setFlag(self, pilot_id, flag_str):
        assert flag_str in self.flag_set
        self._setRawStat(pilot_id, flag_str, 1)
        self.pushStepper(Stepper(['flag_{}'.format(flag_str)], active_id=pilot_id))

    def unsetFlag(self, pilot_id, flag_str):
        assert flag_str in self.flag_set
        self._setRawStat(pilot_id, flag_str, 0)
        self.pushStepper(Stepper(['unflag_{}'.format(flag_str)], active_id=pilot_id))

    # FIXME: add acquire/spend/discard target lock functions

    def dealDamage(self, pilot_id, faceup):
        for i in range(self.damage_array.shape[1]):
            if self.damage_array[pilot_id, i] == 0:
                # FIXME: make this a random card draw?
                self.damage_array[pilot_id, i] = 1

                if not faceup:
                    self.damage_array[pilot_id, i] *= -1

                break

        if faceup:
            self.pushStepper(Stepper(['dealtCrit'], active_id=pilot_id))
        else:
            self.pushStepper(Stepper(['dealtHit'], active_id=pilot_id))

    # Stepper stuff
    def nextRound(self, includeDials_bool=True):
        self.pushStepper(Stepper(Stepper.steps_round(includeDials_bool)))

    def pushStepper(self, stepper):
        log.debug(stepper)
        self._stepper_stack.append(deque([stepper]))
        stepper.count = self._stepper_count
        self._stepper_count += 1

    def appendStepper(self, stepper):
        log.debug(stepper)
        self._stepper_stack[self._stepper_index].append(stepper)
        stepper.count = self._stepper_count
        self._stepper_count += 1


    def nextStep(self):
        if self._stepper_index != len(self._stepper_stack) - 1:
            self._stepper_index = len(self._stepper_stack) - 1

            # log.info(self._stepper_index)
            # log.info(self._stepper_stack)
            # if self._stepper_stack and self.step is None:
            if self.step is None:
                log.debug("self.step is None; calling self.nextStep()")
                self.nextStep()

            return

        try:
            self._stepper_stack[self._stepper_index][0].nextStep(self)

        except StopIteration:
            self._stepper_stack[self._stepper_index].popleft()
            log.debug("StopIteration; calling self.nextStep()")
            self.nextStep()
            return

        except IndexError:
            if not self._stepper_stack:
                log.debug("IndexError; self._stepper_stack is empty")
                return

            if not self._stepper_stack[self._stepper_index]:
                self._stepper_stack.pop()
                log.debug("IndexError; calling self.nextStep()")
                self.nextStep()
                return

        else:
            log.debug("self.step is {}".format(self.step))


    @property
    def stepper(self):
        # try:
        return self._stepper_stack[self._stepper_index][0]
        # except:
        #     log.warn(self._stepper_index)
        #     log.warn(self._stepper_stack)
        #     raise

    @property
    def step(self):
        return self.stepper.step_tup

    @property
    def step_count(self):
        return self.stepper.step_count

    @property
    def active_id(self):
        return self.stepper.active_id
    @active_id.setter
    def active_id(self, value):
        assert self.stepper.active_id == None
        self.stepper.active_id = value

    @property
    def active_pilot(self):
        return Pilot(self, self.active_id)

    @property
    def attack_id(self):
        return self.stepper.attack_id
    @attack_id.setter
    def attack_id(self, value):
        assert self.stepper.attack_id == None
        self.stepper.attack_id = value

    @property
    def attack_pilot(self):
        return Pilot(self, self.attack_id)

    @property
    def target_id(self):
        return self.stepper.target_id
    @target_id.setter
    def target_id(self, value):
        assert self.stepper.target_id == None
        self.stepper.target_id = value

    @property
    def target_pilot(self):
        return Pilot(self, self.target_id)

    @property
    def pilots(self):
        return [Pilot(self, pilot_id) for pilot_id in range(self.const.pilot_count)]

    @property
    def attackDice_pool(self):
        return StateBackedAttackDicePool(self, self.attack_id)

    @property
    def defenseDice_pool(self):
        return StateBackedDefenseDicePool(self, self.target_id)


    def useOpportunity(self, opportunity_list):
        assert isinstance(opportunity_list, list), repr(opportunity_list)
        self.usedOpportunity_set.update(opportunity_list)

    def getOpportunityStepKey(self):
        return (self.stepper.count,) + self.step

    def endOfRoundCleanup(self):
        prevStat_array = copy.deepcopy(self.stat_array)

        for stat_key in self.flag_list:
            if stat_key in self.statIndex_dict:
                self.stat_array[:, self.statIndex_dict[stat_key]] = 0

        self.stat_array[:, self.statIndex_dict['weaponsDisabled']] = prevStat_array[:, self.statIndex_dict['nextRound:weaponsDisabled']]
        self.stat_array[:, self.statIndex_dict['isDestroyed']] = prevStat_array[:, self.statIndex_dict['isDestroyed']]

        self.usedOpportunity_set.clear()
        self.maneuver_list = [None] * self.const.pilot_count

        # for pilot in self.pilots:
        #     pilot.maneuver_tup = None

    def toJson(self):
        j = {'players': [{} for _ in range(self.const.player_count)]}
        for pilot in self.pilots:
            player_dict = j['players'][self.const._getRawStat(pilot.pilot_id, 'player_id')]
            player_dict.setdefault('pilots', []).append(pilot.toJson(self))

        return j

