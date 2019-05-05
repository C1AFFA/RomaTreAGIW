from metrics import *
from xpath_combiner import *
from utils import *
import os
import glob

# small test
#ANNOTATED_PAGES_PATH = 'test-input/small/0.html'
#UNANNOTATED_PAGES_PATH = 'test-input/small/unann/*'
#GOLDEN_RULE = "//h1"

#slightly bigger test
ANNOTATED_PAGES_PATH = 'test-input/annotated-pages/*'
UNANNOTATED_PAGES_PATH = 'test-input/unannotated-pages/*'
GOLDEN_RULE = "//*[@itemprop=\'birthDate\']/a[1]"
#GOLDEN_RULE = "//*[@itemprop='name']"
#GOLDEN_RULE = "//*[@annotation='here']"


def test_learner():
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
    learn_xslt_rule(annotated_pages, unannotated_pages, features_set)


def learn_xslt_rule(ann_pages, unann_pages, global_features):
    print('-' * 100)
    print("****** STARTING Learning Algorithm")
    print("Annotated pages: " + str(len(ann_pages)))
    print("Unannotated pages " + str(len(unann_pages)))
    print("Global feature set [" + str(len(global_features)) + "]:")
    pretty_print(global_features, 5)

    k = 1
    C = list(map(lambda s: AprioriSubset(s), all_k_feature_subsets(global_features, k)))
    min_dist = 99999
    max_sup = 0
    max_prec = 0
    best_XPath = None
    max_prec_XPath = None

    while len(C) > 0:
        L = []

        print('-' * 70)
        print("**** Starting iteration " + str(k)
              + "\nSubsets size(k): " + str(k)
              + "\nC contains [" + str(len(C)) + "] subsets")
        print('-' * 70)

        for i, subset in enumerate(C):
            subset.combined_xpath = features_to_xpath(subset.features)
            subset.prec = Metrics.prec(ann_pages, subset.combined_xpath)
            subset.dist = Metrics.dist(subset.features)
            subset.sup, subset.mto = Metrics.sup(unann_pages, subset.combined_xpath)
            print("*** Subset "
                  + str(i + 1) + ":" + str(subset)
                  + " - XPATH:" + str(subset.combined_xpath)
                  + " - PREC: " +str(subset.prec)
                  + " - DIST: " +str(subset.dist)
                  + " - SUP: " +str(subset.sup)
                  + " - MTO: "+str(subset.mto))

            if subset.prec > 0:
                if subset.prec < 1 or subset.mto:
                        L.append(subset)
                        if subset.prec > max_prec \
                                or (subset.prec == max_prec and subset.dist < min_dist) \
                                or (subset.prec == max_prec and subset.dist == min_dist and subset.sup > max_sup):
                            max_prec_XPath = subset.combined_xpath
                            max_prec = subset.prec
                            min_dist = subset.dist
                            max_sup = subset.sup
                            print("\n\t----- Found new max precision XPath ------")
                            print("\tUpdating max_prec_XPath: " + subset.combined_xpath)
                            print("\tCurrent Precision : " + str(subset.prec))
                            print("\tCurrent Distance : " + str(subset.dist))
                            print("\tCurrent Support : " + str(subset.sup) + "\n")
                elif subset.dist < min_dist or (subset.dist == min_dist and (subset.sup > max_sup or max_prec < 1)):
                        best_XPath = subset.combined_xpath
                        max_prec = 1
                        min_dist = subset.dist
                        max_sup = subset.sup
                        print("\n\t----- Found new BEST XPath (Precision=1) ------")
                        print("\tUpdating best_XPath: " + subset.combined_xpath)
                        print("\tCurrent Precision : " + str(subset.prec))
                        print("\tCurrent Distance : " + str(subset.dist))
                        print("\tCurrent Support : " + str(subset.sup)+ "\n")

        print('-' * 70)
        print("**** (Before pruning) L contains [" + str(len(L)) + "] subsets")

        subsets_to_remember = []
        num = 1
        print("Pruning...")
        for j, subset in enumerate(L):
            if not ((best_XPath is not None)
                    # TODO figure out what is the correct condition
                    and ((subset.dist > min_dist) or (subset.dist == min_dist and subset.sup <= max_sup))):
                    # and ((subset.dist > min_dist) or (subset.dist == min_dist and subset.sup <= max_sup))):
                subsets_to_remember.append(subset)
            else:
                print("" + str(j+1), end=' ')
                if (num%10==0): print(' ')
            num = num + 1
        print(' ')
        print("(After pruning)  L contains [" + str(len(subsets_to_remember)) + "] subsets")

        after_pruning_set = set()
        for subset in subsets_to_remember:
            after_pruning_set = after_pruning_set.union(subset.features)
        k += 1
        C = list(map(lambda s: AprioriSubset(s), all_k_feature_subsets(after_pruning_set, k)))

        print("Updated C contains [" + str(len(after_pruning_set)) + "] subsets")
        print('-' * 70)
        print("**** Finished iteration " + str(k))

    print("**** C is empty: terminating.")
    if best_XPath is not None:
        print("Best XPATH is : " + str(best_XPath) + "\n" + '-' * 100)
        return best_XPath
    else:
        print("The maximum precision XPATH is : " + str(max_prec_XPath) + "\n" + '-' * 100)
        return max_prec_XPath


if __name__ == '__main__':
    test_learner()