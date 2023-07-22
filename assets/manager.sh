#!/bin/bash
cd /home/controlroom/SOMA/
source ./venv/bin/activate
flask --app flaskr run init-db
flask --app flaskr run --debug
