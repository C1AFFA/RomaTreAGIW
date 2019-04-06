from utils import *

//hello world!

p = Page("C:\\Users\\Marco\\AGI\\RomaTreAGIW\\pages\\0.html", "//h1")


p.featuresGenerator()

for feature in p.featureList:
    print("(" + str(feature.ftype) + " - " + str(feature.l) + " - " + str(feature.value) + ")")

combs = p.featuresCombiner(k_subset=1)

for c in combs:
    for i in c:
        print("(" + str(i.ftype) + " - " + str(i.l) + " - " + str(i.value) + ")")
    print("-----------------")