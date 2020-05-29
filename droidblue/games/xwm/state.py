from droidblue.core.pilot import Pilot, PilotId

__author__ = 'elis'

# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

import collections
import copy
import uuid


import numpy as np

from droidblue.core.edge import ChoosePassEdge, RandomEdge
from droidblue.core.rules import Rule, default_ruleKey, RuleState
# from droidblue.core.dice import StateBackedAttackDicePool, StateBackedDefenseDicePool

StepTuple = collections.namedtuple('StepTuple', ['step', 'count', 'active_id', 'target_id'])

class ConstantState(RuleState):
    """
    Responsible for global game state (rules for pilots and upgrades, point
    values, etc.). Nothing on this class will change after players select
    and/or reveal the lists that they plan on flying.

    Doesn't really count as "State" per se, since it never changes.
    We just want to reuse the bag-of-rules mechanics from RuleState.
    """
    id2obj_dict = {}

    @classmethod
    def getInst(cls, const_id):
        return cls.id2obj_dict[const_id]

    stat_list = [
        'player_id',
        'points',
        'unique',
        'init',
        'atk_front',
        'atk_back',
        'atk_left',
        'atk_right',
        'atk_widefront',
        'atk_wideback',
        'atk_turret',
        'atk_bowtie',
        'agi',
        'hull_max',
        'shield_max',
        'charge_max',
        'force_max',
        'size',
        'ionizedAt_count',
        # 'upgrade_count',
        # 'upgrade_offset',
        # 'simplifyForTraining'
    ]
    stat_set = set(stat_list)
    statIndex_dict = {k: i for i, k in enumerate(stat_list)}

    def __init__(self, squads_list, simplifyForTraining_bool=False):
        # Register ID in global cache
        self.const_id = str(uuid.uuid4()) # FIXME: make this something similar, but easier to read
        self.id2obj_dict[self.const_id] = self

        self.player_count = len(squads_list)
        self.pilot_count = 0
        self.upgrade_count = 0
        self.rule_count = 0
        # self.ship_list = []
        # self.pilot_list = []

        for player_id, squad_json in enumerate(squads_list):
            self.pilot_count += len(squad_json['pilots'])

        super().__init__(True, self.pilot_count)

        pilot_id: PilotId = 0
        for player_id, squad_json in enumerate(squads_list):
            for pilot_json in squad_json['pilots']:
                self._setRawStat(pilot_id, 'player_id', player_id)
                # self._setRawStat(pilot_id, 'upgrade_offset', self.upgrade_count)
                # self._setRawStat(pilot_id, 'simplifyForTraining', simplifyForTraining_bool)
                # self.upgrade_count += Pilot.initRules(self, pilot_id, self.upgrade_count, squad_json['faction'], pilot_json)

                # self.ship_list.append(pilot_json['ship'])
                # self.pilot_list.append(pilot_json['name'])

                pilot_id += 1

    def getRuleId(self):
        self.rule_count += 1
        return self.rule_count


