import pyttsx3
import datetime
import speech_recognition as sr
import random
import time
import os
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
    window.bgpic('brain.GIF')
    window.title("Alpha bot")

    
text = turtle.Turtle()
text.color('yellow')
text.penup()
#text.hideturtle()
text.goto(-350, 50)
text.right(90)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
        newVoiceRate = 155
        engine.setProperty('rate',newVoiceRate)
        engine.say(audio)
        engine.runAndWait()

def wishMe():
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<12:
            speak("Good Morning Sir")
            text.write('Good Morning Sir', font=('Fixedsys',15,'bold'))
            text.forward(20)

        elif hour>=12 and hour<18:
            speak("Good afternoon sir")
            text.write('Good Afternoon Sir', font=('Fixedsys',15,'bold'))
            text.forward(20)
            
        else:
            speak("Good evening sir")
            text.write('Good Evening Sir', font=('Fixedsys',15,'bold'))
            text.forward(20)
            
        speak("What can I do for you?")
        turtle.forward(15)
        text.write('What can I do for you?', font=('Fixedsys',15,'bold'))
        time.sleep(1)


def takeCommand():

        r = sr.Recognizer()
        with sr.Microphone() as source:
            text.clear()
            text.write('Listening....', font=('Fixedsys',15,'bold'))
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            text.clear()
            text.write('Recognizing...', font=('Fixedsys',15,'bold'))
            text.clear()
            query = r.recognize_google(audio, language='en-in')
            text.write(f"you said: {query}\n", font=('Fixedsys',15,'bold'))
            time.sleep(2)
            #print(f"User said: {query}\n")

        except Exception as e:
            #print(e)
            return "None"

        return query
        

if __name__=="__main__":
    #create window
    window = turtle.Screen()
    window.setup(800,300)
    main_page()
    time.sleep(1)
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wejh' in query:
            a = 0

        elif 'on' in query:
            speak("Got it sir, Switching on the light")
            message = {"LED": "1"}
            mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
            #print("Published: '" + json.dumps(message) + "' to the topic: " + "'pyTopic'")


        elif 'off' in query:
            speak("Got it sir, Switching off the light")
            message = {"LED": "0"}
            mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
            #print("Published: '" + json.dumps(message) + "' to the topic: " + "'pyTopic'")

        if "exit" in query:
            speak("Bye sir")
            time.sleep(1)
            turtle.bye()
            break



#window.mainloop()
