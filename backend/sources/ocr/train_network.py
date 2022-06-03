"""
Trains the network on the EMNIST dataset.
"""

from collections import defaultdict
import sklearn.metrics as metrics
from tqdm import tqdm
import numpy as np
import ocr.network as network
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import torch as th
import torch.nn as nn
import logging
import ocr.generate_dataset as generate_dataset
import ocr.data_preprocessing as data_preprocessing
from sklearn.utils.class_weight import compute_class_weight

DATASET_PATH = generate_dataset.DATASET_PATH
IMAGES_PATH = DATASET_PATH + "emnist_imgs.npy"
LABELS_PATH = DATASET_PATH + "emnist_labels.npy"
DEBUG = False

def compute_network_accuracy_by_classes(predictions: th.Tensor, labels: th.Tensor):
    """
    Computes the accuracy, taking into account classes (for a lowercase only consider lowercase letters etc).
    """
    def is_same_class(a: int, b: int):
        if a == network.CHARACTERS_INDEX[' '] or b == network.CHARACTERS_INDEX[' ']:
            return a == b
        if a == b:
            return True
        if a > b:
            a, b = b, a
        if a == b == network.CHARACTERS_INDEX[' ']:
            return True
        if network.CHARACTERS_INDEX['a'] <= a and b <= network.CHARACTERS_INDEX['z']:
            return True
        if network.CHARACTERS_INDEX['A'] <= a and b <= network.CHARACTERS_INDEX['Z']:
            return True
        if network.CHARACTERS_INDEX['0'] <= a and b <= network.CHARACTERS_INDEX['9']:
            return True
        return False
    
    def check(ord_preds: th.Tensor, label: int):
        for i in ord_preds:
            if is_same_class(i, label):
                return i == label
        assert False

    ordered_predictions = th.flip(np.argsort(predictions, axis=1), [1])
    return sum([check(pred, label) for pred, label in zip(ordered_predictions, labels)]) / labels.shape[0]

train_loss = []
validation_loss = []
train_raw_accuracy = []
train_class_accuracy = []
validation_raw_accuracy = []
validation_class_accuracy = []


