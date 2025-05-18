# raspi_baby_mobile

👉\[\[\[**This is the initial readme for your
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv) template.** Fill it in and
delete this message!
Below are general setup instructions that you may remove or keep and adapt for your
project.\]\]\]

* * *

## Project Docs

For how to install uv and Python, see [installation.md](installation.md).

For development workflows, see [development.md](development.md).

* * *

*This project was built from
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*


## Installation

> This assumes the default configuration with user = `pi` and hostname = `raspberrypi`. Adapt if necessary.

- copy the startup script over to the raspi

```bash
scp ./scripts/pi_startup.sh frk@raspberrypi:/home/frk/pi_startup.sh
ssh frk@raspberrypi "sudo chmod +x /home/pi/pi_startup.sh"
```

- automatically startup the script, eg. via CRON:

```bash
ssh pi@raspberrypi '(crontab -l 2>/dev/null; echo "@reboot /home/pi/startup.sh >> /home/pi/startup.log 2>&1") | crontab -'
```
