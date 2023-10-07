#!/usr/bin/env bash
# Install all the fabric dependencies so that we can start working with it.

sudo pip3 uninstall Fabric
sudo apt-get install libffi-dev
sudo apt-get install libssl-dev
sudo apt-get install build-essential
sudo apt-get install python3.4-dev
sudo apt-get install libpython3-dev
sudo pip3 install pyparsing
sudo pip3 install appdirs
sudo pip3 install setuptools==40.1.0
sudo pip3 install cryptography==2.8
sudo pip3 install bcrypt==3.1.7
sudo pip3 install PyNaCl==1.3.0
sudo pip3 install Fabric3==1.14.post1
