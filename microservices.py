#Código de creacion de la API

from flask import Flask, request
from flask_cors import CORS
import mysql.connector
from load_params import getParams
from datetime import datetime

params = getParams()

def iniciarconexion():
	db = mysql.connector.connect(host=params['MARIADB_IP'], user=params['MARIADB_USR'], password=params['MARIADB_PWD'], database=params['MARIADB_DB'])
	return db

app = Flask(__name__)
CORS(app)

#FUNCIONES APARTE

def id(dev, GPS):
    db = iniciarconexion()
    try:
        with db.cursor() as mycursor:
            val = (dev, GPS)
            print(str(val))
            mycursor.execute("SELECT id FROM devices where device_id = %s and device_GPS = %s ;", val)
            result = mycursor.fetchall()
            print(str(result))
            for row in result:
                r= row[0]
            db.commit()
        return str(r)
    except:
        print("no se ha encontrado la ID")
        return 'ko'

#FUNCIONES API

@app.route("/insert_device/", methods=['POST'])
def insert_device():
    db = iniciarconexion()
    data = request.form
    sql = "INSERT INTO devices (device_id,estado, device_GPS, fecha) VALUES (%s,%s,%s,%s);"
    val = (data["device_id"], data["estado"], data["GPS"], data["fecha"])
    print(str(sql), str(val))
    try:
        mycursor = db.cursor()
        mycursor.execute(sql, val)
        db.commit()
        print(mycursor.rowcount, "records inserted")
        return "ok"
    except:
        sql = ("UPDATE devices SET estado = 'activo' , fecha= %s WHERE device_id = %s and device_GPS = %s;")
        val = (data["fecha"], data["device_id"], data["GPS"])
        try:
            mycursor = db.cursor()
            mycursor.execute(sql, val)
            db.commit()
            print("Ya existe, y hemos cambiado su estado a activo")
            return "ok"
        except:
            print("Algo malo pasa")
            return "ko"

@app.route("/insert_measures/", methods=['POST'])
def insert_measures():
    db = iniciarconexion()
    data = request.form
    id_device = id(data["device"], data["GPS"])
    val_previo = (id_device, 'activo')
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM devices WHERE id = %s and estado = %s", val_previo)
    result = mycursor.fetchall()
    if str(result) != '[]':
        sql = "INSERT INTO sensor_data (temperature,humidity, fecha, id_device) VALUES (%s,%s,%s,%s);"
        val = (data["temperature"], data["humidity"], data["fecha"], id_device)
        print(sql, val)
        mycursor = db.cursor()
        mycursor.execute(sql, val)
        db.commit()
        print(mycursor.rowcount, "records inserted. Existe su id correspondiente")
        return "ok"
    else:
        print("el device esta inactivo")
        return "ko"

@app.route("/nombre_device/",methods=['POST'])
def nombre_device():
    db = iniciarconexion()
    data = request.form
    val = (data["id_device"],'id')
    r = {"id":[], "device":[],  "GPS":[]}
    with db.cursor() as mycursor:
        mycursor.execute("SELECT id, device_id,  device_GPS FROM devices where id = %s ORDER BY %s DESC;", val)
        result = mycursor.fetchall()
        for row in result:
            r["id"].append(row[0])
            r["device"].append(row[1])
            r["GPS"].append(row[2])
        db.commit()
    return r

@app.route('/device_list/')
def device_list():
    db = iniciarconexion()
    r = {"id": [], "device": [], "estado": [], "GPS": [], "fecha": []}
    with db.cursor() as mycursor:
        mycursor.execute("SELECT id, device_id, estado, device_GPS, fecha FROM devices ORDER BY estado ASC,id DESC;")
        result = mycursor.fetchall()
        for row in result:
            r["id"].append(row[0])
            r["device"].append(row[1])
            r["estado"].append(row[2])
            r["GPS"].append(row[3])
            r["fecha"].append(row[4])
        db.commit()
    return r

@app.route("/sensor_list/",methods=['POST'])
def sensor_list():
    db = iniciarconexion()
    data = request.form
    val = (data["id_device"], 'id')
    r = {"id": [], "temperature": [], "humidity": [], "fecha": []}
    sql = "SELECT id, temperature, humidity, fecha FROM sensor_data where id_device = %s ORDER BY %s DESC ;"
    with db.cursor() as mycursor:
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        for row in result:
            r["id"].append(row[0])
            r["temperature"].append(row[1])
            r["humidity"].append(row[2])
            r["fecha"].append(row[3])
        db.commit()
    return r

@app.route("/sensor_list_filtrado/",methods=['POST'])
def sensor_list_filtrado():
    db = iniciarconexion()
    data = request.form
    val = (data["id_device"],data["fecha_inicio"], data["fecha_fin"])
    r = {"id":[], "temperature":[],"humidity":[],"fecha":[]}
    sql = "SELECT id, temperature, humidity, fecha FROM sensor_data where id_device = %s and fecha>= %s and fecha <= %s ORDER BY id DESC ;"
    with db.cursor() as mycursor:
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        for row in result:
            r["id"].append(row[0])
            r["temperature"].append(row[1])
            r["humidity"].append(row[2])
            r["fecha"].append(row[3])
        db.commit()
    return r

@app.route("/desactivar/",methods=['POST'])
def desactivar():
    fecha = datetime.now()
    db = iniciarconexion()
    data = request.form
    val = (fecha, data["id"],'activo')
    sql = ("UPDATE devices SET estado = 'inactivo', fecha = %s WHERE id = %s and estado= %s;")
    try:
        mycursor = db.cursor()
        mycursor.execute(sql, val)
        db.commit()
        print("Sensor " + data["id"] + " inactivo")
        return 'ok'
    except:
        print("Algo malo pasa en desactivar")
        return "ko"

@app.route("/last_will/",methods=['POST'])
def last_will():
    fecha = datetime.now()
    db = iniciarconexion()
    data = request.form
    id_device = id(data["device"],data["GPS"])
    val = (fecha,id_device)
    sql = ("UPDATE devices SET estado = 'inactivo', fecha = %s WHERE id = %s;")
    try:
        mycursor = db.cursor()
        mycursor.execute(sql, val)
        db.commit()
        print("Sensor " + id + " inactivo. Se ha desconectado")
        return 'ok'
    except:
        print("Algo malo pasa en desconectar el last_will")
        return "ko"


app.run(host="0.0.0.0")

