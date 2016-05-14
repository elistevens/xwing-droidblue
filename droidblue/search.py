
import random
import sys

import droidblue.alphabeta

from droidblue.core.state import BoardState
from droidblue.testing.fixtures import chase_state
from droidblue.alphabeta import findBestScore_minmax, findBestScore_alphabeta
from droidblue.core.score import MovAndHpDeltaScore

class Search(object):
    def __init__(self, score_cls, squads_list, slop_list):
        self.root_state = BoardState(squads_list)
        self.slop_list = slop_list
        self.score_cls = score_cls

class SearchPlay(object):
    def __init__(self):
        self.root_state = chase_state()
        # self.slop_list = slop_list
        # self.score_cls = score_cls

    def main(self, sys_argv):
        self.state = self.root_state
        self.state.nextRound()

        score, edge_list = findBestScore_minmax(self.state, MovAndHpDeltaScore)
        # score, edge_list = findBestScore_alphabeta(self.state, MovAndHpDeltaScore)

        print score.individual_list
        for edge in edge_list:
            print edge

        # print json.dumps(self.state.toJson(), indent=4, sort_keys=True)

        print droidblue.alphabeta.totalStates_count


def main(sys_argv=None):
    SearchPlay().main(sys_argv)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
