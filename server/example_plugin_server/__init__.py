
""" This module provides a server-side plugin for accessing an ExampleService object. """

from typing import List, Any, override
import json
import traceback
from deephaven.plugin.object_type import MessageStream, BidirectionalObjectType
from deephaven.plugin import Registration, Callback
from deephaven.plugin import Registration, Callback
from deephaven.plugin.object_type import BidirectionalObjectType, MessageStream
from deephaven.table import Table


class ExampleService:
    """ Example service that echoes strings and tables. """
    
    def hello_string(self, data: str) -> str:
        """ Returns a string containing the input data. """
        return f"Hello client.  You said: {data}"
    
    def hello_table(self, table: Table, data: str) -> Table:
        """ Returns a table generated from the input table and the input data. """
        return table.update(["Client = data", "Server = `Hello client!`"])


class ExampleServiceMessageStream(MessageStream):
    """ MessageStream implementation for ExampleService. This will be called when the client sends a message to the server. """

    def __init__(self, service: ExampleService, client_connection: MessageStream):
        self.service = service
        self.client_connection = client_connection

        # Send an empty payload to the client to acknowledge successful connection
        self.client_connection.on_data(b'', [])

    @override
    def on_data(self, payload: bytes, references: List[Any]):
        """ Called when the client sends a message to the server. """

        #TODO: input is labeled as bytes, but it is actually a java byte array -> bug to be fixed... line below must also be fixed

        input_string = bytes(payload).decode("utf-8")
        print(f"Received data from client: {input_string}")
        inputs = json.loads(input_string)

        # Initialize the result payload and references to Deephaven objects
        result_payload = {}
        result_references = []

        try:
            if inputs["method"] == "hello_string":
                print(f"Calling hello_string(\"{inputs['data']}\")")
                result_payload["result"] = self.service.hello_string(inputs["data"])
            elif inputs["method"] == "hello_table":
                print(f"Calling hello_table({references[0]}, \"{inputs['data']}\")")
                result_payload["result"] = ''
                result_references = [self.service.hello_table(references[0], inputs["data"])]
            else:
                print(f"Unknown message type: {inputs['method']}")
                raise NotImplementedError(f"Unknown message type: {inputs['method']}")
        except Exception as e:
            result_payload["error"] = traceback.format_exc()
            print(f"Error processing message: {result_payload['error']}")

        print(f"Sending result to client: {result_payload}")

        # Serialize the result payload to JSON bytes
        json_string = json.dumps(result_payload).encode("utf-8")
        self.client_connection.on_data(payload=json_string, references=result_references)

    @override
    def on_close(self):
        """ Called when the client closes the connection. """
        print("Client connection closed.")


class ExampleServicePlugin(BidirectionalObjectType):
    """ Plugin for ExampleService. """

    @property
    @override
    def name(self) -> str:
        """ Get the name of the service. """
        return "ExampleService"

    @override
    def is_type(self, object) -> bool:
        """ Check if an object is an ExampleService. """
        return isinstance(object, ExampleService)

    @override
    def create_client_connection(self, obj: ExampleService, connection: MessageStream) -> MessageStream:
        """ Create a connection to an ExampleService instance. """
        return ExampleServiceMessageStream(obj, connection)


class ExampleServicePluginRegistration(Registration):
    """ Registration for ExampleServicePlugin. """

    @classmethod
    @override
    def register_into(cls, callback: Callback) -> None:
        """ Register the ExampleServicePlugin. """
        callback.register(ExampleServicePlugin)

