import sys
from Adafruit_IO import MQTTClient
from uart import *

AIO_FEED_ID = ["AIvision", "ADC0", "ADC1", "ADC0_Send", "ADC1_Send", "ACK"]
AIO_USERNAME = "xuan_bach"
AIO_KEY = "aio_wejQ496duLYwQl4fNbBMfP6NkZXr"


class FSMIoT(MQTTClient):
    def __init__(self, ser=None, ai=None):
        super().__init__(AIO_USERNAME, AIO_KEY)
        self.on_connect = connected
        self.on_disconnect = disconnected
        self.on_message = message
        self.on_subscribe = subscribe
        self.connect()
        self.loop_background()
        self.ser = ser
        self.ai = ai
        
def message_decoder(client: FSMIoT, feed_id: str, payload):
    #DECODE MESSAGE FROM UART AND OTHERS
    if(feed_id == "AI"):
        print("AI")   
    elif(feed_id == "ADC0_Send" or feed_id == "ADC1_Send"): #1-Hop 2-Hop
        if(payload == '1'): #TOGGLE ON BUTTON
            writeSerial(client.ser, "!RST#")
        elif(payload == '0'): #TOGGLE OFF BUTTON
            writeSerial(client.ser, "!OK#")
    elif(feed_id == "UART"):
        pass
    
def connected(client):
    for id in AIO_FEED_ID:
        client.subscribe(id)
    print("Ket noi thanh cong ...")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")
    
def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)

def message(client , feed_id , payload):
    print("Data is from: " + feed_id + ", Payload: " + payload)
    message_decoder(client, feed_id, payload)
    
    