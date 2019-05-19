from model import *

model = ILDA("bike", "./bikes-dataset")
model.prepare_input()
model.train(150)
model.save()

