from model import *

model = ILDA("bike", "./datasets/bikes-dataset")
model.load()
accuracy, predicted, truth = model.test_model()

print("Accuracy on Test set: "+str(accuracy))