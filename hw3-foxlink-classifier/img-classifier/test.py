from model import *
import pandas as pd

#model = ILDA("bike", "./bikes-dataset")
model = ILDA("bike", "./input")
model.load("3")
model.save_test_examples()
# precision, recall, accuracy, results = model.test_model()
#
#
# print("- Precision\t"+str(precision))
# print("- Recall\t"+str(recall))
# print("- Accuracy\t"+str(accuracy))
# print("- F1 Score\t"+str(2*precision*recall/(precision+recall)))
