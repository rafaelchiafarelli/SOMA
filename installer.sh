#!/bin/bash


sudo apt install -y python3.8
sudo apt install -y python3.8-venv

echo "installing dependencies"

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
sudo systemctl stop manager.service
cp /etc/SOMA/assets/manager.service /etc/systemd/system/manager.service
sudo systemctl daemon-reload
sudo systemctl start manager.service
sudo systemctl enable manager.service





