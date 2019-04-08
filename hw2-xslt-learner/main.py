from pathlib import Path
from xslt_learner import *
from evaluation import *

DIR_NAME = Path(__file__).parent
DATA_PATH = DIR_NAME / "input/"
PAGES_PATH = DIR_NAME / "input/pages/"
GOLDEN_RULES = DIR_NAME / "input/goldenRules.txt"
REPRESENTATIVES = "input/representatives-"

TRAINING_SET_SIZE = 4  # maximum is 8


def main():
    golden_attributes = []
    with open(GOLDEN_RULES) as file:
        for line in file:
            values = line.split("\t")
            attribute = Attribute(values[0], values[1].replace("/text()", "").strip())
            golden_attributes.append(attribute)

    for attribute in golden_attributes:
        filename = REPRESENTATIVES + attribute.name + ".txt"
        with open(DIR_NAME / filename) as file:
            indexes = []
            for line in file:
                indexes.append(line.strip())
            attribute.ann_pages_indexes = indexes

    print("Loaded the following annotated attributes:")
    for attribute in golden_attributes:
        print(attribute)

    print("\nWe will generate the following feature types:\n" + str(FEATURE_TYPES.keys()) + "\n")

    # TODO REMOVE LIST SLICING TO ITERATE ON ALL ATTRIBUTES
    for attr in golden_attributes[:1]:
        print("=" * 100
              + "\nLearning attribute: " + attr.name
              + "\n(annotated xpath:" + attr.golden_rule + ")\n"
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

        print("[STARTING TRAINING PHASE]")

        # PAGE FETCH & FEATURE GENERATION
        annotated_pages_training = []
        unannotated_pages = []
        annotated_pages_test = []
        for path in annotated_pages_paths:
            annotated_pages_training.append(Page(path, attr.golden_rule))
        for path in annotated_pages_paths_test:
            annotated_pages_test.append(Page(path, "//foo"))
        for path in unannotated_pages_paths:
            unannotated_pages.append(Page(path, "//foo"))

        for page in annotated_pages_training:
            page.features = generate_features(page)
            features_set = list(get_global_feature_set(annotated_pages_training))

        # TODO UNCOMMENT TO RUN LEARNER
        # attr.learnt_rule = learn_xslt_rule(annotated_pages_training, unannotated_pages, features_set)
        attr.learnt_rule = "//h1" # TODO TEMPORARY HARDCODED RULE

        print("=" * 3 + " Learnt xpath: " + attr.learnt_rule)
        print("=" * 3 + " Annotated xpath was " + attr.golden_rule)

        print("\n\n[STARTING TEST PHASE]")

        # TODO SOMETHING BROKE HERE (help!!!)
        precision, recall = evaluate(annotated_pages_test, attr.learnt_rule, attribute.golden_rule)
        print("Precision for attribute " + attribute.name + ": " + str(precision))
        print("Recall for attribute " + attribute.name + ": " + str(recall))


if __name__ == '__main__':
    main()
