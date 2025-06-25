package com.example.plugin;

import io.deephaven.base.verify.Assert;
import io.deephaven.engine.table.Table;
import io.deephaven.enterprise.config.HttpUrlPropertyInputStreamLoader;
import io.deephaven.enterprise.dnd.client.DndSessionBarrage;
import io.deephaven.enterprise.dnd.client.DndSessionFactoryBarrage;
import io.deephaven.qst.table.TicketTable;
import picocli.CommandLine;

import java.io.IOException;
import java.util.concurrent.Callable;

import static com.example.plugin.IncrementPluginClient.TABLE_COL;

public class ExampleClient implements Callable<Integer> {
    @SuppressWarnings("unused")
    @CommandLine.Option(names = {"-u", "--url"}, description = "The server's URL", required = true)
    private String url;

    @SuppressWarnings("unused")
    @CommandLine.Option(names = {"-n", "--username"}, description = "A user name for authentication")
    private String userName;

    @SuppressWarnings("unused")
    @CommandLine.Option(names = {"-p", "--password"}, description = "A password for authentication")
    private String password;

    @SuppressWarnings("unused")
    @CommandLine.Option(names = {"-k", "--keyfile"}, description = "A keyfile for authentication")
    private String keyfile;

    @SuppressWarnings("unused")
    @CommandLine.Option(names = {"-pq", "--pqname"}, description = "A PQ name for the connection", required = true)
    private String pqName;

    public static void main(String[] args) {
        System.exit(new CommandLine(new ExampleClient()).execute(args));
    }

    /**
     * Used by picocli to inject the inspected command line parameters collected.
     *
     * @return the command line exit code (i.e. shown by echo $?)
     */
    @Override
    public Integer call() {
        if (keyfile == null) {
            if (userName == null || password == null) {
                throw new IllegalArgumentException("Must have a keyfile, or a username and password");
            }
        } else if (userName != null || password != null) {
            throw new IllegalArgumentException("Must have a keyfile, or a username and password");
        }

        DndSessionBarrage barrageSession = null;
        Table table = null;
        try {
            // This must be done very early in program initialization because it tells the program how and where to get its configuration
            HttpUrlPropertyInputStreamLoader.setServerUrl(url);

            final DndSessionFactoryBarrage sessionFactory = new DndSessionFactoryBarrage(url + "/iris/connection.json");
            if (keyfile != null) {
                sessionFactory.privateKey(keyfile);
            } else {
                sessionFactory.password(userName, password);
            }

            // connect to the server PQ and send an integer to the IncrementPlugin
            // the plugin will return a table with the incremented value
            barrageSession = sessionFactory.persistentQuery(pqName);
            final IncrementPluginClient client = new IncrementPluginClient(barrageSession.session(), "holder");
            final TicketTable ticketTable = client.sendInteger(15);
            table = barrageSession.snapshotOf(ticketTable);
            Assert.eq(table.getColumnSource(TABLE_COL).get(table.getRowSet().get(0)), TABLE_COL, 16);
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            if (table != null) {
                table.close();
            }

            if (barrageSession != null) {
                try {
                    barrageSession.close();
                } catch (IOException ignored) {
                }
            }
        }

        return 0;
    }
}
