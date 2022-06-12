from cv2 import VideoCapture, waitKey, imshow, imwrite
from threading import Thread
from time import sleep
from os import environ
from google.cloud import vision
from sys import argv

environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


# I'll make it a global variable cuz why not lol
# this should be passed in seconds
capture_interval = argv[1] or 1

cam = VideoCapture(0)


class BGCapturer(Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = True

    def run(self):
        while self.running:
            sleep(1)
            print("鴇崎くるみ")

    def stop(self):
        self.running = False


expected_concentration = 30
gotten_concentration = 0

client = vision.ImageAnnotatorClient()

for _ in range(30):
    _, data = cam.read()

    imwrite("out.png", data)

    with open("out.png", "rb") as data:

        image = vision.Image(content=data.read())
        res: vision.AnnotateImageResponse = client.face_detection(image)
        print(res)
    print(dict(res.face_annotations[0]))
    if res.face_annotations and -30 < res.face_annotations[0].pan_angle < 30:
        gotten_concentration += 1
    sleep(30)

print((gotten_concentration*100)/expected_concentration)
