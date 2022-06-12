from tkinter.ttk import Frame, Button, Label
from tkinter.messagebox import showwarning
from cv2 import VideoCapture, imwrite
from manager import Manager
from google.cloud import vision
from datetime import datetime
from models import Activity, Emotion
from time import sleep
from simpleaudio import WaveObject
from simpleaudio import stop_all as stop_audio
from queue import Queue
from os import environ
environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
player = WaveObject.from_wave_file("alarma.wav")


emotion_types = ["joy", "sorrow", "anger", "surprise"]


class FocusTab(Frame):
    def __init__(self, *args):
        super().__init__(*args)

        self.init_ui()
        self.system_clock = datetime(2022, 11, 6, 20)  # datetime.today()
        def f():
            self.system_clock = datetime(2022, 11, 6, 21)

        self.after(60000, f)
        self.activities = Queue(
            sorted(
                filter(
                    lambda e: e.date >= self.system_clock.date(), Manager().activities
                ),
                key=lambda e: e.date,
            )
        )
        #print(self.activities.queue)
        self.current_activity = None

        self.concentration_running = True
        self.emotions_running = True
        self.alive = True

        self.activities_worker()

        # self.concentration_job = RepatedTimer(1, self.concentration_worker)
        self.emotions_worker()
        self.concentration_worker()

    def init_ui(self):
        self.pack(fill="both", expand=True)

        Label(self, text="Toggle focus tracking").grid(column=1, row=1)
        Button(self, command=self.toggle_status, text="Toggle").grid(column=2, row=1)

    def clock_ticker(self):
        self.system_clock = datetime.today()
        self.after(1000, self.clock_ticker)

    def toggle_status(self):
        self.concentration_running = not self.concentration_running

    def killall(self):
        self.concentration_running = False
        self.emotions_running = False
        self.alive = False
        self.camera.release()

    def activities_worker(self):
        top: Activity = self.activities.peek()
        if top:
            if top.end < self.system_clock.time():
                self.activities.remove()  # remove last activity
            elif (
                top.date == self.system_clock.date()
                and top.start <= self.system_clock.time() <= top.end
            ):
                self.current_activity = self.activities.remove()
        if self.alive:
            self.after(500, self.activities_worker)

    def emotions_worker(self):
        if self.emotions_running and self.current_activity:
            data = analyze_face('emotions')
            l = len(data.face_annotations)

            if not l:
                showwarning(
                    title="Warning",
                    message="You're not currently paying attention!",
                )
            elif l > 1:
                showwarning(
                    title="Too much people",
                    message="There's too many people in the camera's view",
                )
            else:
                data = normalize_data(data.face_annotations[0])
                for emotion in emotion_types:
                    da = (emotion, data[f"{emotion}_likelihood"])
                    if not self.current_activity.emotions:
                        self.current_activity.emotions = Emotion(*da)
                        continue
                    self.current_activity.emotions.insert(Emotion(*da))

        if self.alive:
            self.after(60000, self.emotions_worker)

    def concentration_worker(self):
        if self.concentration_running:
            res = analyze_face()

            if res.face_annotations and not (
                -30 < res.face_annotations[0].pan_angle < 30
            ):
                should_play = True
                cicles = 0
                while cicles != 30:
                    res = analyze_face()
                    if (
                        res.face_annotations
                        and -30 < res.face_annotations[0].pan_angle < 30
                    ):
                        should_play = False
                        break
                    cicles += 5
                    sleep(5)
                if should_play:
                    player.play()
                    showwarning(
                        title="You're too distracted",
                        message="Please keep your eyes on the screen or pointing towards the camera",
                    )
                    stop_audio()

        if self.alive:
            self.after(30000, self.concentration_worker)


camera = VideoCapture(0)
annotator_client = vision.ImageAnnotatorClient()

def analyze_face(path="pictures"):
    could, data = camera.read()
    if could: # TODO: actually do something if could is False
        imwrite(f"./{path}/out.png", data)

        with open(f"./{path}/out.png", "rb") as d:
            img = vision.Image(content=d.read())

    return annotator_client.face_detection(img)
def normalize_data(face_annotations) -> dict:
    return {
        "joy_likelihood": face_annotations.joy_likelihood.value,
        "anger_likelihood": face_annotations.anger_likelihood.value,
        "sorrow_likelihood": face_annotations.sorrow_likelihood.value,
        "surprise_likelihood": face_annotations.surprise_likelihood.value,
    }
