import itertools
import math
import random
import time

import numpy as np

class TestingState(object):
    def __init__(self):
        self.players = [TestingPlayer(0), TestingPlayer(1)]

    def clone(self, readonly=True):
        pass

    def assignDial(self, ship_id, move):
        pass

    def semiRandomPlayout(self, ai_list):
        pass

class TestingAi(object):
    def getScore(self, state, player_id):
        pass

    def predictMoveScores(self, state):
        pass



class Round(object):
    def __init__(self, planning_state, ai_list):
        self.ai_list = ai_list
        self.planning_state = planning_state
        self.player2dialPlan_list = [DialPlan.makeList(planning_state, player.id, ai_list[player.id]) for player in planning_state.players]

        self.plays_count = 0

    def mctsPlayout(self, limit_sec=60):
        self.mctsContinue_bool = True
        start_ts = time.time()

        while self.mctsContinue_bool:
            current_state = self.planning_state.clone(readonly=False)

            for player_id, dialPlan_list in enumerate(self.player2dialPlan_list):
                dialPlan_list.sort(key=lambda d: d.sortValue(self.plays_count))

                for ship_id, move in dialPlan_list[-1].ship2move_dict:
                    current_state.assignDial(ship_id, move)

            current_state.semiRandomPlayout(self.ai_list)

            for player_id, dialPlan_list in enumerate(self.player2dialPlan_list):
                score = self.ai_list[player_id].getFinalScore(current_state, player_id)
                dialPlan_list[-1].addPlayout(score)

            if limit_sec and start_ts + limit_sec > time.time():
                self.mctsContinue_bool = False

        return self.bestScorePerMove()

    def mctsCancel(self):
        self.mctsContinue_bool = False

    def bestScorePerMove(self):
        ship2move2score_dict = {}

        for dialPlan_list in self.player2dialPlan_list:
            for dialPlan in dialPlan_list:
                if dialPlan.plays_count:
                    score = dialPlan.playScore_sum / dialPlan.plays_count

                    for ship_id, move in dialPlan.ship2move_dict:
                        best_score = ship2move2score_dict.setdefault(ship_id, {}).setdefault(move, score)

                        if score > best_score:
                            ship2move2score_dict[ship_id][move] = score

        return ship2move2score_dict



class DialPlan(object):
    @classmethod
    def makeList(cls, planning_state, player_id, ai=None, limit_int=0, randomMove_min=3, score_cutoff=0.9):
        if ai:
            ship2move2score_dict = ai.predictMoveScores(planning_state)

            for ship in planning_state.players[player_id].ships:
                score2move_list = []

                for move in ship.getValidMoves():
                    score2move_list.append((ship2move2score_dict[ship.id][move], move))

                if limit_int:
                    score2move_list.sort()
                    best_score = score2move_list[-1][0]
                    move2score_dict = {}

                    while score2move_list[-1][0] > best_score * score_cutoff:
                        score, move = score2move_list.pop()
                        move2score_dict[move] = score

                    random_int = max(randomMove_min, limit_int - len(move2score_dict))
                    random.shuffle(score2move_list)
                    for score, move in score2move_list[:random_int]:
                        move2score_dict[move] = score

                    ship2move2score_dict[ship.id] = move2score_dict
                else:
                    ship2move2score_dict[ship.id] = {m:s for s, m in score2move_list}

        else:
            ship2move2score_dict = {}

            for ship in planning_state.players[player_id].ships:
                ship2move2score_dict[ship.id] = move2score_dict = {}

                for move in ship.getValidMoves():
                    move2score_dict[move] = 0

        ship_list = []
        moveScore_list = []
        for ship_id, move2score_dict in sorted(ship2move2score_dict.items()):
            ship_list.append(ship_id)
            moveScore_list.append(list(move2score_dict.items()))

        dialPlan_list = []
        for moveScore_tup in itertools.product(moveScore_list):
            dialPlan_list.append(cls(ship_list, moveScore_tup))

        return dialPlan_list

    def __init__(self, ship_list, moveScore_tup):
        self.individualMoveScore_avg = 0
        self.playScore_sum = 0
        self.plays_count = 0

        self.ship2move_dict = {}

        for ship_id, (move, score) in zip(ship_list, moveScore_tup):
            self.individualMoveScore_avg += score / len(ship_list)

            self.ship2move_dict[ship_id] = move

    def sortValue(self, plays_total, individual_wt=10, explore_wt=200):
        # Note this is in a different order from the terms on https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
        # also adds a predicted initial value that decays with plays
        return (
            explore_wt * math.sqrt(math.log2(plays_total) / self.plays_count)
            + (self.playScore_sum) / (self.plays_count or 1)
            + (individual_wt * self.individualMoveScore_avg) / (individual_wt + self.plays_count)
        )

    def addPlayout(self, score):
        self.playScore_sum += score
        self.plays_count += 1
