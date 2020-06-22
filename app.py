from flask import Flask, render_template, request
import Resizer

config = Resizer.config
application = Flask(__name__)
application.config["UPLOAD_FOLDER"] = str("upload_folder")


@application.route("/")
def hello_world():
    return render_template("index.html")


@application.route("/upload", methods=["GET", "POST"])
def upload_image():
    return Resizer.upload_image()


@application.route("/<int:order_id>")
def show_status(order_id):
    return Resizer.get_status(order_id)


@application.errorhandler(404)
def show_404():
    return render_template("error.html", page=request.base_url.split("//")[-1])


if __name__ == "__main__":
    application.run()
