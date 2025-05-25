import math
import time

import cv2
import numpy as np


def buzzer_beep(buzzer, count):
    for _ in range(count):
        buzzer.start(8)
        time.sleep(0.2)
        buzzer.ChangeDutyCycle(0)
        time.sleep(0.2)
    buzzer.stop()


def buzzer_notification(buzzer, type):
    if type == "startup":
        buzzer_beep(buzzer, 4)
    elif type == "no_servo":
        while True:
            buzzer_beep(buzzer, 2)
            time.sleep(1)
    elif type == "no_camera":
        while True:
            buzzer_beep(buzzer, 3)
            time.sleep(1)
    elif type == "no_face":
        while True:
            buzzer_beep(buzzer, 1)
            time.sleep(1)
    else:
        TypeError("Unsupported buzzer error type")


def poweron_selftest(buzzer, servo):
    """4 beeps + 4 servo twitches (L-R-L-R) to verify wiring."""

    buzzer_notification(buzzer=buzzer, type="startup")

    servo.start(7.5)
    for i in range(4):
        duty = 6.0 if i % 2 == 0 else 9.0
        servo.ChangeDutyCycle(duty)
        time.sleep(0.25)
        servo.ChangeDutyCycle(7.5)
        time.sleep(0.25)
    servo.stop()


def extract_head_orientation_from_frame(frame_bgr, facemesh):
    """
    Fast yaw-only estimate from a single BGR frame.
    Expects an *open* mediapipe.solutions.face_mesh.FaceMesh instance.
    Returns {"yaw": degrees}
    """

    # helper: convert normalized landmark → pixel coordinates
    def _px(lmk, w, h):
        return np.array([lmk.x * w, lmk.y * h], dtype=np.float32)

    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    res = facemesh.process(rgb)
    if not res.multi_face_landmarks:
        raise RuntimeError("No face detected")

    # landmark indices (kept local)
    idx_nose_tip = 1  # nose tip
    idx_eye_left = 33  # outer left eye corner
    idx_eye_right = 263  # outer right eye corner

    lmk = res.multi_face_landmarks[0].landmark
    h, w = rgb.shape[:2]

    nose = _px(lmk[idx_nose_tip], w, h)
    eye_l = _px(lmk[idx_eye_left], w, h)
    eye_r = _px(lmk[idx_eye_right], w, h)

    # horizontal displacement of nose, scaled by half the eye distance
    eye_mid_x = (eye_l[0] + eye_r[0]) * 0.5
    ipd = abs(eye_r[0] - eye_l[0]) + 1e-6  # avoid divide-by-zero
    ratio = (nose[0] - eye_mid_x) / (0.5 * ipd)

    yaw_deg = math.degrees(math.asin(max(-1.0, min(1.0, ratio))))
    return {"yaw": yaw_deg}


def yaw_to_servo_rotation(yaw_deg, dead_band=10, end_band=35):
    """
    Map yaw angle (degrees) to a normalised rotation score in [-100, 100].
    """
    if abs(yaw_deg) <= dead_band:
        return 0.0

    if yaw_deg < 0:  # head turned left
        if yaw_deg <= -end_band:
            return -100.0
        return (yaw_deg + dead_band) / -(end_band - dead_band) * 100
    else:  # head turned right
        if yaw_deg >= end_band:
            return 100.0
        return (yaw_deg - dead_band) / (end_band - dead_band) * 100


def rotation_to_duty(rotation_score):
    return 7.5 + (rotation_score / 100.0) * 1.5  # 7.5 % ±1.5 %
