package com.example.plugin;

import io.deephaven.client.impl.*;
import io.deephaven.qst.table.TicketTable;
import org.apache.commons.lang3.mutable.MutableBoolean;
import org.json.JSONObject;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

public class IncrementPluginClient {

    public static final String VALUE_KEY = "value";
    public static final String TABLE_COL = "ResultValue";
    public static final String PLUGIN_NAME = "IncrementPlugin";

    private final ObjectService.MessageStream<ClientData> messageStream;
    private final CompletableFuture<TicketTable> result = new CompletableFuture<>();

    public IncrementPluginClient(final Session session, final String holderVarNameOnServer) throws ExecutionException, InterruptedException {
        // Variable name must match the server-side variable name used in the persistent query. See ExampleServerPQ.groovy
        final HasTypedTicket typedTicket = new ScopeId(holderVarNameOnServer).ticketId().toTypedTicket(PLUGIN_NAME);
        final ServerObject serverObject = session.export(typedTicket).get();

        this.messageStream = session.connect(serverObject, new PluginMessageStream(result));
    }

    /*
     * Sends an integer to the server, which is expected to return a table with the incremented value.
     */
    public TicketTable sendInteger(int number) throws ExecutionException, InterruptedException, TimeoutException {
        final JSONObject jsonPayload = new JSONObject();
        jsonPayload.put(VALUE_KEY, number);
        final byte[] payloadBytes = jsonPayload.toString().getBytes(StandardCharsets.UTF_8);
        final ByteBuffer buffer = ByteBuffer.wrap(payloadBytes);

        messageStream.onData(new ClientData(buffer, Collections.emptyList()));
        return result.get(15, TimeUnit.SECONDS);
    }

    private static class PluginMessageStream implements ObjectService.MessageStream<ServerData> {
        private final MutableBoolean firstReceived;
        private final CompletableFuture<TicketTable> result;

        public PluginMessageStream(final CompletableFuture<TicketTable> result) {
            this.firstReceived = new MutableBoolean();
            this.result = result;
        }

        @Override
        public void onData(final ServerData serverData) {
            final ByteBuffer payload = serverData.data();

            // Check if this is the first message received (which should be empty)
            if (firstReceived.isFalse()) {
                if (payload.hasRemaining()) {
                    result.completeExceptionally(new IllegalStateException("Expected empty first payload."));
                }
                firstReceived.setValue(true);
                return;
            }

            // The server is expected to return a table ticket
            final List<ServerObject> exports = serverData.exports();
            if (exports != null && !exports.isEmpty()) {
                final ServerObject serverObject = exports.get(0);
                if ("Table".equals(serverObject.typedTicket().type().orElse(null))) {
                    result.complete(serverObject.ticketId().table());
                } else {
                    final String type = serverObject.typedTicket().type().orElse("unknown");
                    result.completeExceptionally(
                            new IllegalArgumentException("Server did not return a Table. Type: " + type));
                }
            } else {
                result.completeExceptionally(
                        new IllegalStateException("Server sent no exported objects."));
            }
        }

        @Override
        public void onClose() {
            System.out.println("IncrementPluginClient: Connection closed.");
        }
    }
}