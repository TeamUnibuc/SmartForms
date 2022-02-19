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
CHARACTERS = "abcdefghijklmnopqrstuvwxyz" +\
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +\
             "01234567890" +\
             "!@#$%^&*()-_=+[]\{}|;':\",./<>?"
CHARACTERS_INDEX = { c: i for i, c in enumerate(CHARACTERS) }

def load_train_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns X, Y
    """
    X, Y = np.array([]), np.array([])
    # TODO:

    return X, Y

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
        Network.__init__ = self

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
            layers.Dense(10, activation='softmax')
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
            logging.info("Model not found on disk. Training...")
            self.train_model()

    def train_model(self):
        """
        Train the model on the data.
        """
        x, y = load_train_data()

        x_train, x_test, x_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=21)

        # normalize
        x_train = x_train / 255.0
        x_test = x_test / 255.0

        # one-hot encode
        y_test_raw = y_test
        y_train = to_categorical(y_train)
        y_test = to_categorical(y_test)

        print("Training model...")
        self.model.fit(
            x_train,
            y_train,
            validation_data=(x_test, y_test),
            epochs=20,
            batch_size=50,
        )

        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)

        self.model.save_weights(MODEL_LOCATION)

        # Final evaluation of the model
        scores = self.model.evaluate(x_test, y_test, verbose=0)

        predictions = np.argmax(self.model.predict(x_test), axis=1)
        confusion_matrix = tensorflow.math.confusion_matrix(y_test_raw, predictions)

        print("Confusion matrix:")
        print(confusion_matrix)

        print("Validation error: %.2f%%" % (100-scores[1]*100))

    def predict(self, images: np.ndarray) -> List[str]:
        """
        Predict the most probable character for a given image.
        images is 3d, where the first dim is the number of images.
        """
        predictions = self.model.predict(images)
        predictions = np.argmax(predictions, axis=1)

        results = [CHARACTERS[i] for i in predictions]
        return results