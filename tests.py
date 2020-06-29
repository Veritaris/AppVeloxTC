import app as app_to_test
from Resizer import cwd
from faker import Faker
import unittest
import requests
import os
import sys

fake = Faker()


testImagesDir = os.path.join(os.path.curdir, "testImages")
uploadsDir = os.path.join(os.path.curdir, "uploads")
resizedImagesDir = os.path.join(os.path.curdir, "resizedImages")

for _dir in [uploadsDir, resizedImagesDir]:
    for _file in os.listdir(_dir):
        os.remove(os.path.join(_dir, _file))


def upload_image(file):
    with open(os.path.join(testImagesDir, file), 'rb') as f:
        files = {
            "file": f
        }
        data = {
            "width": fake.random.randint(-50, 9999),
            "height": fake.random.randint(-50, 9999)
        }
        # Setting verifying ssl to false because of self-signed certificate
        p = requests.post(f"{url}/upload", files=files, verify=False, data=data)
        return p.status_code, p.content, p.url


def test_upload():
    if ".DS_Store" in os.listdir(testImagesDir):
        os.remove(os.path.join(testImagesDir, ".DS_Store"))
    test_amount = len(os.listdir(testImagesDir))
    passed_tests = 0
    failed_tests = {}
    failed_tests_extended = {}
    for i, file in enumerate(os.listdir(testImagesDir)):
        print(75*"=")
        if file != ".DS_Store":
            tmp = ""
            print(f"Passing test {i + 1} of {test_amount}")
            print(f"\tUploading {file}...")
            p = upload_image(file)
            print(f"\t{p[2]}")
            if p[0] == 200:
                print(f"\t{file} uploaded...")
            try:
                with open(os.path.join(testImagesDir, file), 'rb') as test_file:
                    with open(os.path.join(uploadsDir, file), 'rb') as uploaded_file:
                        if test_file.read() == uploaded_file.read():
                            print("\tPassed!")
                            passed_tests += 1
                        else:
                            failed_tests[i + 1] = [p[0], p[1].decode()]
                            failed_tests_extended[i + 1] = (f"\tPassing test {i + 1} of {test_amount}"
                                                            f"\t\tUploading {file}..."
                                                            f"\t\t\t{p[2]}")
                            print("\tFailed!")
            except FileNotFoundError:
                failed_tests[i + 1] = [p[0], p[1].decode()]
                print(f"\tTest {i + 1} failed: file was not uploaded")
                failed_tests_extended[i + 1] = (f"\tPassing test {i + 1} of {test_amount}"
                                                f"\t\tUploading {file}..."
                                                f"\t\t\t{p[2]}")
    print(75*"=")
    print(f"Tests passed: {passed_tests}")
    print(f"Tests failed: {test_amount - passed_tests}")
    # for k, v in failed_tests.items():
    #     print(f"\tTest {k}: \n"
    #           f"\tserver responded with status code {v[0]} and returned \"{v[1]}\"\n"
    #           f"\t\tExtended traceback:\n"
    #           f"\t\t{failed_tests_extended[k]}")
    # print(failed_tests_extended)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    elif cwd.split("/")[-2] == "Work":
        url = "http://127.0.0.1:5000"
    else:
        url = "https://167.71.58.132"
    test_upload()
