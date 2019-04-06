import string
from itertools import combinations
from lxml import etree
from structs import *

'''
This script provides utilities to manipulate features and xpaths
'''


def tag_feature(l, v):
    return Feature(FEATURE_TYPES["TAG"], l, v)


def id_feature(l, v):
    # TODO implement me
    pass


def class_feature(l, v):
    # TODO implement me
    pass


def generate_features(page, distance=1, node=None):
    if page.is_annotated:
        if distance == 1:
            parent = page.annotated_node.parent
        else:
            parent = node.getparent()

        if parent is not None:
            page.features.append(tag_feature(distance, parent.tag))
            for f in page.features_attrib_types:
                if f in parent.attrib.keys():
                    page.features.append(Feature(f, distance, parent.attrib[f]))
            generate_features(page, (distance + 1), parent)


def all_k_feature_subsets(feature_set, k):
    return list(combinations(feature_set, k))


def features_to_xpath(feature_set):
    xpath = ""
    # TODO implement me
    # codice che genera l'XPATH dalle features
    return xpath


def feature_to_xpath(feature):
    xpath = ""
    # TODO implement me (am i global or local?)
    return xpath


def print_feature_list(feature_list):
    str_list = ["{"]
    for f in feature_list:
        str_list.append(str(f))
        str_list.append(",")
    str_list.pop()
    str_list.append("}")
    print (''.join(str_list))
