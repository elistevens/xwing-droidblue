
# stdlib
import collections
import gc
import random
import sys


# 3rd party packages
import numpy

# in-house

from droidblue.core.state import BoardState
from droidblue.testing.fixtures import chase_state


# Recursively expand slist's objects
# into olist, using seen to track
# already processed objects.
def _getr(slist, olist, seen):
    for e in slist:
        if id(e) in seen:
            continue
        seen[id(e)] = None
        olist.append(e)
        tl = gc.get_referents(e)
        tl = [x for x in tl if not isinstance(x, type) or x != type(e)]
        if tl:
            _getr(tl, olist, seen)

# The public function.
def get_downstream_objects(obj):
    """Return a list of all live Python
    objects, not including the list itself."""
    # gcl = gc.get_objects()
    olist = []
    seen = {}
    # Just in case:
    # seen[id(gcl)] = None
    seen[id(olist)] = None
    seen[id(seen)] = None
    # _getr does the real work.
    _getr([obj], olist, seen)
    return olist


# The public function.
def get_all_objects():
    """Return a list of all live Python
    objects, not including the list itself."""
    gcl = gc.get_objects()
    olist = []
    seen = {}
    # Just in case:
    seen[id(gcl)] = None
    seen[id(olist)] = None
    seen[id(seen)] = None
    # _getr does the real work.
    _getr(gcl, olist, seen)
    return olist

def memoryUsageDump(obj_list, topn=50):
    count_dict = collections.defaultdict(int)
    used_dict  = collections.defaultdict(int)
    array_list = []
    for obj in obj_list:
        count_dict[type(obj)] += 1
        size = sys.getsizeof(obj) + (obj.nbytes if hasattr(obj, 'nbytes') and isinstance(obj.nbytes, int) else 0)
        used_dict[type(obj)] += size

        if type(obj) == numpy.ndarray:
            array_list.append((size, obj.shape, obj.dtype, obj))

    print "used\tcount\ttype"
    for u, c, t in sorted((used_dict[t], count_dict[t], t) for t in count_dict)[-topn:]:
        s = str(t)
        # if c > 100 or (('mms.dicom.apirelationships_gen.TemplatedDataset' not in s) and ('OpenGL.' not in s) and ('XXXctypes.' not in s) and ('nose.' not in s)):
        print "{}\t{}\t{}".format(u, c, t)
    #del count_dict
    #del used_dict

    # gc.collect()
    #
    # array_list.sort(key=lambda x: x[:2])
    # for x in array_list[-10:]:
    #
    #     print x[:3], len(gc.get_referrers(x[3])), [[type(z) for z in gc.get_referrers(y)] for y in gc.get_referrers(x[3])]


# eof


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

        count_dict = {}
        used_dict  = {}
        array_list = []

        obj_list = get_downstream_objects(self.state)

        memoryUsageDump(obj_list)

        for obj in obj_list:
            if isinstance(obj, dict):
                print id(obj), sys.getsizeof(obj)
                for key in obj.keys():
                    print '   ', key

        print '=' * 50

        for i in range(5):
            try:
                self.state.getOutgoingEdges()
            except IndexError:
                print "Done, but just fastforwarded:"
                for ff_edge in self.state.fastforward_list:
                    print "FF: ", ff_edge
                break

            for ff_edge in self.state.fastforward_list:
                print "FF: ", ff_edge

            # print self.state.edge_list

            random_edge = random.choice(self.state.edge_list)
            print "Rnd:", random_edge, len(self.state.edge_list)

            self.state = random_edge.getExactState(self.state)

        obj_list = get_downstream_objects(self.state)

        memoryUsageDump(obj_list)

        for obj in obj_list:
            if isinstance(obj, dict):
                print id(obj), sys.getsizeof(obj)
                for key in obj.keys():
                    print '   ', key



        # for x in gc.get_referents(self.state):
        #     print x

        # score, edge_list = findBestScore_minmax(self.state, MovAndHpDeltaScore)
        # # score, edge_list = findBestScore_alphabeta(self.state, MovAndHpDeltaScore)
        #
        # print score.individual_list
        # for edge in edge_list:
        #     print edge
        #
        # # print json.dumps(self.state.toJson(), indent=4, sort_keys=True)
        #
        # print droidblue.alphabeta.totalStates_count


def main(sys_argv=None):
    SearchPlay().main(sys_argv)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
