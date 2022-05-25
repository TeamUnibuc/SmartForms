"""
Trains the network on the EMNIST dataset.
"""

from tqdm import tqdm
from collections import defaultdict
import numpy as np
import ocr.network as network
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import torch as th
import torch.nn as nn
import logging
import cv2
import random

DATASET_PATH = "../data/OCR/dataset/"
IMAGES_PATH = DATASET_PATH + "emnist_imgs.npy"
LABELS_PATH = DATASET_PATH + "emnist_labels.npy"
DEBUG = False

def generate_dataset():
    """
    Generates the dataset and places it in the data/OCR/dataset folder.
    As this function should not be called regularely, it depends on
    `tensorflow-datasets` which is NOT included in the requirements.txt
    file. If you need to run it please run `pip3 install tensorflow-datasets`.
    """
    # we load it here so that the module doesn't crash if tensorflow-datasets
    # is not installed.

    print("Generating dataset...")

    import tensorflow_datasets as t_d
    ds = t_d.load('emnist', split='train', shuffle_files=True)

    data = []
    d = defaultdict(lambda: 0)

    for i in tqdm(ds):
        img = i["image"]
        img = img.numpy().transpose((1, 0, 2))
        img = img.reshape((28, 28))
        lbl = i["label"]
        data.append((img, lbl))

    # add spaces
    for i in range(100000):
        data.append((np.zeros((28, 28), dtype=np.uint8), 62))

    np.random.shuffle(data)

    imgs = [d[0] for d in data]
    labels = [d[1] for d in data]

    def convert_label(l):
        if l < 10:
            return network.CHARACTERS_INDEX[chr(ord('0') + l)]
        elif l < 10 + 26:
            return network.CHARACTERS_INDEX[chr(ord('A') + l - 10)]
        elif l < 10 + 2 * 26:
            return network.CHARACTERS_INDEX[chr(ord('a') + l - 10 - 26)]
        elif l == 62:
            return network.CHARACTERS_INDEX[' ']
        else:
            raise Exception()

    # convert from emnist format to own format
    labels = [convert_label(i) for i in labels]

    data = None

    imgs = np.stack(imgs)
    labels = np.stack(labels)

    print(f"Imgs shape:   {imgs.shape}")
    print(f"Labels shape: {labels.shape}")

    if DEBUG:
        for i in range(10):
            for j in range(10):
                print(network.CHARACTERS[labels[i * 10 + j]], end='')
            print('')

        print(f"Max value: {np.max(imgs[0])}")
        print(f"Average: {np.sum(imgs[0]) / imgs[0].shape[0] / imgs[0].shape[1]}")

        fig, ax = plt.subplots(nrows=10, ncols=10)
        for i in range(100):
            ax[i // 10][i % 10].imshow(imgs[i])

        plt.show()

    os.makedirs(DATASET_PATH)
    np.save(IMAGES_PATH, imgs)
    np.save(LABELS_PATH, labels)
