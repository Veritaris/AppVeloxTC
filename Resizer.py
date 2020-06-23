from werkzeug.utils import secure_filename
from flask import request
from envparse import Env
from flask import json
import sqlite3


def load_config(path: str):
    env = Env(
        upload_folder=str,
        allowed_extention=list
    )
    env.read_envfile(path)
    return env


def get_status(order_id):
    """
    Get resize order status from DB and return it's value
    :param order_id:
    :return: order status
    """
    return f"Status of {order_id}"


def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.list("allowed_extensions")


def upload_image():
    if request.method == "POST":
        file = str(request.files.items)
        return file
    else:
        return "This is not allowed, sorry"


def show_resized_images():
    return None


config = load_config("environment.env")
