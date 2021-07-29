#!/bin/bash

screen -dmS icbot bash -c 'cd /home/ubuntu/icbot; source env/bin/activate; python src/main.py &> icbot.log;'