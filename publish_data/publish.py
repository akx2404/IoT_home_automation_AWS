from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3idduyxut8qzd-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "Esp8266_led_control"
PATH_TO_CERT = "certificates/509f09039b-certificate.pem.crt"
PATH_TO_KEY = "certificates/509f09039b-private.pem.key"
PATH_TO_ROOT = "certificates/root.pem"
MESSAGE = "Hello from AWS IoT console"
TOPIC = "pyTopic"
RANGE = 1

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERT,
            pri_key_filepath=PATH_TO_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_ROOT,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')
for i in range (RANGE):
    message = {"LED": "0"}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'pyTopic'")
    t.sleep(1)
print('Publish End')
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
