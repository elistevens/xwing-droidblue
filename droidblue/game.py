from droidblue.state import BoardState


class Game(object):
    def __init__(self, score_cls, squads_list, slop_list):
        self.root_state = BoardState(squads_list)
        self.slop_list = slop_list
        self.score_cls = score_cls
