from __future__ import division

from typing import NewType, Optional, Dict, List, Tuple

import numpy as np

from droidblue.util import FancyRepr

# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
# log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)


import math
import re


class Point(FancyRepr):
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def distanceSq(self, p: 'Point'):
        dx = self.x - p.x
        dy = self.y - p.y
        return dx * dx + dy * dy

    def distance(self, p):
        return math.sqrt(self.distanceSq(p))

class Circle(Point):
    def __init__(self, x: float, y: float, radius: float):
        super(Circle, self).__init__(x, y)
        self.radius = radius

    def overlapsPoint(self, p: Point, extra_radius=0.0):
        tr = self.radius + extra_radius

        return tr * tr <= self.distanceSq(p)

    def overlapsCircle(self, c: 'Circle'):
        return self.overlapsPoint(c, self.radius)

    def overlapsSquare(self, s):
        return s.overlapsCircle(self)


class Square(Point):
    width = 0.0

    def __init__(self, x: float = 0.0, y: float = 0.0, h: float = 0.0):
        self.inner_radius: float = self.width / 2.0
        self.outer_radius: float = math.sqrt((self.inner_radius ** 2) * 2)


        super(Square, self).__init__(0.0, 0.0)

        self.heading_radians: float = 0.0
        self._changePosition(x, y, h) # this sets dx, dy

    @property
    def heading_degrees(self):
        return math.degrees(self.heading_radians)

    def slide(self, mx, my, mh=0.0):
        s = math.sin(self.heading_radians)
        c = math.cos(self.heading_radians)
        tx = c * mx + s * my
        ty = s * mx + c * my

        self._changePosition(tx, ty, mh)

    def _changePosition(self, tx, ty, th_radians):
        self.x += tx
        self.y += ty
        self.heading_radians += th_radians

        sin = math.sin(self.heading_radians)
        cos = math.cos(self.heading_radians)

        if sin > cos:
            [sin, cos] = [cos, sin]

        self.dx = abs(sin / self.inner_radius)
        self.dy = abs(cos / self.inner_radius)

    def _resetPosition(self):
        self._changePosition(-self.x, -self.y, -self.heading_radians)

    @property
    def corners(self):
        radians = self.heading_radians + math.pi * 0.25

        s = math.sin(radians) * self.outer_radius
        c = math.cos(radians) * self.outer_radius

        corners = [
            Point(self.x + c, self.y + s),
            Point(self.x - s, self.y + c),
            Point(self.x - c, self.y - s),
            Point(self.x + s, self.y - c),
        ]

        return corners

    def overlapsPoint(self, p: Point):
        dx = abs(p.x - self.x)
        dy = abs(p.y - self.y)

        if dx > dy:
            [dx, dy] = [dy, dx]

        return dx * self.dx + dy * self.dy < 1.0

    def overlapsCircle(self, c: Circle):
        # Most things are far away
        if not c.overlapsPoint(self, self.outer_radius):
            return False

        # Clearly overlaps
        if c.overlapsPoint(self, self.inner_radius):
            return True

        # Just the corner landed on it
        for corner in self.corners:
            if c.overlapsPoint(corner):
                return True


        # The r*4 is to short-circuit out when the circle is too big to fit
        # inside the area between the inner circle and the corner point.
        # Doing point-testing on a square is vaguely expensive.
        # inner = width = 1
        # outer = 1.41 (2**0.5)
        # biggest circle that can fit in the corner: r = 0.41/2 = 0.205
        # r * 4 = 0.82 < 1
        # Since most circles we care about are at most LargeBase.width / 2,
        # this should shortcut out most of the time.
        if c.radius * 4 < self.width and self.overlapsPoint(c):
            return True

        # FIXME: there can be a slight overlap here, where the circle nips the
        # FIXME: edge, but not enough to hit the corner or the midpoint.
        # FIXME: I don't care enough to fix it right now. Patches welcome!
        return False

    def overlapsSquare(self, s: 'Square'):
        if (self.outer_radius + s.outer_radius) ** 2 < self.distanceSq(s):
            return False

        for corner in self.corners:
            if s.overlapsPoint(corner):
                return True
        for corner in s.corners:
            if self.overlapsPoint(corner):
                return True

        return False

