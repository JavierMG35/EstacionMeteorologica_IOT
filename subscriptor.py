#Codigo para conectarse por ssh a nuestro broker MQTT

import paho.mqtt.client
import requests
from load_params import getParams
from datetime import datetime

def last_will():
    json = {"device": dev, "GPS": GPS}
    requests.post("http://" + params["MICROIP"] + ":5000/last_will", data=json)

def insert_measures(temp, hum, fecha, dev, GPS):
    if temp != 0 and hum != 0:
        json = {"temperature": temp, "humidity": hum, "fecha": fecha, "device": dev, "GPS": GPS}
        requests.post("http://"+ params["MICROIP"] + ":5000/insert_measures", data=json)

def insert_dev(dev, estado, GPS, fecha):
    json = {"device_id": dev, "estado": estado, "GPS": GPS, "fecha": fecha}
    requests.post("http://"+ params["MICROIP"] + ":5000/insert_device", data=json)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected")
        client.subscribe("humidity")
        client.subscribe("temperature")
        client.subscribe("devices")
        client.subscribe("GPS")
        client.subscribe("last_will")
    else:
        print("Connect fail, code: ", rc)

def on_message (client, userdata, msg):
    global temp, hum, GPS, dev, estado
    fecha = datetime.now()
    print({msg.topic}, {msg.payload})
    if msg.topic == "temperature":
        temp = float(msg.payload.decode("utf-8"))
        insert_measures(temp, hum, fecha, dev, GPS)
        print(temp, hum, fecha, dev, GPS)
    elif msg.topic == "humidity":
        hum = float(msg.payload.decode("utf-8"))
        insert_measures(temp, hum, fecha, dev, GPS)
        print(temp, hum, fecha, dev, GPS)
    elif msg.topic == "GPS":
        GPS = msg.payload.decode("utf-8")
    elif msg.topic == "devices":
        dev = msg.payload.decode("utf-8")
        insert_dev(dev, estado, GPS, fecha)
        print(dev, estado, GPS, fecha)
    elif msg.topic == "last_will":
        print("desconectando....")
        last_will()

temp = 0
hum = 0
GPS = ""
dev = ""
estado = "activo"
params = getParams()


mqtt = paho.mqtt.client.Client()
mqtt.username_pw_set(username=params["MQTTUSR"], password=params["MQTTPWD"])
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect(params["MQTTIP"], 1883, 60)
mqtt.loop_forever()