from tkinter.ttk import Frame, Button, Label
from repeater import RepatedTimer
from cv2 import VideoCapture, imwrite

from google.cloud import vision


class FocusTab(Frame):
    def __init__(self, *args):
        super().__init__(*args)

        self.init_ui()

        self.camera = VideoCapture(0)
        self.annotator_client = vision.ImageAnnotatorClient()
        self.running = False
        self.alive = True
        # self.concentration_job = RepatedTimer(1, self.concentration_worker)
        self.concentration_worker()

    def init_ui(self):
        self.pack(fill="both", expand=True)

        Label(self, text="Toggle focus tracking").grid(column=1, row=1)
        Button(self, command=self.toggle_status, text="Toggle").grid(column=2, row=1)

    def toggle_status(self):
        self.running = not self.running

    def killall(self):
        self.running = False
        self.alive = False
        self.camera.release()

    def concentration_worker(self):
        if self.running:
            could, data = self.camera.read()
            if could:
                imwrite("./pictures/out.png", data)

                with open("./pictures/out.png", "rb") as data:
                    image = vision.Image(content=data.read())
                    res = self.annotator_client.face_detection(image)
                print("Me cago en la puta")

        if self.alive:
            self.after(1000, self.concentration_worker)
