# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

from droidblue.testing.fixtures import *

import random
import numpy as np

def test_corners(vs_state):
    vs_state.pilots[0]._resetPosition()
    vs_state.pilots[1]._resetPosition()

    log.info(vs_state.pilots[0].x)
    log.info(vs_state.pilots[0].y)
    log.info(vs_state.pilots[0].heading_degrees)
    log.info(vs_state.pilots[0].corners)

    corner_set = set((int(round(p.x)), int(round(p.y))) for p in vs_state.pilots[0].corners)

    assert corner_set == {(20, 20), (20, -20), (-20, 20), (-20, -20)}


    vs_state.pilots[0].heading_radians = math.pi * 0.25

    log.info(vs_state.pilots[0].heading_degrees)
    log.info(vs_state.pilots[0].corners)

    corner_set = set((int(round(p.x)), int(round(p.y))) for p in vs_state.pilots[0].corners)

    assert corner_set == {(0, 28), (28, 0), (0, -28), (-28, 0)}


    vs_state.pilots[0].heading_radians = math.pi * 0.1

    log.info(vs_state.pilots[0].heading_degrees)
    log.info(vs_state.pilots[0].corners)

    corner_set = set((int(round(p.x)), int(round(p.y))) for p in vs_state.pilots[0].corners)

    assert corner_set == {(13, 25), (-25, 13), (-13, -25), (25, -13)}


    vs_state.pilots[0].heading_radians = math.pi * -0.1

    log.info(vs_state.pilots[0].heading_degrees)
    log.info(vs_state.pilots[0].corners)

    corner_set = set((int(round(p.x)), int(round(p.y))) for p in vs_state.pilots[0].corners)

    assert corner_set == {(25, 13), (13, -25), (-25, -13), (-13, 25)}


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


def test_ranges_with_maneuvers1(vs_state):
    vs_state.pilots[0]._resetPosition()
    vs_state.pilots[1]._resetPosition()

    log.info(vs_state.pilots[0].x)
    log.info(vs_state.pilots[0].y)
    log.info(vs_state.pilots[0].heading_degrees)

    vs_state.pilots[1].slide(300, 0)

    dist_list = vs_state.pilots[0].getArcDistances(vs_state.pilots[1])
    range_list = vs_state.pilots[0].getArcRanges(vs_state.pilots[1])

    assert np.allclose(dist_list, [260.0, 260.0, 3000, 260.0])
    assert range_list == [3, 3, 4, 3]

    log.info(vs_state.pilots[0]._maneuverOffsets_xyr[0]['forward2'])
    vs_state.pilots[0].performManeuver('forward2')

    dist_list = vs_state.pilots[0].getArcDistances(vs_state.pilots[1])
    range_list = vs_state.pilots[0].getArcRanges(vs_state.pilots[1])

    assert np.allclose(dist_list, [140.0, 140.0, 3000, 140.0])
    assert range_list == [2, 2, 4, 2]

def test_ranges_with_maneuvers2(vs_state):
    vs_state.pilots[0]._resetPosition()
    vs_state.pilots[1]._resetPosition()

    log.info(vs_state.pilots[0].x)
    log.info(vs_state.pilots[0].y)
    log.info(vs_state.pilots[0].heading_degrees)

    vs_state.pilots[1].slide(200, 200)

    dist_list = vs_state.pilots[0].getArcDistances(vs_state.pilots[1])
    range_list = vs_state.pilots[0].getArcRanges(vs_state.pilots[1])

    # >>> 160 * 2**0.5
    # 226.27416997969522
    # 256.125 is because the 80 degree arc doesn't have the close corner in arc
    assert np.allclose(dist_list, [256.12496949731394, 226.27416997969522, 3000, 226.27416997969522])
    assert range_list == [3, 3, 4, 3]

    vs_state.pilots[0].performManeuver('bankL1')

    log.info(vs_state.pilots[0].x)
    log.info(vs_state.pilots[0].y)
    log.info(vs_state.pilots[0].heading_degrees)

    dist_list = vs_state.pilots[0].getArcDistances(vs_state.pilots[1])
    range_list = vs_state.pilots[0].getArcRanges(vs_state.pilots[1])

    assert np.allclose(dist_list, [144.91725231019282, 144.91725231019282, 3000, 144.91725231019282])
    assert range_list == [2, 2, 4, 2]

