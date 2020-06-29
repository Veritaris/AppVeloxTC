import json
import os


def load_config(path):
    """
    Load .json file to config
    :param path: path to .json config
    :return: JSON object with config
    """
    with open(path, "r") as f:
        data = json.load(f)
        return data


cwd = os.getcwd()
config = load_config(f"{cwd}/environment.json")
secret = load_config(f"{cwd}/secrets.json")
