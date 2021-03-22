import turtle
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

# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()


def main_page():
    window.clearscreen()
    window.title('IOT LED control')
    window.bgpic('iot.GIF')
    on = turtle.Turtle()
    on.penup()
    on.shape('circle')
    on.shapesize(2,2)
    on.goto(-150,0)
    

    off = turtle.Turtle()
    off.penup()
    off.shape('circle')
    off.shapesize(2,2)
    off.goto(150,0)
    
    texton=turtle.Turtle()
    texton.color('yellow')
    texton.hideturtle()
    texton.penup()
    texton.goto(-150, 60)
    texton.write('ON', align = 'center', font=('Fixedsys',30,'bold'))
    
    textoff=turtle.Turtle()
    textoff.color('yellow')
    textoff.hideturtle()
    textoff.penup()
    textoff.goto(150, 60)
    textoff.write('OFF', align = 'center',font=('Fixedsys',30,'bold'))

    border = turtle.Turtle()
    border.color('white')
    border.width(4)
    border.hideturtle()
    border.penup()
    border.goto(0,135)
    border.pendown()
    border.goto(0,-115)

    def ledon(x,y):
        on.color('yellow')
        off.color('black')
        message = {"LED": "1"}
        mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)

    
    def ledoff(x,y):
        off.color('yellow')
        on.color('black')
        message = {"LED": "0"}
        mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)    
        
    on.onclick(ledon)
    off.onclick(ledoff)
    
window = turtle.Screen()
window.setup(600,300)
main_page()

window.mainloop()
