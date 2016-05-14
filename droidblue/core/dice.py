from __future__ import division
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

__author__ = 'elis'

import itertools

from edge import RandomEdge

class DicePool(object):
    faces = None
    cache = None

    @classmethod
    def _rollDice(cls, count):
        if count not in cls.cache:
            if count == 0:
                cls.cache[count] = {'': 1.0}
            else:
                prob_dict = {}
                for previous_faces, prob_frac in cls._rollDice(count - 1).iteritems():
                    for f in cls.faces:
                        new_faces = cls.clean(previous_faces + f)

                        prob_dict.setdefault(new_faces, 0.0)
                        prob_dict[new_faces] += prob_frac / len(cls.faces)

                cls.cache[count] = prob_dict

        return cls.cache[count]

    @classmethod
    def clean(cls, faces):
        return ''.join(sorted(faces))

    def __init__(self, count=0, rolled_faces='', rerolled_faces=''):
        self.count = count
        # self.total = None

        self.rolled_faces = rolled_faces
        self.rerolled_faces = rerolled_faces

    def rollDice(self):
        return self._rollDice(self.count)

    # Intital roll
    def addDice(self, extra_count=1):
        self.count += extra_count

    def setRoll(self, rolled_faces):
        self.count = 0
        self.rolled_faces = rolled_faces
        # self.total = len(rolled_faces)

    # Rerolls
    def getRerollOptions(self, allowed_faces, count):
        candidate_faces = self.clean([f for f in self.rolled_faces if f in allowed_faces])

        choice_set = set()
        for i in range(count+1):
            for removed_faces in set(itertools.combinations(candidate_faces, i)):
                removed_faces = self.clean(removed_faces)
                choice_set.add(removed_faces)

        return choice_set

    def flagForReroll(self, faces, count=1):
        for face in faces:
            tmp_faces = self.rolled_faces.replace(face, '', count)
            self.count += len(self.rolled_faces) - len(tmp_faces)
            self.rolled_faces = tmp_faces

    def setReroll(self, rerolled_faces):
        self.count = 0
        self.rerolled_faces = rerolled_faces

    # Modify
    def modifyFaces(self, from_face, to_face, max_count, lockRerolls=False):
        mod_count = 0

        if lockRerolls:
            while from_face in self.rolled_faces and mod_count < max_count:
                self.rolled_faces = self.rolled_faces.replace(from_face, '', 1)
                self.rerolled_faces = self.clean(self.rerolled_faces + to_face)
                mod_count += 1

        while from_face in self.rerolled_faces and mod_count < max_count:
            self.rerolled_faces = self.rerolled_faces.replace(from_face, to_face, 1)
            mod_count += 1

        while from_face in self.rolled_faces and mod_count < max_count:
            self.rolled_faces = self.rolled_faces.replace(from_face, to_face, 1)
            mod_count += 1

        return mod_count

    def addResults(self, faces):
        self.rerolled_faces = self.clean(self.rerolled_faces + faces)


    def getResults(self):
        return self.clean(self.rolled_faces + self.rerolled_faces)



class AttackDicePool(DicePool):
    faces = 'CHHHffxx'
    cache = {}

class DefenseDicePool(DicePool):
    faces = 'EEEffxxx'
    cache = {}

class StateBackedDicePool(DicePool):
    def __init__(self, state, pilot_id):
        # We don't call super init here, because these objects are transient.
        # It's important that super init only does things equivalent to zeroing out
        self.state = state
        self.pilot_id = pilot_id

    def reset(self):
        self.state._setRawStat(self.pilot_id, 'dice_count', 0)
        for face in sorted(set(self.faces)):
            self.state._setRawStat(self.pilot_id, 'rolled_' + face, 0)
            self.state._setRawStat(self.pilot_id, 'rerolled_' + face, 0)

    @property
    def count(self):
        return self.state._getRawStat(self.pilot_id, 'dice_count')
    @count.setter
    def count(self, value):
        self.state._setRawStat(self.pilot_id, 'dice_count', value)

    @property
    def rolled_faces(self):
        face_str = ''
        for face in sorted(set(self.faces)):
            face_str += face * self.state._getRawStat(self.pilot_id, 'rolled_' + face)

        return face_str

    @rolled_faces.setter
    def rolled_faces(self, value):
        face_dict = {}
        for face in sorted(set(self.faces)):
            face_dict[face] = 0
            self.state._setRawStat(self.pilot_id, 'rolled_' + face, 0)

        for face in value:
            face_dict[face] += 1
            self.state._setRawStat(self.pilot_id, 'rolled_' + face, face_dict[face])

    @property
    def rerolled_faces(self):
        face_str = ''
        for face in sorted(set(self.faces)):
            face_str += face * self.state._getRawStat(self.pilot_id, 'rerolled_' + face)

        return face_str

    @rerolled_faces.setter
    def rerolled_faces(self, value):
        face_dict = {}
        for face in sorted(set(self.faces)):
            face_dict[face] = 0
            self.state._setRawStat(self.pilot_id, 'rerolled_' + face, 0)

        for face in value:
            face_dict[face] += 1
            self.state._setRawStat(self.pilot_id, 'rerolled_' + face, face_dict[face])


class StateBackedAttackDicePool(StateBackedDicePool):
    faces = 'CHHHffxx'
    cache = {}

class StateBackedDefenseDicePool(StateBackedDicePool):
    faces = 'EEEffxxx'
    cache = {}


