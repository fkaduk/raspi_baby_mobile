# Raspi Baby Mobile

A Raspberry Pi–powered system that brings interactivity to a baby mobile.

![](./doc/baby_yaw_mobile_rotation.svg)

It visually detects yaw movement of the head and translates it to a proportional rotation of a visual display.

## Background

Young infants quickly learn that their own actions can make things happen around them - a phenomenon known as **response-contingent learning**.

In [Rovee-Collier’s (1969)](https://www.sciencedirect.com/science/article/abs/pii/0022096569900253)
classic experiment,
babies as young as two months had one leg connected to an overhead mobile via a ribbon.
Whenever the infant kicked that leg, the mobile moved.
Even at this early age,
infants learned the contingency between their action and the mobile’s motion.

Building on this idea, [Watson and Ramey (1972)](https://psycnet.apa.org/record/1973-28652-001)
placed two-month-old babies on pressure-sensitive pillows wired to a rotating array of colored shapes.
The infants quickly adjusted their posture to keep the display turning,
again demonstrating an emerging sense of agency.

Crucially, contingent feedback elicited longer looking times as well as clear signs of positive affect such as smiling, cooing, and vocalizing.
In contrast, identical but non-contingent movements held little interest.

## Hardware Setup

### Parts List

- raspberry pi >3b+
- passive buzzer
- 360 deg servo
- enclosure
- visual display to be rotated (avoid strings, plastic sticks/balsa wood will have a more immediate response)

### Wiring Table

| Net        | From Part      | From Pin                      | To Part        | To Pin |
|------------|----------------|------------------------------|----------------|--------|
| GND        | Raspberry Pi   | any GND pin                  | Ground Rail    |        |
| GND        | Passive Buzzer | - lead                       | Ground Rail    |        |
| GND        | Servo          | GND                          | Ground Rail    |        |
| BUZZ_SIG   | Raspberry Pi   | GPIO 18                      | 220 Ω Resistor | pin 1  |
| BUZZ_SIG   | 220 Ω Resistor | pin 2                        | Passive Buzzer | + lead |
| SERVO_SIG  | Raspberry Pi   | GPIO 12                      | Servo          | Signal |
| 5 V        | Servo          | +5 V                         | 5 V Rail       |        |

## Installation

### Directly Source from GitHub

> This assumes the default configuration with user = `pi` and hostname = `raspberrypi`. Adapt if necessary.

Copy the startup script over to the raspi:

```bash
scp ./scripts/pi_startup.sh pi@raspberrypi:/home/pi/pi_startup.sh
ssh pi@raspberrypi "sudo chmod +x /home/pi/pi_startup.sh"
```

Automatically startup the script, eg. via CRON:

```bash
ssh pi@raspberrypi '(crontab -l 2>/dev/null; echo "@reboot /home/pi/startup.sh >> /home/pi/startup.log 2>&1") | crontab -'
```
