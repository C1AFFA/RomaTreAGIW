from utils import *

class Metrics:
    def prec(page  , combinedXPath):
        precision = 0
        if page.is_annotated:
            nodesRetrieved = page.DOM.xpath(combinedXPath)
            if page.annotated_node in nodesRetrieved:
                precision = 1/len(nodesRetrieved)
        return precision

    def dist(fCombination):
        distance = 0
        for feature in fCombination:
            if feature.level > distance:
                distance = feature.level
        return distance

    def sup(self):
        return None

    def getSelectedNodes(page , XPath):
        nodesRetrieved = page.DOM.xpath(XPath)
        return nodesRetrieved
