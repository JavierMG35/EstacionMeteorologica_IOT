#Código para conectarse por ssh a nuestra Raspberry Pi

import adafruit_dht
import board
import time
import uuid
import threading
import paho.mqtt.client
import pynmea2
import serial
import io
from load_params import getParams

def error_sensor(tipo):
    mqtt.publish("error_sensor", payload=tipo, qos=0, retain=False)
    print("Publicado error tipo:  ", tipo)

def send_id(mqtt,id):
    mqtt.publish("devices",payload=id,qos=0,retain=False)
    print("Publicado id ",id)

def send_GPS(mqtt,GPS):
    mqtt.publish("GPS",payload=GPS,qos=0,retain=False)
    print("Publicado GPS ",GPS)

def send_temperature(mqtt,temp):
    print("Publicada temperatura ",temp)
    mqtt.publish("temperature",payload=temp,qos=0,retain=False)

def send_humidity(mqtt,hum):
    mqtt.publish("humidity",payload=hum,qos=0,retain=False)
    print("Publicada humedad ",hum)

def sensor_GPS(mqtt):
    ser = serial.Serial('/dev/serial0', 9600, timeout=1.0)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    while True:
        try:
            line = sio.readline()
            if line[:6] == "$GPGGA":
                msg = pynmea2.parse(line)
                send_GPS(mqtt, (str(msg.latitude) + " " + str(msg.longitude)))
                break
        except serial.SerialException as e:
            print('Device error: {}'.format(e))
            break
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            continue

def temperatureSensor(mqtt,pin):
    sensor = adafruit_dht.DHT11(pin,use_pulseio = False)
    prevtemp = -273
    while True:
        try:
            temp = sensor.temperature
            if temp is not None:
                if temp != prevtemp:
                    prevtemp = temp
                    print("Lectura de temperatura %0.1f"%temp)
                    send_temperature(mqtt,temp)
        except:
            pass
        time.sleep(1)

def humiditySensor(mqtt,pin):
    sensor = adafruit_dht.DHT11(pin,use_pulseio = False)
    prevhum = -1
    while True:
        try:
            hum = sensor.humidity
            if hum is not None:
                if hum != prevhum:
                    prevhum = hum
                    print("Lectura de humedad %0.1f"%hum)
                    send_humidity(mqtt,hum)
        except:
            pass
        time.sleep(1)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected")
    else:
        print("Connect fail, code: ",rc)

def make_connection(ip,usr,pwd):

    mqtt = paho.mqtt.client.Client()
    mqtt.will_set("last_will", payload=None, qos=0, retain=False)
    mqtt.username_pw_set(username=usr,password=pwd)
    mqtt.on_connect = on_connect
    mqtt.connect(ip,1883,60)
    return mqtt

def weather_sensor(ip,usr,pwd):
    mqtt = make_connection(ip,usr,pwd)
    id = ":".join(["{:02x}".format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    sensor_GPS(mqtt)
    print("Id:",id)
    send_id(mqtt,id)
    return mqtt


PIN = board.D4
params = getParams()
#IP = "34.89.88.54" #DOCKERS
IP = "34.105.236.222" #MQTT

mqtt = weather_sensor(IP, params["MQTTUSR"], params["MQTTPWD"])
temp_thread = threading.Thread(target=temperatureSensor,args=(mqtt,PIN))
hum_thread = threading.Thread(target=humiditySensor,args=(mqtt,PIN))

hum_thread.start()
temp_thread.start()
