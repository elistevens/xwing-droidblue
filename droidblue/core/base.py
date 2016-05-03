from __future__ import division

import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

    @property
    def corners(self):
        corners = []
        for r in [0.25, 0.75, 1.25, 1.75]:
            radians = self.heading_radians + math.pi * r

            sin = math.sin(radians)
            cos = math.cos(radians)

            x = sin * self.outer_radius + self.x
            y = cos * self.outer_radius + self.y

            corners.append(Point(x, y))

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
    _maneuverOffsets_xyr = [{}, {}]
    _widths = [40.0, 80.0]

        # self.hasAuxBackArc = args.hasAuxBackArc or False
        # self.hasAuxWideArc = args.hasAuxWideArc or False

    def performManeuver(self, label):
        self.slide(*self._maneuverOffsets_xyr[self.isLarge][label])


    def _getRangeCheckPoints(self, other_base):
        # FIXME: all sorts of other complicated things go here...
        # intersection of arc lines
        # point to parallel side
        return self.corners

    # def getArcRanges(self, other_base):
    #     arcs = {}
    #
    #     for other_p in other_base._getRangeCheckPoints(self):
    #         dx = self.center.x - other_p.x
    #         dy = self.center.y - other_p.y
    #         angle_min = abs(math.atan2(dy, dx) - self.heading_radians)
    #
    #         distance_min = min([other_p.distance(this_p) for this_p in self._getRangeCheckPoints(other_base)])
    #
    #         arcs['range'] == min(distance_min, arcs['range'] or LONG_RANGE)
    #
    #         if angle_min < self.arcAngle:
    #             arcs['front'] == min(distance_min, arcs['front'] or LONG_RANGE)
    #
    #         elif self.hasAuxWideArc and angle_min < math.pi / 2.0:
    #             arcs['auxwide'] == min(distance_min, arcs['auxwide'] or LONG_RANGE)
    #
    #         elif self.hasAuxBackArc and angle_min > math.pi - self.arcAngle:
    #             arcs['auxback'] == min(distance_min, arcs['auxback'] or LONG_RANGE)
    #
    #     return arcs
    #
    # def getRange(self, other_base):
    #     return [min(4, math.ceil(self.getArcRanges(other_base)['range'] / 100.0)), this_p, other_p]


# http://teamcovenant.com/mu0n/2013/11/28/the-road-to-4-6-0-and-better-firing-arcs/
LONG_RANGE = 3000
_movementConstants = {
    'turn':     [0, 35, 63, 90],
    'bank':     [0, 80, 130, 180],
    'forward':  [0, 40, 80, 120, 160, 200],
    'range':    [0, 100, 200, 300, 400, 500, LONG_RANGE]
}


def _movementFunction(angle, radius, base_offset):
    x = radius      - math.cos(angle) * radius + math.sin(angle) * base_offset
    y = base_offset + math.sin(angle) * radius + math.cos(angle) * base_offset
    return [x, y, angle]

for j, width in enumerate(Base._widths):
    mo = Base._maneuverOffsets_xyr[j]
    for i in ['1', '2', '3']:
        mo['turnR' + i] = _movementFunction(0.5 * math.pi, _movementConstants['turn'][int(i)], width / 2.0)
        mo['turnL' + i] = [-mo['turnR' + i][0], mo['turnR' + i][1], -
        mo['turnR' + i][2]]

        # FIXME: need to implement the troll slide forward/back somehow...
        mo['trollR' + i] = [mo['turnR' + i][0], mo['turnR' + i][1], mo['turnR' + i][2] + math.pi / 2.0]
        mo['trollL' + i] = [mo['turnL' + i][0], mo['turnL' + i][1], mo['turnL' + i][2] - math.pi / 2.0]

        mo['bankR' + i] = _movementFunction(0.25 * math.pi, _movementConstants['bank'][int(i)], width / 2.0)
        mo['bankL' + i] = [-mo['bankR' + i][0], mo['bankR' + i][1], -
        mo['bankR' + i][2]]

        mo['sloopR' + i] = [mo['bankR' + i][0], mo['bankR' + i][1], mo['bankR' + i][2] + math.pi]
        mo['sloopL' + i] = [mo['bankL' + i][0], mo['bankL' + i][1], mo['bankL' + i][2] + math.pi]

    for i in ['1', '2', '3', '4', '5']:
        mo['forward' + i] = [0.0, _movementConstants['forward'][int(i)] + width, 0.0]
        mo['kturn' + i] = [0.0, _movementConstants['forward'][int(i)] + width, math.pi]

    mo['stop'] = [0.0, 0.0, 0.0]
    mo['ionized'] = mo['forward1']

maneuver_list = list(Base._maneuverOffsets_xyr[0])
