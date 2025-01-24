import json
from typing import Dict, List
import numpy as np


def print_info(*args):
    print("[INFO]", *args)


def print_warning(*args):
    print("[WARNING]", *args)


def print_error(*args):
    print("[ERROR]", *args)


def npdict_to_json(data: Dict[str, List[Dict[str, np.ndarray]]], fpath: str) -> None:
    def convert_to_serializable(d):
        if isinstance(d, dict):
            return {key: convert_to_serializable(value) for key, value in d.items()}
        elif isinstance(d, list):
            return [convert_to_serializable(item) for item in d]
        elif isinstance(d, np.ndarray):
            return d.tolist()
        else:
            return d

    json_data = convert_to_serializable(data)

    # Save to a JSON file
    with open(fpath, "w") as f:
        json.dump(json_data, f)
