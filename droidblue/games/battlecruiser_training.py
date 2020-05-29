import argparse
import datetime
import logging
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
from droidblue.core.agent import RandomAgent
from droidblue.core.game import Game

from .battlecruiser import BattleCruiserState

log = logging.getLogger(__name__)
# log.setLevel(logging.WARN)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)


class BattleCruiserDataset(Dataset):
    def __init__(self):
        self.agents = [
            RandomAgent(),
            RandomAgent(),
        ]

    def __len__(self):
        return 1000

    def __getitem__(self, ndx):
        game = Game(BattleCruiserState, self.agents)
        game.playGame()

        trainable_nodes = [node for node in game.played_nodes if node.state.isTrainable]
        chosen_node = random.choice(trainable_nodes)

        score = game.current_node.state.getFinalScore(chosen_node.parent_active_player)

        input_t = torch.from_numpy(chosen_node.state.getTrainableInput()).to(torch.float32)
        score_t = torch.tensor([score], dtype=torch.float32)

        training_sample = (input_t,), (score_t,), ({},)

        return training_sample


class Model(nn.Module):
    def __init__(self, in_channels=4):
        super().__init__()

        layer_list = []

        for conv_channels in [6, 4, 2, 1]:
            layer_list.extend(
                [
                    nn.Conv2d(
                        in_channels, conv_channels, kernel_size=3, padding=1, bias=True,
                    ),
                    nn.ReLU(inplace=True),
                ]
            )

            in_channels = conv_channels

        self.conv_seq = nn.Sequential(*layer_list)
        self.linear_layer = nn.Linear(36, 1)

    def forward(self, input_t):
        conv_t = self.conv_seq(input_t)

        # print(conv_t.shape)
        output_t = self.linear_layer(conv_t.view(conv_t.shape[0], -1))

        return output_t


class TrainingApp:
    def __init__(self, sys_argv=None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser = argparse.ArgumentParser()
        parser.add_argument('--num-workers',
            help='Number of worker processes for background data loading',
            default=4,
            type=int,
        )
        parser.add_argument('--batch-size',
            help='Batch size to use for training',
            default=4,
            type=int,
        )
        parser.add_argument('--epochs',
            help='Number of epochs to train for',
            default=1,
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

        self.trn_writer = None
        self.val_writer = None
        self.totalTrainingSamples_count = 0

        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.use_cuda else "cpu")

        self.model = self.initModel()
        self.optimizer = self.initOptimizer()

    def initModel(self):
        model = Model()

        if self.use_cuda:
            log.info("Using CUDA with {} devices.".format(torch.cuda.device_count()))
            if torch.cuda.device_count() > 1:
                model = nn.DataParallel(model)
            model = model.to(self.device)
        return model

    def initOptimizer(self):
        # return SGD(self.model.parameters(), lr=0.001, momentum=0.99)
        return Adam(self.model.parameters())

    def initTrainDl(self):
        train_ds = BattleCruiserDataset()

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

    def initValDl(self):
        val_ds = BattleCruiserDataset()

        batch_size = self.cli_args.batch_size
        if self.use_cuda:
            batch_size *= torch.cuda.device_count()

        val_dl = DataLoader(
            val_ds,
            batch_size=batch_size,
            num_workers=self.cli_args.num_workers,
            pin_memory=self.use_cuda,
        )

        return val_dl

    # def initTensorboardWriters(self):
    #     if self.trn_writer is None:
    #         log_dir = os.path.join('runs', self.cli_args.tb_prefix, self.time_str)
    #
    #         self.trn_writer = SummaryWriter(
    #             log_dir=log_dir + '-trn_cls-' + self.cli_args.comment)
    #         self.val_writer = SummaryWriter(
    #             log_dir=log_dir + '-val_cls-' + self.cli_args.comment)


    def main(self):
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        train_dl = self.initTrainDl()
        val_dl = self.initValDl()

        # self.initTensorboardWriters()

        for epoch_ndx in range(1, self.cli_args.epochs + 1):

            log.info("Epoch {} of {}, {}/{} batches of size {}*{}".format(
                epoch_ndx,
                self.cli_args.epochs,
                len(train_dl),
                len(val_dl),
                self.cli_args.batch_size,
                (torch.cuda.device_count() if self.use_cuda else 1),
            ))

            self.doTraining(epoch_ndx, train_dl)
            # self.logMetrics(epoch_ndx, 'trn', trnMetrics_t)

            self.doValidation(epoch_ndx, val_dl)
            # self.logMetrics(epoch_ndx, 'val', valMetrics_t)

        # if hasattr(self, 'trn_writer'):
        #     self.trn_writer.close()
        #     self.val_writer.close()


    def doTraining(self, epoch_ndx, train_dl):
        self.model.train()
        # trnMetrics_g = torch.zeros(
        #     METRICS_SIZE,
        #     len(train_dl.dataset),
        #     device=self.device,
        # )

        # batch_iter = enumerateWithEstimate(
        #     train_dl,
        #     "E{} Training".format(epoch_ndx),
        #     start_ndx=train_dl.num_workers,
        # )
        # for batch_ndx, batch_tup in batch_iter:
        for batch_ndx, batch_tup in enumerate(train_dl):
            self.optimizer.zero_grad()

            input_tup, label_tup, metadata_tup = batch_tup

            input_t = input_tup[0]
            label_t = label_tup[0]

            input_g = input_t.to(self.device, non_blocking=True)
            label_g = label_t.to(self.device, non_blocking=True)

            output_g = self.model(input_g)

            loss_func = nn.MSELoss()
            loss_g = loss_func(
                output_g,
                label_g,
            )

            loss_g.backward()
            self.optimizer.step()

            print("Training loss:", loss_g.item())


    def doValidation(self, epoch_ndx, val_dl):
        self.model.eval()
        # trnMetrics_g = torch.zeros(
        #     METRICS_SIZE,
        #     len(train_dl.dataset),
        #     device=self.device,
        # )

        # batch_iter = enumerateWithEstimate(
        #     train_dl,
        #     "E{} Training".format(epoch_ndx),
        #     start_ndx=train_dl.num_workers,
        # )
        # for batch_ndx, batch_tup in batch_iter:
        with torch.no_grad():
            for batch_ndx, batch_tup in enumerate(val_dl):
                input_tup, label_tup, metadata_tup = batch_tup

                input_t = input_tup[0]
                label_t = label_tup[0]

                input_g = input_t.to(self.device, non_blocking=True)
                label_g = label_t.to(self.device, non_blocking=True)

                output_g = self.model(input_g)

                loss_func = nn.MSELoss()
                loss_g = loss_func(
                    output_g,
                    label_g,
                )


                print("Validation loss:", loss_g.item())

if __name__ == '__main__':
    TrainingApp().main()
