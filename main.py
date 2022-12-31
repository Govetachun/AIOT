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

def main(fsm):
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


if __name__ == '__main__':
    # ser = initSerial()
    ser = None # SERIAL
    # ai = keras.models.load_model("keras_model.h5") # AI
    ai = None
    fsm = FSMIoT(ser, ai)
    # staying_alive(fsm)
    print("DONE INIT FSM")
    try:
        main(fsm)
    except KeyboardInterrupt:
        fsm.publish("ACK", '1')
        print("KEYBOARD EXCEPTION, SENDING ERRORS TO SERVER")
        sys.exit(0)


