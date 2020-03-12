import cv2
from threading import Thread


class Camera:

    def __init__(self, resolution=(640, 480), framerate=30):
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoCapture_fourcc(*'MJPG1'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])

        self.grabbed, self.frame = self.stream.read()

        self.stopped = False

    def start(self):
        Thread(target=self.update, agrs=())
        return self

    def update(self):
        while not self.stopped:
            self.grabbed, self.frame = self.stream.read()

        self.stream.release()

    def read_frame(self):
        return self.frame

    def end(self):
        self.stopped = True
