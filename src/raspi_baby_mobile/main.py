#!/usr/bin/env python3
import time

import RPi.GPIO as GPIO

BUZZER_PIN = 18
SERVO_PIN = 12


def poweron_selftest():
    """4 beeps + 4 servo twitches (L-R-L-R) to verify wiring."""
    buzzer = GPIO.PWM(BUZZER_PIN, 2_000)
    buzzer.start(8)
    for _ in range(4):
        time.sleep(0.10)
        buzzer.ChangeDutyCycle(0)
        time.sleep(0.05)
        buzzer.ChangeDutyCycle(8)
    buzzer.stop()

    servo = GPIO.PWM(SERVO_PIN, 50)
    servo.start(7.5)
    for i in range(4):
        duty = 6.0 if i % 2 == 0 else 9.0
        servo.ChangeDutyCycle(duty)
        time.sleep(0.25)
        servo.ChangeDutyCycle(7.5)
        time.sleep(0.25)
    servo.stop()


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([BUZZER_PIN, SERVO_PIN], GPIO.OUT)

    try:
        poweron_selftest()

        #     ...
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
