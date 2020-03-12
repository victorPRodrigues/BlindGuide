import cv2
import os
import numpy as np
import sys
import importlib.util


class Detector:

    def __init__(self):
        self.model = '/pi/Desktop/BlindGuide/model'
        self.graph = 'detect.tflite'
        self.label_map = 'l_map.txt'
        self.threshold = 0.5
        self.imWidth = 1280
        self.imHeight = 720

        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime.interpreter import Interpreter
        else:
            from tensorflow.lite.python.interpreter import Interpreter

        self.model_path = os.join(self.model, self.graph)
        self.labels_path = os.join(self.model, self.label_map)

        with open(self.labels_path, 'r') as l:
            self.labels = [line.strip() for line in l.readlines()]

        if self.labels[0] == '???':
            del(self.labels[0])

        self.interpreter = Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_dets = self.interpreter.get_input_details()
        self.output_dets = self.interpreter.get_output_details()
        self.height = self.input_dets[0]['shape'][1]
        self.width = self.input_dets[0]['shape'][2]
        self.is_floating_model = self.input_dets[0]['dtype'] == np.float32
        self.input_mean = 127.5
        self.input_std = 127.5
        self.frame_rate = 1
        self.frequency = cv2.getTickFrequency()
