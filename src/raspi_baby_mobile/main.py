#!/usr/bin/env python3
import time

import cv2
import mediapipe as mp
import pigpio

import raspi_baby_mobile as rbm  # the helper module above

BUZZER_PIN = 18
SERVO_PIN = 12


def main(camera_index=0, poweron_selftest=True):
    # Connect to pigpiod only at runtime
    pi = pigpio.pi()
    if not pi.connected:  # fails in CI but nothing imports pigpio here
        print("❌ pigpiod not running")
        return  # pigpiod must be started in production
        # e.g. sudo systemctl start pigpiod
    try:
        if poweron_selftest:
            rbm.poweron_selftest(pi, SERVO_PIN, BUZZER_PIN)

        cap = cv2.VideoCapture(camera_index)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        if not cap.isOpened():
            rbm.buzzer_notification(pi, BUZZER_PIN, "no_camera")
            raise SystemExit(f"❌ Could not open camera {camera_index}")

        facemesh = mp.solutions.face_mesh.FaceMesh(max_num_faces=1)
        print("Facemesh initialised")
        pi.set_servo_pulsewidth(SERVO_PIN, 1500)  # centre

        while True:
            ok, frame = cap.read()
            if not ok:
                continue

            try:
                yaw = rbm.extract_head_orientation_from_frame(frame, facemesh)["yaw"]
                rotation = rbm.yaw_to_servo_rotation(yaw)
                pulse = rbm.rotation_to_pulse(rotation)
                pi.set_servo_pulsewidth(SERVO_PIN, pulse)
            except RuntimeError:  # no face
                pi.set_servo_pulsewidth(SERVO_PIN, 1500)
                rbm.buzzer_notification(pi, BUZZER_PIN, "no_face")

            time.sleep(0.5)
    finally:  # always clean up
        pi.set_servo_pulsewidth(SERVO_PIN, 0)  # stop pulses
        pi.stop()  # close socket


if __name__ == "__main__":
    main()
