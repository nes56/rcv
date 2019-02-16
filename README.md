# rcv
raspberry pi computer vision

## install on rasberry PI device

As user pi

```
    cd /home/pi
    git clone https://github.com/nes56/rcv.git
    cd rcv
    ./install.sh
    systemctl enable rcv.service
```

## runing the service

```
    sudo systemctl start rcv.service
```

## checking health of service

```
    sudo systemctl status rcv.service
```
logs of rcv service are located under /opt/logs


## howto test distance logic

python measure distance_on_mouse_click.py --image=images_height_38.5_y_angle_28\img_1_320x240_2019_02_07_20_53_24.png --camera-height=38.5 --y_leaning_angle=28 --x_turning_angle=1.9
