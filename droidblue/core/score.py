from __future__ import division
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

__author__ = 'elis'

import re

class Score(object):
    @classmethod
    def averageScores(cls, state_list, owner_id):
        individual_list = [0] * len(state_list[0][1])
        total_weight = 0.0
        for weight, score in state_list:
            total_weight += weight

            for i, subscore_num in enumerate(score.individual_list):
                individual_list[i] += subscore_num * weight

        individual_list = [s / total_weight for s in individual_list]

        return cls(None, owner_id, _individual_list=individual_list)


    def __init__(self, state, _individual_list=None, _lossFor=None):
        self._lossFor = _lossFor

        if state:
            self.individual_list = [self.computeIndividualScore(state, player_id) for player_id in range(state.const.player_count)]
        else:
            assert _individual_list
            self.individual_list = list(_individual_list)

        # self.composite_num = self.computeCompositeScore(state.playerWithInit_id)

    def __repr__(self):
        extra_str = "{}, margin {}".format(self.individual_list, [self.marginFor(p) for p in range(len(self.individual_list))])

        r = super(Score, self).__repr__()
        r = re.sub(r'\<droidblue\.([a-z]+\.)+', '<', r)
        return r.replace('>', ' {}>'.format(extra_str))


    def computeIndividualScore(self, state, player_id):
        raise NotImplementedError()

    def marginFor(self, player_id):
        # log.debug(player_id)
        if self._lossFor is not None:
            if self._lossFor == player_id:
                return -9999
            else:
                return 9999

        otherScore_list = [s for (i, s) in enumerate(self.individual_list) if i != player_id]
        other_score = max(otherScore_list)
        this_score = self.individual_list[player_id]
        return this_score - other_score


class MovDeltaScore(Score):
    def computeIndividualScore(self, state, player_id):
        pointsLost_int = 0
        hasUndestroyedPilots_bool = False
        for pilot_id, pilot in enumerate(state.pilots):
            if state.getStat(pilot_id, 'player_id') == player_id:
                if state.getStat(pilot_id, 'isDestroyed'):
                    pointsLost_int += state.getStat(pilot_id, 'points')
                elif state.getStat(pilot_id, 'grantsHalfMov'):
                    pointsLost_int += int(state.getStat(pilot_id, 'points') / 2)
                    hasUndestroyedPilots_bool = True
                else:
                    hasUndestroyedPilots_bool = True

        return (100 - pointsLost_int) if hasUndestroyedPilots_bool else 0

class MovAndHpDeltaScore(MovDeltaScore):
    def computeIndividualScore(self, state, player_id):
        mov_score = super(MovAndHpDeltaScore, self).computeIndividualScore(state, player_id)

        pointsLost_int = 0
        hasUndestroyedPilots_bool = False
        for pilot_id, pilot in enumerate(state.pilots):
            if state.getStat(pilot_id, 'player_id') == player_id:
                if state.getStat(pilot_id, 'isDestroyed'):
                    pointsLost_int += state.getStat(pilot_id, 'points')
                else:
                    pointsLost_int += int(state.getStat(pilot_id, 'points') * (state.getStat(pilot_id, 'currentHp') / state.getStat(pilot_id, 'totalHp')))
                    hasUndestroyedPilots_bool = True

        return mov_score + (100 - pointsLost_int) if hasUndestroyedPilots_bool else 0

class TournamentMovDeltaScore(MovDeltaScore):
    def marginFor(self, player_id):
        delta_score = super(TournamentMovDeltaScore, self).marginFor(player_id)

        tournament_score = 0
        if delta_score > 12:
            tournament_score = 5000
        if delta_score > 0:
            tournament_score = 3000
        if delta_score == 0:
            tournament_score = 1000

        return delta_score + tournament_score

class TournamentMovAndHpDeltaScore(TournamentMovDeltaScore, MovAndHpDeltaScore):
    pass
