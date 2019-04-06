#from utils import *
from metrics import *
import os
import random
import unittest


class FeatureTest(unittest.TestCase):

    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'test-input\\0.html')
        self.page = Page(filename, "//h1")

    def test_featuresGenerator(self):
        self.page.featuresGenerator()
        print("------------TESTING FEATURE GENERATION-------------")
        for feature in self.page.featureList:
            print("(" + str(feature.ftype) + " - " + str(feature.l) + " - " + str(feature.value) + ")")

    def test_featuresCombiner(self):
        print("------------TESTING FEATURE COMBINATION-------------")
        self.page.featuresGenerator()
        combs = Methods.featuresCombiner(self.page.featureList , k_subset=2)
        for c in combs:
            for i in c:
                print("(" + str(i.ftype) + " - " + str(i.l) + " - " + str(i.value) + ")")
            print("-----------------")

    def test_distance(self):
        print("------------TESTING FEATURE DISTANCE-------------")
        self.page.featuresGenerator()
        k_subset = 3
        combs = Methods.featuresCombiner(self.page.featureList,k_subset=k_subset)
        randomFeatureCombination = random.choice(combs)
        for i,f in enumerate(randomFeatureCombination):
            print("F"+str(i)+" - "+str(f.l))

        distance = Metrics.dist(randomFeatureCombination)
        print(distance)

    def test_precision(self):
        print("------------TESTING FEATURE PRECISION-------------")
        precision = Metrics.prec(self.page , "//header/*/*")
        print(precision)

if __name__ == '__main__':
    unittest.main()