from keras.applications import InceptionResNetV2
from keras import layers
from keras import models
from keras import optimizers
import numpy as np
from data_loader import *


class ILDA():
    def __init__(self, vertical, dataset_dir, batch_size=8, width=150, height=150):
        self.vertical = vertical
        self.dataset_dir = dataset_dir
        self.width = width
        self.height = height
        self.batch_size = batch_size
        self.train_generator, self.val_generator, self.ntrain, self.nval, self.history = None, None, None, None, None

        conv_base = InceptionResNetV2(weights='imagenet', include_top=False, input_shape=(self.width, self.height, 3))
        print("- InceptionResNetV2 loaded.")
        model = models.Sequential()
        model.add(conv_base)
        model.add(layers.Flatten())
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))  # Sigmoid function at the end because we have just two classes
        print("- Fully connected layer added.")
        conv_base.trainable = False     # Freeze the
        print("- Deeper layers frozen.")
        model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=2e-5), metrics=['acc'])
        print("- ILDA inizialized.")
        self.model = model

    def prepare_input(self, validation_split=0.1):
        train_imgs = load_data(self.dataset_dir, self.vertical, prepare_test=False)
        train_set, labels = read_and_process_image(self.vertical, train_imgs, self.width, self.height)

        self.train_generator, self.val_generator, self.ntrain, self.nval = get_data_generators(train_set,
                                                                                               labels,
                                                                                               validation_split,
                                                                                               self.batch_size)

    def train(self, epochs):
        self.history = self.model.fit_generator(self.train_generator,
                                                steps_per_epoch=self.ntrain // self.batch_size,
                                                epochs=epochs,
                                                validation_data=self.val_generator,
                                                validation_steps=self.nval // self.batch_size)

    def test_model(self):
        test_imgs = load_data(self.dataset_dir, self.vertical, prepare_test=True)
        random.shuffle(test_imgs)
        x_test, y_test = read_and_process_image(self.vertical, test_imgs, self.width, self.height)
        x = np.array(x_test)
        y = np.array(y_test)
        test_datagen = ImageDataGenerator(rescale=1. / 255)
        positives = 0
        cont = 0
        predicted = []
        print()
        print("- Starting prediction on Test set")
        for batch, by in test_datagen.flow(x, y, batch_size=1):
            pred = self.model.predict(batch)
            if pred > 0.5 and by == 1:
                positives += 1
            elif pred <= 0.5 and by == 0:
                positives += 1
            cont += 1
            if cont % len(test_imgs) == 0:
                break
            predicted.append(pred)
            print("", end=".")
        print()
        accuracy = positives / len(test_imgs)
        return accuracy, predicted, y

    # def show_prediction_example(self):

    def save(self, version="1"):
        # os.makedirs('saved_model', exist_ok=True)
        self.model.save_weights('./saved-models/ILDA-v%s.h5' % version)

    def load(self, version="1"):
        self.model.load_weights("./saved-models/ILDA-v%s.h5" % version)
