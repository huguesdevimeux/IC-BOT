#!/bin/bash

screen -dmS icbot bash -c 'source env/bin/activate; python src/main.py &> icbot.log;'