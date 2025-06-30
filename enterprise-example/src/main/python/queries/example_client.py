""" This module provides a client-side interface to the IncrementPlugin server-side object. """

import json
from deephaven_enterprise.client.session_manager import SessionManager

connection_info = "https://deephaven-host.com:8123/iris/connection.json"
session_mgr: SessionManager = SessionManager(connection_info)
session_mgr.private_key("/path-to-private-key/priv-username.base64.txt")

session = session_mgr.connect_to_persistent_query("MY PQ")
# Get a ticket for an IncrementPlugin object from the server named "example_service"
example_service_ticket = session.exportable_objects["example_service"]

# Wrap the ticket as a PluginClient
example_service_plugin_client = session.plugin_client(example_service_ticket)

# serialize the inputs to JSON bytes
inputs = {'value': '15'}
input_bytes = json.dumps(inputs).encode("utf-8")
references = []

example_service_plugin_client.req_stream.write(input_bytes, references)

# first message is empty, so we skip it
next(example_service_plugin_client.resp_stream)

result_bytes, result_references = next(example_service_plugin_client.resp_stream)
# fetch and print the result table
print(result_references[0].fetch().to_arrow())

