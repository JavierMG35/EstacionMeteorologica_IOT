import serial
import pynmea2
import os

#port = subprocess.Popen(["sudo", "cat", "/dev/serial0"])
#os.system("sudo chmod 777 /dev/serial0")
#os.system("sudo chown pi:pi /dev/serial0")
port = "/dev/serial0"

# #>>> import pynmea2
# >>> msg = pynmea2.parse("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")
# >>> msg
# <GGA(timestamp=datetime.time(18, 43, 53), lat='1929.045', lat_dir='S', lon='02410.506', lon_dir='E', gps_qual='1', num_sats='04', horizontal_dil='2.6', altitude=100.0, altitude_units='M', geo_sep='-33.9', geo_sep_units='M', age_gps_data='', ref_station_id='0000')>


def parseGPS(str):
    if str.startswith( '$GPGGA' ):
        msg = pynmea2.parse(str)
        print(msg)
        print(msg.lat)
        print( "Timestamp: %s -- Lat: %s%s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" % (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units, msg.num_sats))

serialPort = serial.Serial(port, baudrate=9600, timeout=1)

while True:
    try:
        str = serialPort.readline().decode()
        parseGPS(str)
    except:
        pass