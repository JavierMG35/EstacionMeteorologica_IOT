#Código de creacion de la API

from flask import Flask, request
from flask_cors import CORS
import mysql.connector
from load_params import getParams

params = getParams()

def iniciarconexion():
	db = mysql.connector.connect(host=params['MARIADB_IP'], user=params['MARIADB_USR'], password=params['MARIADB_PWD'], database=params['MARIADB_DB'])
	return db

app = Flask(__name__)
CORS(app)

@app.route("/insert_device", methods=['POST'])
def insert_device():
    db = iniciarconexion()
    data = request.form
    sql = "INSERT INTO devices (device_id) VALUES (%s)"
    val = (data["device_id"],)
    print(sql, val)
    try:
        mycursor = db.cursor()
        mycursor.execute(sql, val)
        db.commit()
        print(mycursor.rowcount, " records inserted")
        return "ok"
    except:
        print("Device already registered")
        return "ko"

@app.route("/insert_measures", methods=['POST'])
def insert_measures():
    db = iniciarconexion()
    data = request.form
    sql = "INSERT INTO sensor_data (temperature,humidity) VALUES (%s,%s)"
    val = (data["temperature"],data["humidity"])
    print(sql, val)
    mycursor = db.cursor()
    mycursor.execute(sql, val)
    db.commit()
    print(mycursor.rowcount, " records inserted")
    return "ok"

@app.route("/sensor_data/")
def sensor_data():
    db = iniciarconexion()
    r = {}
    with db.cursor() as mycursor:
        mycursor.execute("SELECT temperature,humidity FROM sensor_data ORDER BY id DESC LIMIT 1;")
        result = mycursor.fetchall()
        for temp, hum in result:
            r = {"temperature": temp, "humidity": hum}
        db.commit()
        print(r)
    return r


@app.route("/sensor_list/")
def sensor_list():
    db = iniciarconexion()
    r = {"id":[], "temperature":[], "humidity":[]}
    with db.cursor() as mycursor:
        mycursor.execute("SELECT id,temperature,humidity FROM sensor_data ORDER BY id DESC;")
        result = mycursor.fetchall()
        for row in result:
            r["id"].append(row[0])
            r["temperature"].append(row[1])
            r["humidity"].append(row[2])
        db.commit()
    return r

@app.route('/device_list/')
def device_list():
    db = iniciarconexion()
    r = {"id":[], "device":[]}
    with db.cursor() as mycursor:
        mycursor.execute("SELECT id,device_id FROM devices ORDER BY id DESC;")
        result = mycursor.fetchall()
        for row in result:
            r["id"].append(row[0])
            r["device"].append(row[1])
        db.commit()
    return r

app.run(host='0.0.0.0')