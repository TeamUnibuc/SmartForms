import random
import cv2
import torch as th
import numpy as np
import ocr.network as network

def data_augment_single_image(img: np.ndarray) -> np.ndarray:
    """
    Performs data augmentation on a single image.
    """
    # change shape
    img = img.reshape((network.IMAGE_SIZE, network.IMAGE_SIZE))

    if random.choice([True, False]):
        # Perform erosion / dilatation
        kernel_size = random.choice([2, 3])
        kernel = np.ones((kernel_size, kernel_size), np.uint8)

        if random.choice([True, False]):
            img = cv2.erode(img, kernel, iterations=1)
        else:
            img = cv2.dilate(img, kernel, iterations=1)

    if random.choice([True, False]):
        # zoom in/out
        zoom_px = random.randint(1, 4)

        if random.choice([True, False]):
            # zoom in    
            img = img[zoom_px : -zoom_px, zoom_px : -zoom_px]
            img = cv2.resize(img, (network.IMAGE_SIZE, network.IMAGE_SIZE))
        else:
            # zoom out
            img = cv2.resize(img, (network.IMAGE_SIZE + 2 * zoom_px, network.IMAGE_SIZE + 2 * zoom_px))[
                zoom_px : -zoom_px, zoom_px : -zoom_px
            ]

    # max nr of pixels to move the image
    MAX_OFFSET = network.IMAGE_SIZE // 5
    x_offset = random.randint(-MAX_OFFSET, MAX_OFFSET)
    y_offset = random.randint(-MAX_OFFSET, MAX_OFFSET)
    
    # translate by x_offset, y_offset
    translate_matrix = np.float32([[1, 0, x_offset], [0, 1, y_offset]])
    img = cv2.warpAffine(img, translate_matrix, (network.IMAGE_SIZE, network.IMAGE_SIZE))

    return img.reshape((1, network.IMAGE_SIZE, network.IMAGE_SIZE))

def data_augment(imgs: th.Tensor) -> th.Tensor:
    """
    Takes a 4d tensor (minibatch, single channel, image)
    and performs data augmentation on all the images.
    """
    return th.stack([
        th.from_numpy(data_augment_single_image(i.numpy()))
        for i in imgs
    ])