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
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, 'test-input\\0.html')
        self.page = Page(filepath, "//h1")

        filepath2 = os.path.join(dirname, 'test-input\\sample.html')
        self.smallpage1 = Page(filepath2, "//h1")
        self.smallpage2 = Page(filepath2, "//li")

    def test_generate_features(self):
        self.page.features = generate_features(self.page)
        print("------------TESTING FEATURE GENERATION-------------")
        print_feature_list(self.page.features)

    def test_combine(self):
        print("------------TESTING FEATURE COMBINATION-------------")
        k = 2
        self.page.features = generate_features(self.page)
        subsets = all_k_feature_subsets(self.page.features, k)
        print("Printing all " + str(k) + "-subsets:")
        for c in subsets:
            print_feature_list(c)

    def test_get_global_feature_set(self):
        print("------------TESTING GLOBAL FEATURE SET UNION -------------")
        f1 = Feature("t2", 0, "v2")
        f2 = Feature("t2", 0, "v2")
        f3 = Feature("t3", 0, "v3")
        f4 = Feature("t4", 0, "v4")
        self.smallpage1.features = [f1, f2]
        self.smallpage2.features = [f1, f3, f4]
        print(self.smallpage1.features)
        print(self.smallpage2.features)
        global_features = get_global_feature_set([self.smallpage1, self.smallpage2])
        print(global_features)
        self.assertEqual(set([f1, f2, f3, f4]), global_features)

    def test_features_to_xpath(self):
        print("------------TESTING FEATURES TO XPATH -------------")
        features_to_test = [
            Feature("tag", 0, "div"),
            Feature("tag", 1, "div"),
            Feature("tag", 2, "div"),
            Feature("tag", 3, "div"),
            Feature("id", 0, "*"),
            Feature("id", 0, "i1"),
            Feature("class", 0, "*"),
            Feature("class", 4, "c1")
        ]
        for f in features_to_test:
            print(features_to_xpath([f]))

    def test_distance(self):
        print("------------TESTING FEATURE DISTANCE-------------")
        self.page.features = generate_features(self.page)
        num_elements_per_set = 3
        subsets = all_k_feature_subsets(self.page.features, num_elements_per_set)

        random_combination = random.choice(subsets)
        for i, f in enumerate(random_combination):
            print("F" + str(i) + " - " + str(f.level))

        distance = Metrics.dist(random_combination)
        print(distance)

    def test_precision(self):
        print("------------TESTING FEATURE PRECISION-------------")
        filename = os.path.join(os.path.dirname(__file__), 'test-input\\example_basidati.html')
        page_list = [self.page, Page(filename, "/html/body/h2")]
        precision = Metrics.prec(page_list, "//div/h1|//body/*")
        print(precision)

    def test_sup(self):
        print("------------TESTING SUP-------------")
        u_pages = []
        file_pages = glob.glob(os.path.join(os.path.dirname(__file__), 'test-input/unannotated-pages/*'))
        for p in file_pages:
            u_pages.append(Page(p, "//tag_sbagliato"))
        sup = Metrics.sup(u_pages, "//header/h1")
        print(sup)

    def test_list(self):
        print("------------TESTING LIST-------------")
        FL = set()

        FL1 = [Feature("tag", 1, "h1"), Feature("tag", 2, "div"), Feature("tag", 3, "div"), Feature("tag", 4, "div"),
               Feature("tag", 5, "div")]
        FL2 = [Feature("tag", 1, "h1"), Feature("tag", 2, "div")]

        for f in FL2:
            if f not in FL1:
                FL1.append(f)

        print(FL1)

if __name__ == '__main__':
    unittest.main()
