
""" This module provides a client-side interface to the ExampleService server-side object. """

import io
from typing import Any, List
from pydeephaven import Table
from pydeephaven.experimental import plugin_client, server_object
import json


class ExampleServiceProxy(server_object.ServerObject):
    """
    This class provides a client-side interface to the ExampleService server-side object.

    When you call a method on this class, it sends a message to the server-side object and returns the result.
    The inputs are serialized to JSON bytes and sent to the server, and the result is deserialized from JSON and returned.
    """

    def __init__(self, plugin_client: plugin_client.PluginClient):
        #TODO: change the assignments to the constructor call in 0.37
        # super().__init__(type=plugin_client.type_, ticket=plugin_client.ticket)
        self.type_ = plugin_client.type_
        self.ticket = plugin_client.ticket

        self.plugin_client = plugin_client

        # Consume the first (empty) payload from the server to acknowledge successful connection
        next(self.plugin_client.resp_stream)

    def hello_string(self, data: str) -> str:
        """ Call ExampleService.hello_string() on the server. 
        Returns a string containing the input data."""

        inputs = {'method': 'hello_string', 'data': data}

        # serialize the inputs to JSON bytes
        input_bytes = json.dumps(inputs).encode("utf-8")

        # no input references
        input_references = []

        self.plugin_client.req_stream.write(input_bytes, input_references)
        result_bytes, result_references = next(self.plugin_client.resp_stream)
        results = json.loads(result_bytes.decode("utf-8"))

        if 'error' in results:
            raise Exception(results['error'])

        # return the result string
        return results['result']
    
    def hello_table(self, table: Table, data: str) -> Table:
        """ Call ExampleService.hello_table() on the server. 
        Returns a table generated from the input table and the input data."""
        
        inputs = {'method': 'hello_table', 'data': data}

        # serialize the inputs to JSON bytes
        input_bytes = json.dumps(inputs).encode("utf-8")

        # input references
        input_references = [table]

        self.plugin_client.req_stream.write(input_bytes, input_references)
        result_bytes, result_references = next(self.plugin_client.resp_stream)
        results = json.loads(result_bytes.decode("utf-8"))

        if 'error' in results:
            raise Exception(results['error'])
        
        # fetch and return the result table
        return result_references[0].fetch()






