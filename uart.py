print("Hello Sensors")
import serial.tools.list_ports
import time

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "T" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return "COM7"

mess = "A"

def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "T":
        client.publish("AI", splitData[2])

def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]
    print(mess)
    
portName = getPort()

if portName != "None":
    ser = serial.Serial(port=portName, baudrate=115200)
    print(ser)


# while True:
#     readSerial()
#     print(mess)
#     time.sleep(1)