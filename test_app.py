from Resizer import database, ProcessedImages, Images
from random import choice, randint
from app import app
import unittest
import PIL
import os
import io

images = os.listdir("./testImages")


class TestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_main(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200, "Expected code 200")

    def test_upload(self):
        i = choice(images)
        with open(f"./testImages/{i}", "rb") as f:
            data = {
                "width": randint(-500, 10500),
                "height": randint(-500, 10500),
                "file": (f.read(), i)
            }
            try:
                result = self.app.post("/upload", content_type='multipart/form-data', data=data)

                self.assertEqual(result.status_code, 202)
            except PIL.UnidentifiedImageError:
                pass

    def test_get_single_image(self):
        result = self.app.get(f"/upload/{randint(-1, 100)}")
        self.assertEqual(result.status_code, 200)

    def test_get_all_images(self):
        result = self.app.get("/upload")
        self.assertEqual(result.status_code, 200)

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
    TestCase.me
