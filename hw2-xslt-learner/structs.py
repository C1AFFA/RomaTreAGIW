from lxml import etree

'''
This script declares all the main data structures used in the learning system
'''

FEATURE_TYPES = {
    "TAG": "tag",
    "ID": "id",
    "CLASS": "class",
}

WILD_CARD = "*"


class Feature:
    def __init__(self, t: str, l: int, v: str) -> object:
        self.type = t
        self.level = l
        self.value = v

    def __str__(self):
        return "(" + self.type + "," + str(self.level) + "," + str(self.value) + ")"

    def __repr__(self):
        return "(" + self.type + "," + str(self.level) + "," + str(self.value) + ")"

    def __eq__(self, other):
        if isinstance(other, Feature):
            return (self.type == other.type) and (self.level == other.level) and (self.value == other.value)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


class Page:
    # each page is referred only in the scope of one single attribute to extract
    def __init__(self, filepath, golden_rule):
        encoded_html = open(filepath).read().encode('utf-8')
        utf8_parser = etree.HTMLParser()
        tree = etree.fromstring(encoded_html, parser=utf8_parser)
        self.DOM = tree
        self.annotated_node = AnnotatedNode(tree, golden_rule)
        self.is_annotated = True if self.annotated_node else False
        self.features = []
        self.features_attrib_types = ["id", "class"]


class AnnotatedNode:
    def __init__(self, tree, golden_rule):
        retrieved_nodes = tree.xpath(golden_rule)
        self.rule = golden_rule
        # the golden rule should always select exactly one node
        if len(retrieved_nodes) == 1:
            self.node = retrieved_nodes[0]
            self.parent = self.node.getparent()
        else:
            self.node = None
            self.parent = None
