from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
    """
    Render web app main page
    :return:
    """
    return render_template("index.html")


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
    return Resizer.get_image(image_name)


@app.route("/upload/<int:image_id>", methods=["DELETE"])
def delete_image(image_id):
    print("deleting")
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
