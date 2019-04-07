from typing import List

from metrics import *
from structs import *
import os
import glob
import random
import unittest

from structs import Page

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
        subsets = all_k_feature_subsets(self.page.features, k)
        print("Printing all " + str(k) + "-subsets:")
        for c in subsets:
            print_feature_list(c)

    def test_distance(self):
        print("------------TESTING FEATURE DISTANCE-------------")
        generate_features(self.page)
        num_elements_per_set = 3
        subsets = all_k_feature_subsets(self.page.features, num_elements_per_set)

        random_combination = random.choice(subsets)
        for i,f in enumerate(random_combination):
            print("F"+str(i)+" - "+str(f.level))

        distance = Metrics.dist(random_combination)
        print(distance)

    def test_precision(self):
        print("------------TESTING FEATURE PRECISION-------------")
        filename = os.path.join(os.path.dirname(__file__), 'test-input\\example_basidati.html')
        page_list = [self.page, Page(filename,  "/html/body/h2")]
        precision = Metrics.prec(page_list, "//div/h1|//body/*")
        print(precision)

    def test_sup(self):
        print("------------TESTING SUP-------------")
        u_pages = []
        file_pages = glob.glob(os.path.join(os.path.dirname(__file__), 'test-input/unannotated-pages/*'))
        for p in file_pages:
            u_pages.append(Page(p , "//tag_sbagliato"))
        sup = Metrics.sup(u_pages, "//header/h1")
        print(sup)

if __name__ == '__main__':
    unittest.main()