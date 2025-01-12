from pydantic import BaseModel
import json
import yaml


def save_cfg(cfg: BaseModel, yaml_path: str) -> None:
    assert yaml_path.endswith(".yaml")
    json_string = cfg.model_dump_json()
    python_dict = json.loads(json_string)
    yaml_string = yaml.dump(python_dict)
    with open(yaml_path, "w") as file:
        file.write(yaml_string)


def load_cfg(yaml_path: str, CfgClass: type[BaseModel] = BaseModel) -> BaseModel:
    with open(yaml_path, "r") as file:
        data = yaml.safe_load(file)
    config = CfgClass.model_validate(data)
    return config
