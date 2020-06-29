from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import Config

config = Config.config
secret = Config.secret
cwd = Config.cwd

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{cwd}{config['sqlalchemy_database_uri']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config["sqlalchemy_track_modifications"]
app.config["UPLOAD_FOLDER"] = config["upload_folder"]
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["SECRET_KEY"] = secret["secret_key"]
app.config["LOGFILE"] = config["logs_file"]


database = SQLAlchemy(app)
migrate = Migrate(app, database)

import DatabaseModels
import Resizer


@app.route("/", methods=["GET", "POST"])
def hello_world():
    """
    Render web app main page if method==GET and refuse if other
    :return:
    """

    response = make_response()
    response.status_code = 405
    response.headers = {"Allow": ["GET"]}
    if request.method == "GET":
        return render_template("index.html")
    else:
        return response


@app.route("/upload", methods=["POST"])
def upload_image():
    """
    Uploads an image to server and write to database
    Necessary parameters:
    file – a file to upload
    width – image width to resize to
    height – image width to resize to
    """
    return Resizer.upload_image()


@app.route("/upload", methods=["GET"])
def show_resized_image():
    """
    Return JSON object with all processed images from database
    """
    return Resizer.show_resized_images(None)


@app.route("/upload/<int:image_id>", methods=["GET"])
def show_images(image_id):
    """
    Return JSON object of precessed image with given image_id and 404 status if
    there is no image with such id
    """
    return Resizer.show_resized_images(image_id)


@app.route("/upload/<string:image_name>", methods=["GET"])
def show_image(image_name):
    """
    Render image with filename if it exists on server
    :param image_name: image filename on server
    """
    return Resizer.get_image(image_name)


@app.route("/upload/<int:image_id>", methods=["DELETE"])
def delete_image(image_id):
    """
    Delete image with given id on server and from database. Requires password
    """
    return Resizer.delete_image(image_id)


@app.errorhandler(404)
def show_404(error):
    """
    Render error page if user tries to visit page that does not exists
    """
    return render_template("error.html", page=request.base_url.split("//")[-1])
