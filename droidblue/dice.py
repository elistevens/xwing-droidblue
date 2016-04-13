__author__ = 'elis'

import copy
import itertools
import weakref

from edge import RandomEdge

class DicePool(object):
    faces = None
    cache = None

    @classmethod
    def roll(cls, count):
        if count not in cls.cache:
            if count == 0:
                cls.cache[count] = {'': 1.0}
            else:
                prob_dict = {}
                for previous_faces, prob_frac in cls.roll(count - 1).iteritems():
                    for f in cls.faces:
                        new_faces = cls.clean(previous_faces + f)

                        prob_dict.setdefault(new_faces, 0.0)
                        prob_dict[new_faces] += prob_frac / len(cls.faces)

                cls.cache[count] = prob_dict

        return cls.cache[count]

    @classmethod
    def clean(cls, faces):
        return ''.join(sorted(faces))

    def __init__(self, count=0, rolled_faces=None, removed_faces=None, rerolled_faces=None):
        self.count = count

        self.rolled_faces = rolled_faces
        self.removed_faces = removed_faces
        self.rerolled_faces = rerolled_faces

    def getRerollPools(self, allowed_faces, count):
        candidate_faces = self.clean([f for f in self.rolled_faces if f in allowed_faces])

        choice_dict = {}
        for i in range(count+1):
            for removed_faces in set(itertools.combinations(candidate_faces, i)):
                removed_faces = self.clean(removed_faces)
                if removed_faces in choice_dict:
                    continue

                rolled_faces = self.rolled_faces
                for removed_face in removed_faces:
                    rolled_faces = rolled_faces.replace(removed_face, '', 1)

                cls_inst = type(self)(i, rolled_faces=rolled_faces, removed_faces=removed_faces, rerolled_faces=self.rerolled_faces)
                choice_dict[removed_faces] = cls_inst

        return choice_dict


    def getRollBranches(self, state):
        branches = BranchChoices()

        # random_list = []
        for faces, prob_frac in self.roll(self.count).iteritems():

            if self.rolled_faces is None:
                rolled_faces = faces
                rerolled_faces = None
            else:
                rolled_faces = self.rolled_faces
                rerolled_faces = self.clean((self.rerolled_faces or '') + faces)

            cls_inst = type(self)(rolled_faces=rolled_faces, removed_faces=self.removed_faces, rerolled_faces=rerolled_faces)

            branches.addBranch(prob_frac, state)
            # random_list.append((prob_frac, cls_inst))

        return branches

    def modifyFaces(self, from_face, to_face, max_count):
        mod_count = 0
        while from_face in self.rerolled_faces and mod_count < max_count:
            self.rerolled_faces = self.rerolled_faces.replace(from_face, to_face, 1)
            mod_count += 1

        while from_face in self.rolled_faces and mod_count < max_count:
            self.rolled_faces = self.rolled_faces.replace(from_face, to_face, 1)
            mod_count += 1

        return mod_count



class AttackDicePool(DicePool):
    faces = 'CHHHffxx'
    cache = {}

class DefenseDicePool(DicePool):
    faces = 'EEEffxxx'
    cache = {}