def train_model_epoch(model: nn.Sequential, optimizer: th.optim.Adam, loss_fn: nn.CrossEntropyLoss,
        train_dataloader: th.utils.data.DataLoader, test_dataloader: th.utils.data.DataLoader, epochs: int):
    """
    Run the algorithm a few epochs
    """
    global train_loss, train_raw_accuracy, train_class_accuracy
    global validation_loss, validation_raw_accuracy, validation_class_accuracy

    for epoch_n in range(epochs):
        print(f"Epoch #{epoch_n + 1}")

        running_loss = []
        running_accuracy = []
        running_class_accuracy = []

        model.train()
        for batch in tqdm(train_dataloader):
            model.zero_grad()

            inputs, targets = batch
            # data augmentation
            inputs = data_preprocessing.data_augment(inputs)
            inputs = data_preprocessing.images_processing(inputs)
            inputs = th.tensor(inputs.reshape((-1, 1, 28, 28)), dtype=th.float32)

            inputs = inputs.to(network.DEVICE)
            targets = targets.to(network.DEVICE)

            output = model(inputs)

            loss = loss_fn(output, targets)
            
            loss.backward()
            optimizer.step()

            loss = loss.detach().cpu().item()
            predictions = output.detach().cpu()
            targets = targets.detach().cpu()

            raw_accuracy = sum(predictions.argmax(1) == targets) / predictions.shape[0]
            class_accuracy = compute_network_accuracy_by_classes(predictions, targets)
            
            train_loss.append(loss)
            train_raw_accuracy.append(raw_accuracy)
            train_class_accuracy.append(class_accuracy)
            running_loss.append(loss)
            running_accuracy.append(raw_accuracy)
            running_class_accuracy.append(class_accuracy)

        print(f"Train loss: {th.mean(th.tensor(running_loss))}")
        print(f"Train raw accuracy: {th.mean(th.tensor(running_accuracy))}")
        print(f"Train class accuracy: {th.mean(th.tensor(running_class_accuracy))}")
            
        # validare
        model.eval()

        running_loss = []
        running_accuracy = []
        running_class_accuracy = []

        for batch in test_dataloader:
            inputs, targets = batch
            inputs = data_preprocessing.images_processing(inputs)
            inputs = th.tensor(inputs.reshape((-1, 1, 28, 28)), dtype=th.float32)

            inputs = inputs.to(network.DEVICE)
            targets = targets.to(network.DEVICE)

            with th.no_grad():
                output = model(inputs)

            loss = loss_fn(output, targets).detach().cpu()
            predictions = output.detach().cpu()
            targets = targets.detach().cpu()

            raw_accuracy = sum(predictions.argmax(1) == targets) / predictions.shape[0]
            class_accuracy = compute_network_accuracy_by_classes(predictions, targets)
            
            validation_loss.append(loss)
            validation_raw_accuracy.append(raw_accuracy)
            validation_class_accuracy.append(class_accuracy)
            running_loss.append(loss)
            running_accuracy.append(raw_accuracy)
            running_class_accuracy.append(class_accuracy)

        print(f"Validation loss: {th.mean(th.tensor(running_loss))}")
        print(f"Validation raw accuracy: {th.mean(th.tensor(running_accuracy))}")
        print(f"Validation class accuracy: {th.mean(th.tensor(running_class_accuracy))}")

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
        generate_dataset.generate_dataset()
        x = np.load(IMAGES_PATH)
        y = np.load(LABELS_PATH)    

    # x = x[:100000]
    # y = y[:100000]

    weights = compute_class_weight('balanced', classes=np.unique(y), y=y)
    weights = np.concatenate([weights, np.zeros(len(network.CHARACTERS) - len(weights))])

    x = x.reshape((-1, 28, 28))
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=21)

    x_train = th.from_numpy(x_train)
    y_train = th.from_numpy(y_train)
    x_test = th.from_numpy(x_test)
    y_test = th.from_numpy(y_test)

    if DEBUG:
        for i in range(10):
            for j in range(10):
                print(network.CHARACTERS[y_train[i * 10 + j]], end='')
            print('')

        print(f"Max value: {th.max(x_train[0])}")
        print(f"Average: {th.sum(x_train[0]) / x_train[0].shape[0] / x_train[0].shape[1]}")

        # print("Raw data:")
        # fig, ax = plt.subplots(nrows=10, ncols=10)
        # imgs = x_train[:100]
        # for i in range(100):
        #     ax[i // 10][i % 10].imshow(imgs[i])
        # plt.show()

        # print("Processed data:")
        # fig, ax = plt.subplots(nrows=10, ncols=10)
        # imgs = data_preprocessing.data_augment(x_train[:100])
        # for i in range(100):
        #     ax[i // 10][i % 10].imshow(imgs[i])
        # plt.show()

        # print("Raw data processed:")
        # fig, ax = plt.subplots(nrows=10, ncols=10)
        # imgs = data_preprocessing.images_processing(x_train[:100])
        # for i in range(100):
        #     ax[i // 10][i % 10].imshow(imgs[i])
        # plt.show()

        print("Processed data:")
        fig, ax = plt.subplots(nrows=10, ncols=10)
        imgs = data_preprocessing.images_processing(
            data_preprocessing.data_augment(x_train[:100])
        )
        for i in range(100):
            ax[i // 10][i % 10].imshow(imgs[i])
        plt.show()

    model = network.Network.get_instance().model

    train_dataset = th.utils.data.TensorDataset(x_train, y_train)
    train_dataloader = th.utils.data.DataLoader(train_dataset, batch_size=256, shuffle=True)

    test_dataset = th.utils.data.TensorDataset(x_test, y_test)
    test_dataloader = th.utils.data.DataLoader(test_dataset, batch_size=128, shuffle=False)

    print("Training model...")

    criterion = nn.CrossEntropyLoss(weight=th.tensor(weights, dtype=th.float32)).to(network.DEVICE)

    optimizer = th.optim.Adam(model.parameters(), lr=1e-3)
    train_model_epoch(model, optimizer, criterion, train_dataloader, test_dataloader, 2)

    th.save(model.state_dict(), network.MODEL_LOCATION)

    optimizer = th.optim.Adam(model.parameters(), lr=1e-4)
    train_model_epoch(model, optimizer, criterion, train_dataloader, test_dataloader, 2)

    th.save(model.state_dict(), network.MODEL_LOCATION)

    optimizer = th.optim.Adam(model.parameters(), lr=1e-5)
    train_model_epoch(model, optimizer, criterion, train_dataloader, test_dataloader, 1)

    th.save(model.state_dict(), network.MODEL_LOCATION)

    optimizer = th.optim.Adam(model.parameters(), lr=1e-6)
    train_model_epoch(model, optimizer, criterion, train_dataloader, test_dataloader, 1)

    if not os.path.exists(network.DATA_FOLDER):
        os.makedirs(network.DATA_FOLDER)

    th.save(model.state_dict(), network.MODEL_LOCATION)

    # Final evaluation of the model
    labels = []
    predictions = []

    for batch in test_dataloader:
        inputs, targets = batch
        inputs = data_preprocessing.images_processing(inputs)
        inputs = th.tensor(inputs.reshape((-1, 1, 28, 28)), dtype=th.float32)

        inputs = inputs.to(network.DEVICE)
        targets = targets.to(network.DEVICE)

        with th.no_grad():
            output = model(inputs)

        predicted = output.argmax(1)
        labels.append(targets.detach().cpu())
        predictions.append(predicted.detach().cpu())

    labels = th.concat(labels).numpy()
    predictions = th.concat(predictions).numpy()

    accuracy = metrics.accuracy_score(labels, predictions)
    logging.info(f"Final validation accuracy: {accuracy}")
    conf_matrix = metrics.confusion_matrix(labels, predictions)
    confusion = [(conf_matrix[i][j], network.CHARACTERS[i], network.CHARACTERS[j], i, j) for i in range(len(conf_matrix)) for j in range(len(conf_matrix)) if i != j]
    confusion.sort()
    confusion = confusion[::-1]

    print("Biggest confusions:")
    for nr_conf, a, b, id_a, id_b in confusion[:30]:
        print(f" * '{a}' read as '{b}': {nr_conf}  -  '{a}' seen correctly: {conf_matrix[id_a][id_a]}, '{b}' seen correctly: {conf_matrix[id_b][id_b]}")


    global train_class_accuracy, train_raw_accuracy, train_loss
    global validation_class_accuracy, validation_raw_accuracy, validation_loss

    np.save(network.DATA_FOLDER + "train_class_accuracy.npy", np.array(train_class_accuracy))
    np.save(network.DATA_FOLDER + "val_class_accuracy.npy", np.array(validation_class_accuracy))
    np.save(network.DATA_FOLDER + "train_raw_accuracy.npy", np.array(train_raw_accuracy))
    np.save(network.DATA_FOLDER + "val_raw_accuracy.npy", np.array(validation_raw_accuracy))
    np.save(network.DATA_FOLDER + "train_loss.npy", np.array(train_loss))
    np.save(network.DATA_FOLDER + "val_loss.npy", np.array(validation_loss))
    
    # conf_matrix = metrics.ConfusionMatrixDisplay.from_predictions(labels, predictions) # , display_labels=[i for i in network.CHARACTERS])

    # plt.show()

    # plt.matshow()
    # print(matrix)
    # scores = model.evaluate(x_test, y_test, verbose=0)

    # predictions = np.argmax(net.model.predict(x_test), axis=1)
    # confusion_matrix = tf.math.confusion_matrix(y_test_raw, predictions)

    # print("Confusion matrix:")
    # print(confusion_matrix)

    # print("Validation error: %.2f%%" % (100-scores[1]*100))