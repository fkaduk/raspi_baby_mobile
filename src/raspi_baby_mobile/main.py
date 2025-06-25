#!/usr/bin/env python3

import cv2
import mediapipe as mp
import pigpio

import raspi_baby_mobile as rbm

BUZZER_PIN = 18
SERVO_PIN = 12


def main(camera_index=0, poweron_selftest=True):
    pi = pigpio.pi()
    if not pi.connected:
        print("❌ pigpiod not running, start with `sudo systemctl start pigpiod`")
        return
    try:
        if poweron_selftest:
            rbm.poweron_selftest(pi, SERVO_PIN, BUZZER_PIN)

        cap = cv2.VideoCapture(camera_index)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not cap.isOpened():
            rbm.buzzer_notification(pi, BUZZER_PIN, "no_camera")
            raise SystemExit(f"❌ Could not open camera {camera_index}")

        facemesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=False,  # 468 pts instead of 478
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        print("Facemesh initialised", flush=True)
        pi.set_servo_pulsewidth(SERVO_PIN, 1500)  # center

        while True:
            ok, frame = cap.read()
            if not ok:
                continue

            try:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
                yaw = rbm.extract_head_orientation_from_frame(frame, facemesh)["yaw"]
                rotation = rbm.yaw_to_servo_rotation(yaw)
                pulse = rbm.rotation_to_pulse(rotation)
                pi.set_servo_pulsewidth(SERVO_PIN, pulse)
            except RuntimeError:  # no face
                pi.set_servo_pulsewidth(SERVO_PIN, 1500)
                rbm.buzzer_notification(pi, BUZZER_PIN, "no_face")
                print("No face detected", flush=True)

    finally:
        pi.set_servo_pulsewidth(SERVO_PIN, 0)
        pi.stop()


if __name__ == "__main__":
    main()
