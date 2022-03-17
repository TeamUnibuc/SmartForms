from typing import List, Tuple
import numpy as np
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import logging
import ocr
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import os
import tensorflow
import cv2 as cv

DATA_FOLDER = "../data/OCR/"
MODEL_LOCATION = DATA_FOLDER + "ocr_model.bin"
# all possible characters
# we only train by default on 0-9a-zA-Z, but the rest of them
# are trainable on characters sent by the users
CHARACTERS = " " +\
             "abcdefghijklmnopqrstuvwxyz" +\
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +\
             "01234567890" +\
             "!@#$%^&*()-_=+[]\{}|;':\",./<>?"
CHARACTERS_INDEX = { c: i for i, c in enumerate(CHARACTERS) }

# def load_train_data() -> Tuple[np.ndarray, np.ndarray]:
#     """
#     Returns X, Y
#     """
#     def process_img(img):
#         # resize to the good dimension
#         img = cv.resize(img, (ocr.IMAGE_SIZE, ocr.IMAGE_SIZE))
#         # resize to the good shape
#         img = img.reshape((ocr.IMAGE_SIZE, ocr.IMAGE_SIZE, 1))
#         # # make black be the lines and white the background
#         # img = 255. - img TODO:
#         return img

#     X = np.load(DATA_FOLDER + "alphanum-img.npy")
#     X = np.stack([process_img(i) for i in X])

#     Y = np.load(DATA_FOLDER + "alphanum-chr.npy")
#     Y = np.array([CHARACTERS_INDEX[i] for i in Y])
    
#     return X, Y

class Network:
    """
    Network class, storing a keras network, and training it.
    """
    __instance__: "Network" = None
    
    @staticmethod
    def get_instance():
        if Network.__instance__ is None:
            Network()
        return Network.__instance__

    def __init__(self):
        # handle singleton stuff
        if Network.__instance__ is not None:
            raise Exception("Singleton class Network instanciated twice.")
        Network.__instance__ = self

        # initialization of the network
        self.model = keras.Sequential([
            layers.Conv2D(30, (5, 5), input_shape=(ocr.IMAGE_SIZE, ocr.IMAGE_SIZE, 1), activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(15, (3, 3), activation='relu'),
            layers.MaxPooling2D(),
            layers.Dropout(0.2),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(50, activation='relu'),
            layers.Dense(len(CHARACTERS), activation='softmax')
        ])
        self.model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

        # try to load model
        try:
            self.model.load_weights(MODEL_LOCATION)
            logging.info("Loaded model weights from disk.")
        except:
            logging.info("Model not found on disk.")

    def predict(self, images: np.ndarray) -> List[str]:
        """
        Predict the most probable character for a given image.
        images is 3d, where the first dim is the number of images.
        """
        predictions = self.model.predict(images)
        predictions = np.argmax(predictions, axis=1)

        results = [CHARACTERS[i] for i in predictions]
        return results