#!/usr/bin/env python3

from benchmarl.algorithms import MappoConfig, IppoConfig
from benchmarl.benchmark import Benchmark
from benchmarl.environments import VmasTask
from benchmarl.experiment import ExperimentConfig
from benchmarl.models.mlp import MlpConfig

from torch.cuda import is_available

experiment_config = ExperimentConfig.get_from_yaml()

if is_available():
    print('Running experiment via cuda')
    experiment_config.sampling_device = "cuda"
    experiment_config.trin_device = "cuda"
    experiment_config.buffer_device = "cuda"
else:
    print('Running experiment on cpu')

# Don't depend on w&b, I don't want to make an account
experiment_config.loggers = ['csv']

benchmark = Benchmark(
    algorithm_configs=[
        IppoConfig.get_from_yaml(),
        MappoConfig.get_from_yaml(),
    ],
    tasks=[
        VmasTask.TRANSPORT.get_from_yaml(),
        VmasTask.GIVE_WAY.get_from_yaml(),
        VmasTask.WHEEL.get_from_yaml(),
        VmasTask.BALANCE.get_from_yaml(),
        # VmasTask.DROPOUT.get_from_yaml(),
        # VmasTask.DISPERSION.get_from_yaml(),
        # VmasTask.REVERSE_TRANSPORT.get_from_yaml(),
        # VmasTask.FOOTBALL.get_from_yaml(),
        # VmasTask.DISCOVERY.get_from_yaml(),
        # VmasTask.FLOCKING.get_from_yaml(),
        # VmasTask.PASSAGE.get_from_yaml(),
        # VmasTask.JOINT_PASSAGE_SIZE.get_from_yaml(),
        # VmasTask.JOINT_PASSAGE.get_from_yaml(),
        # VmasTask.BALL_PASSAGE.get_from_yaml(),
        # VmasTask.BALL_TRAJECTORY.get_from_yaml(),
        # VmasTask.BUZZ_WIRE.get_from_yaml(),
        # VmasTask.MULTI_GIVE_WAY.get_from_yaml(),
        # VmasTask.NAVIGATION.get_from_yaml(),
        # VmasTask.SAMPLING.get_from_yaml(),
        # VmasTask.WIND_FLOCKING.get_from_yaml(),
        # VmasTask.ROAD_TRAFFIC.get_from_yaml(), # Does not exist
    ],
    seeds={0, 1},
    experiment_config=experiment_config,
    model_config=MlpConfig.get_from_yaml(),
    critic_model_config=MlpConfig.get_from_yaml(),
)

for bench in benchmark.get_experiments():
    try:
        bench.run()
    except Exception as e:
        print(bench, "failed with:")
        print(e)

