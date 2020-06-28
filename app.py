from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import Config

config = Config.config
secret = Config.secret
cwd = Config.cwd

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = config("upload_folder")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{cwd}{config('sqlalchemy_database_uri')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.bool("sqlalchemy_track_modifications")
app.config["SECRET_KEY"] = secret("secret_key")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

database = SQLAlchemy(app)
migrate = Migrate(app, database)

import DatabaseModels
import Resizer


@app.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_image():
    return Resizer.upload_image()


@app.route("/upload", methods=["GET"])
def show_resized_images():
    return Resizer.show_resized_images(None)


@app.route("/upload/<int:image_id>", methods=["GET"])
def show_status(image_id):
    return Resizer.show_resized_images(image_id)


@app.route("/upload/<int:image_id>", methods=["DELETE"])
def delete_image(image_id):
    return Resizer.delete_image(image_id)


@app.errorhandler(404)
def show_404(error):
    return render_template("error.html", page=request.base_url.split("//")[-1])
