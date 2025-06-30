## Java Core+ Plugin Example

The Core+ Plugin Example is a simple Deephaven bidirectional plugin that demonstrates how to send a message from your client to a Deephaven Persistent Query, process the message inside the Persistent Query, and send a Table back to the client.

### Getting Started

1. Run `./gradlew build` to build the plugin jar. The IncrementPlugin class has the following annotation:
```java
@AutoService(ObjectType.class)
```
This configures the plugin as a service-provider, which is required to register the plugin inside Deephaven. If the jar is built correctly, you will see the following file in the jar:
```text
META-INF/services/io.deephaven.plugin.type.ObjectType
```
Which will contain a single line with the fully qualified class name of the plugin:
```text
com.example.plugin.IncrementPlugin
```
2. Deploy this jar to your Deephaven installation by copying it to the `/usr/illumon/coreplus/latest/custom_lib/` directory. This example also requires the `org.json:json` dependency specified in `build.gradle`.

```text
$ ls -ltr /usr/illumon/coreplus/latest/custom_lib/
-rw-r--r--. 1 irisadmin dbmergegrp 82710 Jun 23 15:00 json-20250517.jar
-rw-r--r--. 1 irisadmin dbmergegrp  9272 Jun 25 16:51 plugin-bidirectional-example.jar
```

3. Open the Deephaven Web UI and create a new Persistent Query with the script in `ExampleServerPQ.groovy`
4. Once the PQ is running, try running the `ExampleClient.java`. You will need to set the following VM option:
```text
-DDeephavenEnterprise.rootFile=iris-common.prop
```
Example program arguments:
```text
--url https://my.host.com:8123 --keyfile mykey.file --pqname PluginServerPQ
```



## Python Core+ Plugin Example

The Core+ Plugin Example is a simple Deephaven bidirectional plugin that demonstrates how to send a message from your client to a Deephaven Persistent Query, process the message inside the Persistent Query, and send a Table back to the client.

### Getting Started

1. Navigate to enterprise-example/src/main/python and run `python3 -m build` to build the plugin whl. Note the following line in the setup.cfg file:
```text
[options.entry_points]
deephaven.plugin =
    registration_cls = deephaven.ent.plugin._register:IncrementPluginRegistration
```
This entry point is required to register the plugin inside Deephaven.
2. Deploy this package to your Deephaven installation by installing it in the latest Core+ venv (`/usr/illumon/coreplus/venv/latest`).

```text
$ pip list
Package                         Version
------------------------------- --------------
...
deephaven-ent-plugin            0.0.1
```

3. Open the Deephaven Web UI and create a new Persistent Query with the script in `example_server.py`.
4. Once the PQ is running, try running the `example_client.py`. You will need to have installed the Core+ Python client package https://deephaven.io/enterprise/docs/clients/python/coreplus-python-client/