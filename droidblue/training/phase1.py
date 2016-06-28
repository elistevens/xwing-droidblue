import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

import datetime
import errno
import math
import os
import cPickle as pickle
import sys


import numpy as np

from droidblue.core.pilot import Pilot
from droidblue.core.score import MovAndHpDeltaScore
from droidblue.core.state import BoardState, ConstantState
from droidblue.search.minmax import findBestScore_minmax
from droidblue.testing import squads as squads
from droidblue.search.visit import visitAllLeaves


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

class Phase1(object):
    def __init__(self):
        pass

    def main(self, sys_argv):
        assert len(sys_argv) == 2

        pilot0_str = sys_argv[0]
        pilot1_str = sys_argv[1]

        squads_list = [getattr(squads, cli_arg) for cli_arg in sys_argv]
        const = ConstantState(squads_list)
        state = BoardState(const.const_id)

        heading_list = range(-270, 451, 30)
        heading_list = [270]

        pos_list = []
        pos_list.extend(range(-1000, 1001, 100))
        pos_list.extend(range(-550, 551, 100))

        xpos_list = ypos_list = pos_list

        xpos_list = [200]
        ypos_list = [100]

        data_dict = {}
        existing_set = set()
        date_str = datetime.datetime.now().strftime('%Y-%m-%dT%H.%M.%S')

        try:
            self.train(state.clone(), pilot0_str, pilot1_str, xpos_list, ypos_list, heading_list, data_dict, existing_set)
        finally:
            mkdir_p('data/phase1/a/{}/{}/'.format(pilot0_str, pilot1_str))
            with open('data/phase1/a/{}/{}/{}.data.pkl'.format(pilot0_str, pilot1_str, date_str), 'w') as f:
                pickle.dump(data_dict, f, pickle.HIGHEST_PROTOCOL)
            with open('data/phase1/a/{}/{}/{}.keys.pkl'.format(pilot0_str, pilot1_str, date_str), 'w') as f:
                pickle.dump(set(data_dict), f, pickle.HIGHEST_PROTOCOL)

    def train(self, state, pilot0_str, pilot1_str, xpos_list, ypos_list, heading_list, data_dict, existing_set):
        move2scores_dict = {0: {}, 1: {}}
        def leafCallback_recordMoveScore(state, weight):
            pilot = Pilot(state, 0)
            score = pilot.phase1_toNeuralNetOutput()

            for i in range(2):
                move2scores_dict[i].setdefault(state.maneuver_list[i], [[], []])
                move2scores_dict[i][state.maneuver_list[i]][0].append(score)
                move2scores_dict[i][state.maneuver_list[i]][1].append(weight)

        pilot = Pilot(state, 0)
        pilot._resetPosition()
        pilot = Pilot(state, 1)
        pilot._resetPosition()

        state.perspectivePlayer_id = 0


        for x in xpos_list:
            for y in ypos_list:
                existing_key = (pilot0_str, pilot1_str, int(x), int(y))
                if existing_key in existing_set:
                    continue

                input_list = []
                output_list = []

                for heading in heading_list:
                    heading_radians = math.radians(heading)

                    log.info("h: {}, x: {}, y: {}".format(heading, x, y))

                    for stress_index in range(4):
                        state.clearToken(0, 'stress')
                        if stress_index % 2:
                            state.assignToken(0, 'stress')
                        state.clearToken(1, 'stress')
                        if stress_index >= 2:
                            state.assignToken(1, 'stress')
                        state.nextRound(dials=False, activation=True, combat=False, endphase=False)

                        pilot = Pilot(state, 1)
                        pilot.x = x
                        pilot.y = y
                        pilot.heading_radians = heading_radians

                        for j in range(4):
                            # if j:
                            #     print '====', j, datetime.datetime.now()
                            visitAllLeaves(leafCallback_recordMoveScore, state.clone())
                            state.dialWeight_dict = {}
                            for i in range(2):
                                # if i:
                                #     print '----'
                                move2avg_dict = {k: (np.average(v, weights=w), np.std(v), len(v)) for k,(v,w) in move2scores_dict[i].iteritems()}
                                move2scores_dict[i].clear()

                                score_max = max(v[0] for v in move2avg_dict.values())
                                score_min = min(min(v[0] for v in move2avg_dict.values()), 0.0)

                                for k, v in sorted(move2avg_dict.iteritems(), key=lambda (k,v): v[0]):
                                    state.dialWeight_dict[(i, k[0])] = ((v[0] - score_min + 0.1) / (score_max - score_min + 0.1001)) ** 2
                                    # print i, k, '\t', v, '\t', state.dialWeight_dict[(i, k[0])]

                        tmp_list = [Pilot(state, i).phase1_toNeuralNetInput() for i in range(2)]
                        input_array = np.array(tmp_list, dtype=np.float32)
                        input_list.append(input_array)

                        tmp_list = [state.dialWeight_dict.get(k, 0.0) for k in sorted(Pilot._maneuverOffsets_xyr[0])]
                        output_array = np.array(tmp_list, dtype=np.float32)
                        output_list.append(output_array)

                data_dict[existing_key] = (input_list, output_list)




def main(sys_argv=None):
    Phase1().main(sys_argv)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
