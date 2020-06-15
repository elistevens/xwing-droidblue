import argparse
import datetime
import logging
import math
import os
import random
import sys

import numpy as np

import torch

from torch import nn
from torch.utils.data import Dataset
from torch.optim import SGD, Adam
from torch.utils.data import DataLoader
# from torch.utils.tensorboard import SummaryWriter

from droidblue.core.basecls import PlayerId
from droidblue.core.game import Game

from .battlecruiser import BattleCruiserState, BattleCruiserAgent, BattleCruiserPlaceModel, BattleCruiserShotModel, BattleCruiserPlaceEdge, BattleCruiserShotEdge

log = logging.getLogger(__name__)
# log.setLevel(logging.WARN)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)


class BattleCruiserDataset(Dataset):
    def __init__(self, model_cls, placeModel_path = "droidblue/games/bc/BattleCruiserPlaceModel-latest.state", shotModel_path = "droidblue/games/bc/BattleCruiserShotModel-latest.state"):
        self.model_cls = model_cls
        self.agents = [
            BattleCruiserAgent(placeModel_path, shotModel_path),
            BattleCruiserAgent(placeModel_path, shotModel_path),
        ]

    def __len__(self):
        return 128 * 64

    def __getitem__(self, ndx):
        game = Game(BattleCruiserState, self.agents)
        game.playGame()

        trainable_nodes = [node for node in game.played_nodes if type(node.outgoingEdge) in self.model_cls.supportedEdgeTypes]

        if not trainable_nodes:
            print(f"len(game.played_nodes): {len(game.played_nodes)}")
            for i, node in enumerate(game.played_nodes):
                print(f"{self.model_cls.supportedEdgeTypes} vs. {node.outgoingEdge}")
                # print(f"node.edgeType_to_trainingSample_dict: {node.edgeType_to_trainingData}")

        chosen_node = random.choice(trainable_nodes)

        final_score = game.current_node.state.getFinalScore(chosen_node.state.active_player)
        return self.model_cls.getTrainingSampleFromNode(chosen_node, final_score)

        # inputs, labels, outputs = chosen_node.edgeType_to_trainingSample_dict[self.event_type]
        #
        # labels.append(np.array([final_score], dtype=np.float32))
        #
        # input_tup = tuple(torch.from_numpy(x) for x in inputs)
        # label_tup = tuple(torch.from_numpy(x) for x in labels)
        #
        # training_sample = input_tup, label_tup
        #
        # return training_sample




