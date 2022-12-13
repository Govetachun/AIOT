import keras
import tensorflow as tf
from keras.preprocessing import image
import numpy as np
from keras.applications.resnet import preprocess_input, decode_predictions
import cv2
import torch


def get_webcam_frame(vid):
    ret, frame = vid.read()
    image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = image/127.5 - 1
    return image

def detect(model, image, labels):
    probabilities = model.predict(image)
    # Print what the highest value probabilitie label
    return labels[np.argmax(probabilities)]