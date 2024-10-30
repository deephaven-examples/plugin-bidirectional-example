
""" This script starts a Deephaven server with a single ExampleService object. """

from deephaven_server import Server

server = Server(
    jvm_args=["-Xmx4g", "-Dauthentication.psk=YOUR_PASSWORD_HERE"]
)
server.start()

import sys
from example_plugin_server import ExampleService

# Create an ExampleService object in the global scope.  This will make the object exportable to clients.
example_service = ExampleService()

# Keep the server running until the user presses Control-C

print("Press Control-C to exit")

try:
    while True:
        input()
except KeyboardInterrupt:
    print("Exiting Deephaven...")
    sys.exit(0)
