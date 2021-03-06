from itertools import combinations
from lxml import etree
from structs import *
import re

'''
This script provides utilities to manipulate features
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


def print_feature_list(feature_list):
    str_list = ["{"]
    if not feature_list:
        str_list.append("}")
    else:
        for f in feature_list:
            str_list.append(str(f))
            str_list.append(",")
        str_list.pop()
        str_list.append("}")
    print(''.join(str_list))


def pretty_print(input_list, tab_size=3):
    for i, element in enumerate(input_list):
        if (i+1) % tab_size == 0:
            print(element)
        elif i != len(input_list):
            print(element, end=' ')
    print(' ')

def prepare_golden_rule(golden_rule):
    golden_rule_prepared = golden_rule
    matches = re.findall(r"(/[A-Z]+)", golden_rule_prepared)
    if matches:
        for match in matches:
            #print(match)
            golden_rule_prepared = golden_rule_prepared.replace(match, match.lower())
        return golden_rule_prepared
    else:
        return golden_rule
