create a service ini in the systemd/system folder that will call our python file when it runs
sudo nano /lib/systemd/system/"some name".service

INI format
[Unit]
 Description=my service
 After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/rcv/"some name".py

[Install]
WantedBy=multi-user.target

enables it to write and read

sudo chmod 644 /lib/systemd/system/"some name".service

next time on reboot the program will run and this service would be called
sudo systemctl daemon-reload
sudo systemctl enable "some name".service
