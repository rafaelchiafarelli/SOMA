#!/bin/bash
cd /home/rafael/workspace/SOMA/
source ./venv/bin/activate
flask --app flaskr init-db
flask --app flaskr run --debug
