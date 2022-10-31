# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# AIO_FEED_ID = ""

print("Hello IoT Python")
import sys
from Adafruit_IO import MQTTClient
import random
import time
from uart import *

AIO_FEED_ID = ["bbc-temp"]
AIO_USERNAME = "haiphamcse"
AIO_KEY = "aio_Iktq909kNHktdKuYpY4MBfSEr0RM"

def connected(client):
    for id in AIO_FEED_ID:
        client.subscribe(id)
    print("Ket noi thanh cong ...")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Data is from: " + feed_id + ", Payload: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
# counter_sensor = 30
while True:
    time.sleep(1)
    #
    # counter_sensor = counter_sensor - 1
    # if counter_sensor <= 0:
    #     counter_sensor = 30
    #     temp = random.randint(20,40)
    #     client.publish("sensor1", temp)
    #     humi = random.randint(0, 100)
    #     client.publish("sensor2", humi)
    #     lux = random.randint(0, 400)
    #     client.publish("sensor3", lux)

    readSerial()
    pass
