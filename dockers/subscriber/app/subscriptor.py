#Codigo para conectarse por ssh a nuestro broker MQTT

import time
import paho.mqtt.client
import requests
from load_params import getParams

def insert_measures(temp, hum):
    json = {"temperature":temp, "humidity":hum}
    requests.post("http://"+ params["MICROIP"] + ":5000/insert_measures", data=json)

def insert_dev(dev):
    json = {"device_id":dev}
    requests.post("http://"+ params["MICROIP"] + ":5000/insert_device", data=json)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected")
        client.subscribe("humidity")
        client.subscribe("temperature")
        client.subscribe("devices")
    else:
        print("Connect fail, code: ", rc)

def on_message (client, userdata, msg):
    global temp, hum
    print({msg.topic},{msg.payload})
    if msg.topic == "temperature":
        temp = float(msg.payload.decode("utf-8"))
        insert_measures(temp, hum)
        print(temp, hum)
    elif msg.topic == "humidity":
        hum = float(msg.payload.decode("utf-8"))
        insert_measures(temp, hum)
        print(temp, hum)
    elif msg.topic == "devices":
        dev = msg.payload.decode("utf-8")
        insert_dev(dev)
        print(dev)

temp = 0
hum = 0

params = getParams()
mqtt = paho.mqtt.client.Client()
mqtt.username_pw_set(username=params["MQTTUSR"], password=params["MQTTPWD"])
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect(params["MQTTIP"], 1883, 60)
mqtt.loop_forever()