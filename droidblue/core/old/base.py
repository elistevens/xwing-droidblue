from __future__ import division

# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
# log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)


import math
import re


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        extra_str = ', '.join(['{}:{!r}'.format(k, v) for k, v in sorted(self.__dict__.iteritems())])
        r = super(Point, self).__repr__()
        r = re.sub(r'\<droidblue\.([a-z]+\.)+', '<', r)
        return r.replace('>', ' {}>'.format(extra_str))

    def insideCircle(self, c, extra_radius=0.0):
        tr = c.radius + extra_radius

        return tr * tr < self.distanceSq(c.center)

    def insideSquare(self, s):
        dx = abs(self.x - s.x)
        dy = abs(self.y - s.y)

        if dx > dy:
            [dx, dy] = [dy, dx]

        return dx * s.dx + dy * s.dy < 1.0

    def distanceSq(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return dx * dx + dy * dy

    def distance(self, p):
        return math.sqrt(self.distanceSq(p))

class Circle(Point):
    def __init__(self, x, y, radius):
        super(Circle, self).__init__(x, y)
        self.radius = radius

    def overlapsCircle(self, c):
        return self.insideCircle(c, self.radius)

    def overlapsSquare(self, s):
        return s.overlapsCircle(self)


class Square(Point):
    width = 0.0

    def __init__(self, x=0.0, y=0.0, h=0.0):
        super(Square, self).__init__(0.0, 0.0)

        self.heading_radians = 0.0
        self._changePosition(x, y, h)

    @property
    def heading_degrees(self):
        return math.degrees(self.heading_radians)

    @property
    def inner_radius(self):
        return self.width / 2.0

    @property
    def outer_radius(self):
        return math.sqrt((self.inner_radius ** 2) * 2)

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

    def overlapsCircle(self, c):
        if not self.insideCircle(c, self.outer_radius):
            return False
        if self.insideCircle(c, self.inner_radius):
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
        if c.radius * 4 < self.width and c.insideSquare(self):
            return True

        for corner in self.corners:
            if corner.insideCircle(c):
                return True

        # FIXME: there can be a slight overlap here, where the circle nips the
        # FIXME: edge, but not enough to hit the corner or the midpoint.
        # FIXME: I don't care enough to fix it right now. Patches welcome!
        return False

    def overlapsSquare(self, s):
        for corner in self.corners:
            if corner.insideSquare(s):
                return True
        for corner in s.corners:
            if corner.insideSquare(self):
                return True

        return False



class Base(Square):
    isLarge = None
    _maneuverOffsets_xyr = [{}, {}, {}]
    _widths = [40.0, 60.0, 80.0]

    arcForward_index = 0
    arcSide_index = 1
    arcBack_index = 2
    arcTurret_index = 3

    arcAngle_list = [
        # front, side, back, turret
        [math.radians(a/2) for a in [80.9,  180, 360-80.9,  360]],
        [math.radians(a/2) for a in [80.9,  180, 360-80.9,  360]], # FIXME
        [math.radians(a/2) for a in [84.05, 180, 360-84.05, 360]],
    ]

    def performManeuver(self, label):
        self.slide(*self._maneuverOffsets_xyr[self.isLarge][label])


    def _getRangeCheckPoints(self, other_base):
        # FIXME: all sorts of other complicated things go here...
        # intersection of arc lines
        # point to parallel side
        return self.corners

    def getArcDistances(self, other_base):
        # front, side, back, turret

        arcs = [LONG_RANGE] * 4

        for other_p in other_base._getRangeCheckPoints(self):
            dx = other_p.x - self.x
            dy = other_p.y - self.y

            # log.info("x:{}, y:{}".format(dx, dy))

            distance_p = min([other_p.distance(this_p) for this_p in self._getRangeCheckPoints(other_base)])
            angle_p = math.atan2(dy, dx) - self.heading_radians
            while angle_p > math.pi:
                angle_p -= math.pi * 2
            while angle_p < -math.pi:
                angle_p += math.pi * 2

            assert angle_p <= math.pi
            assert angle_p >= -math.pi


            for i, comparison_angle in enumerate(self.arcAngle_list[bool(self.isLarge)]):
                # if i == 3:
                #     angle_min *= -1
                #     comparison_angle *= -1

                # log.debug("{}: {} >= {}, at {}".format(i, math.degrees(comparison_angle), math.degrees(angle_p), distance_p))

                if i == self.arcBack_index:
                    if abs(angle_p) >= comparison_angle:
                        arcs[i] = min(arcs[i], distance_p)
                else:
                    if abs(angle_p) <= comparison_angle:
                        arcs[i] = min(arcs[i], distance_p)

        return arcs

    def getArcRanges(self, other_base):
        return [min(4, int(math.ceil(d / 100.0))) for d in self.getArcDistances(other_base)]


# http://teamcovenant.com/mu0n/2013/11/28/the-road-to-4-6-0-and-better-firing-arcs/
LONG_RANGE = 3000
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

for j, width in enumerate(Base._widths):
    mo = Base._maneuverOffsets_xyr[j]
    for i in ['1', '2', '3']:
        mo['turnL' + i] = _movementFunction(0.5 * math.pi, _movementConstants['turn'][int(i)], width / 2.0)
        mo['turnR' + i] = [mo['turnL' + i][0], -mo['turnL' + i][1], -mo['turnL' + i][2]]

        # FIXME: need to implement the troll slide forward/back somehow...
        mo['trollL' + i] = [mo['turnL' + i][0], mo['turnL' + i][1], mo['turnL' + i][2] + math.pi / 2.0]
        mo['trollR' + i] = [mo['turnR' + i][0], mo['turnR' + i][1], mo['turnR' + i][2] - math.pi / 2.0]

        mo['bankL' + i] = _movementFunction(0.25 * math.pi, _movementConstants['bank'][int(i)], width / 2.0)
        mo['bankR' + i] = [mo['bankL' + i][0], -mo['bankL' + i][1], -mo['bankL' + i][2]]

        mo['sloopL' + i] = [mo['bankL' + i][0], mo['bankL' + i][1], mo['bankL' + i][2] + math.pi]
        mo['sloopR' + i] = [mo['bankR' + i][0], mo['bankR' + i][1], mo['bankR' + i][2] + math.pi]

    for i in ['1', '2', '3', '4', '5']:
        mo['forward' + i] = [_movementConstants['forward'][int(i)] + width, 0.0, 0.0]
        mo['kturn' + i] =   [_movementConstants['forward'][int(i)] + width, 0.0, math.pi]

    mo['stop'] = [0.0, 0.0, 0.0]
    mo['ionized'] = mo['forward1']

maneuver_list = sorted(Base._maneuverOffsets_xyr[0])
