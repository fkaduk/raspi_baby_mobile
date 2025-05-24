# raspi_baby_mobile

👉\[\[\[**This is the initial readme for your
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv) template.** Fill it in and
delete this message!
Below are general setup instructions that you may remove or keep and adapt for your
project.\]\]\]

## roadmap

- [ ] document hardware and parts
- [ ] warning beep if no face detected
- [ ] make servo rotation linearly dependent on face position
- [ ] add reviewed documentation

* * *

## Project Docs

For how to install uv and Python, see [installation.md](installation.md).

For development workflows, see [development.md](development.md).

* * *

*This project was built from
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*

## Hardware Setup

### wiring table

| Net        | From Part      | From Pin                      | To Part        | To Pin |
|------------|----------------|------------------------------|----------------|--------|
| GND        | Raspberry Pi   | any GND pin                  | Ground Rail    | —      |
| GND        | Passive Buzzer | “–” (- lead)                 | Ground Rail    | —      |
| GND        | Servo          | GND                          | Ground Rail    | —      |
| BUZZ_SIG   | Raspberry Pi   | GPIO 18   | 220 Ω Resistor | pin 1  |
| BUZZ_SIG   | 220 Ω Resistor | pin 2                        | Passive Buzzer | “+”    |
| SERVO_SIG  | Raspberry Pi   | GPIO 12  | Servo          | Signal |
| 5 V        | Servo          | +5 V                         | 5 V Rail       | —      |

## Installation

> This assumes the default configuration with user = `pi` and hostname = `raspberrypi`. Adapt if necessary.

- copy the startup script over to the raspi

```bash
scp ./scripts/pi_startup.sh pi@raspberrypi:/home/pi/pi_startup.sh
ssh pi@raspberrypi "sudo chmod +x /home/pi/pi_startup.sh"
```

- automatically startup the script, eg. via CRON:

```bash
ssh pi@raspberrypi '(crontab -l 2>/dev/null; echo "@reboot /home/pi/startup.sh >> /home/pi/startup.log 2>&1") | crontab -'
```
