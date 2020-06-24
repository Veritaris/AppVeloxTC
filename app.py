from flask import Flask, render_template, request
import Resizer

config = Resizer.config
secret = Resizer.secret
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = config("upload_folder")
app.config["SECRET_KEY"] = secret("secret_key")


@app.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_image():
    return Resizer.upload_image()


@app.route("/upload", methods=["GET"])
def show_upload():
    return Resizer.show_upload()


@app.route("/images", methods=["GET"])
def show_resized_images():
    return Resizer.show_resized_images()


@app.route("/upload/<int:order_id>", methods=["GET"])
def show_status(order_id):
    return Resizer.get_status(order_id)


@app.errorhandler(404)
def show_404(error):
    return render_template("error.html", page=request.base_url.split("//")[-1])


if __name__ == "__main__":
    app.run()
