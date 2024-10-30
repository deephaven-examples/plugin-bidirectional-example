# Example Bidirectional Plugin for Deephaven

This repository contains all of the code necessary to create a simple example bidirectional plugin for Deephaven. A bidirectional plugin is one that facilitates communication between a running Deephaven server and client API that allows the client to manage and interact with objects on the server.

The contents of this repository are as follows:

- [./server](./server): The server-side code and packaging.
- [./client](./client): The client-side code and packaging.
- [./run_server.py](./run_server.py): A Python script to run the server.
- [./run_server.sh](./run_server.sh): A shell script that creates a venv, installs the necessary packages, and runs [./run_server.py](./run_server.py).
- [./run_client.py](./run_client.py): A python script to run the Deephaven Python client API.
- [./run_client.sh](./run_client.sh): A shell script that creates a venv, installs the necessary packages, and runs [./run_client.py](./run_client.py).

Be sure to instantiate a Deephaven server via one of the run scripts or on your own before running any client scripts.