class TrainingApp:
    def __init__(self, sys_argv=None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser = argparse.ArgumentParser()
        parser.add_argument('--num-workers',
            help='Number of worker processes for background data loading',
            # default=2,
            default=6,
            type=int,
        )
        parser.add_argument('--batch-size',
            help='Batch size to use for training',
            default=128,
            type=int,
        )
        parser.add_argument('--epochs',
            help='Number of epochs to train for',
            default=10,
            type=int,
        )
        parser.add_argument('--generations',
            help='Number of generations to train for',
            default=5,
            type=int,
        )

        parser.add_argument('--tb-prefix',
            default='p2ch11',
            help="Data prefix to use for Tensorboard run. Defaults to chapter.",
        )

        parser.add_argument('comment',
            help="Comment suffix for Tensorboard run.",
            nargs='?',
            default='dwlpt',
        )
        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

        # self.trn_writer = None
        # self.val_writer = None
        # self.totalTrainingSamples_count = 0

        self.placeModel_path = None
        self.shotModel_path = None

        # self.use_cuda = False
        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.use_cuda else "cpu")


    def initModels(self):
        self.place_model: BattleCruiserPlaceModel = BattleCruiserPlaceModel()
        self.shot_model: BattleCruiserShotModel = BattleCruiserShotModel()

        if self.use_cuda:
            log.info("Using CUDA with {} devices.".format(torch.cuda.device_count()))
            if torch.cuda.device_count() > 1:
                self.place_model = nn.DataParallel(self.place_model)
                self.shot_model = nn.DataParallel(self.shot_model)
            self.place_model = self.place_model.to(self.device)
            self.shot_model = self.shot_model.to(self.device)


        # return SGD(self.model.parameters(), lr=0.001, momentum=0.99)
        self.place_opt = Adam(self.place_model.parameters())
        self.shot_opt = Adam(self.shot_model.parameters())


    def makePlaceDl(self):
        train_ds = BattleCruiserDataset(BattleCruiserPlaceModel, self.placeModel_path, self.shotModel_path)

        batch_size = self.cli_args.batch_size
        if self.use_cuda:
            batch_size *= torch.cuda.device_count()

        train_dl = DataLoader(
            train_ds,
            batch_size=batch_size,
            num_workers=self.cli_args.num_workers,
            pin_memory=self.use_cuda,
        )

        return train_dl

    def makeShotDl(self):
        train_ds = BattleCruiserDataset(BattleCruiserShotModel, self.placeModel_path, self.shotModel_path)

        batch_size = self.cli_args.batch_size
        if self.use_cuda:
            batch_size *= torch.cuda.device_count()

        train_dl = DataLoader(
            train_ds,
            batch_size=batch_size,
            num_workers=self.cli_args.num_workers,
            pin_memory=self.use_cuda,
        )

        return train_dl


    def main(self):
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        random_agent = this_agent = BattleCruiserAgent(None, None)

        for generation_ndx in range(1, self.cli_args.generations + 1):
            self.initModels()

            # Shot
            total_loss = None
            for epoch_ndx in range(1, self.cli_args.epochs + 1):
                log.info("Gen {} of {}, Epoch {} of {}, {} shot batches of size {}*{}".format(
                    generation_ndx,
                    self.cli_args.generations,
                    epoch_ndx,
                    self.cli_args.epochs,
                    len(self.makeShotDl()),
                    self.cli_args.batch_size,
                    (torch.cuda.device_count() if self.use_cuda else 1),
                ))
                last_loss = total_loss
                total_loss = self.doTraining(self.makeShotDl(), self.shot_model, self.shot_opt)

                if epoch_ndx == 2:
                    assert total_loss < last_loss * 0.975

            self.shotModel_path = self.saveModel(generation_ndx, self.shot_model, self.shot_opt)

            last_agent = this_agent
            this_agent = BattleCruiserAgent(self.placeModel_path, self.shotModel_path)
            self.reportWinRate(last_agent, this_agent, "last vs. shot")

            # Place
            total_loss = None
            for epoch_ndx in range(1, self.cli_args.epochs + 1):
                log.info("Gen {} of {}, Epoch {} of {}, {} place batches of size {}*{}".format(
                    generation_ndx,
                    self.cli_args.generations,
                    epoch_ndx,
                    self.cli_args.epochs,
                    len(self.makePlaceDl()),
                    self.cli_args.batch_size,
                    (torch.cuda.device_count() if self.use_cuda else 1),
                ))

                last_loss = total_loss
                total_loss = self.doTraining(self.makePlaceDl(), self.place_model, self.place_opt)

                if epoch_ndx == 2:
                    assert total_loss < last_loss * 0.975, repr(total_loss / last_loss)

            self.placeModel_path = self.saveModel(generation_ndx, self.place_model, self.place_opt)

            last_agent = this_agent
            this_agent = BattleCruiserAgent(self.placeModel_path, self.shotModel_path)
            self.reportWinRate(last_agent, this_agent, "last vs. place vs")


    def doTraining(self, dl, model, opt):
        model.train()
        total_loss = 0.0
        for batch_ndx, batch_tup in enumerate(dl):
            opt.zero_grad()

            loss_g, metadata_dict = model.getTrainingLossAndMetadata(batch_tup, self.device)

            loss_g.backward()
            opt.step()

            total_loss += loss_g.item()

        log.info(f"Training shot loss: {total_loss}")
        return total_loss

    def saveModel(self, generation_ndx, model, opt):
            state = {
                'sys_argv': sys.argv,
                'time': str(datetime.datetime.now()),
                'model_state': model.state_dict(),
                'model_name': type(model).__name__,
                'optimizer_state' : opt.state_dict(),
                'optimizer_name': type(opt).__name__,
                # 'epoch': epoch_ndx,
                # 'totalTrainingSamples_count': self.totalTrainingSamples_count,
            }
            model_path = f"droidblue/games/bc/{type(model).__name__}-latest.state"
            torch.save(state, model_path)
            model_path = f"droidblue/games/bc/{type(model).__name__}-gen{generation_ndx}.state"
            torch.save(state, model_path)

            return model_path

    def reportWinRate(self, a_agent, b_agent, msg):
        agents = [a_agent, b_agent]
        wins = 0
        games = 100
        turns = 0

        for i in range(games):
            game = Game(BattleCruiserState, agents)
            game.playGame()

            wins += game.current_node.state.getFinalScore(PlayerId(1)) > 0
            turns += len(game.played_nodes)

        log.info(f"wins last vs. this: {wins}, avg. length {turns/games}.  {msg}")

        return wins / games


if __name__ == '__main__':
    TrainingApp().main()
