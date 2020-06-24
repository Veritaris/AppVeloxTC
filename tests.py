import unittest
import requests
import app as app_to_test
import os
import sys

testImagesDir = os.path.join(os.path.curdir, "testImages")
uploadsDir = os.path.join(os.path.curdir, "uploads")


class TestFlaskApp(unittest.TestCase):
    def setUp(self) -> None:
        app_to_test.config["TESTING"] = True
        self.app = app_to_test.app.test_client()


def upload_image(file):
    with open(os.path.join(testImagesDir, file), 'rb') as f:
        files = {
            "file": f
        }
        p = requests.post(f"{url}/upload", files=files, verify=False)  # Setting verifying ssl to false because of self-signed cerificate
        return p.status_code, p.content


def test_upload():
    if ".DS_Store" in os.listdir(testImagesDir):
        os.remove(os.path.join(testImagesDir, ".DS_Store"))
    test_amount = len(os.listdir(testImagesDir))
    passed_tests = 0
    failed_tests = {}
    for i, file in enumerate(os.listdir(testImagesDir)):
        print(75*"=")
        if file != ".DS_Store":
            print(f"Passing test {i + 1} of {test_amount}")
            print(f"\tUploading {file}...")
            p = upload_image(file)
            if p[0] == 200:
                print(f"\t{file} uploaded...")
            try:
                with open(os.path.join(testImagesDir, file), 'rb') as test_file:
                    with open(os.path.join(uploadsDir, file), 'rb') as uploaded_file:
                        if test_file.read() == uploaded_file.read():
                            print("\tPassed!")
                            passed_tests += 1
                        else:
                            failed_tests[i] = [p[0], p[1].decode()]
                            print("\tFailed!")
            except FileNotFoundError:
                failed_tests[i] = [p[0], p[1].decode()]
                print(f"\tTest {i + 1} failed: file was not uploaded")
    print(75*"=")
    print(f"Tests passed: {passed_tests}")
    print(f"Tests failed: {test_amount - passed_tests}")
    for k, v in failed_tests.items():
        print(f"\tTest {k}: server responded with status code {v[0]} and returned \"{v[1]}\"")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://167.71.58.132"
    test_upload()
