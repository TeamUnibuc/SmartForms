"""
Submodule handling Optical Caracter Recognition.
Relies mostly on:
    * Pytorch
    * the `data/` folder at the root of the project.
"""

from typing import List
import numpy as np
import ocr.network

IMAGE_SIZE = 30

def predict_characters(imgs: np.ndarray) -> List[str]:
    """
    imgs: 4d array, where:
        1st dim - number of images to predict
        2nd dim - rgb channel
        3-4 dim - image dimensions
    """
    
    # sanity check
    for i in imgs:
        if i.shape != (IMAGE_SIZE, IMAGE_SIZE):
            raise Exception(
                f"Invalid size passed. Expected ({IMAGE_SIZE}, {IMAGE_SIZE}, received {i.shape}"
            )

    network = ocr.network.Network.get_instance()
    return network.predict(imgs)

