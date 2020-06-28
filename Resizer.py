from flask import request, redirect, render_template, flash
from DatabaseModels import ProcessedImages, Images, database
from werkzeug.utils import secure_filename
from multiprocessing import Process
from flask import jsonify
from uuid import uuid4
from PIL import Image
import Config
import json
import os

cwd = Config.cwd
config = Config.config
session = database.session


def is_file_allowed(filename):
    """
    Check for file extension to be an image in .png or .jpg/.jpeg
    :param filename: string, filename with extension
    :return true or false
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.list("allowed_extensions")


def upload_image():
    """
    Uploading image to server and resizing it.
    Uploads image to /upload folder and write it name to database if succeed.
    After starts to resize it in the background using multiprocessing.Process
    :return http status 200 on succeed, 403 if file is not image and 413 if width, height or file
    was not provided
    """
    if request.method == 'POST':
        # check if request contains a file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # check if request contains width and height to resize
        if request.form.get("width") and request.form.get("height"):
            width, height = request.form["width"], request.form["height"]
        else:
            return "Not enough data to resize, sorry", 413

        if file and is_file_allowed(file.filename):
            filename = secure_filename(file.filename)
            save_result = save_image(file, filename)

            if save_result[0]:
                internal_filename = save_result[1]
                image = Images(imageFileName=internal_filename)
                session.add(image)
                session.commit()
                imageID = image.id

                resize_thread = Process(target=resize_image, args=(file, int(width), int(height), internal_filename, imageID))
                resize_thread.start()

                return render_template(
                    "uploaded_image.html",
                    imageID=imageID,
                    downloadURL=f"./uploads/{internal_filename}")

        if not is_file_allowed(file.filename):
            return "Wrong file extension", 403

    return "uploaded", 200


def save_image(file, filename):
    """
    Save image to /uploads folder
    :param file: file from form
    :param filename: string
    :return: True and internal filename if succeed, 500 error if something went wrong
    """
    ext = filename.split(".")[-1]
    internal_filename = f"{str(uuid4().hex)}.{ext}"

    try:
        file.save(
            os.path.join(
                cwd, config.str('upload_folder'),
                internal_filename
            )
        )
    except Exception as e:
        return "Sorry, file was not uploaded because of internal error", 500
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
    resized_image.save(f"{cwd}/resizedImages/{filename}")

    processed_image = ProcessedImages(
        id=imageID,
        imageFileName=filename,
        sizeFrom=f"{size_from[0]}x{size_from[1]}",
        sizeTo=f"{width}x{height}",
        resizeStatus="Succeed",
        downloadFileURL=f"./uploads/{filename}"
    )
    session.add(processed_image)
    session.commit()
    return None


def show_resized_images(image_id):
    """
    Show all images in database as json or image with specified id if given
    :return: json object of image with image_id or all images if image_id == None
    """
    if image_id:
        image = database.session.query(ProcessedImages).get(image_id)
        if image:
            return jsonify(image.serialize), 200
        else:
            return f"No image with index {image_id}", 404
    else:
        return jsonify({
            "images": [
                json.dumps(x.serialize) for x in session.query(ProcessedImages).all()
            ]
        }), 200


def delete_image(image_id):
    """
    Delete image on sever and from database if given password was correct
    :param image_id:
    :return:
    """
    image = database.session.query(ProcessedImages).get(image_id)
    if not image:
        return f"No image with index {image_id}", 404
    password = request.form.get("password")
    return None
