from typing import List
from black import Line
import numpy as np
import torch as th
import torch.nn as nn
import logging

IMAGE_SIZE = 28
DEVICE = th.device("cuda") if th.cuda.is_available() else th.device("cpu")
DATA_FOLDER = "../data/OCR/"
MODEL_LOCATION = DATA_FOLDER + "ocr_model.pth"
# all possible characters
# we only train by default on 0-9a-zA-Z, but the rest of them
# are trainable on characters sent by the users
CHARACTERS = " " +\
             "abcdefghijklmnopqrstuvwxyz" +\
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
        Network.__instance__ = self

        self.model = nn.Sequential(
            nn.Conv2d(1, 4, kernel_size=(5, 5), padding=(2, 2)),
            nn.ReLU(),
            nn.Conv2d(4, 32, kernel_size=(3, 3), padding=(1, 1)),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d((2, 2)),
            nn.Conv2d(32, 64, kernel_size=(3, 3), padding=(1, 1)),
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
            self.model.load_state_dict(th.load(MODEL_LOCATION))
            logging.info("Loaded model weights from disk.")
        except:
            logging.info("Model not found on disk.")

        self.model.to(DEVICE)
        self.model.eval()

    def predict(self, images: np.ndarray) -> List[str]:
        """
        Predict the most probable character for a given image.
        images is 3d, where the first dim is the number of images.
        """
        self.model.eval()
        predictions = self.model(th.tensor(images, dtype=th.float32).to(DEVICE))
        predictions = np.argmax(predictions.detach().cpu().numpy(), axis=1)

        results = [CHARACTERS[i] for i in predictions]
        return results