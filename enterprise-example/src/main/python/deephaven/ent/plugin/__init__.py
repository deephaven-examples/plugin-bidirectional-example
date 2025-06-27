
""" This module provides a server-side plugin for accessing an IncrementPlugin object. """

from typing import Any, List
import json
import traceback
from deephaven.plugin.object_type import MessageStream, BidirectionalObjectType
from deephaven.plugin import Registration, Callback
from deephaven import new_table
from deephaven.column import int_col
from deephaven.table import Table

NAME = "deephaven.ent.plugin.IncrementPlugin"

class IncrementPlugin(BidirectionalObjectType):
    """ Plugin for IncrementPlugin. """

    @property
    def name(self) -> str:
        """ Get the name of the service. """
        return NAME

    def is_type(self, object: Any) -> bool:
        """ Check if an object is an IncrementPlugin. """
        return isinstance(object, IncrementPlugin)

    def create_client_connection(self, obj: Any, connection: MessageStream) -> MessageStream:
        """ Create a connection to an IncrementPlugin instance. """
        return IncrementPluginMessageStream(obj, connection)

    def increment_table(self, data: int) -> Table:
        """ Returns a table with one cell, the integer + 1. """
        print(f"IncrementPlugin: increment_table called with data: {data}")
        return new_table([int_col("ResultValue", [data + 1])])


class IncrementPluginMessageStream(MessageStream):
    """ MessageStream implementation for IncrementPlugin. This will be called when the client sends a message to the server. """

    def __init__(self, service: IncrementPlugin, client_connection: MessageStream):
        self.service = service
        self.client_connection = client_connection

        # Send an empty payload to the client to acknowledge successful connection
        self.client_connection.on_data("".encode(), [])

    def on_data(self, payload: bytes, references: List[Any]):
        """ Called when the client sends a message to the server. """

        #TODO: input is labeled as bytes, but it is actually a java byte array -> bug to be fixed... line below must also be fixed

        # Deserialize the input JSON bytes
        input_string = bytes(payload).decode("utf-8")
        inputs = json.loads(input_string)
        print(f"IncrementPlugin: Received data from client: {input_string}")

        result_references = []
        result_payload = {}
        try:
            if "value" in inputs:
                result_references.append(self.service.increment_table(int(inputs["value"])))
            else:
                print("Message missing 'value' key. Ignoring.")
        except Exception as e:
            result_payload["error"] = traceback.format_exc()
            print(f"IncrementPlugin: Error processing message: {result_payload['error']}")

        # Serialize the result payload to JSON bytes
        json_string = json.dumps(result_payload).encode("utf-8")
        print(f"IncrementPlugin: Sending result to client: {json_string.decode('utf-8')}, Result references: {result_references}")
        self.client_connection.on_data(payload=json_string, references=result_references)

    def on_close(self):
        """ Called when the client closes the connection. """
        print("IncrementPlugin: Client connection closed.")


example_service = IncrementPlugin()
