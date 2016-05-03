from __future__ import division

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

    def __init__(self, state, owner_id, _individual_list=None):
        self.owner_id = owner_id

        if state:
            self.individual_list = [self.computeIndividualScore(state, player_id) for player_id in range(state.player_count)]
        else:
            assert _individual_list
            self.individual_list = _individual_list

        self.composite_num = self.computeCompositeScore()

    def computeIndividualScore(self, state, player_id):
        raise NotImplementedError()

    def computeCompositeScore(self):
        otherScore_list = [s for (i, s) in enumerate(self.individual_list) if i != self.owner_id]
        other_score = max(otherScore_list)
        this_score = self.individual_list[self.owner_id]
        return this_score - other_score


class MovDeltaScore(Score):
    def computeIndividualScore(self, state, player_id):
        pointsLost_int = 0
        hasUndestroyedShips_bool = False
        for pilot_id, ship in enumerate(state.ships):
            if ship.owner_id == player_id:
                if state._getStat('isDestroyed', pilot_id):
                    pointsLost_int += ship.points
                elif ship.givesHalfMov():
                    pointsLost_int += int(ship.points / 2)
                    hasUndestroyedShips_bool = True
                else:
                    hasUndestroyedShips_bool = True

        return 100 - pointsLost_int if hasUndestroyedShips_bool else 0

class MovAndHpDeltaScore(MovDeltaScore):
    def computeIndividualScore(self, state, player_id):
        mov_score = super(TournamentMovAndHpDeltaScore, self).computeIndividualScore(state, player_id)

        pointsLost_int = 0
        hasUndestroyedShips_bool = False
        for pilot_id, ship in enumerate(state.ships):
            if ship.owner_id == player_id:
                if state._getStat('isDestroyed', pilot_id):
                    pointsLost_int += ship.points
                else:
                    pointsLost_int += int(ship.points * (state._getStat('totalHp', pilot_id) / state._getStat('currentHp', pilot_id)))
                    hasUndestroyedShips_bool = True

        return mov_score + 100 - pointsLost_int if hasUndestroyedShips_bool else 0

class TournamentMovDeltaScore(MovDeltaScore):
    def computeCompositeScore(self):
        delta_score = super(MovDeltaScore, self).computeCompositeScore()

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
