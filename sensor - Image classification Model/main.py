import sys
import random
import time
from simple_ai import *
from  Adafruit_IO import  MQTTClient
AIO_FEED_ID = ["bbc-led", "bbc-pump"]
AIO_USERNAME = "xuan_bach1809"
AIO_KEY = "aio_yIiB30Zf6B6kqgVPQATfJ7jnyzJR"

def connected(client):
    print("Ket noi thanh cong ...")
    for id in AIO_FEED_ID:
        client.subscribe(id)

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
var = 0
counter_ai = 5
while True:
    if var == 10:
       value = random.randint(0, 100)
       print("Cap nhat1:", value)
       client.publish("bbc-temp", value)
    elif var == 20:
       value2 = random.randint(0, 90) + random.randint(0, 10)
       print("Cap nhat2:", value2)
       client.publish("bcc-temp2", value2)
    elif var == 30:
       value3 = random.randint(0, 80) + random.randint(0, 20)
       print("Cap nhat3:", value3)
       client.publish("bcc-temp3", value3)
       var = 0
    var+=1

    counter_ai = counter_ai - 1
    if counter_ai <=0:
        counter_ai = 5
        image_capture()
        ai_result = image_detector()
        client.publish("visiondetection", ai_result)
    time.sleep(1)
