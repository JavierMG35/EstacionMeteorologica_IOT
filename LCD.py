from signal import signal, SIGTERM, SIGHUP
from rpi_lcd import LCD
import RPi.GPIO as GPIO
import paho.mqtt.client
from load_params import getParams


# PARTE LCD Y SUS MENSAJES
def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)
lcd = LCD()

def temperature():
    global temp, hum
    try:
        dato = str(temp) + " Grados"
        lcd.text("TEMPERATURA", 1)
        lcd.text(dato, 2)
        print("Temperatura")
        print(str(dato))

    except KeyboardInterrupt:
            pass

def humidity():
    global temp, hum
    try:
        dato = str(hum) + " %"
        lcd.text("HUMEDAD", 1)
        lcd.text(dato, 2)
        print("Humedad")
        print(str(dato))

    except KeyboardInterrupt:
            pass

def error(tipo):
    try:
        lcd.text("ERROR EN ", 1)
        lcd.text(tipo, 2)
        print("Emprime el error en la "+ tipo)


    except KeyboardInterrupt:
            pass

# BOTON PANTALLA LCD

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
IN = 21
GPIO.setup(IN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

mensaje = 1

def click(channel):
    global mensaje
    if GPIO.input(IN) == GPIO.LOW:
        if mensaje == 1:
            mensaje = mensaje +1
            humidity()
        elif mensaje ==2:
            mensaje = mensaje - 1
            temperature()


GPIO.add_event_detect(IN, GPIO.BOTH, callback=click, bouncetime=100)

#Subscripccion
def on_connect(client, userdata, flags, rc):
    print("hey")
    if rc==0:
        print("Connected")
        client.subscribe("humidity")
        client.subscribe("temperature")
        client.subscribe("error_sensor")
    else:
        print("Connect fail, code: " + rc)

def on_message(client, userdata, msg):
    global temp, hum

    if msg.topic == "temperature":
        temp = msg.payload.decode("utf-8")
        temp = str(temp)
        print(temp)
    elif msg.topic == "humidity":
        hum = msg.payload.decode("utf-8")
        hum = str(hum)
        print(hum)
    elif msg.topic == "error_sensor":
        tipo = msg.payload.decode("utf-8")
        tipo = str(tipo)
        print("error")
        error(tipo)


temp=0
hum=0
params = getParams()

mqtt = paho.mqtt.client.Client()
mqtt.username_pw_set(username=params["MQTTUSR"], password=params["MQTTPWD"])
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect("34.105.236.222", 1883, 60)
mqtt.loop_forever()
