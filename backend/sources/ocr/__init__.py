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

IMAGE_SIZE = 32

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

    network = ocr.network.Network.get_instance()
    return network.predict(imgs)

