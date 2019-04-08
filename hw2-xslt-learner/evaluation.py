def evaluate(test_pages, learnt_rule, golden_rule):
    # Applichiamo l'XPATH restituito dall'XSLT LEARNER alle pagine di test.
    # Applichiamo poi la golden rule e confrointiamo nodo a nodo i risultati
    print("****** Evaluation")

    positive_nodes = []
    retrieved_nodes = []

    for t_page in test_pages:
        gr_nodes = t_page.DOM.xpath(golden_rule)
        learnt_nodes = t_page.DOM.xpath(learnt_rule)
        positive_nodes.extend(gr_nodes)
        retrieved_nodes.extend(learnt_nodes)

    positives_retrieved_nodes = [value for value in positive_nodes if value in retrieved_nodes]

    print(positive_nodes)
    print(retrieved_nodes)
    print(positives_retrieved_nodes)
    print("---------------------")

    precision = len(positives_retrieved_nodes) / len(retrieved_nodes)
    recall = len(positives_retrieved_nodes) / len(positive_nodes)

    return precision, recall
