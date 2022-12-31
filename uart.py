import serial.tools.list_ports
import time

def initSerial():
    portName = getPort()
    if portName != "None":
        ser = serial.Serial(port=portName, baudrate=9600, timeout=1)
    return ser

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
    return "COM11"

mess = ""
    

def processData(client, data):
    #PROCESS DATA AND ACTIVATE 1 HOP
    if("!END#" in data):
        client.publish("ACK", 1)
        print("Timed out, shutting down UART") #IF AFTER 5s STM32 doesn't get !OK# 
    elif("!ADC0" in data): #SEND ADC DATA
        data = data.replace("!ADC0=", "")
        data = data.replace("#", "")
        # print(f"ADC0: {data}") 
        client.publish("humid", data)
    elif("!ADC1" in data):
        data = data.replace("!ADC1=", "")
        data = data.replace("#", "")
        client.publish("pump", data)
    elif("!ADC=" in data):
        data = data.replace("!ADC=", "")
        data = data.replace("#","")
        client.publish("BBC_LED", data)
def writeSerial(ser, data):
    ser.write(str(data).encode('UTF-8'))

def readSerial(ser, client):
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
    return mess