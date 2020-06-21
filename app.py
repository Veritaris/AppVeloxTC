from flask import Flask
import Resizer

config = Resizer.config
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str("upload_folder")


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    return Resizer.upload_image()


@app.route("/<int:order_id>")
def show_status(order_id):
    return Resizer.get_status(order_id)


if __name__ == "__main__":
    app.run()
