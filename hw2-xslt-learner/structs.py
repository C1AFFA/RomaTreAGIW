from lxml import etree

'''
This script declares all the main data structures used in the learning system
'''

FEATURE_TYPES = {
    "TAG": "tag",
    "ID": "id",
    "CLASS": "class",
}


class Feature:
    def __init__(self, t, l, v):
        self.type = t
        self.level = l
        self.value = v

    def __str__(self):
        return "(" + self.type + ", " + str(self.level) + ", " + str(self.value) + ")"


class Page:
    def __init__(self, filepath, golden_rule):
        htmlparser = etree.HTMLParser()
        tree = etree.parse(filepath, htmlparser)
        self.DOM = tree
        self.annotated_node = AnnotatedNode(tree, golden_rule)
        self.is_annotated = True if self.annotated_node else False
        self.features = []
        self.features_attrib_types = ["id", "class"]


class AnnotatedNode:
    def __init__(self, tree, golden_rule):
        node = tree.xpath(golden_rule)
        self.rule = golden_rule
        if len(node) == 1:
            self.node = node[0]
            self.parent = self.node.getparent()
        else:
            self.node = None
            self.parent = None
