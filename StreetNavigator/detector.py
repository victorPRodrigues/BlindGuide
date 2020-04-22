import cv2
import os
import numpy as np
import sys
import importlib.util
import time
from pi_cam import PiCamera
from gps_tracker import play_sound_notification

def street_crosser():
    play_sound_notification("look_right")
    time.sleep(0.01)
    verification(5)
    time.sleep(0.01)
    play_sound_notification("look_left")
    verification(5)
    play_sound_notification("all_clear")



def verification(limit):
    timer = time.time()
    done = 0 
    while timer < limit:
        detected = approximation()
        if detected:
            play_sound_notification("waiting")
            limit += timer

        timer = time.time()



def approximation():
    MODEL_NAME = 'obj_detection_tflite'
    GRAPH_NAME = 'detect.tflite'
    LABELMAP_NAME = 'labelmap.txt'
    min_conf_threshold = 0.6
    imW, imH = 1280, 720

    pkg = importlib.util.find_spec('tflite_runtime')
    if pkg:
        from tflite_runtime.interpreter import Interpreter

    else:
        from tensorflow.lite.python.interpreter import Interpreter

    CWD_PATH = os.getcwd()

    PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)
    PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    if labels[0] == '???':
        del (labels[0])

    interpreter = Interpreter(model_path=PATH_TO_CKPT)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    pi_camera = PiCamera(resolution=(imW, imH), framerate=30).start()
    time.sleep(1)

    p_height = 0
    p_width = 0
    detections = 0
    approximation_detected = False
    while True:
        frame1 = pi_camera.read()

        frame = frame1.copy()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)

        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        boxes = interpreter.get_tensor(output_details[0]['index'])[0]  # Bounding box coordinates of detections objects
        classes = interpreter.get_tensor(output_details[1]['index'])[0]  # Class index of detections objects
        scores = interpreter.get_tensor(output_details[2]['index'])[0]  # Confidence of detections objects

        for i in range(len(scores)):

            if (scores[i] > min_conf_threshold) and (scores[i] <= 1.0):
                y_min = int(max(1, (boxes[i][0] * imH)))
                x_min = int(max(1, (boxes[i][1] * imW)))
                y_max = int(min(imH, (boxes[i][2] * imH)))
                x_max = int(min(imW, (boxes[i][3] * imW)))
                object_name = labels[int(classes[i])]

                if object_name == 'car' or object_name == 'bus' or object_name == 'truck':
                    detections += 1
                    if (y_max - y_min) > p_height * 1.15 or (x_max - x_min) > p_width * 1.15\
                            and detections > 1:
                        return True

                    p_height = y_max - y_min
                    p_width = x_max - x_min

    cv2.destroyAllWindows()
    PiCamera.stop()
