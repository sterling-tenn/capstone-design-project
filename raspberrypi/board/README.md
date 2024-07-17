this files in this folder are the ones relevant to being stored on the raspberry pi

## Setup (example) startup service (for `launcher.sh`):

`sudo nano /etc/systemd/system/cargobuddy-startup.service`
```
[Unit]
Description=CargoBuddy Startup
After=network.target

[Service]
ExecStart=/home/raspberrypi/CargoBuddy/launcher.sh
WorkingDirectory=/home/raspberrypi/CargoBuddy
User=raspberrypi
Group=raspberrypi
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload
sudo systemctl enable cargobuddy-startup.service
```

## Raspberry Pi 5 Pinout
![alt text](assets/Raspberry-Pi-5-Pinout.jpg)

## Servo
- connect servo to GPIO 15 (defined in `servo.py`)
- connect to 5V power and ground
- cable colouring
    - orange - GPIO
    - red - 5V power
    - brown - ground

## Ultrasonic Sensor
- 