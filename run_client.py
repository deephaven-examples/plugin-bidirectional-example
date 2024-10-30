
""" Example client script that connects to a Deephaven server and calls methods on a server-side ExampleService object. """

from pydeephaven import Session
from example_plugin_client import ExampleServiceProxy

session = Session(
    auth_type="io.deephaven.authentication.psk.PskAuthenticationHandler",
    auth_token="YOUR_PASSWORD_HERE",
)

# Print the objects the server can export
print("")
print(f"Exportable Objects: {list(session.exportable_objects.keys())}")

# Get a ticket for an ExampleService object from the server named "example_service"
example_service_ticket = session.exportable_objects["example_service"]

# Wrap the ticket as a PluginClient
example_service_plugin_client = session.plugin_client(example_service_ticket)

# Create a proxy object for the ExampleService
example_service = ExampleServiceProxy(example_service_plugin_client)

print("")
print("Calling ExampleService.hello_string()")
result = example_service.hello_string("Hello server!")
print(f"Result: {result}")

print("")
print("Calling ExampleService.hello_table()")
table_in = session.empty_table(10).update("X = i")
table_result = example_service.hello_table(table_in, "Hello server!")
print("Result:")
print(table_result.to_arrow().to_pandas())

# Close the session so that Python can exit
session.close()
