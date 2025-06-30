package com.example.plugin;

import com.google.auto.service.AutoService;
import io.deephaven.engine.table.Table;
import io.deephaven.engine.util.TableTools;
import io.deephaven.plugin.type.ObjectCommunicationException;
import io.deephaven.plugin.type.ObjectType;
import io.deephaven.plugin.type.ObjectTypeBase;
import org.json.JSONObject;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;

import static com.example.plugin.IncrementPluginClient.*;

@AutoService(ObjectType.class)
public class IncrementPlugin extends ObjectTypeBase {

    @Override
    public String name() {
        return PLUGIN_NAME;
    }

    @Override
    public boolean isType(final Object object) {
        return object instanceof IncrementPlugin;
    }

    @Override
    public MessageStream compatibleClientConnection(final Object object, final MessageStream connection)
            throws ObjectCommunicationException {
        // must send an empty payload when the client first connects
        connection.onData(ByteBuffer.allocate(0));
        return new ServerMessageStream(connection);
    }

    private class ServerMessageStream implements MessageStream {
        private final MessageStream connection;

        public ServerMessageStream(final MessageStream connection) {
            this.connection = connection;
        }
        @Override
        public void onData(ByteBuffer payload, Object[] references) throws ObjectCommunicationException {
            // Parses the payload as a JSON string, returns a table with the incremented value.
            final String jsonString = StandardCharsets.UTF_8.decode(payload).toString();
            JSONObject jsonObject = new JSONObject(jsonString);
            if (!jsonObject.has(VALUE_KEY)) {
                System.out.println("IncrementPlugin: Received JSON does not contain '" + VALUE_KEY + "' key. Ignoring payload.");
                return;
            }
            int receivedInteger = jsonObject.getInt(VALUE_KEY);
            int resultInteger = receivedInteger + 1;

            final Table resultTable = TableTools.newTable(TableTools.intCol(TABLE_COL, resultInteger));

            // Send a reference to the table to the client
            payload.flip();
            connection.onData(payload, resultTable);
        }

        @Override
        public void onClose() {
            connection.onClose();
        }
    }
}
