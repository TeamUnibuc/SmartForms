"""
Trains the network on the EMNIST dataset.
"""

from tqdm import tqdm
from collections import defaultdict
import numpy as np
import ocr.network as network
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import tensorflow as tf
import os

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
        lbl = i["label"]
        data.append((img, lbl))

    # add spaces
    for i in range(100000):
        data.append((np.zeros((28, 28, 1), dtype=np.uint8), 62))

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
    imgs = imgs.reshape((-1, 28, 28))
    labels = np.stack(labels)

    print(f"Imgs shape:   {imgs.shape}")
    print(f"Labels shape: {labels.shape}")

    np.save(IMAGES_PATH, imgs)
    np.save(LABELS_PATH, labels)

def train_model():
    """
        Trains the model on the dataset provided
    """
    try:
        x = np.load(IMAGES_PATH)
        y = np.load(LABELS_PATH)
    except:
        print("Dataset not available. Generating it...")
        generate_dataset()
        x = np.load(IMAGES_PATH)
        y = np.load(LABELS_PATH)    

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=21)

    # normalize
    x_train = x_train / 255.0
    x_test = x_test / 255.0

    if DEBUG:
        fig, ax = plt.subplots(nrows=10, ncols=10)
        for i in range(100):
            ax[i // 10][i % 10].imshow(x_train[i])

        plt.show()

        for i in range(10):
            for j in range(10):
                print(network.CHARACTERS[y_train[i * 10 + j]], end='')
            print('')

        print(f"Max value: {np.max(x_train[0])}")
        print(f"Average: {np.average(x_train[0])}")


    # one-hot encode
    y_test_raw = y_test
    y_train = to_categorical(y_train, num_classes=len(network.CHARACTERS))
    y_test = to_categorical(y_test, num_classes=len(network.CHARACTERS))

    print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

    net = network.Network.get_instance()

    print("Training model...")
    net.model.fit(
        x_train,
        y_train,
        validation_data=(x_test, y_test),
        epochs=1,
        batch_size=50,
    )

    if not os.path.exists(network.DATA_FOLDER):
        os.makedirs(network.DATA_FOLDER)

    net.model.save_weights(network.MODEL_LOCATION)

    # Final evaluation of the model
    scores = net.model.evaluate(x_test, y_test, verbose=0)

    predictions = np.argmax(net.model.predict(x_test), axis=1)
    confusion_matrix = tf.math.confusion_matrix(y_test_raw, predictions)

    print("Confusion matrix:")
    print(confusion_matrix)

    print("Validation error: %.2f%%" % (100-scores[1]*100))