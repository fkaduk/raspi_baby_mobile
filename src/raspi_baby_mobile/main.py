#!/usr/bin/env python3

import RPi.GPIO as GPIO

import raspi_baby_mobile

BUZZER_PIN = 18
SERVO_PIN = 12


def main(poweron_selftest=True):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([BUZZER_PIN, SERVO_PIN], GPIO.OUT)
    buzzer = GPIO.PWM(BUZZER_PIN, 2_000)
    servo = GPIO.PWM(SERVO_PIN, 50)

    if poweron_selftest:
        raspi_baby_mobile.poweron_selftest(buzzer, servo)

    GPIO.cleanup()


if __name__ == "__main__":
    main()
