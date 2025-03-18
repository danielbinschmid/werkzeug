from pydantic import BaseModel
import json
import yaml
import glob
import os
from .general_utils import print_info
from typing import Optional


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


class DynBaseModel(BaseModel):
    original_base_path: str
    new_base_path: Optional[str] = None

    def get_relative_path(self, fpath: str) -> str:
        return os.path.relpath(fpath, self.original_base_path)

    def map(self, fpath: str):
        if self.new_base_path is not None:
            return os.path.join(self.new_base_path, self.get_relative_path(fpath))
        return fpath


def load_cfg_dynamic(
    cfg_path: str, CfgClass: "DynBaseModel"
) -> Optional["DynBaseModel"]:
    if os.path.exists(cfg_path):
        cfg: DynBaseModel = load_cfg(yaml_path=cfg_path, CfgClass=CfgClass)
        cfg.new_base_path = os.path.dirname(cfg_path)
        return cfg
    else:
        return None
