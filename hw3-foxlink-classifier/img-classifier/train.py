from model import *

model = ILDA("bike", "./datasets/bikes-dataset")
model.prepare_input()
model.train(20)
model.save(2)

