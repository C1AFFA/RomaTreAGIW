from utils import *

class Metrics:
    def prec(page  , combinedXPath):
        precision = 0
        if page.isAnnotated :
            nodesRetrieved = page.DOM.xpath(combinedXPath)
            if page.annotatedNode.node in nodesRetrieved:
                precision = 1/len(nodesRetrieved)
        return precision


    def dist(fCombination):
        distance = 0
        for feature in fCombination:
            if feature.l > distance:
                distance = feature.l
        return distance

    def sup(self):
        return None

    def getSelectedNodes(page , XPath):
        nodesRetrieved = page.DOM.xpath(XPath)
        return nodesRetrieved