# def _arcAngles(a):
#     return [
#         (-math.radians(a/2), math.radians(a/2))
#         (-math.radians(90), math.radians(90))
#         (-math.radians(a/2 + 180), math.radians(a/2 + 180))
#         ()
#
#     ]

class Base(Square):
    _size = 0
    _maneuverOffsets_xyr = [{}, {}, {}]
    _widths = [40.0, 60.0, 80.0]
    _angles = [81.24, 82.80, 83.52]
    
    arcBullseye_ndx = 0
    arcFront_ndx = 1
    arcLeft_ndx = 2
    arcRight_ndx = 3
    arcBack_ndx = 4
    
    arcWideFront_ndx = 5
    arcWideBack_ndx = 6

    def performManeuver(self, label):
        self.slide(*self._maneuverOffsets_xyr[self._size][label])


    # def _getRangeCheckPoints(self, other_base):
    #     # FIXME: all sorts of other complicated things go here...
    #     # intersection of arc lines
    #     # point to parallel side
    #     return self.corners

    def getArcDistances(self, other_base):
        # front, side, back, turret

        arc_ary = np.zeros((4, 7), dtype=np.bool)
        range_ary = np.zeros((4, 2), dtype=np.float32)

        arc_rad = self._angles[self._size] / 2.

        for i, other_p in enumerate(other_base.corners):
            dx = other_p.x - self.x
            dy = other_p.y - self.y
            
            angle_p = math.atan2(dy, dx) - self.heading_radians
            while angle_p > math.pi:
                angle_p -= math.pi * 2
            while angle_p < -math.pi:
                angle_p += math.pi * 2

            assert angle_p <= math.pi
            assert angle_p >= -math.pi

            if math.fabs(angle_p) <= arc_rad:
                arc_ary[i, self.arcFront_ndx] = True
            elif 0 < angle_p < -math.pi + arc_rad:
                arc_ary[i, self.arcRight_ndx] = True
            elif 0 < angle_p <  math.pi - arc_rad:
                arc_ary[i, self.arcLeft_ndx] = True
            else:
                arc_ary[i, self.arcBack_ndx] = True

            if math.fabs(angle_p) <= math.pi / 2.:
                arc_ary[i, self.arcWideFront_ndx] = True
            else:
                arc_ary[i, self.arcWideBack_ndx] = True

            if dx < 7.5:
                arc_ary[i, self.arcBullseye_ndx] = True

            range_ary[i,0] = other_p.distance(self.corners[0])
            for this_corner in self.corners:
                range_ary[i,0] = min(range_ary[i,0], other_p.distance(this_corner))

            range_ary[i,1] = np.ceil(range_ary[i,0] / 100.)
            if range_ary[i,1] < 1 and not self.overlapsPoint(other_p):
                range_ary[i,1] = 1

        return arc_ary, range_ary

    def getArcRanges(self, other_base):
        return [min(4, int(math.ceil(d / 100.0))) for d in self.getArcDistances(other_base)]


# http://teamcovenant.com/mu0n/2013/11/28/the-road-to-4-6-0-and-better-firing-arcs/
# LONG_RANGE = 3000
_movementConstants = {
    'turn':     [0, 35, 63, 90],
    'bank':     [0, 80, 130, 180],
    'forward':  [0, 40, 80, 120, 160, 200],
    # 'range':    [0, 100, 200, 300, 400, 500, LONG_RANGE]
}


def _movementFunction(angle, radius, base_offset):
    x = base_offset + math.sin(angle) * radius + math.cos(angle) * base_offset
    y = radius      - math.cos(angle) * radius + math.sin(angle) * base_offset
    return [x, y, angle]


def _forwardBack(j, mo, key_str):
    if key_str.startswith('broll') and j > 0:
        template_offset = _movementConstants['forward'][1] / 2.
    else:
        template_offset = 10

    for i in ['1', '2', '3', '4', '5']:
        if key_str + i not in mo:
            continue

        angle = mo[key_str + i][2]
        ox = template_offset * math.cos(angle)
        oy = template_offset * math.sin(angle)

        mo[key_str + i + 'f'] = [mo[key_str + i][0] + ox, mo[key_str + i][1] + oy, mo[key_str + i][2]]
        mo[key_str + i + 'b'] = [mo[key_str + i][0] - ox, mo[key_str + i][1] - oy, mo[key_str + i][2]]


