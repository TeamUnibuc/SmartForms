from typing import List
import numpy as np
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import logging
import ocr

DATA_FOLDER = "../data/OCR/"
MODEL_LOCATION = DATA_FOLDER + "ocr_model.bin"
CHARACTERS = "abcdefghijklmnopqrstuvwxyz" +\
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +\
             "01234567890" +\
             "!@#$%^&*()-_=+[]\{}|;':\",./<>?"
CHARACTERS_INDEX = { c: i for i, c in enumerate(CHARACTERS) }

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
        pass
        # TODO:

    def predict(self, images: np.ndarray) -> List[str]:
        """
        Predict the most probable character for a given image.
        images is 3d, where the first dim is the number of images.
        """
        predictions = self.model.predict(images)
        predictions = np.argmax(predictions, axis=1)

        results = [CHARACTERS[i] for i in predictions]
        return results