from keras.applications import InceptionResNetV2
from keras import layers
from keras import models
from keras import optimizers
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt

from data_loader import *


class ILDA():
    def __init__(self, vertical, dataset_dir, batch_size=8, width=150, height=150):
        self.vertical = vertical
        self.dataset_dir = dataset_dir
        self.width = width
        self.height = height
        self.batch_size = batch_size
        self.train_generator, self.val_generator, self.ntrain, self.nval, self.history = None, None, None, None, None
        print("- Starting ILDA initialization")
        conv_base = InceptionResNetV2(weights='imagenet', include_top=False, input_shape=(self.width, self.height, 3))
        print("- InceptionResNetV2 loaded.")
        model = models.Sequential()
        model.add(conv_base)
        model.add(layers.Flatten())
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))  # Sigmoid function at the end because we have just two classes
        print("- Fully connected layer added.")
        conv_base.trainable = False     # Freeze the training on imagenet
        print("- Deeper layers frozen.")
        model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=2e-5), metrics=['acc'])
        print("- ILDA initialized.")
        self.model = model

    def prepare_input(self, validation_split=0.1):
        train_imgs = load_data(self.dataset_dir, self.vertical, prepare_test=False)
        train_set, labels = read_and_process_image(self.vertical, train_imgs, self.width, self.height)
        self.train_generator, self.val_generator, self.ntrain, self.nval = get_data_generators(train_set,
                                                                                               labels,
                                                                                               validation_split,
                                                                                               self.batch_size)

    def train(self, epochs):
        #checkpoint = ModelCheckpoint('ILDA.h5', monitor='val_acc', verbose=1, save_best_only=True, mode='max')
        #callbacks_list = [checkpoint]
        self.history = self.model.fit_generator(self.train_generator,
                                                steps_per_epoch=self.ntrain // self.batch_size,
                                                epochs=epochs,
                                                validation_data=self.val_generator,
                                                validation_steps=self.nval // self.batch_size)
                                                #callbacks=callbacks_list)

    def test_model(self):
        test_imgs = load_data(self.dataset_dir, self.vertical, prepare_test=True)
        random.shuffle(test_imgs)
        x_test, y_test = read_and_process_image(self.vertical, test_imgs, self.width, self.height)
        test_datagen = ImageDataGenerator(rescale=1. / 255)

        true_positives = 0
        true_negatives = 0
        false_positives = 0
        false_negatives = 0

        cont = 0
        predicted = []

        print()
        print("- Starting prediction on Test set")
        print("- Test datapoints: "+str(len(x_test)))
        print("- Labels datapoints: "+str(len(y_test)))
        for batch, by in test_datagen.flow(x_test, y_test, batch_size=1):
            pred = self.model.predict(batch)

            if pred > 0.5 and by == 1:
                true_negatives += 1
            elif pred <= 0.5 and by == 0:
                true_positives += 1
            elif pred < 0.5 and by == 1:
                false_positives += 1
            elif pred >= 0.5 and by == 0:
                false_negatives += 1

            cont += 1
            predicted.append(pred[0][0])
            if cont % len(test_imgs) == 0:
                break

            print("", end=".")
        print()

        accuracy = (true_positives+true_negatives)/len(test_imgs)
        predicted = np.asarray(predicted).reshape(len(predicted), 1)
        truth = np.asarray(y_test).reshape(len(y_test), 1)
        results = np.append(truth, predicted, axis=1)
        precision = true_positives/(true_positives+false_positives)
        recall = true_positives/(true_positives+false_negatives)

        return precision, recall, accuracy, results

    # def show_prediction_example(self):

    def save_history(self):
        if self.history:
            acc = self.history.history['acc']
            val_acc = self.history.history['val_acc']
            loss = self.history.history['loss']
            val_loss = self.history.history['val_loss']
            epochs = range(1, len(acc) + 1)

            #Train and validation accuracy
            plt.plot(epochs, smooth_plot(acc), 'b', label='Training accurarcy')
            plt.plot(epochs, smooth_plot(val_acc), 'r', label='Validation accurarcy')
            plt.title('Training and Validation accurarcy')
            plt.legend()
            plt.savefig('acc.png')

            plt.figure()
            #Train and validation loss
            plt.plot(epochs, smooth_plot(loss), 'b', label='Training loss')
            plt.plot(epochs, smooth_plot(val_loss), 'r', label='Validation loss')
            plt.title('Training and Validation loss')
            plt.legend()
            plt.savefig('./output/loss.png')

        else:
            print("No training history. Train the model first.")

    def save_test_examples(self):
        test_imgs = load_data(self.dataset_dir, self.vertical, prepare_test=True)
        random.shuffle(test_imgs[:10])
        x_test, y_test = read_and_process_image(self.vertical, test_imgs, self.width, self.height)
        test_datagen = ImageDataGenerator(rescale=1. / 255)

        i = 0
        columns = 5
        text_labels = []
        plt.figure(figsize=(30,20))
        for batch, by in test_datagen.flow(x_test,y_test ,batch_size=1):
            pred = self.model.predict(batch)
            if pred > 0.5:
                text_labels.append('not a bike')
            else:
                text_labels.append('a bike')
            plt.subplot(5 / columns + 1, columns, i + 1)
            plt.title('This is ' + text_labels[i])
            imgplot = plt.imshow(batch[0])
            i += 1
            if i % 10 == 0:
                break
        plt.show()
        plt.savefig('./output/test_samples.png')

    def save(self, version="1"):
        # os.makedirs('saved_model', exist_ok=True)
        self.save_history()
        self.model.save_weights("ILDA-v%s.h5" % version)

    def load(self, version="1"):
        self.model.load_weights("ILDA-v%s.h5" % version)
