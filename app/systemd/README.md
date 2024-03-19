```bash
cd /home/rpi/repos/pi-rgb-slot-machine
sudo cp app/systemd/slot-machine.service /etc/systemd/system
cd /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl stop slot-machine.service
sudo systemctl start slot-machine.service
```