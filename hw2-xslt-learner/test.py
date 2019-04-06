from utils import *
import os
import unittest

class FeatureTest(unittest.TestCase):

    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'test-input\example_basidati.html')
        self.page = Page(filename, "//h1")

    def test_featuresGenerator(self):
        self.page.featuresGenerator()

        for feature in self.page.featureList:
            print("(" + str(feature.ftype) + " - " + str(feature.l) + " - " + str(feature.value) + ")")

    def test_featuresCombiner(self):
        combs = self.page.featuresCombiner(k_subset=1)

        for c in combs:
            for i in c:
                print("(" + str(i.ftype) + " - " + str(i.l) + " - " + str(i.value) + ")")
            print("-----------------")


if __name__ == '__main__':
    unittest.main()