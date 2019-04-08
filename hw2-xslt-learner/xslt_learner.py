from metrics import *
from combiner import *
from utils import *
import os
import glob


# small test
ANNOTATED_PAGES_PATH = 'test-input/small/0.html'
UNANNOTATED_PAGES_PATH = 'test-input/small/unann/*'
GOLDEN_RULE = "//h1"

# slightly bigger test
# ANNOTATED_PAGES_PATH = 'test-input/annotated-pages/*'
# UNANNOTATED_PAGES_PATH = 'test-input/unannotated-pages/*'
# GOLDEN_RULE = "//*[@itemprop='name']"


# TODO SCRIVERE COMPONENTE CHE SMAZZA LE PAGINE E SEPARARLO DA APRIORI
def prepare_input():
    # prepare annotated pages
    annotated_pages = []
    annotated_pages_paths = glob.glob(os.path.join(os.path.dirname(__file__), ANNOTATED_PAGES_PATH))
    for path in annotated_pages_paths:
        annotated_pages.append(Page(path, GOLDEN_RULE))

    # prepare unannotated pages
    unannotated_pages = []
    unannotated_pages_paths = glob.glob(os.path.join(os.path.dirname(__file__), UNANNOTATED_PAGES_PATH))
    for path in unannotated_pages_paths:
        unannotated_pages.append(Page(path, "//foo"))  # TODO fix dummy var usage

    # prepare feature set
    for page in annotated_pages:
        page.features = generate_features(page)
    features_set = list(get_global_feature_set(annotated_pages))
    # for f in features_set:
    #     print(f)

    # execute apriori algorithm
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
        L = []
        print("**** Starting iteration " + str(k) + "****")

        print('-' * 100)
        print("[SUBSETS SIZE: " + str(k) + "]")
        print("C contains the current subsets:")
        for a, b, c, d in zip(*[iter(C)]*4):
            print(a, b, c, d)
        print('-' * 100)

        for i, subset in enumerate(C):
            print("** Iterating subset " + str(i) + ":" + str(subset))
            combined_xpath = features_to_xpath(subset)
            current_prec = Metrics.prec(ann_pages, combined_xpath)
            current_sup, more_than_one = Metrics.sup(unann_pages, combined_xpath)
            current_distance = Metrics.dist(subset)
            if current_prec > 0:
                # TODO figure out what is the correct condition
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
                            print("\t----- Updating for subset : ------")
                            print("\tUpdating max_prec_XPath: " + combined_xpath)
                            print("\tCurrent Precision : " + str(current_prec))
                            print("\tCurrent Distance : " + str(current_distance))
                            print("\tCurrent Support : " + str(current_sup))
                elif current_distance < min_dist or (current_distance < min_dist and current_sup > max_sup):
                    best_XPath = combined_xpath
                    max_prec = 1
                    min_dist = current_distance
                    max_sup = current_sup
                    print("\t----- Updating BEST for subset : ------")
                    print("\tUpdating best_XPath: " + combined_xpath)
                    print("\tCurrent Precision : " + str(current_prec))
                    print("\tCurrent Distance : " + str(current_distance))
                    print("\tCurrent Support : " + str(current_sup))
            else:
                print("** Subset " + str(i) + " has lower precision than local max. Skipping")

        print('-' * 100)
        print("[BEFORE PRUNING] L contains the current subsets:")
        for a, b, c, d in zip(*[iter(L)]*4):
            print(a, b, c, d)
        print('-' * 100)

        subsets_to_remember = []
        for j, subset in enumerate(L):
            combined_xpath = features_to_xpath(subset)
            # current_prec = Metrics.prec(ann_pages, combined_xpath) # unused
            current_sup, more_than_one = Metrics.sup(unann_pages, combined_xpath)
            current_distance = Metrics.dist(subset)

            if not ((best_XPath is not None)
                    # TODO figure out what is the correct condition
                    or ((current_distance > min_dist) or (current_distance == min_dist and current_sup <= max_sup))):
                    # and ((current_distance > min_dist) or (current_distance == min_dist and current_sup <= max_sup))):
                subsets_to_remember.append(subset)
            else:
                print("\t\t ** Pruning subset " + str(j))

        print('-' * 100)
        print("[BEFORE PRUNING] L contains the current subsets:")
        for a, b, c, d in zip(*[iter(subsets_to_remember)]*4):
            print(a, b, c, d)
        print('-' * 100)

        after_pruning_set = set()
        for subset in subsets_to_remember:
            after_pruning_set = after_pruning_set.union(subset)
        k += 1
        C = all_k_feature_subsets(list(after_pruning_set), k)

    print("**** C is empty. Showing results:")
    if best_XPath is not None:
        print("\tBest XPATH is : " + str(best_XPath))
    else:
        print("\tThe maximum precision XPATH is : " + str(max_prec_XPath))


if __name__ == '__main__':
    prepare_input()