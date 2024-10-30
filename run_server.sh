#!/bin/bash

# Create a virtual environment for the server, install the server plugin, and run the server

rm -rf ./venv-server
python3.12 -m venv ./venv-server
source ./venv-server/bin/activate
python -m pip install --upgrade pip
python -m pip install deephaven_server
python -m pip install ./server
python run_server.py
