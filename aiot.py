import keras
import tensorflow as tf
from keras.preprocessing import image
import numpy as np
from keras.applications.resnet import preprocess_input, decode_predictions

def predict(img, model):
    img = tf.image.resize(img,(224, 224))
    x = preprocess_input(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    return decode_predictions(preds)[0]