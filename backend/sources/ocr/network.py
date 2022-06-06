from typing import List
import numpy as np
import torch as th
import torch.nn as nn
import logging
import os
import ocr.data_preprocessing as data_preprocessing
import matplotlib.pyplot as plt


IMAGE_SIZE = 28
DEVICE = th.device("cuda") if th.cuda.is_available() else th.device("cpu")
# need absolute path to avoid problems with testing
DATA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "/../../data/OCR/"
MODEL_LOCATION = DATA_FOLDER + "ocr_model.pth"
# all possible characters
# we only train by default on 0-9a-zA-Z, but the rest of them
# are trainable on characters sent by the users
CHARACTERS = " " +\
             "abcdefghijklmnopqrstuvwxyz" +\
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +\
             "0123456789" +\
             "!@#$%^&*()-_=+[]\{}|;':\",./<>?"
CHARACTERS_INDEX = { c: i for i, c in enumerate(CHARACTERS) }
DEBUG = False

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

        self.model = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(5, 5), padding=(2, 2)),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d((2, 2)),
            nn.Conv2d(32, 64, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),

            nn.BatchNorm2d(64),
            nn.MaxPool2d((2, 2)),

            nn.Flatten(),
            nn.Dropout(0.2),

            nn.Linear((IMAGE_SIZE // 4)**2 * 64, 1024),
            nn.ReLU(),

            nn.Linear(1024, len(CHARACTERS))
        )

        # try to load model        
        try:
            self.model.load_state_dict(th.load(MODEL_LOCATION, map_location=DEVICE))
            logging.info("Loaded model weights from disk.")
        except:
            logging.info("Model not found on disk.")

        self.model.to(DEVICE)
        self.model.eval()

    def predict(self, images: np.ndarray, allowed_characters: str) -> List[str]:
        """
        Predict the most probable character for a given image.
        images is 3d, where the first dim is the number of images.
        images has types np.uint8
        """
        images = th.from_numpy(images)
        images = data_preprocessing.images_processing(images)
        
        if DEBUG:
            fig, ax = plt.subplots(nrows=6, ncols=6)
            for i in range(min(36, len(images))):
                ax[i // 6][i % 6].imshow(images[i])

            plt.show()

        inputs = images.reshape((-1, 1, 28, 28)).type(th.float32).to(DEVICE)

        # pass model in eval mode
        self.model.eval()
        # compute predictions
        predictions = self.model(inputs)
        # convert to numpy
        predictions = predictions.detach().cpu().numpy()
        # sort according to probabilities
        predictions = np.argsort(predictions, axis=1)[:, ::-1]

        results = []
        allowed_characters_set = set(allowed_characters)

        # for each question, get character most probable, out of allowed list
        for prediction in predictions:
            result = ""

            # no characters specified. Just accept most probable char.
            if len(allowed_characters_set) == 0:
                result = CHARACTERS[prediction[0]]
            else:
                for pred in prediction:
                    if CHARACTERS[pred] in allowed_characters_set:
                        result = CHARACTERS[pred]
                        break
            
            assert result != ""
            results.append(result)
            
        return results