class BoardState(RuleState):
    """
    Responsible for the state of the board as play progresses.

    Gameplay is represented as a DAG with the Nodes containing BoardState instances,
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
        'charge',
        'force',
        'cloak',

        'focus',
        'calculate',
        'evade',
        'reinforceFront',
        'reinforceRear',

        'stress',
        'ion',
        'jam',
        'weaponDisabled',
        'tractor',

    ]
    token_set = set(token_list)
    flag_list = [
        'bonusAttacked',
        'dialRevealed',
        'nextRound:weaponDisabled',
        'checkPilotStress:red',
        'checkPilotStress:blue',
        'isDestroyed',
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
        'charge',
        # 'isDiscarded',
        # 'extraMunitions',
        # 'token',
    ]
    upgrade_set = set(upgrade_list)
    upgradeIndex_dict = {k: i for i, k in enumerate(upgrade_list)}

    @property
    def const(self):
        return ConstantState.getInst(self.const_id)

    def getRuleId(self):
        return self.const.getRuleId()

    def __init__(self, const_id, perspectivePlayer_id=None, dialWeight_dict=None): #, clone=None):
        """
        BoardStateNode.__init__ is only called at the start of the game.
        All other instances are created by shallow copying the previous state,
        then applying the edge.transformImpl function.
        """
        self.const_id = const_id
        self.perspectivePlayer_id = perspectivePlayer_id
        self.dialWeight_dict = dialWeight_dict or {}
        super().__init__(True, self.const.pilot_count)

        self.fastforward_list = []
        self.maneuver_list = [None] * self.const.pilot_count
        self.opportunity_set = set()

        hull_max = 1
        pilot_id: PilotId
        for pilot_id in range(self.const.pilot_count):
            # self.getStat(pilot_id, 'hull_max')
            self._setRawStat(pilot_id, 'shield', self.getStat(pilot_id, 'shield_max'))
            self._setRawStat(pilot_id, 'charge', self.getStat(pilot_id, 'charge_max'))
            self._setRawStat(pilot_id, 'force', self.getStat(pilot_id, 'force_max'))
            # self.pilots.append(Pilot(self, pilot_id))

        self.damage_array = np.zeros((self.const.pilot_count, hull_max), np.int8)
        self.position_array = np.zeros((self.const.pilot_count, 5), np.float32)
        self.upgrade_array = np.zeros((self.const.upgrade_count, 2), np.int8)

        # self.step_list = []
        # self.step_index = 0
        # self._step_count = 0

    def clone(self):
        # other = BoardState(None, clone=self)
        # self.stat_array.flags.writeable = False
        # self.damage_array.flags.writeable = False
        # self.position_array.flags.writeable = False
        # self.upgrade_array.flags.writeable = False

        other = copy.copy(self)
        other.fastforward_list = []
        other.step_list = self.step_list[:]
        other.maneuver_list = self.maneuver_list[:]
        other.opportunity_set = set(self.opportunity_set)

        return other

    # Rules
    def getEdgeRules(self, step, active_id, target_id):
        # Here we collect rules for both global game state, as well as local
        # board state, check to make sure that those rules are active, and pass
        # them along.
        rule_list = super(BoardState, self).getEdgeRules(step, active_id, target_id)
        rule_list.extend(self.const.getEdgeRules(step, active_id, target_id))

        replaced_set = set(rule.replacesRule_cls for rule in rule_list if rule.replacesRule_cls)
        rule_list = sorted([rule for rule in rule_list if type(rule) not in replaced_set and rule.isAvailable(self)])

        return rule_list

    def getStatRules(self, stat_key):
        # Here we collect rules for both global game state, as well as local
        # board state, check to make sure that those rules are active, and pass
        # them along.
        rule_list = super(BoardState, self).getStatRules(stat_key)
        rule_list.extend(self.const.getStatRules(stat_key))

        replaced_set = set(rule.replacesRule_cls for rule in rule_list if rule.replacesRule_cls)
        rule_list = sorted([rule for rule in rule_list if type(rule) not in replaced_set])
        rule_list = sorted([rule for rule in rule_list if rule.isAvailable(self)])

        return rule_list

    # Stats
    def getStat(self, pilot_id, stat_key):
        try:
            return super(BoardState, self).getStat(pilot_id, stat_key)
        except KeyError:
            pass

        try:
            return self.const.getStat(pilot_id, stat_key)
        except KeyError:
            pass

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


        return 0

    def _setRawStat(self, pilot_id, stat_key, value):
        self.stat_array = np.copy(self.stat_array)

        return super(BoardState, self)._setRawStat(pilot_id, stat_key, value)

    def getStat_damage(self, pilot_id):
        hull_max = int(self.getStat(pilot_id, 'hull_max'))
        shield_max = int(self.getStat(pilot_id, 'shield_max'))
        shield = int(self._getRawStat(pilot_id, 'shield'))
        damage = int(np.sum(self.damage_array[pilot_id] != 0) + np.sum(self.damage_array[pilot_id] == 2))
        points = int(self.const._getRawStat(pilot_id, 'points'))
        isLarge = bool(self.const._getRawStat(pilot_id, 'isLarge'))

        hull = hull_max - damage
        totalHp = hull_max + shield_max
        currentHp = shield + hull

        return totalHp, currentHp, hull, points, isLarge


    # Edges
    def getOutgoingEdges(self, fastforward_bool=True):
        edge_list = []
        activePlayer_id = None

        # while True:
        for _ in range(100):
            # # Make sure we're using the correct step
            if self.step_index != 0:
                self.step_index = 0


            step_str, _count, active_id, target_id = self._step


            edge_list = self._getEdges(step_str, active_id, target_id)

            if edge_list:
                # Restrict to player with the best init
                activePilot_id = min(edge.active_id for edge in edge_list)
                activePlayer_id = self.getStat(activePilot_id, 'player_id')

                edge_list = [edge for edge in edge_list if self.getStat(edge.active_id, 'player_id') == activePlayer_id]

                # Provide option to pass
                if edge_list and not any(edge.isMandatory(self) for edge in edge_list):

                    passOpportunity_key = Rule.getPassOpportunityKey(self, activePlayer_id)
                    edge_list.append(ChoosePassEdge(activePilot_id, [passOpportunity_key]))

            if fastforward_bool:
                # Next/Fastforward if nothing interesting to choose from
                if not edge_list:
                    self.nextStep()

                elif len(edge_list) == 1 and not isinstance(edge_list[0], RandomEdge):
                    only_edge = edge_list.pop()
                    self.fastforward_list.append(only_edge)
                    # log.info("Fastforward {}: {}".format(fastforward_bool, only_edge))
                    only_edge.getExactState(self, doCopy=False)

                else:
                    break
            else:
                break


        edge_list.sort()
        return edge_list, activePlayer_id


    # Tokens, a special kind of stat
    def getToken(self, pilot_id, token_str):
        assert token_str in self.token_set
        return self.getStat(pilot_id, token_str)

    def assignToken(self, pilot_id, token_str):
        assert token_str in self.token_set
        token_count = self.getStat(pilot_id, token_str)
        if token_count < 99:
            self._setRawStat(pilot_id, token_str, token_count + 1)
        self.pushSteps(['assign_{}'.format(token_str)], active_id=pilot_id)

    def removeToken(self, pilot_id, token_str):
        assert token_str in self.token_set
        token_count = self.getStat(pilot_id, token_str)
        assert token_count > 0

        self._setRawStat(pilot_id, token_str, token_count - 1)
        self.pushSteps(['remove_{}'.format(token_str)], active_id=pilot_id)

    def clearToken(self, pilot_id, token_str):
        assert token_str in self.token_set
        token_count = self.getStat(pilot_id, token_str)
        if token_count > 0:
            self._setRawStat(pilot_id, token_str, 0)
            self.pushSteps(['clear_{}'.format(token_str)], active_id=pilot_id)

    # Flags, a special kind of stat
    def getFlag(self, pilot_id, flag_str):
        assert flag_str in self.flag_set
        return bool(self.getStat(pilot_id, flag_str))

    def setFlag(self, pilot_id, flag_str):
        assert flag_str in self.flag_set
        self._setRawStat(pilot_id, flag_str, 1)
        self.pushSteps(['flag_{}'.format(flag_str)], active_id=pilot_id)

    def unsetFlag(self, pilot_id, flag_str):
        assert flag_str in self.flag_set
        self._setRawStat(pilot_id, flag_str, 0)
        self.pushSteps(['unflag_{}'.format(flag_str)], active_id=pilot_id)

    # FIXME: add acquire/spend/discard target lock functions

    def dealDamage(self, pilot_id, faceup):
        self.damage_array = np.copy(self.damage_array)

        for i in range(self.damage_array.shape[1]):
            if self.damage_array[pilot_id, i] == 0:
                # FIXME: make this a random card draw?
                self.damage_array[pilot_id, i] = 1

                if not faceup:
                    self.damage_array[pilot_id, i] *= -1

                break

        if faceup:
            self.pushSteps(['dealtCrit'], active_id=pilot_id)
        else:
            self.pushSteps(['dealtHit'], active_id=pilot_id)

    # Stepper stuff
    def nextRound(self, **kwargs):
        from droidblue.core.steps import steps_round
        self.step_list = []
        self.step_index = 0
        self.pushSteps(steps_round(**kwargs))

    def pushSteps(self, new_list, active_id=None, target_id=None):
        self._step_count += 1
        tup_list = [StepTuple(s, self._step_count, active_id, target_id) for s in new_list]
        self.step_list[self.step_index:self.step_index] = tup_list
        self.step_index += len(tup_list)


    def nextStep(self):
        if self.step_index != 0:
            self.step_index = 0
        else:
            try:
                self.step_list.pop(0)
            except IndexError:
                pass

    @property
    def _step(self):
        try:
            return self.step_list[self.step_index]
        except IndexError:
            return StepTuple(None, None, None, None)

    @property
    def step(self):
        return self._step.step

    @property
    def step_count(self):
        return self._step.count

    @property
    def active_id(self):
        return self._step.active_id

    @property
    def active_pilot(self):
        return Pilot(self, self.active_id)


    @property
    def target_id(self):
        return self._step.target_id

    @property
    def target_pilot(self):
        return Pilot(self, self.target_id)

    @property
    def pilots(self):
        return [Pilot(self, pilot_id) for pilot_id in range(self.const.pilot_count)]

    # @property
    # def attackDice_pool(self):
    #     return StateBackedAttackDicePool(self, self.active_id)
    #
    # @property
    # def defenseDice_pool(self):
    #     return StateBackedDefenseDicePool(self, self.target_id)


    def useOpportunity(self, opportunity_list):
        self.opportunity_set.update(opportunity_list)

    def hasOpportunityBeenUsed(self, opportunity_key):
        return opportunity_key in self.opportunity_set

    def getStepOpportunityKeys(self):
        return {
            'step': self.step,
            'count': self.step_list[self.step_index][1],
        }

    def endOfRoundCleanup(self):
        prevStat_array = copy.deepcopy(self.stat_array)

        for stat_key in self.flag_list:
            if stat_key in self.statIndex_dict:
                self.stat_array[:, self.statIndex_dict[stat_key]] = 0

        self.stat_array[:, self.statIndex_dict['weaponsDisabled']] = prevStat_array[:, self.statIndex_dict['nextRound:weaponsDisabled']]
        self.stat_array[:, self.statIndex_dict['isDestroyed']] = prevStat_array[:, self.statIndex_dict['isDestroyed']]

        self.maneuver_list = [None] * self.const.pilot_count

    def toJson(self):
        j = {'players': [{} for _ in range(self.const.player_count)]}
        for pilot in self.pilots:
            player_dict = j['players'][self.const._getRawStat(pilot.pilot_id, 'player_id')]
            player_dict.setdefault('pilots', []).append(pilot.toJson(self))

        return j

