import cv2 as cv2
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import os
import random
import numpy as np

def load_data(dataset_dir, vertical, prepare_test=False):
    if not prepare_test:
        train_dir = dataset_dir + '/train'
        train_vertical = [(train_dir + '/{}').format(i) for i in os.listdir(train_dir) if vertical in i]
        train_generic = [(train_dir + '/{}').format(i) for i in os.listdir(train_dir) if 'generic' in i]
        train_imgs = train_vertical + train_generic
        random.shuffle(train_imgs)
        return train_imgs
    else:
        test_dir = dataset_dir + '/test'
        test_imgs = [(test_dir + '/{}').format(i) for i in os.listdir(test_dir)]  # get test images
        random.shuffle(test_imgs)
        return test_imgs


# A function to read and process the images to an acceptable format for our model
def read_and_process_image(vertical, list_of_images, nrows, ncolumns):
    """
    Returns two arrays:
        X is an array of resized images
        y is an array of labels
    """
    X = []  # images
    y = []  # labels

    for image in list_of_images:
        print("- Loading: "+image)
        X.append(cv2.resize(cv2.imread(image, cv2.IMREAD_COLOR), (nrows, ncolumns),
                            interpolation=cv2.INTER_CUBIC))  # Read the image
        # get the labels
        if 'generic' in image:
            y.append(1)
        elif vertical in image:
            y.append(0)

    X = np.array(X)
    y = np.array(y)

    return X, y

# A function to get data generator to use for training the model. 
# Every time a data point is passed to the model, the generator applies some transformations to augment the dataset input diversity
def get_data_generators(train_set, labels, validation_split, bs):
    x_train, x_val, y_train, y_val = train_test_split(train_set, labels, test_size=validation_split, random_state=2)
    ntrain = len(x_train)
    nval = len(x_val)

    train_datagen = ImageDataGenerator(rescale=1. / 255,  # Scale the image between 0 and 1
                                       rotation_range=40,
                                       width_shift_range=0.2,
                                       height_shift_range=0.2,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True,
                                       fill_mode='nearest')

    val_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow(x_train, y_train, batch_size=bs)
    val_generator = val_datagen.flow(x_val, y_val, batch_size=bs)

    return train_generator, val_generator, ntrain, nval
