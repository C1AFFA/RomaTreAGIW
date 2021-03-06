from pathlib import Path
from xslt_learner import *
from evaluation import *

DIR_NAME = Path(__file__).parent
DATA_PATH = DIR_NAME / "input/"
PAGES_PATH = DIR_NAME / "input/pages/"
GOLDEN_RULES = DIR_NAME / "input/goldenRules.txt"
REPRESENTATIVES = "input/representatives-"

TRAINING_SET_SIZE = 3  # maximum is 8


def main():
    golden_attributes = []
    print(GOLDEN_RULES)
    with open(str(GOLDEN_RULES)) as file:
        for line in file:
            values = line.split("\t")
            attribute = Attribute(values[0], prepare_golden_rule(values[1].replace("/text()", "").strip()))
            golden_attributes.append(attribute)

    for attribute in golden_attributes:
        filename = REPRESENTATIVES + attribute.name + ".txt"
        with open(str(DIR_NAME / filename)) as file:
            indexes = []
            for line in file:
                indexes.append(line.strip())
            attribute.ann_pages_indexes = indexes

    print("Loaded the following annotated attributes:")
    for attribute in golden_attributes:
        print(attribute)

    print("\nWe will generate the following feature types:\n" + str(FEATURE_TYPES.keys()) + "\n")

    for attr in golden_attributes[:3]:
        print("=" * 100
              + "\n[LEARNING ATTRIBUTE - " + attr.name + "]"
              + "\n(Annotated xpath:" + attr.golden_rule + ")\n"
              + "=" * 100)

        # SPLIT TRAINING / VALIDATION DATA
        training_set = list(PAGES_PATH.glob('**/*'))
        annotated_pages_paths = []
        unannotated_pages_paths = []
        for index in attr.ann_pages_indexes:
            filename = index + ".html"
            path = PAGES_PATH / filename
            if path in training_set:
                annotated_pages_paths.append(path)
                unannotated_pages_paths = \
                    list(set(training_set).difference(set(annotated_pages_paths)))

        annotated_pages_paths_training = annotated_pages_paths[:TRAINING_SET_SIZE]
        annotated_pages_paths_test = annotated_pages_paths[TRAINING_SET_SIZE:]

        print("=" * 3 + " Dataset: " + str(len(training_set)))
        print("=" * 3 + " Annotated pages for Training: " + str(len(annotated_pages_paths_training)))
        print("=" * 3 + " Annotated pages for Test: " + str(len(annotated_pages_paths_test)))
        print("=" * 3 + " Unannotated pages: " + str(len(unannotated_pages_paths)))

        print("\n[STARTING TRAINING PHASE - " + attr.name + "] ")

        # PAGE FETCH & FEATURE GENERATION
        annotated_pages_training = []
        unannotated_pages = []
        annotated_pages_test = []
        for path in annotated_pages_paths_training:
            annotated_pages_training.append(Page(str(path), attr.golden_rule))
        for path in annotated_pages_paths_test:
            annotated_pages_test.append(Page(str(path), "//foo"))
        for path in unannotated_pages_paths:
            unannotated_pages.append(Page(str(path), "//foo"))

        for page in annotated_pages_training:
            page.features = generate_features(page)
        features_set = list(get_global_feature_set(annotated_pages_training))

        attr.learnt_rule = learn_xslt_rule(annotated_pages_training, unannotated_pages, features_set)
        #attr.learnt_rule = "//*[@itemprop='jobTitle'][1]"

        print("=" * 3 + " Learnt xpath: " + str(attr.learnt_rule))
        print("=" * 3 + " Annotated xpath was " + str(attr.golden_rule))

        print("\n[STARTING TEST PHASE - " + attr.name + "] ")

        attr.precision, attr.recall = evaluate(annotated_pages_test, attr.learnt_rule, attr.golden_rule)
        print("Precision for attribute " + attr.name + ": " + str(attr.precision))
        print("Recall for attribute " + attr.name + ": " + str(attr.recall))
        print("[LEARNING ATTRIBUTE COMPLETED - " + attr.name + "]\n\n")


    for a in golden_attributes:
        print(a.name, a.golden_rule, a.learnt_rule, a.precision, a.recall, sep='\t')


    # import matplotlib.pyplot as plt
    # from matplotlib.dates import date2num
    # import datetime
    #
    # x =  np.arange(3)
    # y = [0.99541197, 0.99433107, 0.92897727]
    # z=[0.99118943,0.91240876,0.9650924]
    # k=[0.94117647,0.95402299 , 0]
    #
    # ax = plt.subplot(111)
    # ax.bar(x -0.2, y,width=0.2,color='b',align='center')
    # ax.bar(x, z,width=0.2,color='g',align='center')
    # ax.bar(x +0.2 , k,width=0.2,color='r',align='center')
    # plt.show()

if __name__ == '__main__':
    main()
