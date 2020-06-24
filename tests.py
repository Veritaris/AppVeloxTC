import requests
import os
import sys

testImagesDir = os.path.join(os.path.curdir, "testImages")
uploadsDir = os.path.join(os.path.curdir, "uploads")
url = sys.argv[1]


def upload_image(file):
    with open(os.path.join(testImagesDir, file), 'rb') as f:
        files = {
            "file": f
        }
        p = requests.post(f"{url}", files=files)


def test_upload():
    if ".DS_Store" in os.listdir(testImagesDir):
        os.remove(os.path.join(testImagesDir, ".DS_Store"))
    test_amount = len(os.listdir(testImagesDir))
    passed_tests = 0
    for i, file in enumerate(os.listdir(testImagesDir)):
        if file != ".DS_Store":
            print(f"Passing test {i + 1} of {test_amount}")
            print(f"\tUploading {file}...")
            upload_image(file)
            print(f"\t{file} uploaded...")
            with open(os.path.join(testImagesDir, file), 'rb') as test_file:
                with open(os.path.join(uploadsDir, file), 'rb') as uploaded_file:
                    if test_file.read() == uploaded_file.read():
                        print("\tPassed!")
                        passed_tests += 1
                        print(passed_tests)
                    else:
                        print("\tFailed!")
    print(f"Tests passed: {passed_tests}")
    print(f"Tests failed: {test_amount - passed_tests}")


test_upload()
