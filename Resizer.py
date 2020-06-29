from DatabaseModels import ProcessedImages, Images, database
from werkzeug.exceptions import RequestEntityTooLarge
from logging.handlers import RotatingFileHandler
from flask import request, render_template
from werkzeug.utils import secure_filename
from multiprocessing import Process
from logging import Formatter
from flask import jsonify
from uuid import uuid4
from PIL import Image
from app import app
import logging
import random
import Config
import json
import os

cwd = Config.cwd
config = Config.config
session = database.session

handler = RotatingFileHandler(f"{cwd}/{config['logs_file']}", maxBytes=1000000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(Formatter('%(levelname)-8s %(asctime)s: %(message)s \t[in %(pathname)s:%(lineno)d]'))

logging.getLogger('werkzeug').setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# TESTING = app.testing
TESTING = True

def main_page():
    # return render_template("index.html")
    return jsonify({"status": "ok"}), 200


def is_file_allowed(filename: str) -> bool:
    """
    Check for file extension to be an image in .png or .jpg/.jpeg
    :param filename: string, filename with extension
    :return true or false
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config["allowed_extensions"]


def upload_image():
    """
    Uploading image to server and resizing it.
    Uploads image to /upload folder and write it name to database if succeed.
    After starts to resize it in the background using multiprocessing.Process
    :return http status 200 on succeed, 415 if file is not image and 413 if width, height or file
    was not provided
    """
    try:
        file = request.files.get("file")
    except RequestEntityTooLarge:
        logger.warning(f"User tried to upload file, but it was too large.")
        return jsonify({"error": "File is too large"}), 413
    if not file:
        logger.warning(f"User tried to upload file, but didn't provide a file.")
        return jsonify({"error": "No file to resize"}), 400

    width, height = request.form.get("width"), request.form.get("height")
    if not (width and height):
        logger.warning(f"User tried to upload file, but didn't provide width or height.")
        return jsonify({"error": "Not enough data to resize"}), 400
    width, height = map(int, (width, height))

    try:
        assert width in range(1, 10000)
    except AssertionError:
        logger.warning(f"User tried to upload file, but provided not allowed width")
        return jsonify({"error": f"Wrong width: {width} is not in range 1..9999"}), 400

    try:
        assert width in range(1, 10000)
    except AssertionError:
        logger.warning(f"User tried to upload file, but provided not allowed height")
        return jsonify({"error": f"Wrong width: {width} is not in range 1..9999"}), 400

    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        save_result = save_image(file, filename)

        if save_result[0]:
            internal_filename = save_result[1]
            password = random.random().hex().split(".")[-1][:8]
            image = Images(
                deleteImagePassword=password)
            session.add(image)
            session.commit()
            imageID = image.id

            resize_thread = Process(
                target=resize_image,
                args=(file, width, height, internal_filename, imageID)
            )
            resize_thread.start()

            return jsonify(
                {
                    "imageID": imageID,
                    "password": password,
                    "downloadURL": f"/static/resizedImages{internal_filename.split('.')[0]}_"
                                   f"{width}x{height}.{internal_filename.split('.')[-1]}"
                }
            ), 202

    if not is_file_allowed(file.filename):
        logger.warning(f"User tried to upload file, but it was not a png/jpg image: {file.filename}")
        return jsonify({"error": "Wrong file extension"}), 415


def save_image(file, filename):
    """
    Save image to /uploads folder
    :param file: file from form
    :param filename: string
    :return: True and internal filename if succeed, 500 error if something went wrong
    """
    ext = filename.split(".")[-1]
    if not TESTING:
        internal_filename = f"{str(uuid4().hex)}.{ext}"
    else:
        internal_filename = filename

    try:
        file.save(
            os.path.join(
                cwd, config['upload_folder'],
                internal_filename
            )
        )
    except Exception as e:
        logger.error(f"Error while tried to save file {internal_filename}")
        return jsonify({"error": "Sorry, file was not uploaded because of internal error"}), 500
    logger.info(f"Uploaded file {internal_filename}")
    return True, internal_filename


def resize_image(image, width, height, filename, imageID):
    """
    Resize image to given (width, height) and saves it, add a link for file uploading ot database
    :param filename:
    :param image: image file
    :param width: width to resize to
    :param height: height to resize to
    :param imageID: unique image id to write to database
    :return:
    """

    im = Image.open(image)
    size_from = im.size
    resized_image = im.resize((width, height))
    filename_without_ext, ext = filename.split(".")
    filename = f"{filename_without_ext}_{width}x{height}.{ext}"
    resized_image.save(f"{cwd}/static/resizedImages/{filename}")

    processed_image = ProcessedImages(
        id=imageID,
        imageFileName=filename,
        sizeFrom=f"{size_from[0]}x{size_from[1]}",
        sizeTo=f"{width}x{height}",
        resizeStatus="Succeed",
    )
    session.add(processed_image)
    session.commit()
    logger.info(f"Resized file {filename}")
    return None


def show_resized_images(image_id):
    """
    Show all images in database as json or image with specified id if given
    :return: json object of image with image_id or all images if image_id == None
    """
    if image_id:
        image = database.session.query(ProcessedImages).get(image_id)
        if image:
            logger.info(f"User requested file {image.imageFileName}")
            return jsonify(image.serialize), 200
        else:
            logger.warning(f"User requested file with id {image_id}, but it does not exists.")
            return jsonify({"error": f"No image with index {image_id} or it was deleted"}), 404
    else:
        if database.session.query(ProcessedImages).all():
            logger.info(f"User requested all images")
            return jsonify({
                "images": [
                    json.dumps(x.serialize) for x in session.query(ProcessedImages).all()
                ]
            }), 200
        else:
            logger.warning(f"User requested all images, but there is no one yet.")
            return jsonify({"error": "No images in database yet or they were deleted"}), 200


def delete_image(image_id):
    """
    Delete image on sever and from database if given password was correct
    :param image_id:
    :return:
    """
    image_images = session.query(Images).get(image_id)
    image_processed_images = session.query(ProcessedImages).get(image_id)

    if not image_images:
        return jsonify({"error": f"No image with index {image_id} or it was deleted"}), 404

    password = request.form.get("password")

    image_delete_password = session.query(Images).get(image_id).deleteImagePassword
    image_filename = image_processed_images.imageFileName

    if password == image_delete_password:
        os.remove(f"{cwd}/static/resizedImages/{image_filename}")
        os.remove(f"{cwd}/static/uploads/{image_filename.split('_')[0]}.{image_filename.split('.')[-1]}")
        session.delete(image_images)
        session.delete(image_processed_images)
        session.commit()
    logger .info(f"User deleted image with id {image_id}")
    return jsonify({"imageID": image_id, "status": "deleted"}), 200


def get_image(image_name):
    return render_template(
        "image.html",
        downloadURL=f"/static/uploads/{image_name}"
    )
