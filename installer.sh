#!/bin/bash


apt install -y python3.8
apt install -y python3.8-venv
cp -r ../SOMA/ /etc/SOMA/
echo "installing dependencies"

cd /etc/SOMA/

python3.8 -m venv venv

source ./venv/bin/activate
echo "update pip"
pip install --upgrade pip
echo "install requirements"
pip install -r assets/requirements.txt
echo "patch mediapipe"
cp ./assets/face_mesh_connections.py ./venv/lib/python3.8/site-packages/mediapipe/python/solutions/face_mesh_connections.py
cp ./assets/holistic.py ./venv/lib64/python3.8/site-packages/mediapipe/python/solutions/holistic.py
echo "install service"
systemctl stop manager.service
cp /etc/SOMA/assets/manager.service /etc/systemd/system/manager.service
systemctl daemon-reload
systemctl start manager.service
systemctl enable manager.service





