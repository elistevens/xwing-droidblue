
import random
import sys

try:
    import simplejson as json
except ImportError:
    import json


from droidblue.core.state import BoardState
from droidblue.testing.fixtures import chase_state

class Game(object):
    def __init__(self, score_cls, squads_list, slop_list):
        self.root_state = BoardState(squads_list)
        self.slop_list = slop_list
        self.score_cls = score_cls

class RandomPlay(object):
    def __init__(self):
        self.root_state = chase_state()
        # self.slop_list = slop_list
        # self.score_cls = score_cls

    def main(self, sys_argv):
        self.state = self.root_state
        self.state.nextRound()

        for i in range(50):
            try:
                self.state.getEdges()
            except IndexError:
                print "Done, but just fastforwarded:"
                break
            finally:
                for ff_edge in self.state.fastforward_list:
                    print "    FF: ", ff_edge

            if not self.state.edge_list:
                break

            # for ff_edge in self.state.fastforward_list:
            #     print "FF: ", ff_edge

            # print self.state.edge_list

            random_edge = random.choice(self.state.edge_list)
            print "    Rnd:", random_edge, len(self.state.edge_list)

            self.state = random_edge.getExactState(self.state)

        print json.dumps(self.state.toJson(), indent=4, sort_keys=True)


def main(sys_argv=None):
    RandomPlay().main(sys_argv)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
