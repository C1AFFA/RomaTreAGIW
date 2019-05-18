from model import *
import pandas as pd

#model = ILDA("bike", "./datasets/bikes-dataset")
model = ILDA("bike", "./input")
model.load()
precision, recall, accuracy, results = model.test_model()


print("Precision on Test set: "+str(precision))
print("Recall on Test set: "+str(recall))
print("Accuracy on Test set: "+str(accuracy))