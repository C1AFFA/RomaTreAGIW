from metrics import *
from combiner import *
import os
import glob

# TODO SCRIVERE COMPONENTE CHE SMAZZA LE PAGINE E SEPARARLO DA APRIORI
filename = os.path.join(os.path.dirname(__file__), 'test-input/0.html')
page = Page(filename, "//h1")
page.features = generate_features(page)
# features_set = []

annotated_pages = [page]
# for a_page in annotated_pages:
#     generate_features(a_page)
#     features_set.extend(a_page.features)
features_set = list(get_global_feature_set(annotated_pages))

unannotated_pages = []
unnotated_pages_paths = glob.glob(os.path.join(os.path.dirname(__file__), 'test-input/unannotated-pages/*'))
for path in unnotated_pages_paths:
    unannotated_pages.append(Page(path, "//pippo"))

k = 1
C = all_k_feature_subsets(features_set, k)
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
        current_prec = Metrics.prec(annotated_pages, combined_xpath)
        current_sup, more_than_one = Metrics.sup(unannotated_pages, combined_xpath)
        current_distance = Metrics.dist(subset)
        if current_prec > 0:
            if current_prec < 1 or more_than_one:
                L.append(subset)
                if current_prec > max_prec \
                        or (current_prec == max_prec and current_distance < min_dist) \
                        or (current_prec == max_prec and current_distance == min_dist and current_sup > max_sup):
                    max_prec = current_prec
                    max_prec_XPath = combined_xpath
                    min_dist = current_distance
                    max_sup = current_sup
                    print("----- Updating for subset : ------")
                    print(subset)
                    print("Updating max_prec_XPath: " + combined_xpath)
                    print("Current Precision : " + str(current_prec))
                    print("Current Support : " + str(current_sup))
                    print("Current Distance : " + str(current_distance))
            elif current_distance < min_dist or (current_distance < min_dist and current_sup > max_sup):
                best_XPath = combined_xpath
                min_dist = current_distance
                max_sup = current_sup
                max_prec = 1
                print("----- Updating BEST for subset : ------")
                print(subset)
                print("Updating best_XPath: " + combined_xpath)
                print("Current Precision : " + str(current_prec))
                print("Current Support : " + str(current_sup))
                print("Current Distance : " + str(current_distance))

    print("L before pruning :")
    print(L)
    subsets_to_remember = []
    for subset in L:
        combined_xpath = features_to_xpath(subset)
        current_prec = Metrics.prec(annotated_pages, combined_xpath)
        current_sup , more_than_one = Metrics.sup(unannotated_pages, combined_xpath)
        current_distance = Metrics.dist(subset)

        if not ((best_XPath is not None) and ((current_distance > min_dist) or (current_distance == min_dist and current_sup <= max_sup))):
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
