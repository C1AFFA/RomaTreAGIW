from utils import *

class Metrics:
    def prec(page_list  , combinedXPath):
        precision = 0
        are_all_selected , positive_nodes , selected_nodes = Metrics.is_selecting_all_positive_nodes(page_list,combinedXPath)
        if are_all_selected:
            precision = len(positive_nodes)/len(selected_nodes)
        return precision

    def dist(fCombination):
        distance = 0
        for feature in fCombination:
            if feature.level > distance:
                distance = feature.level
        return distance

    def sup(unannotatedPages, combinedXPath):
        positives = 0
        sup = 0
        if (len(unannotatedPages) > 0):
            for page in unannotatedPages:
                nodes_retrieved = page.DOM.xpath(combinedXPath)
                if len(nodes_retrieved) > 0:
                    positives += 1
            sup = positives / len(unannotatedPages)

        return sup

    def get_selected_nodes(page_list , combinedXPath):
        nodes_retrieved = []
        for page in page_list:
            page_nodes_retrieved = page.DOM.xpath(combinedXPath)
            nodes_retrieved.extend(page_nodes_retrieved)
        return nodes_retrieved

    def get_positive_nodes(page_list):
        positive_nodes = []
        for page in page_list:
            positive_nodes.append(page.annotated_node)
        return positive_nodes

    def is_selecting_all_positive_nodes(page_list , combinedXPath):
        nodes_retrieved = Metrics.get_selected_nodes(page_list , combinedXPath)
        positive_nodes = Metrics.get_positive_nodes(page_list)
        are_them_all = True
        for p_node in positive_nodes:
            if p_node.node not in nodes_retrieved:
                are_them_all = False

        return [are_them_all , positive_nodes, nodes_retrieved]