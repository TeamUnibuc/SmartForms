"""
Submodule handling Optical Caracter Recognition.
Relies mostly on:
    * Pytorch
    * the `data/` folder at the root of the project.
"""

from typing import List
import numpy as np
import ocr.network as network
import cv2 as cv
import cv2
import matplotlib.pyplot as plt

DEBUG = False

# fixed to 28 as this is what most datasets offer
IMAGE_SIZE = network.IMAGE_SIZE

def predict_characters(imgs: np.ndarray, allowed_characters: str) -> List[str]:
    """
    imgs: 3d array, where:
        1st dim - number of images to predict
        2-3 dim - image dimensions
    """

    imgs = [cv.resize(i, (IMAGE_SIZE, IMAGE_SIZE)).reshape(1, IMAGE_SIZE, IMAGE_SIZE) for i in imgs]
    imgs = np.stack(imgs)

    # sanity check
    for i in imgs:
        if i.shape != (1, IMAGE_SIZE, IMAGE_SIZE):
            raise Exception(
                f"Invalid size passed. Expected (1, {IMAGE_SIZE}, {IMAGE_SIZE}), received {i.shape}"
            )

    # Normalize to be the same format as training data
    for i in range(len(imgs)):
        imgs[i] = imgs[i] / 255
        imgs[i] = 1. - imgs[i]

    if DEBUG:
        print(f"Max value: {np.max(imgs[0])}")
        print(f"Average value: {np.average(imgs[0])}")
        fig, ax = plt.subplots(nrows=6, ncols=6)
        for i in range(min(36, len(imgs))):
            ax[i // 6][i % 6].imshow(imgs[i][0])

        plt.show()

    return network.Network.get_instance().predict(imgs, allowed_characters)

