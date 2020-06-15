import numpy as np

from droidblue.core.basecls import PlayerId
from droidblue.core.game import Game
from droidblue.core.node import Node

from .battlecruiser import BattleCruiserState, BattleCruiserAgent
# from .battlecruiser_training import Model

def main():
    placeModel_path = None
    shotModel_path = "droidblue/games/bc/BattleCruiserShotModel-gen1.state"

    agents = [
        BattleCruiserAgent(placeModel_path, shotModel_path),
        BattleCruiserAgent(placeModel_path, shotModel_path),
    ]
    # save_path = "droidblue/games/bc/BattleCruiserShotModel-latest.state"
    # agents = [
    #     TrainedAgent(Model, save_path),
    #     TrainedAgent(Model, save_path),
    # ]

    import cProfile, pstats, io
    pr = cProfile.Profile()
    pr.enable()

    for i in range(10):
        game = Game(BattleCruiserState, agents)
        game.playGame()

    pr.disable()

    pr.dump_stats('bc_profile.out')
    pstats.Stats(pr).sort_stats('cumulative').print_stats(20)
    pstats.Stats(pr).sort_stats('tot').print_stats(20)


if __name__ == '__main__':
    main()
