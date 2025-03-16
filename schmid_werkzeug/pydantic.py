from pydantic import BaseModel
import json
import yaml
import glob
import os
from .general_utils import print_info


def save_cfg(cfg: BaseModel, yaml_path: str) -> None:
    assert yaml_path.endswith(".yaml")
    json_string = cfg.model_dump_json()
    python_dict = json.loads(json_string)
    yaml_string = yaml.dump(python_dict)
    with open(yaml_path, "w") as file:
        file.write(yaml_string)


def load_cfg(yaml_path: str, CfgClass: type[BaseModel] = BaseModel) -> BaseModel:
    with open(yaml_path, "r") as file:
        if yaml_path.endswith(".yaml"):
            data = yaml.safe_load(file)
        elif yaml_path.endswith(".json"):
            data = json.load(file)
        else:
            raise ValueError("")
    config = CfgClass.model_validate(data)
    return config


def gather_yaml_files(directory, recursive=True, verbose=True, suffix: str = ".yaml"):
    pattern = f"**/*{suffix}" if recursive else f"*{suffix}"
    yaml_files = glob.glob(os.path.join(directory, pattern), recursive=recursive)

    if verbose:
        print_info(f"Found {len(yaml_files)} YAML files:")
        for file in yaml_files:
            print(file)

    return yaml_files