for j, width in enumerate(Base._widths):
    mo = Base._maneuverOffsets_xyr[j]
    for i in ['1', '2', '3']:
        mo['turnL' + i] = _movementFunction(0.5 * math.pi, _movementConstants['turn'][int(i)], width / 2.0)
        mo['turnR' + i] = [mo['turnL' + i][0], -mo['turnL' + i][1], -mo['turnL' + i][2]]

        mo['revturnL' + i] = [-mo['turnL' + i][0], mo['turnL' + i][1], -mo['turnL' + i][2]]
        mo['revturnR' + i] = [-mo['turnR' + i][0], mo['turnR' + i][1], -mo['turnR' + i][2]]

        mo['trollL' + i] = [mo['turnL' + i][0], mo['turnL' + i][1], mo['turnL' + i][2] + math.pi / 2.0]
        mo['trollR' + i] = [mo['turnR' + i][0], mo['turnR' + i][1], mo['turnR' + i][2] - math.pi / 2.0]
        _forwardBack(j, mo, 'trollL')
        _forwardBack(j, mo, 'trollR')

        mo['bankL' + i] = _movementFunction(0.25 * math.pi, _movementConstants['bank'][int(i)], width / 2.0)
        mo['bankR' + i] = [mo['bankL' + i][0], -mo['bankL' + i][1], -mo['bankL' + i][2]]
        
        mo['sloopL' + i] = [mo['bankL' + i][0], mo['bankL' + i][1], mo['bankL' + i][2] + math.pi]
        mo['sloopR' + i] = [mo['bankR' + i][0], mo['bankR' + i][1], mo['bankR' + i][2] + math.pi]

        mo['revbankL' + i] = [-mo['bankL' + i][0], mo['bankL' + i][1], -mo['bankL' + i][2]]
        mo['revbankR' + i] = [-mo['bankR' + i][0], mo['bankR' + i][1], -mo['bankR' + i][2]]

        mo['srollFL' + i] = [mo['bankL' + i][1], mo['bankL' + i][0], -mo['bankL' + i][2]]
        mo['srollBL' + i] = [-mo['bankL' + i][1], mo['bankL' + i][0], mo['bankL' + i][2]]
        mo['srollFR' + i] = [mo['bankL' + i][1], -mo['bankL' + i][0], mo['bankL' + i][2]]
        mo['srollBR' + i] = [-mo['bankL' + i][1], -mo['bankL' + i][0], -mo['bankL' + i][2]]
        _forwardBack(j, mo, 'srollFL')
        _forwardBack(j, mo, 'srollBL')
        _forwardBack(j, mo, 'srollFR')
        _forwardBack(j, mo, 'srollBR')

    for i in ['1', '2', '3', '4', '5']:
        mo['forward' + i] = [_movementConstants['forward'][int(i)] + width, 0.0, 0.0]
        mo['reverse' + i] = [-_movementConstants['forward'][int(i)] - width, 0.0, 0.0]
        mo['kturn' + i] =   [_movementConstants['forward'][int(i)] + width, 0.0, math.pi]

        if j == 0:
            mo['brollL' + i] = [0.0, _movementConstants['forward'][int(i)] + width, 0.0]
            mo['brollR' + i] = [0.0, -_movementConstants['forward'][int(i)] - width, 0.0]
        else:
            mo['brollL' + i] = [0.0, 20. + width, 0.0]
            mo['brollR' + i] = [0.0, -20. - width, 0.0]

        _forwardBack(j, mo, 'brollL')
        _forwardBack(j, mo, 'brollR')

    mo['stop'] = [0.0, 0.0, 0.0]
    mo['ionized'] = mo['forward1']

maneuver_list = sorted(set(k.split('_')[0] for k in Base._maneuverOffsets_xyr[0]))
