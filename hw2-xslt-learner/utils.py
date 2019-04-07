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


def generate_features(page, distance=0, node=None):
    if page.is_annotated:
        if distance == 0:
            current_node = page.annotated_node.node
        else:
            current_node = node.getparent()

        if current_node is not None:
            # generate tag feature
            page.features.append(tag_feature(distance, current_node.tag))
            # generate id and class features
            for f in page.features_attrib_types:
                if f in current_node.attrib.keys():
                    page.features.append(Feature(f, distance, current_node.attrib[f]))
            generate_features(page, (distance + 1), current_node)


def all_k_feature_subsets(feature_set, k):
    return list(combinations(feature_set, k))


def get_global_feature_set(page_list):


    # TODO implement me
    # return feature_list
    return None


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
    print(''.join(str_list))
