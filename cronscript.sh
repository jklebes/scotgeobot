#!/bin/sh
cd /home/jsk/scotgeobot
export DISPLAY=:0.0
export $(dbus-launch)
#conda activate
python3 -m scotgeobot --desktop --redo --homealert
