import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

from droidblue.core.edge import Edge

from droidblue.core.rules import ActiveAbilityRule


class PerformActionRule(ActiveAbilityRule):
    isOncePerRound_bool = True

    def __init__(self, state, pilot_id):
        super(PerformActionRule, self).__init__(state, 'performAction', pilot_id)

    def getOpportunityKey(self, state):
        opportunity_key = (self,)
        # if not self.isOncePerRound_bool:
        #     opportunity_key += state.getOpportunityStepKey()

        return [opportunity_key, ('performAction', self.pilot_id) + state.getOpportunityStepKey()]

class StressPreventsPerformActionRule(ActiveAbilityRule):
    def __init__(self, state, pilot_id):
        super(StressPreventsPerformActionRule, self).__init__(state, '*', pilot_id)

    def isAvailable(self, state):
        return super(StressPreventsPerformActionRule, self).isAvailable(state) and \
            state.getToken(self.pilot_id, 'stress') > 0

    def filterEdges(self, edge_list, state):
        return [edge for edge in edge_list if not isinstance(edge, PerformActionRule)]


# class PreventDuplicatePerformActionRule(ActiveAbilityRule):
#     def __init__(self, state, pilot_id):
#         super(PreventDuplicatePerformActionRule, self).__init__(state, '*', pilot_id)
#
#     def filterEdge(self, edge, state):
#         return str(type(edge)) not in  state.pilots[self.pilot_id].performedActions
#         # log.debug("before {}: {}".format(performed, edge_list))
#         # edge_list = [edge for edge in edge_list if str(type(edge)) not in performed]
#         # log.debug("after  {}: {}".format(performed, edge_list))
#         #
#         # return edge_list



class PerformActionEdge(Edge):
    def transitionImpl(self, state):
        # state.pilots[self.active_id].performedActions.add(str(type(self)))
        pass

class PerformFocusActionRule(PerformActionRule):
    card_type = 'generic'

    def _getEdges(self, state):
        return [PerformFocusActionEdge(self.pilot_id)]


class PerformFocusActionEdge(PerformActionEdge):
    def transitionImpl(self, state):
        state.assignToken(self.active_id, 'focus')
        super(PerformFocusActionEdge, self).transitionImpl(state)


class PerformEvadeActionRule(PerformActionRule):
    card_type = 'generic'

    def _getEdges(self, state):
        return [PerformEvadeActionEdge(self.pilot_id)]


class PerformEvadeActionEdge(PerformActionEdge):
    def transitionImpl(self, state):
        state.assignToken(self.active_id, 'evade')
        super(PerformEvadeActionEdge, self).transitionImpl(state)


class PerformTargetLockActionRule(PerformActionRule):
    card_type = 'generic'

    def _getEdges(self, state):
        edge_list = [PerformTargetLockActionEdge(self.pilot_id)]
        return [] #edge_list


class PerformTargetLockActionEdge(PerformActionEdge):
    def transitionImpl(self, state):
        state.pilots[self.active_id].acquireTargetLock(state, 'focus')
        super(PerformTargetLockActionEdge, self).transitionImpl(state)


class PerformBarrelRollActionRule(PerformActionRule):
    card_type = 'generic'

    def _getEdges(self, state):
        base_width = state.pilots[self.pilot_id].width
        if base_width == 80.0:
            mx = base_width + 20.0
            my = 40.0
        else:
            mx = base_width + 40.0
            my = 20.0

        edge_list = []
        for sx in [-1, 1]:
            for sy in [-1, 0, 1]:
                edge_list.append(PerformBarrelRollActionEdge(self.pilot_id, mx * sx, my * sy))
        return edge_list

class PerformBarrelRollActionEdge(PerformActionEdge):
    def __init__(self, active_id, mx, my):
        super(PerformBarrelRollActionEdge, self).__init__(active_id)

        self.mx = mx
        self.my = my

    def transitionImpl(self, state):
        pilot_obj = state.pilots[self.active_id]
        pilot_obj.slide(self.mx, self.my)
        super(PerformBarrelRollActionEdge, self).transitionImpl(state)

class PerformBoostActionRule(PerformActionRule):
    card_type = 'generic'

    def _getEdges(self, state):
        edge_list = [
            PerformBoostActionEdge(self.pilot_id, 'bankL1'),
            PerformBoostActionEdge(self.pilot_id, 'bankR1'),
            PerformBoostActionEdge(self.pilot_id, 'forward1'),
        ]
        return edge_list

class PerformBoostActionEdge(PerformActionEdge):
    def __init__(self, active_id, maneuver_str):
        super(PerformBoostActionEdge, self).__init__(active_id)

        self.maneuver_str = maneuver_str

    def transitionImpl(self, state):
        pilot_obj = state.pilots[self.active_id]
        pilot_obj.performManeuver(self.maneuver_str)
        super(PerformBoostActionEdge, self).transitionImpl(state)


class PerformCloakActionRule(PerformActionRule):
    card_type = 'generic'

# FIXME: Not actually an action...
class PerformDecloakActionRule(PerformActionRule):
    card_type = 'generic'

    def _getEdges(self, state):
        base_width = state.pilots[self.pilot_id].width
        if base_width == 80.0:
            mx = base_width + 20.0
            my = 40.0
        else:
            mx = base_width + 80.0
            my = 20.0

        edge_list = []
        for sx in [-1, 1]:
            for sy in [-1, 0, 1]:
                edge_list.append(PerformDecloakActionEdge(self.pilot_id, mx * sx, my * sy))
        return edge_list

class PerformDecloakActionEdge(PerformActionEdge):
    def __init__(self, active_id, mx, my):
        super(PerformDecloakActionEdge, self).__init__(active_id)

        self.mx = mx
        self.my = my

    def transitionImpl(self, state):
        pilot_obj = state.pilots[self.active_id]
        pilot_obj.slide(self.mx, self.my)
        state.removeToken(self.active_id, 'cloak')
        super(PerformDecloakActionEdge, self).transitionImpl(state)

class PerformSlamActionRule(PerformActionRule):
    card_type = 'generic'

rule_list = [StressPreventsPerformActionRule]
