#!/usr/bin/env python3

from benchmarl.algorithms import MappoConfig, IppoConfig
from benchmarl.benchmark import Benchmark
from benchmarl.environments import PettingZooTask
from benchmarl.experiment import ExperimentConfig
from benchmarl.models.mlp import MlpConfig

import torch
from tqdm import tqdm

experiment_config = ExperimentConfig.get_from_yaml()

if torch.cuda.is_available():
    print('Running experiment via cuda')
    experiment_config.sampling_device = "cuda"
    experiment_config.trin_device = "cuda"
    experiment_config.buffer_device = "cuda"
else:
    print('Running experiment on cpu')

# Don't depend on w&b, I don't want to make an account
experiment_config.loggers = ['csv']
# experiment_config.max_cycles = 500

benchmark = Benchmark(
    algorithm_configs=[
        IppoConfig.get_from_yaml(),
        MappoConfig.get_from_yaml(),
    ],
    tasks=[
        PettingZooTask.MULTIWALKER.get_from_yaml(),
        # PettingZooTask.WATERWORLD.get_from_yaml(),
        # PettingZooTask.SIMPLE_ADVERSARY.get_from_yaml(),
        # PettingZooTask.SIMPLE_CRYPTO.get_from_yaml(),
        # PettingZooTask.SIMPLE_PUSH.get_from_yaml(),
        # PettingZooTask.SIMPLE_SPEAKER_LISTENER.get_from_yaml(),
        # PettingZooTask.SIMPLE_SPREAD.get_from_yaml(),
        # PettingZooTask.SIMPLE_TAG.get_from_yaml(),
        # PettingZooTask.SIMPLE_WORLD_COMM.get_from_yaml(),
    ],
    seeds={0, 1},
    experiment_config=experiment_config,
    model_config=MlpConfig.get_from_yaml(),
    critic_model_config=MlpConfig.get_from_yaml(),
)

benchmark.run_sequential()
