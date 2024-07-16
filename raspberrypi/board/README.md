this files in this folder are the ones stored on the raspberry pi

Setup (example) startup service (for `launcher.sh`):

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