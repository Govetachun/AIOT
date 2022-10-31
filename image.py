import tensorflow_datasets as tfds
import time
from Adafruit_IO import MQTTClient

def load_image(client: MQTTClient) -> None:
    ds = tfds.load('mnist', split='test', shuffle_files=True)
    ds = ds.take(10)
    for image, label in tfds.as_numpy(ds):
        print(image)
        client.publish("bbc-temp ", image)
        time.sleep(30)

