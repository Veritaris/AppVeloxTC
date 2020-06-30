from Resizer import database, ProcessedImages, Images
from random import choice, randint
from io import BytesIO
from PIL import Image
from app import app
import unittest
import os


images = os.listdir("./testImages")


class TestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.i = choice(images)
        self.app = app.test_client()

    def test_main(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200, "Expected code 200")

    def test_main_post(self):
        result = self.app.post("/")
        self.assertEqual(result.status_code, 405)
        self.assertEqual(result.headers["Allow"], "GET")

    def test_upload(self):
        with open(os.path.join(os.getcwd(), "testImages", self.i), "rb") as f:
            data = {
                "width": randint(1, 9999),
                "height": randint(1, 9999),
                "file": (f, "test_image.png")
            }
            result = self.app.post("/upload", content_type="multipart/form-data", data=data)
            self.assertEqual(result.status_code, 202)
            self.assertIsNotNone(result.json["imageID"])

    def test_upload_no_file(self):
        data = {
            "width": randint(1, 9999),
            "height": randint(1, 9999)
        }
        result = self.app.post("/upload", content_type="multipart/form-data", data=data)
        self.assertEqual(result.status_code, 400)
        self.assertIsNotNone(result.json["error"], "No file to resize")

    def test_failed_extension(self):
        with open(os.path.join(os.getcwd(), "testImages", self.i), "rb") as f:
            data = {
                "width": randint(1, 9999),
                "height": randint(1, 9999),
                "file": (f, "test_image.txt")
            }
            result = self.app.post("/upload", content_type="multipart/form-data", data=data)
            self.assertEqual(result.status_code, 415)
            self.assertEqual(result.json["error"], "Wrong file extension")

    def test_not_enough_data(self):
        with open(os.path.join(os.getcwd(), "testImages", self.i), "rb") as f:
            data = {
                "width": randint(1, 9999),
                "file": (f, "test_image.png")
            }
            result = self.app.post("/upload", content_type="multipart/form-data", data=data)
            self.assertEqual(result.status_code, 400)
            self.assertEqual(result.json["error"], "Not enough data to resize")

    def test_wrong_width(self):
        with open(os.path.join(os.getcwd(), "testImages", self.i), "rb") as f:
            data = {
                "width": 10001,
                "height": randint(1, 9999),
                "file": (f, "test_image.png")
            }
            result = self.app.post("/upload", content_type="multipart/form-data", data=data)
            self.assertEqual(result.status_code, 400)
            self.assertIsNotNone(
                result.json["error"],
                "Wrong width: {10500} is not in range 1..9999"
            )

    def test_wrong_height(self):
        with open(os.path.join(os.getcwd(), "testImages", self.i), "rb") as f:
            data = {
                "width": randint(1, 9999),
                "height": 10001,
                "file": (f, "test_image.png")
            }
            result = self.app.post("/upload", content_type="multipart/form-data", data=data)
            self.assertEqual(result.status_code, 400)
            self.assertIsNotNone(
                result.json["error"],
                "Wrong height: {10500} is not in range 1..9999"
            )

    def test_get_single_image(self):
        result = self.app.get(f"/upload/{randint(-1, 100)}")
        self.assertEqual(result.status_code, 200)

    def test_get_single_image_with_negative_index(self):
        result = self.app.get(f"/upload/-1")
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.json["error"], "No such file or page")

    def test_get_not_existing_index(self):
        result = self.app.get(f"/upload/{1000000}")
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.json["error"], f"No image with index {1000000} or it was deleted")

    def test_get_all_images(self):
        result = self.app.get("/upload")
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.json["images"])

    def test_delete_image(self):
        i = randint(-1, 100)
        password = database.session.query(Images).get(i)
        data = {
            "password": password
        }
        result = self.app.delete(f"/upload/{i}", data=data)
        self.assertEqual(result.status_code, 200)


if __name__ == "__main__":
    unittest.main()
