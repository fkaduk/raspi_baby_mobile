import time


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
