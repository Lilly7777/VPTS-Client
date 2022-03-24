from pynmea2 import parse
import time
from time import sleep
import serial
from configparser import ConfigParser
from gps_record import GPSRecord
from mqtt_client import MQTTClient

config_object = ConfigParser()
config_object.read("config.ini")
path_info = config_object["PATH"]
device_info = config_object["DEVICEID"]

DEVICE_ID = device_info["deviceId"]

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=20.0)

mqtt_client = MQTTClient(10, "Client-1")
mqtt_client.start()

while True:
    try:
        message = ser.readline().decode('utf-8')
        message = message.strip()
        if '$GNGGA' in message:
            gpgga = parse(message)
            lat = float(gpgga.latitude)
            lon = float(gpgga.longitude)
            loc = str(GPSRecord(lat, lon))
            mqtt_client.send_message("device/" + DEVICE_ID, loc, 1)
            print(time.strftime("%H:%M:%S"))
            sleep(15)
    except UnicodeDecodeError:
        print("Wrong data, retrying...")
        continue
    except KeyboardInterrupt:
        mqtt_client.disconnect()
        break
