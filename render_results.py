#!/usr/bin/env python3

from benchmarl.eval_results import load_and_merge_json_dicts, Plotting
from matplotlib import pyplot as plt
from marl_eval.utils.diagnose_data_errors import DiagnoseData

import sys
import glob
import numpy as np

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} path/or/glob/to/experiments.json [path/or/glob/to/experiment2.json [...]]")
    exit()

json_files = []
for item in sys.argv[1:]:
    json_files += [p for p in glob.glob(item)]

raw_dict = load_and_merge_json_dicts(json_files, json_output_file = './results_merged.json')

processed_data = Plotting.process_data(raw_dict)
# print(DiagnoseData(processed_data).check_data())

rng = np.random.default_rng()
for env_name in raw_dict.keys():
    (environment_comparison_matrix, sample_efficiency_matrix, ) = Plotting.create_matrices(processed_data, env_name=env_name)

    # Plotting
    Plotting.performance_profile_figure(
        environment_comparison_matrix=environment_comparison_matrix
    )
    Plotting.aggregate_scores(
        environment_comparison_matrix=environment_comparison_matrix
    )
    Plotting.environemnt_sample_efficiency_curves(
        sample_effeciency_matrix=sample_efficiency_matrix
    )
    Plotting.task_sample_efficiency_curves(
        processed_data=processed_data, env=env_name, task="navigation"
    )
    Plotting.probability_of_improvement(
        environment_comparison_matrix,
        algorithms_to_compare=[["ippo", "mappo"]],
    )
    plt.savefig(f'./renderings/{env_name}.png')
