#!/usr/bin/env python3

import cv2
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
    if not cap.isOpened():
        print(f"❌ Could not open camera {camera_index}")
        raspi_baby_mobile.buzzer_notification(buzzer, "no_camera")

    GPIO.cleanup()


if __name__ == "__main__":
    main()
