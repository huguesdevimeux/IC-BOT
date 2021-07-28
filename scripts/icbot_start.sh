#!/bin/bash

screen -dmS icbot bash -c 'source ICEBOT/bin/activate; python src/main.py &> icbot.log;'