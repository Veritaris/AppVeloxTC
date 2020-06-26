from envparse import Env
import os


def load_config(path):
    env = Env(
        upload_folder=str,
        allowed_extention=list
    )
    env.read_envfile(path)
    return env


cwd = os.getcwd()
config = load_config(f"{cwd}/environment.env")
secret = load_config(f"{cwd}/secrets.env")
