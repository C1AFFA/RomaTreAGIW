from utils import *


class Metrics:
    def prec(page_list, combined_xpath):
        precision = 0
        are_all_selected, positive_nodes, selected_nodes = Metrics.is_selecting_all_positive_nodes(page_list,
                                                                                                   combined_xpath)
        if are_all_selected:
            precision = len(positive_nodes) / len(selected_nodes)
        return precision

    def dist(f_combination):
        distance = 0
        for feature in f_combination:
            if feature.level > distance:
                distance = feature.level
        return distance

    def sup(unannotated_pages, combined_xpath):
        positives = 0
        sup = 0
        more_than_one = False

        if (len(unannotated_pages) > 0):
            for page in unannotated_pages:
                nodes_retrieved = page.DOM.xpath(combined_xpath)
                if len(nodes_retrieved) > 0:
                    positives += 1
                    if len(nodes_retrieved) > 1 :
                        more_than_one = True
            sup = positives / len(unannotated_pages)

        return [sup, more_than_one]

    def get_selected_nodes(page_list, combined_xpath):
        nodes_retrieved = []
        for page in page_list:
            page_nodes_retrieved = page.DOM.xpath(combined_xpath)
            nodes_retrieved.extend(page_nodes_retrieved)
        return nodes_retrieved

    def get_positive_nodes(page_list):
        positive_nodes = []
        for page in page_list:
            positive_nodes.append(page.annotated_node)
        return positive_nodes

    def is_selecting_all_positive_nodes(page_list, combined_xpath):
        nodes_retrieved = Metrics.get_selected_nodes(page_list, combined_xpath)
        positive_nodes = Metrics.get_positive_nodes(page_list)
        are_them_all = True
        for p_node in positive_nodes:
            if p_node.node not in nodes_retrieved:
                are_them_all = False

        return [are_them_all, positive_nodes, nodes_retrieved]
