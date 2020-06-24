from werkzeug.utils import secure_filename
from flask import request, redirect, url_for, render_template, flash
from envparse import Env
from flask import json
import sqlite3
import os


def load_config(path: str):
    env = Env(
        upload_folder=str,
        allowed_extention=list
    )
    env.read_envfile(path)
    return env


cwd = os.getcwd()
config = load_config(f"{cwd}/environment.env")
secret = load_config(f"{cwd}/secrets.env")


def get_status(order_id):
    """
    Get resize order status from DB and return it's value
    :param order_id:
    :return: order status
    """
    return f"Status of {order_id}"


def is_file_allowed(filename):
    """

    :param filename:
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.list("allowed_extensions")


def upload_image():
    """

    :return:
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and is_file_allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(cwd, config.str('upload_folder'), filename))
            return redirect(url_for('upload_image',
                                    filename=filename))
        if not is_file_allowed(file.filename):
            return "Wrong file extension", 403
    return "uploaded"


def show_resized_images():
    """

    :return:
    """
    return None


def show_upload():
    """

    :return:
    """
    return "ok"
