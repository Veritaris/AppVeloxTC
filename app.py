from flask import Flask, render_template, request
import Resizer

config = Resizer.config
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str("upload_folder")


@app.route("/")
def hello_world():
    return render_template("main.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    return Resizer.upload_image()


@app.route("/<int:order_id>")
def show_status(order_id):
    return Resizer.get_status(order_id)


@app.errorhandler(404)
def show_404(error):
    return render_template("error.html", page=request.base_url.split("//")[-1])


if __name__ == "__main__":
    app.run()
