from metrics import *
from combiner import *
import os
import glob


# TODO SCRIVERE COMPONENTE CHE SMAZZA LE PAGINE E SEPARARLO DA APRIORI
def prepare_input():
    filename = os.path.join(os.path.dirname(__file__), 'test-input/__small/0.html')
    page = Page(filename, "//h1")
    annotated_pages = [page]

    # annotated_pages = []
    # annotated_pages_paths = glob.glob(os.path.join(os.path.dirname(__file__), 'test-input/annotated-pages/*'))
    # for path in annotated_pages_paths:
    #     annotated_pages_paths.append(Page(path, "//*[@itemprop='name']"))

    unannotated_pages = []
    unnotated_pages_paths = glob.glob(os.path.join(os.path.dirname(__file__), 'test-input/__small/__unann/*'))
    for path in unnotated_pages_paths:
        unannotated_pages.append(Page(path, "//pippo"))

    features_set = list(get_global_feature_set(annotated_pages))
    # for f in features_set:
    #     print(f)
    learn_xslt_rule(annotated_pages,unannotated_pages,features_set)


def learn_xslt_rule(ann_pages, unann_pages, global_features):
    k = 1
    C = all_k_feature_subsets(global_features, k)
    # C = [global_features]
    min_dist = 99999
    max_sup = 0
    max_prec = 0
    best_XPath = None
    max_prec_XPath = None

    while len(C) > 0:
        print(k)
        L = []
        for subset in C:
            combined_xpath = features_to_xpath(subset)
            current_prec = Metrics.prec(ann_pages, combined_xpath)
            current_sup, more_than_one = Metrics.sup(unann_pages, combined_xpath)
            current_distance = Metrics.dist(subset)
            if current_prec > 0:
                # if current_prec < 1 or more_than_one:
                if current_prec < 1:
                    if more_than_one:
                        L.append(subset)
                        if current_prec > max_prec \
                                or (current_prec == max_prec and current_distance < min_dist) \
                                or (current_prec == max_prec and current_distance == min_dist and current_sup > max_sup):
                            max_prec_XPath = combined_xpath
                            max_prec = current_prec
                            min_dist = current_distance
                            max_sup = current_sup
                            print("----- Updating for subset : ------")
                            print(subset)
                            print("Updating max_prec_XPath: " + combined_xpath)
                            print("Current Precision : " + str(current_prec))
                            print("Current Distance : " + str(current_distance))
                            print("Current Support : " + str(current_sup))
                elif current_distance < min_dist or (current_distance < min_dist and current_sup > max_sup):
                    best_XPath = combined_xpath
                    max_prec = 1
                    min_dist = current_distance
                    max_sup = current_sup
                    print("----- Updating BEST for subset : ------")
                    print(subset)
                    print("Updating best_XPath: " + combined_xpath)
                    print("Current Precision : " + str(current_prec))
                    print("Current Distance : " + str(current_distance))
                    print("Current Support : " + str(current_sup))

        print("L before pruning :")
        print(L)
        subsets_to_remember = []
        for subset in L:
            combined_xpath = features_to_xpath(subset)
            # current_prec = Metrics.prec(ann_pages, combined_xpath)
            current_sup, more_than_one = Metrics.sup(unann_pages, combined_xpath)
            current_distance = Metrics.dist(subset)

            if not ((best_XPath is not None)
                    # and vs or? we don't really know!!!
                    or ((current_distance > min_dist) or (current_distance == min_dist and current_sup <= max_sup))):
                    # and ((current_distance > min_dist) or (current_distance == min_dist and current_sup <= max_sup))):
                subsets_to_remember.append(subset)

        print("L after pruning :")
        print(subsets_to_remember)

        after_pruning_set = set()
        for subset in subsets_to_remember:
            after_pruning_set = after_pruning_set.union(subset)
        # print(after_pruning_set)
        k += 1
        C = all_k_feature_subsets(list(after_pruning_set), k)

    if best_XPath is not None:
        print("Best XPATH is : " + str(best_XPath))
    else:
        print("The maximum precision XPATH is : " + str(max_prec_XPath))


if __name__ == '__main__':
    prepare_input()