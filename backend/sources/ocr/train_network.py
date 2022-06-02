"""
Trains the network on the EMNIST dataset.
"""

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
            
            # train_loss.append(loss)
            # train_raw_accuracy.append(raw_accuracy)
            # train_class_accuracy.append(class_accuracy)
            running_loss.append(loss)
            running_accuracy.append(raw_accuracy)
            running_class_accuracy.append(class_accuracy)

        train_loss.append(th.mean(th.tensor(running_loss)))
        print(f"Train loss: {train_loss[-1]}")
        train_raw_accuracy.append(th.mean(th.tensor(running_accuracy)))
        print(f"Train raw accuracy: {train_raw_accuracy[-1]}")
        train_class_accuracy.append(th.mean(th.tensor(running_class_accuracy)))
        print(f"Train class accuracy: {train_class_accuracy[-1]}")
            
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
            
            running_loss.append(loss)
            running_accuracy.append(raw_accuracy)
            running_class_accuracy.append(class_accuracy)

        validation_loss.append(th.mean(th.tensor(running_loss)))
        print(f"validation loss: {validation_loss[-1]}")
        validation_raw_accuracy.append(th.mean(th.tensor(running_accuracy)))
        print(f"validation raw accuracy: {validation_raw_accuracy[-1]}")
        validation_class_accuracy.append(th.mean(th.tensor(running_class_accuracy)))
        print(f"validation class accuracy: {validation_class_accuracy[-1]}")

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

    # fig, ax = plt.subplots(nrows=8, ncols=8)
    # plt.figure(figsize=(9, 7))
    # for i in range(1000):
    #     l = y[i]
    #     print(l)
    #     ax[l // 8, l % 8].imshow(x[i])

    # plt.show()
    # return

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
        img_size = network.IMAGE_SIZE
        nr_figs = 6

        print("Raw data:")
        raw_data = np.zeros((img_size * nr_figs, img_size * nr_figs))

        imgs = x_train[:nr_figs**2]
        for i in range(nr_figs**2):
            raw_data[(i // nr_figs) * img_size : ((i // nr_figs) + 1) * img_size, (i % nr_figs) * img_size: (i % nr_figs + 1) * img_size] = imgs[i]
        plt.imsave("raw-emnist-data.png", raw_data, dpi=1200)

        print("Processed data:")
        imgs = data_preprocessing.data_augment(x_train[:nr_figs**2])
        for i in range(nr_figs**2):
            raw_data[(i // nr_figs) * img_size : ((i // nr_figs) + 1) * img_size, (i % nr_figs) * img_size: (i % nr_figs + 1) * img_size] = imgs[i]
        plt.imsave("augmented-emnist-data.png", raw_data, dpi=1200)

        print("Raw data processed:")
        imgs = data_preprocessing.images_processing(x_train[:nr_figs**2])
        for i in range(nr_figs**2):
            raw_data[(i // nr_figs) * img_size : ((i // nr_figs) + 1) * img_size, (i % nr_figs) * img_size: (i % nr_figs + 1) * img_size] = imgs[i]
        plt.imsave("processed-emnist-data.png", raw_data, dpi=1200)

        plt.show()

        print("Processed data:")
        imgs = data_preprocessing.images_processing(
            data_preprocessing.data_augment(x_train[:nr_figs**2])
        ) 
        for i in range(nr_figs**2):
            raw_data[(i // nr_figs) * img_size : ((i // nr_figs) + 1) * img_size, (i % nr_figs) * img_size: (i % nr_figs + 1) * img_size] = imgs[i]
        plt.imsave("processed-augmented-emnist-data.png", raw_data, dpi=1200)

        plt.show()

    model = network.Network.get_instance().model

    # split dataset into small chunks to make a nice graph
    CHUNKS = 100
    x_train = th.tensor_split(x_train, CHUNKS)
    y_train = th.tensor_split(y_train, CHUNKS)
    x_test = th.tensor_split(x_test, CHUNKS)
    y_test = th.tensor_split(y_test, CHUNKS)

    train_dataset = [th.utils.data.TensorDataset(x_train[i], y_train[i]) for i in range(CHUNKS)]
    train_dataloader = [th.utils.data.DataLoader(train_dataset[i], batch_size=256, shuffle=True) for i in range(CHUNKS)]

    test_dataset = [th.utils.data.TensorDataset(x_test[i], y_test[i]) for i in range(CHUNKS)]
    test_dataloader = [th.utils.data.DataLoader(test_dataset[i], batch_size=128, shuffle=False) for i in range(CHUNKS)]

    print("Training model...")

    criterion = nn.CrossEntropyLoss()
    optimizer = th.optim.Adam(model.parameters(), lr=1e-3)
    for train_dl, test_dl in zip(train_dataloader, test_dataloader):
        train_model_epoch(model, optimizer, criterion, train_dl, test_dl, 1)

    optimizer = th.optim.Adam(model.parameters(), lr=1e-4)
    for train_dl, test_dl in zip(train_dataloader, test_dataloader):
        train_model_epoch(model, optimizer, criterion, train_dl, test_dl, 1)

    optimizer = th.optim.Adam(model.parameters(), lr=1e-5)
    for train_dl, test_dl in zip(train_dataloader, test_dataloader):
        train_model_epoch(model, optimizer, criterion, train_dl, test_dl, 1)


    if not os.path.exists(network.DATA_FOLDER):
        os.makedirs(network.DATA_FOLDER)

    th.save(model.state_dict(), network.MODEL_LOCATION)

    # Final evaluation of the model
    labels = []
    predictions = []
    for test_dl in test_dataloader:
        for batch in test_dl:
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