print("Hello Sensors")
import serial.tools.list_ports
import time
import sys
from simple_ai import *
from  Adafruit_IO import  MQTTClient
AIO_FEED_ID = ["nutnhan1", "nutnhan2"]
AIO_USERNAME = "xuan_bach"
AIO_KEY = "aio_Gexj60XsQikXDJnnMJaduFhYjyel"

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

    if feed_id == "nutnhan1":
        if payload == '0':
            uart_write(payload)
        elif payload == '1':
            uart_write(payload)
    elif feed_id == "nutnhan2":
        if payload == '2':
            uart_write(payload)
        elif payload == '3':
            uart_write(payload)
    else:
        uart_write(-1)
    print("Data is from: " + feed_id + ", Payload: " + payload)

client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return "COM4"
mess = ""
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    for split in splitData:
        if split[0] == 'H':
            print("CapnhatH:",split[1:])
            client.publish("humid",int(split[1:]))
        if split[0] == 'T':
            print("CapnhatT:",split[1:])
            client.publish("temp",int(split[1:]))
        if split[0] == 'L':
            print("CapnhatL:",split[1:])
            client.publish("led",int(split[1:]))
        if split[0] == 'P':
            print("CapnhatP:", split[1:])
            client.publish("pump", int(split[1:]))
    print(splitData)

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]
def uart_write(data):
    ser.write((str(data) + '#' ).encode())
    return

var = 0
counter_ai = 5
portName = getPort()

if portName != "None":
    ser = serial.Serial(port=portName, baudrate=115200)

print(ser)
while True:
    if var == 10:
        readSerial()
        var = 0

    var += 1
    counter_ai = counter_ai - 1
    if counter_ai <= 0:
        counter_ai = 5
        image_capture()
        ai_result = image_detector()
        client.publish("aivision", ai_result)
    time.sleep(1)
