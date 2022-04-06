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

DATASET_PATH = "../data/OCR/dataset/"
IMAGES_PATH = DATASET_PATH + "emnist_imgs.npy"
LABELS_PATH = DATASET_PATH + "emnist_labels.npy"
DEBUG = True

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

def train_model_epoch(model: nn.Sequential, optimizer: th.optim.Adam, loss_fn: nn.CrossEntropyLoss,
        train_dataloader: th.utils.data.DataLoader, test_dataloader: th.utils.data.DataLoader, epochs: int):
    """
    Run the algorithm a few epochs
    """
    for epoch_n in range(epochs):
        print(f"Epoch #{epoch_n + 1}")

        train_all_predictions = []
        train_all_targets = []
        train_loss = []

        model.train()
        for batch in tqdm(train_dataloader):
            model.zero_grad()

            inputs, targets = batch
            inputs = inputs.to(network.DEVICE)
            targets = targets.to(network.DEVICE)

            # data augmentation
            # TODO:

            output = model(inputs)
            loss = loss_fn(output, targets)
            predictions = output.argmax(1)

            loss.backward()
            optimizer.step()
            
            train_loss.append(loss.detach().cpu().item())
            train_all_targets.append(targets.detach().cpu())
            train_all_predictions.append(predictions.detach().cpu())

        train_all_predictions = th.cat(train_all_predictions)
        train_all_targets = th.cat(train_all_targets)

        val_acc = (train_all_predictions == train_all_targets).float().mean().numpy()
        print(f"Train Accuracy: {val_acc}")
        print(f"Train Loss: {np.mean(np.array(train_loss))}")

        # validare
        model.eval()
        eval_all_predictions = []
        eval_all_targets = []
        for batch in test_dataloader:
            inputs, targets = batch
            inputs = inputs.to(network.DEVICE)
            targets = targets.to(network.DEVICE)

            with th.no_grad():
                output = model(inputs)

            predictions = output.argmax(1)
            eval_all_targets.append(targets.detach().cpu())
            eval_all_predictions.append(predictions.detach().cpu())

        eval_all_predictions = th.cat(eval_all_predictions)
        eval_all_targets = th.cat(eval_all_targets)

        val_acc = (eval_all_predictions == eval_all_targets).float().mean().numpy()

        print(f"Val Accuracy: {val_acc}")

def train_model():
    """
        Trains the model on the dataset provided
    """
    logging.info("Training model...")
    try:
        x = np.load(IMAGES_PATH)
        y = np.load(LABELS_PATH)
    except:
        print("Dataset not available. Generating it...")
        generate_dataset()
        x = np.load(IMAGES_PATH)
        y = np.load(LABELS_PATH)    

    x = x.reshape((-1, 1, 28, 28))
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=21)

    # normalize
    x_train = x_train / 255.0
    x_test = x_test / 255.0

    x_train = th.tensor(x_train, dtype=th.float32)
    y_train = th.tensor(y_train)
    x_test = th.tensor(x_test, dtype=th.float32)
    y_test = th.tensor(y_test)

    if DEBUG:
        for i in range(10):
            for j in range(10):
                print(network.CHARACTERS[y_train[i * 10 + j]], end='')
            print('')

        print(f"Max value: {th.max(x_train[0])}")
        print(f"Average: {th.mean(x_train[0])}")

        fig, ax = plt.subplots(nrows=10, ncols=10)
        for i in range(100):
            ax[i // 10][i % 10].imshow(x_train[i][0])

        plt.show()

    model = network.Network.get_instance().model

    train_dataset = th.utils.data.TensorDataset(x_train, y_train)
    train_dataloader = th.utils.data.DataLoader(train_dataset, batch_size=128, shuffle=True)

    test_dataset = th.utils.data.TensorDataset(x_test, y_test)
    test_dataloader = th.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)

    print("Training model...")

    criterion = nn.CrossEntropyLoss()
    optimizer = th.optim.Adam(model.parameters(), lr=1e-3)
    train_model_epoch(model, optimizer, criterion, train_dataloader, test_dataloader, 4)

    optimizer = th.optim.Adam(model.parameters(), lr=1e-4)
    train_model_epoch(model, optimizer, criterion, train_dataloader, test_dataloader, 4)

    optimizer = th.optim.Adam(model.parameters(), lr=1e-5)
    train_model_epoch(model, optimizer, criterion, train_dataloader, test_dataloader, 4)

    if not os.path.exists(network.DATA_FOLDER):
        os.makedirs(network.DATA_FOLDER)

    th.save(model.state_dict(), network.MODEL_LOCATION)
    # net.model.save_weights(network.MODEL_LOCATION)

    # # Final evaluation of the model
    # scores = model.evaluate(x_test, y_test, verbose=0)

    # predictions = np.argmax(net.model.predict(x_test), axis=1)
    # confusion_matrix = tf.math.confusion_matrix(y_test_raw, predictions)

    # print("Confusion matrix:")
    # print(confusion_matrix)

    # print("Validation error: %.2f%%" % (100-scores[1]*100))