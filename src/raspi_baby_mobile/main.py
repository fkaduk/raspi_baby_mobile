#!/usr/bin/env python3

import time

import cv2
import mediapipe as mp
import RPi.GPIO as GPIO

import raspi_baby_mobile

BUZZER_PIN = 18
SERVO_PIN = 12


def main(camera_index=0, poweron_selftest=True):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([BUZZER_PIN, SERVO_PIN], GPIO.OUT)
    buzzer = GPIO.PWM(BUZZER_PIN, 2_000)
    servo = GPIO.PWM(SERVO_PIN, 50)

    if poweron_selftest:
        raspi_baby_mobile.poweron_selftest(buzzer, servo)

    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    if not cap.isOpened():
        print(f"❌ Could not open camera {camera_index}")
        raspi_baby_mobile.buzzer_notification(buzzer, "no_camera")

    facemesh = mp.solutions.face_mesh.FaceMesh(max_num_faces=1)
    print("Facemesh initialized")
    servo.start(7.5)
    while True:
        ok, frame = cap.read()
        if not ok:
            continue
            print("Frame not captured")

        try:
            print("Extracting facial landmarks...")
            yaw = raspi_baby_mobile.extract_head_orientation_from_frame(frame, facemesh)["yaw"]
            print(f"Detected yaw: {yaw:.2f}°")
        except RuntimeError:
            servo.ChangeDutyCycle(7.5)
            raspi_baby_mobile.buzzer_notification(buzzer, "no_face")
            print("Could not detect face")
            continue

        try:
            rotation = raspi_baby_mobile.yaw_to_servo_rotation(yaw)
            duty = raspi_baby_mobile.rotation_to_duty(rotation)
            print(f"Setting servo to: {duty:.2f}")
            servo.ChangeDutyCycle(duty)
        except Exception:
            print("Error setting servo")

        time.sleep(0.5)


if __name__ == "__main__":
    main()
