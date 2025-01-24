import torch
import json


def load_json_list_as_tensor(fpath: str) -> torch.Tensor:
    with open(fpath, "r") as json_file:
        tensor_list = json.load(json_file)

    tensor = torch.tensor(tensor_list)
    return tensor
