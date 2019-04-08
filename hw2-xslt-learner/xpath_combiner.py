from structs import *

'''
This script provides methods to combine xpaths given a set of features
'''

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
                tokens.append("=\'" + f.value + "\'")
            tokens.append("]")
        if f.level > 0:
            i = f.level
            while i != 1:
                tokens.append("/*")
                i = i - 1
            tokens.append("/node()")
        return ''.join(tokens)

    def merge_features_at_l(features, lvl):
        tkns = []
        tags = list(filter(lambda f: f.type == FEATURE_TYPES["TAG"], features))
        ids = list(filter(lambda f: f.type == FEATURE_TYPES["ID"], features))
        classes = list(filter(lambda f: f.type == FEATURE_TYPES["CLASS"], features))
        if lvl == 0:
            tkns.append("node()")
        else:
            tkns.append("*")
        if tags:
            tkns.append("[")
            for f in tags:
                tkns.append("self::" + f.value)
                tkns.append(" or ")
            tkns.pop()
            tkns.append("]")
        if ids:
            tkns.append("[")
            for f in ids:
                tkns.append("@id")
                if not f.value == WILD_CARD:
                    tkns.append("=\'" + f.value + "\'")
                tkns.append(" or ")
            tkns.pop()
            tkns.append("]")
        if classes:
            tkns.append("[")
            for f in classes:
                tkns.append("@class")
                if not f.value == WILD_CARD:
                    tkns.append("=\'" + f.value + "\'")
                tkns.append(" or ")
            tkns.pop()
            tkns.append("]")
        if not lvl == 0:
            tkns.append("/")
        return ''.join(tkns)

    if len(feature_set) == 1:
        xpath = feature_to_xpath(feature_set[0])
    else:
        max_l = max(feature_set, key=lambda f: f.level).level
        for l in range(max_l, -1, -1):
            features_at_l = list(filter(lambda f: f.level == l, feature_set))
            tokens.append(merge_features_at_l(features_at_l, l))
        xpath = ''.join(tokens)
    return xpath
