from metrics import *
import os


filename = os.path.join(os.path.dirname(__file__), 'test-input/0.html')
page = Page(filename, "//h1")
page.featuresGenerator()
k = 1
C = Methods.featuresCombiner(page.featureList , k)
min_dist = 99999
max_sup = 0
max_prec = 0
best_XPath = None
max_prec_XPath = None

while len(C)>0 :
    L = []
    for

