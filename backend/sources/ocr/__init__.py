"""
Submodule handling Optical Caracter Recognition.
Relies mostly on:
    * Pytorch
    * the `data/` folder at the root of the project.
"""

from typing import List
import numpy as np
import ocr.network
import cv2 as cv
import matplotlib.pyplot as plt

DEBUG = False
# fixed to 28 as this is what most datasets offer
IMAGE_SIZE = 28

def predict_characters(imgs: np.ndarray) -> List[str]:
    """
    imgs: 3d array, where:
        1st dim - number of images to predict
        2-3 dim - image dimensions
    """

    imgs = [cv.resize(i, (IMAGE_SIZE, IMAGE_SIZE)).reshape(IMAGE_SIZE, IMAGE_SIZE, 1) for i in imgs]
    imgs = np.stack(imgs)

    # sanity check
    for i in imgs:
        if i.shape != (IMAGE_SIZE, IMAGE_SIZE, 1):
            raise Exception(
                f"Invalid size passed. Expected ({IMAGE_SIZE}, {IMAGE_SIZE}, 1), received {i.shape}"
            )

    # Normalize to be the same format as training data
    for i in range(len(imgs)):
        imgs[i] = imgs[i] / 255
        imgs[i] = 1. - imgs[i]

    if DEBUG:
        print(f"Max value: {np.max(imgs[0])}")
        print(f"Average value: {np.average(imgs[0])}")
        fig, ax = plt.subplots(nrows=5, ncols=5)
        for i in range(len(imgs)):
            ax[i // 5][i % 5].imshow(imgs[i])

        plt.show()

    network = ocr.network.Network.get_instance()
    return network.predict(imgs)

