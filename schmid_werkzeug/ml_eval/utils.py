import json
from typing import Dict, List
import numpy as np


def compile1(data: Dict[str, List[Dict[str, float]]]) -> Dict[str, Dict[str, float]]:
    metric_keys = data[next(iter(data.keys()))][0].keys()

    compiled_data = {}

    for global_key in data.keys():
        global_entries = data[global_key]

        global_transposed_entries = {metric_key: [] for metric_key in metric_keys}
        for global_entry in global_entries:
            for metric_key in metric_keys:
                global_transposed_entries[metric_key].append(global_entry[metric_key])

        global_compiled_entries = {
            metric_key: float(np.mean(global_transposed_entries[metric_key]))
            for metric_key in metric_keys
        }
        compiled_data[global_key] = global_compiled_entries
    return compiled_data


def compile2(data: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    metric_keys = data[next(iter(data.keys()))].keys()

    transposed_data = {metric_key: [] for metric_key in metric_keys}

    for global_key in data.keys():
        for metric_key in metric_keys:
            transposed_data[metric_key].append(data[global_key][metric_key])

    compiled_data = {
        metric_key: float(np.mean(transposed_data[metric_key]))
        for metric_key in metric_keys
    }
    return compiled_data


def evaluate_json(json_fpath: str):
    with open(json_fpath, "r") as file:
        data = json.load(file)

    data: Dict[str, List[Dict[str, float]]] = data

    data_compiled = compile1(data)
    data_result = compile2(data_compiled)
    print(data_result)
