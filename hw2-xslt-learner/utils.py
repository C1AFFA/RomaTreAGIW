import numpy as np
from itertools import combinations
from lxml import etree


class Page():
    def __init__(self, filepath, golden_rule):
        htmlparser = etree.HTMLParser()
        tree = etree.parse(filepath, htmlparser)
        self.DOM = tree
        self.annotatedNode = AnnotatedNode(tree, golden_rule)
        if self.annotatedNode:
            self.isAnnotated = True
        else:
            self.isAnnotated = False

        self.featureList = []
        self.features_attrib_types = ["id" , "class"]


    def featuresGenerator(self, distance = 1, node = None):
        if self.isAnnotated:
            if (distance == 1):
                parent = self.annotatedNode.parent
            else:
                parent = node.getparent()
            if parent is not None:
                self.featureList.append(Feature("tag", distance, parent.tag))
                for f in self.features_attrib_types :
                    if f in parent.attrib.keys():
                        self.featureList.append(Feature(f, distance, parent.attrib[f]))
                self.featuresGenerator((distance + 1), parent)




    def featuresCombiner(self , k_subset):
        return combinations(self.featureList, k_subset)


class AnnotatedNode():
    def __init__(self, tree, golden_rule):
        node = tree.xpath(golden_rule)
        self.rule = golden_rule
        if len(node) == 1:
            self.node = node[0]
            self.parent = self.node.getparent()
        else:
            self.node = None
            self.parent = None


class Feature():
    def __init__(self, f_type, l, val):
        self.ftype = f_type
        self.l = l
        self.value = val

