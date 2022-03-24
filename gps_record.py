import json
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")
device_info = config_object["DEVICEID"]

DEVICE_ID = device_info["deviceId"]


class GPSRecord:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def __str__(self):
        return_value = {"device_id": DEVICE_ID, "location": {
            "latitude": self.lat, "longitude": self.long}}
        return json.dumps(return_value)
