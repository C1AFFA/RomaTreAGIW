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
    C = all_k_feature_subsets(global_features, k)
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
            combined_xpath = features_to_xpath(subset)
            current_prec = Metrics.prec(ann_pages, combined_xpath)
            current_sup, more_than_one = Metrics.sup(unann_pages, combined_xpath)
            current_distance = Metrics.dist(subset)
            print("*** Subset "
                  + str(i + 1) + ":" + str(subset)
                  + " - XPATH:" + str(combined_xpath)
                  + " - PREC: " +str(current_prec)
                  + " - DIST: " +str(current_distance)
                  + " - SUP: " +str(current_sup)
                  + " - MTO: "+str(more_than_one))

            if current_prec > 0:
                if current_prec < 1 or more_than_one:
                        L.append(subset)
                        if current_prec > max_prec \
                                or (current_prec == max_prec and current_distance < min_dist) \
                                or (current_prec == max_prec and current_distance == min_dist and current_sup > max_sup):
                            max_prec_XPath = combined_xpath
                            max_prec = current_prec
                            min_dist = current_distance
                            max_sup = current_sup
                            print("\n\t----- Found new max precision XPath ------")
                            print("\tUpdating max_prec_XPath: " + combined_xpath)
                            print("\tCurrent Precision : " + str(current_prec))
                            print("\tCurrent Distance : " + str(current_distance))
                            print("\tCurrent Support : " + str(current_sup) + "\n")
                elif current_distance < min_dist or (current_distance == min_dist and (current_sup > max_sup or max_prec < 1)):
                        best_XPath = combined_xpath
                        max_prec = 1
                        min_dist = current_distance
                        max_sup = current_sup
                        print("\n\t----- Found new BEST XPath (Precision=1) ------")
                        print("\tUpdating best_XPath: " + combined_xpath)
                        print("\tCurrent Precision : " + str(current_prec))
                        print("\tCurrent Distance : " + str(current_distance))
                        print("\tCurrent Support : " + str(current_sup)+ "\n")

        print('-' * 70)
        print("**** (Before pruning) L contains [" + str(len(L)) + "] subsets")

        subsets_to_remember = []
        num = 1
        print("Pruning...")
        for j, subset in enumerate(L):
            combined_xpath = features_to_xpath(subset)
            # current_prec = Metrics.prec(ann_pages, combined_xpath) # unused
            current_sup, more_than_one = Metrics.sup(unann_pages, combined_xpath)
            current_distance = Metrics.dist(subset)

            if not ((best_XPath is not None)
                    # TODO figure out what is the correct condition
                    and ((current_distance > min_dist) or (current_distance == min_dist and current_sup <= max_sup))):
                    # and ((current_distance > min_dist) or (current_distance == min_dist and current_sup <= max_sup))):
                subsets_to_remember.append(subset)
            else:
                print("" + str(j+1), end=' ')
                if (num%10==0): print(' ')
            num = num + 1
        print(' ')
        print("(After pruning)  L contains [" + str(len(subsets_to_remember)) + "] subsets")

        after_pruning_set = set()
        for subset in subsets_to_remember:
            after_pruning_set = after_pruning_set.union(subset)
        k += 1
        C = all_k_feature_subsets(list(after_pruning_set), k)

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