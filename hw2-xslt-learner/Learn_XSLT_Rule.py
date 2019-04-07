from metrics import *
import os
import glob


filename = os.path.join(os.path.dirname(__file__), 'test-input/0.html')
page = Page(filename, "//h1")
features_set = []

annotated_pages = [page]
for a_page in annotated_pages:
    generate_features(a_page)
    features_set.extend(a_page.features)

unannotated_pages = []
unnotated_pages_paths = glob.glob(os.path.join(os.path.dirname(__file__), 'test-input/unannotated-pages/*'))
for path in unnotated_pages_paths:
    unannotated_pages.append(Page(path, "//h1"))


k = 1
C = all_k_feature_subsets(features_set , k)
min_dist = 99999
max_sup = 0
max_prec = 0
best_XPath = None
max_prec_XPath = None

while len(C)>0 :
    L = []
    for subset in C:
        combined_xpath = feature_to_xpath(subset)
        current_prec = Metrics.prec(annotated_pages , combined_xpath)
        current_sup = Metrics.sup(unannotated_pages , combined_xpath)
        current_distance = Metrics.dist(subset)
        if current_prec > 0 :
            if current_prec < 1 or current_sup > 0 :
                L.extend(subset)
                if current_prec > max_prec or (current_prec == max_prec and current_distance < min_dist) or (current_prec == max_prec and current_distance == min_dist and current_sup > max_sup) :
                    max_prec = current_prec
                    max_prec_XPath = combined_xpath
                    min_dist = current_distance
                    max_sup = current_sup
            elif current_distance < min_dist or (current_distance < min_dist and current_sup > max_sup) :
                best_XPath = combined_xpath
                min_dist = current_distance
                max_sup = current_sup
                max_prec = 1
    for subset in L :
        combined_xpath = feature_to_xpath(subset)
        current_prec = Metrics.prec(annotated_pages, combined_xpath)
        current_sup = Metrics.sup(unannotated_pages, combined_xpath)
        current_distance = Metrics.dist(subset)
        if best_XPath is not None and ((current_distance > min_dist) or (current_distance == min_dist and current_sup <= max_sup)):
            L.remove(subset)

    C = L

if best_XPath is not None:
    print("Best XPATH is : "+best_XPath)
else:
    print("The maximum precision XPATH is : "+max_prec_XPath)


