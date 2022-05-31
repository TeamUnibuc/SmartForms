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
DEBUG = True

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
            # data augmentation
            inputs = data_preprocessing.data_augment(inputs)
            inputs = data_preprocessing.images_processing(inputs)
            inputs = th.tensor(inputs.reshape((-1, 1, 28, 28)), dtype=th.float32)

            inputs = inputs.to(network.DEVICE)
            targets = targets.to(network.DEVICE)

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
            inputs = data_preprocessing.images_processing(inputs)
            inputs = th.tensor(inputs.reshape((-1, 1, 28, 28)), dtype=th.float32)

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
        generate_dataset.generate_dataset()
        x = np.load(IMAGES_PATH)
        y = np.load(LABELS_PATH)    

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

    train_dataset = th.utils.data.TensorDataset(x_train, y_train)
    train_dataloader = th.utils.data.DataLoader(train_dataset, batch_size=256, shuffle=True)

    test_dataset = th.utils.data.TensorDataset(x_test, y_test)
    test_dataloader = th.utils.data.DataLoader(test_dataset, batch_size=128, shuffle=False)

    print("Training model...")

    criterion = nn.CrossEntropyLoss()
    optimizer = th.optim.Adam(model.parameters(), lr=1e-3)
    train_model_epoch(model, optimizer, criterion, train_dataloader, test_dataloader, 4)

    optimizer = th.optim.Adam(model.parameters(), lr=1e-4)
    train_model_epoch(model, optimizer, criterion, train_dataloader, test_dataloader, 4)

    optimizer = th.optim.Adam(model.parameters(), lr=1e-5)
    train_model_epoch(model, optimizer, criterion, train_dataloader, test_dataloader, 5)

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