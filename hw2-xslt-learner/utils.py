import string
from itertools import combinations
from lxml import etree
from structs import *

'''
This script provides utilities to manipulate features and xpaths
'''


def tag_feature(l, v):
    return Feature(FEATURE_TYPES["TAG"], l, v)


def id_features(l, attributes):
    features_to_add = []
    t = FEATURE_TYPES["ID"]
    if t in attributes.keys():
        features_to_add.append(Feature(t, l, attributes[t]))
        # uncomment to generate also wildcard feature for id
        # features_to_add.append(Feature(t, l, WILD_CARD))
    return features_to_add


def class_features(l, attributes):
    features_to_add = []
    t = FEATURE_TYPES["CLASS"]
    if t in attributes.keys():
        features_to_add.append(Feature(t, l, attributes[t]))
        # uncomment to generate also wildcard feature for id
        # features_to_add.append(Feature(t, l, WILD_CARD))
    return features_to_add


# given a page with an annotated node, recursively visits all the nodes
# from the annotated node to the root and generates all the features for the node.
# returns the list of generated features
def generate_features(page):
    def generate_features_rec(features, distance, current_node):
        if current_node is None:
            return features
        else:
            # generate tag feature
            features.append(tag_feature(distance, current_node.tag))

            # generate id and class features
            attributes = current_node.attrib
            features.extend(id_features(distance, attributes))
            features.extend(class_features(distance, attributes))

            return generate_features_rec(features, (distance + 1), current_node.getparent())

    if page.is_annotated:
        return generate_features_rec([], 0, page.annotated_node.node)


def all_k_feature_subsets(feature_set, k):
    return list(combinations(feature_set, k))


def get_global_feature_set(page_list):
    result = set()
    for page in page_list:
        result = result.union(set(page.features))
    return result




def features_to_xpath(feature_set):
    tokens = ["//"]
    def feature_to_xpath(f):
        if f.type == FEATURE_TYPES["TAG"]:
            tokens.append(f.value)
        elif f.type == FEATURE_TYPES["ID"] or f.type == FEATURE_TYPES["CLASS"]:
            tokens.append("*[@")
            if f.type == FEATURE_TYPES["ID"]:
                tokens.append("id")
            elif f.type == FEATURE_TYPES["CLASS"]:
                tokens.append("class")
            if not f.value == WILD_CARD:
                tokens.append("="+f.value)
            tokens.append("]")
        if f.level > 0:
            i=f.level
            while i!=1:
                tokens.append("/*")
                i=i-1
            tokens.append("/node()")


        return ''.join(tokens)

    if len(feature_set) == 1:
        xpath = feature_to_xpath(feature_set[0])
    else:
        pass
        # TODO COMBINE MULTIPLE FEATURES FROM SINGLE XPATH
    return xpath

def print_feature_list(feature_list):
    str_list = ["{"]
    for f in feature_list:
        str_list.append(str(f))
        str_list.append(",")
    str_list.pop()
    str_list.append("}")
    print(''.join(str_list))
