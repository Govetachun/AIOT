# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# AIO_FEED_ID = ""

print("Hello IoT Python")
from Adafruit_IO import MQTTClient
import time
from fsm import *
from uart import *
import numpy as np
from PIL import Image
import base64
from io import BytesIO


if __name__ == '__main__': 
    # ser = initSerial()
    ser = None # SERIAL
    ai = None # AI
    fsm = FSMIoT(ser, ai)
    
    # img = Image.open("b.png")
    # buffered = BytesIO()
    # img.save(buffered, format="PNG")
    # img_str = base64.b64encode(buffered.getvalue())
    # fsm.publish("AI", img_str)
    while True:
        #DELAY
        # readSerial(ser, fsm)
        time.sleep(1)
        pass
    # After the loop release the cap object

