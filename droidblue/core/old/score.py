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
    def averageScores(cls, scoreWeight_list):
        individual_list = [0] * len(scoreWeight_list[0][0].individual_list)
        total_weight = 0.0
        for score, weight in scoreWeight_list:
            total_weight += weight

            for i, subscore_num in enumerate(score.individual_list):
                individual_list[i] += subscore_num * weight

        individual_list = [s / total_weight for s in individual_list]

        return cls(None, _individual_list=individual_list)


    def __init__(self, state, _individual_list=None, _lossFor=None):
        self._lossFor = _lossFor

        if state:
            self.individual_list = [self.computeIndividualScore(state, player_id) for player_id in range(state.const.player_count)]
        else:
            assert _individual_list, repr(_individual_list)
            self.individual_list = list(_individual_list)


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
    """
    It computes Margin of Victory as per the tournament rules.

    This score is suitable for use in evaluating a state at the end of the
    round or end of the game.
    """
    def computeIndividualScore(self, state, player_id):
        pointsLost_int = 0
        hasUndestroyedPilots_bool = False

        for pilot_id in range(state.const.pilot_count):
            if state.getStat(pilot_id, 'player_id') == player_id:
                totalHp, currentHp, hull, points, isLarge = state.getStat_damage(pilot_id)

                hp_frac = currentHp / totalHp

                if hull == 0:
                    pointsLost_int += points
                elif isLarge and hp_frac <= 0.5:
                    pointsLost_int += int(points / 2)
                    hasUndestroyedPilots_bool = True
                else:
                    hasUndestroyedPilots_bool = True

        return (100 - pointsLost_int) if hasUndestroyedPilots_bool else 0

class MovAndHpDeltaScore(Score):
    """
    It computes MoV plus fractional points per hitpoint, rounded to int on
    a per-ship basis. This makes the range of points be 0 to 200.

    This score is suitable for use in evaluating a state at the end of the
    round. It is probably the best method to use mid-game.
    """
    def computeIndividualScore(self, state, player_id):
        # This copies the above for speed reasons; reuse would result in
        # state.getStat_damage being called twice.
        pointsLost_int = 0
        hasUndestroyedPilots_bool = False

        for pilot_id in range(state.const.pilot_count):
            if state.getStat(pilot_id, 'player_id') == player_id:
                totalHp, currentHp, hull, points, isLarge = state.getStat_damage(pilot_id)

                hp_frac = currentHp / totalHp

                if hull == 0:
                    pointsLost_int += points
                elif isLarge and hp_frac <= 0.5:
                    pointsLost_int += int(points / 2)
                    hasUndestroyedPilots_bool = True
                else:
                    hasUndestroyedPilots_bool = True

                pointsLost_int += int(points * hp_frac)

        return (200 - pointsLost_int) if hasUndestroyedPilots_bool else 0

class TournamentMovDeltaScore(MovDeltaScore):
    """
    It computes Margin of Victory as per the tournament rules, plus 1000 times
    tournament points. This means that from a tie, the expected value of a 50%
    chance of a 12-point MoV gain will be higher than a 90% chance of an 11
    point MoV gain.

    This score is suitable for use in evaluating a state at the end of the
    game.
    """
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
