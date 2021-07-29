#!/bin/bash

screen -dmS icbot bash -c 'cd /home/ubuntu/icbot && source ./env/bin/activate &> icbot.log && python src/main.py &> icbot.log;'