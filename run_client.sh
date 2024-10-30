#!/bin/bash

# Create a virtual environment for the client, install the client plugin, and run the client

rm -rf ./venv-client
python3.12 -m venv ./venv-client
source ./venv-client/bin/activate
python -m pip install --upgrade pip
python -m pip install ./client
python run_client.py
