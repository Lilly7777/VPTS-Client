import paho.mqtt.client as paho
import threading
from gps_record import DEVICE_ID
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")

class MQTTClient(threading.Thread):
    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.client = paho.Client()
        self.thread_name = thread_name
        self.thread_id = thread_id

    def run(self):
        self.connect(self.client)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("device/" + DEVICE_ID)

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def send_message(self, topic, payload, qos):
        if self.client.is_connected():
            self.client.publish(topic, payload=str(
                payload), qos=qos, retain=False)

    def connect(self, client):
        client_info = config_object["CLIENTINFO"]
        connect_info = config_object["CONNECTINFO"]
        client.username_pw_set(username=client_info["username"],
                               password=client_info["password"])
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(
            connect_info["host"], int(connect_info["port"]), int(connect_info["keepalive"]))

    def disconnect(self):
        self.client.disconnect()
