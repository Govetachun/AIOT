import sys
from Adafruit_IO import MQTTClient
from uart import *
import time, threading
from aiot import *
import cv2
import base64
from io import BytesIO
import random
# AIO_FEED_ID = ["humid", "pump", "nutnhan1", "nutnhan2", "ACK", "OK", "ADC0", "ADC0_Send"]
# AIO_USERNAME = "xuan_bach"
# AIO_KEY = "aio_wejQ496duLYwQl4fNbBMfP6NkZXr"
AIO_FEED_ID = ["BBC_LED", "BBC_TEMP", "nutnhan1", "nutnhan2", "SEND", "ACK"]
AIO_USERNAME = "haiphamcse"
AIO_KEY = "aio_qOyi32wBmfiFxcpOE4DP2B9LdMTm"
# vid = cv2.VideoCapture(0)
# class_names = open('labels.txt', 'r').readlines()
vid = None
class_names = None
class FSMIoT(MQTTClient):
    def __init__(self, ser=None, ai=None):
        super().__init__(AIO_USERNAME, AIO_KEY)
        self.on_connect = connected
        self.on_disconnect = disconnected
        self.on_message = message
        # self.on_subscribe = subscribe
        self.connect()
        self.loop_background()
        #SEND ACK
        self.publish("ACK", 0)
        self.ser = ser
        self.ai = ai
                
def process_ai(client: FSMIoT):
    image = get_webcam_frame(vid)
    s = base64.b64encode(image)
    # r = base64.decodebytes(s)
    # q = np.frombuffer(r, dtype=np.float64)
    client.publish("ADC0", s)
    print("PUBLISHED FRAME")
    
def message_decoder(client: FSMIoT, feed_id: str, payload):
    #DECODE MESSAGE FROM UART AND OTHERS
    if(feed_id == "ADC0_Send"):
        print("AI")
        #GET AN IMAGE FROM WEBCAM
        # process_ai(client)
        img = get_webcam_frame(vid)
        # label = detect(client.ai, image, class_names)
        prediction = client.ai.predict(img)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        client.publish("AIvision", class_name)
    # elif(feed_id == "nutnhan1"):
    #     if(payload == '1'):
    #         writeSerial(client.ser, "!RST1#")
    # elif(feed_id == "nutnhan2"):
    #     if(payload == '2'):
    #         writeSerial(client.ser, "!RST2#")
    elif(feed_id == "SEND"):
        if(payload == '1'):
            writeSerial(client.ser, "!OK#")
            client.publish("SEND", '0') #RESET OK0
        if(payload == '2'):
            writeSerial(client.ser, "!OK2#")
            client.publish("OK", '0') #RESET OK1
    elif(feed_id == "nutnhan1"):
        if(payload == '1'):
            writeSerial(client.ser, "!RST#")
            # client.publish("BBC_LED", random.randint(0, 100))
    elif(feed_id == "nutnhan2"):
        if(payload == '1'):
            client.publish("BBC_TEMP", random.randint(0, 100))
def connected(client):
    for id in AIO_FEED_ID:
        client.subscribe(id)
    print("Ket noi thanh cong ...")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")
    
def disconnected(client):
    client.publish("ACK", 1) #REPORTING ERROR
    print("Ngat ket noi ...")
    sys.exit(1)

def message(client , feed_id , payload):
    print("Data is from: " + feed_id + ", Payload: " + payload)
    if(feed_id == "humid" or feed_id == "pump"):
        pass
    else:
        message_decoder(client, feed_id, payload)
    
    