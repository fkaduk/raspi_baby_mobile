import time

import RPi.GPIO as GPIO

BUZZER_PIN = 18

REFERENCE_NOTE = 2000  # Hz
REFERENCE_DURATION = 0.1  # seconds

TEST_NOTE = 500  # Hz
TEST_DURATION = 0.2  # seconds

VOLUME = 0.05  # Range: 0.0 (silent) to 1.0 (max)
# Convert volume to duty cycle (percentage)
DUTY_CYCLE = VOLUME * 100

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZER_PIN, REFERENCE_NOTE)
pwm.start(DUTY_CYCLE)

try:
    for i in range(5):
        print(i)
        pwm.ChangeFrequency(REFERENCE_NOTE)
        pwm.ChangeDutyCycle(DUTY_CYCLE)
        time.sleep(REFERENCE_DURATION)

        pwm.ChangeFrequency(TEST_NOTE)
        pwm.ChangeDutyCycle(DUTY_CYCLE)
        time.sleep(TEST_DURATION)
finally:
    pwm.stop()
    GPIO.cleanup()
