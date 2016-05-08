# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

from droidblue.testing.fixtures import *

import random
import numpy as np

def test_ranges1(vs_state):
    vs_state.pilots[0]._resetPosition()
    vs_state.pilots[1]._resetPosition()

    log.info(vs_state.pilots[0].x)
    log.info(vs_state.pilots[0].y)
    log.info(vs_state.pilots[0].heading_degrees)

    vs_state.pilots[1].slide(170, 0)

    dist_list = vs_state.pilots[0].getArcDistances(vs_state.pilots[1])
    range_list = vs_state.pilots[0].getArcRanges(vs_state.pilots[1])

    assert np.allclose(dist_list, [130.0, 130.0, 3000, 130.0])
    assert range_list == [2, 2, 4, 2]

    dist_list = vs_state.pilots[1].getArcDistances(vs_state.pilots[0])
    range_list = vs_state.pilots[1].getArcRanges(vs_state.pilots[0])

    assert np.allclose(dist_list, [3000, 3000, 130.0, 130.0])
    assert range_list == [4, 4, 2, 2]

    vs_state.pilots[1].slide(-170, 50)

    dist_list = vs_state.pilots[0].getArcDistances(vs_state.pilots[1])
    range_list = vs_state.pilots[0].getArcRanges(vs_state.pilots[1])

    assert np.allclose(dist_list, [3000, 10.0, 3000, 10.0])
    assert range_list == [4, 1, 4, 1]


def test_ranges_random(chase_state):
    for i in range(1000):
        chase_state.pilots[0]._resetPosition()
        chase_state.pilots[1]._resetPosition()

        chase_state.pilots[0].slide(200 * random.random(), 200 * random.random(), math.pi * 2 * random.random())
        chase_state.pilots[1].slide(200 * random.random(), 200 * random.random(), math.pi * 2 * random.random())

        dist_list = chase_state.pilots[1].getArcDistances(chase_state.pilots[0])
        range_list = chase_state.pilots[1].getArcRanges(chase_state.pilots[0])

        assert min(range_list) == range_list[chase_state.pilots[1].arcTurret_index]
        assert min(dist_list) == dist_list[chase_state.pilots[1].arcTurret_index]

