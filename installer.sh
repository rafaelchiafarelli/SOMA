#!/bin/bash


apt install -y python3.8

cp -r ../SOMA/* /etc/SOMA/
echo "installing dependencies"

cd /etc/SOMA/

python3.8 -m venv venv

source ./venv/bin/activate
pip install -r requirements.txt
echo "patch mediapipe"
cp ./assets/face_mesh_connections.py ./venv/lib/python3.8/site-packages/mediapipe/python/solutions/face_mesh_connections.py
cp ./assets/holistic.py ./venv/lib64/python3.8/site-packages/mediapipe/python/solutions/holistic.py

cp /etc/SOMA/assets/manager.service /etc/systemd/system/manager.service


