import pandas as pd
from extractor import Extractor
import urllib
from model import *

# df = pd.read_parquet("./../output__bikes/classifier/evaluation_cluster_pages.parquet")
# df = df.loc[df['cluster_label'] == "products"]["referring_url"]
# data = df.values

vertical = "bike"
dataset_dir = "./input"

data = open("./../dataset/bikes/training_set_cluster_pages.txt")


extractor = Extractor()
cbreak = 0

for i, line in enumerate(data):
    #url = line
    url , label = line.strip().split("\t")
    name = vertical
    if label == "0":
        name = "generic"
    extractor.extract(url)
    print(extractor.url_img_extracted)
    urllib.request.urlretrieve(extractor.url_img_extracted, ("%s/test/%s%s.jpg" % (dataset_dir, name, i)))
    cbreak += 1
    if cbreak > 40 :
        break
    
extractor.stop()


model = ILDA(vertical, dataset_dir)
model.load()
precision, recall, accuracy, results = model.test_model()


print("Precision on Test set: "+str(precision))
print("Recall on Test set: "+str(recall))
print("Accuracy on Test set: "+str(accuracy))