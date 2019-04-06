from metrics import *
from structs import *
import os
import random
import unittest

'''
This script SHOULD contain a unit test for each declared method in the project
'''

class FeatureTest(unittest.TestCase):

    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'test-input\\0.html')
        self.page = Page(filename, "//h1")

    def test_generate_features(self):
        generate_features(self.page)
        print("------------TESTING FEATURE GENERATION-------------")
        print_feature_list(self.page.features)

    def test_combine(self):
        print("------------TESTING FEATURE COMBINATION-------------")
        generate_features(self.page)
        k=2
        combinations = all_k_feature_subsets(self.page.features, k)
        print("Printing all " + str(k) + "-subsets:")
        for c in combinations:
            print_feature_list(c)

    def test_distance(self):
        print("------------TESTING FEATURE DISTANCE-------------")
        generate_features(self.page)
        num_elements_per_set = 3
        combinations = all_k_feature_subsets(self.page.features, num_elements_per_set)

        random_combination = random.choice(combinations)
        for i,f in enumerate(random_combination):
            print("F"+str(i)+" - "+str(f.level))

        distance = Metrics.dist(random_combination)
        print(distance)

    def test_precision(self):
        print("------------TESTING FEATURE PRECISION-------------")
        precision = Metrics.prec(self.page , "//header/*/*")
        print(precision)

if __name__ == '__main__':
    unittest.main()