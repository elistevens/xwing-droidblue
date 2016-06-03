from droidblue.core.pilot import Pilot

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
from droidblue.core.rules import Rule, default_ruleKey
from droidblue.core.dice import StateBackedAttackDicePool, StateBackedDefenseDicePool

StepTuple = collections.namedtuple('StepTuple', ['step', 'count', 'active_id', 'target_id'])

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

    def __eq__(self, other):
        if type(self) != type(other):
            log.debug("type({}) != type({})".format(type(self), type(other)))
            return False

        if self.__dict__.keys() != other.__dict__.keys():
            log.debug("keys({}) != keys({})".format(self.__dict__.keys(), other.__dict__.keys()))
            return False

        for k,v in self.__dict__.iteritems():
            o = other.__dict__[k]
            if type(v) != type(o):
                log.debug("{}: type({}) != type({})".format(k, type(v), type(o)))
                return False

            if isinstance(v, np.ndarray):
                if not (v == o).all():
                    log.debug(v)
                    log.debug(o)
                    return False
            else:
                if v != o:
                    log.debug("{}: {} != {}".format(k, v, o))
                    return False

        return True


    # Rules
    def addEdgeRule(self, rule, step, active_id, target_id):
        rule_sublist = self.edgeRules_dict.setdefault(step, [[], {}, {}])

        if active_id is not None:
            assert target_id is None
            rule_sublist[1].setdefault(active_id, []).append(rule)
        elif target_id is not None:
            assert active_id is None
            rule_sublist[2].setdefault(target_id, []).append(rule)
        else:
            rule_sublist[0].append(rule)

    def getEdgeRules(self, step, active_id, target_id):
        # Returns all rules, but subclasses are free to filter first
        rule_list = []
        for step_str in [Rule.wildcard_key, step]:
            rule_sublist = self.edgeRules_dict.get(step_str, [[], {}, {}])
            rule_list.extend(rule_sublist[0])

            if active_id is not None:
                rule_list.extend(rule_sublist[1].get(active_id, []))

            if target_id is not None:
                rule_list.extend(rule_sublist[2].get(target_id, []))

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
    def getStat(self, pilot_id, stat_key):
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
    def _getEdges(self, step, active_id, target_id):
        rule_list = self.getEdgeRules(step, active_id, target_id)
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
        'unique',
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
        self.rule_count = 0
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

    def getRuleId(self):
        self.rule_count += 1
        return self.rule_count


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
        super(BoardState, self).__init__(self.const.pilot_count)

        self.fastforward_list = []
        self.maneuver_list = [None] * self.const.pilot_count
        self.opportunity_set = set()

        hull_max = 1
        for pilot_id in range(self.const.pilot_count):
            hull_max = max(hull_max, self.getStat(pilot_id, 'hull_max'))
            self._setRawStat(pilot_id, 'shield', self.getStat(pilot_id, 'shield_max'))
            # self.pilots.append(Pilot(self, pilot_id))

        self.damage_array = np.zeros((self.const.pilot_count, hull_max), np.int8)
        self.position_array = np.zeros((self.const.pilot_count, 5), np.float32)
        self.upgrade_array = np.zeros((self.const.upgrade_count, 2), np.int8)

        self.step_list = []
        self.step_index = 0
        self._step_count = 0

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
        rule_list = sorted([rule for rule in rule_list if type(rule) not in replaced_set])
        rule_list = sorted([rule for rule in rule_list if rule.isAvailable(self)])

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
    def getEdges(self, fastforward_bool=True):
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
                if edge_list and not any(edge.mandatory_bool for edge in edge_list):

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

    @property
    def attackDice_pool(self):
        return StateBackedAttackDicePool(self, self.active_id)

    @property
    def defenseDice_pool(self):
        return StateBackedDefenseDicePool(self, self.target_id)


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

