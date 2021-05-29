#!/bin/bash

apt-get update
apt-get upgrade
apt-get -o Dpkg::Options::="--force-confmiss" install --reinstall netbase
apt install -y libsm6 libxext6 libxrender-dev

pip install -r requirements.txt
python3 main.py