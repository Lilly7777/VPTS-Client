from pynmea2 import parse
import time
from time import sleep
import serial
from configparser import ConfigParser
from gps_record import GPSRecord
from mqtt_client import MQTTClient
import pigpio
import difflib
import sys

RX=18

config_object = ConfigParser()
config_object.read("config.ini")
path_info = config_object["PATH"]
device_info = config_object["DEVICEID"]

DEVICE_ID = device_info["deviceId"]

mqtt_client = MQTTClient(10, "Client-1")
mqtt_client.start()

while True:
    try:
        pi = pigpio.pi()
        pi.set_mode(RX, pigpio.INPUT)
        pi.bb_serial_read_open(RX, 9600, 8)
        message = pi.bb_serial_read(RX)
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
        pi.bb_serial_read_close(RX)
        pi.stop()
        break
