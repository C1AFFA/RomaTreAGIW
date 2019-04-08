import glob
from metrics import *
import os



PAGE_INDEX = []
DATAPATH = "./data/"
PAGESPATH = "./data/pages/"
GOLDEN_RULES_FILENAME = "goldenRules.txt"

ATTRIBUTE_NAME = "Name"
GOLDEN_RULE = ""
LEARNED_XPATH = "//*[@class='header']"
ANNOTATED_PAGES = []
TEST_PAGES = []

# apro goldenRules.txt e estraggo la golden rule corrispondente all'attributo


with open(DATAPATH+GOLDEN_RULES_FILENAME) as f:
    for line in f:
        if ATTRIBUTE_NAME in line:
            GOLDEN_RULE = line
            GOLDEN_RULE = GOLDEN_RULE.replace(ATTRIBUTE_NAME, '')
            GOLDEN_RULE = GOLDEN_RULE.replace("/text()", "")
            GOLDEN_RULE = GOLDEN_RULE.strip()
            break
    print("Golden Rule for attribute "+ATTRIBUTE_NAME+":")
    print(GOLDEN_RULE)

with open(DATAPATH+"representatives-"+ATTRIBUTE_NAME+".txt") as f:
    for line in f:
       PAGE_INDEX.append(line.strip())
    print("Page index for attribute "+ATTRIBUTE_NAME+":")
    print(PAGE_INDEX)

for index in PAGE_INDEX:
    pagepath = PAGESPATH+index+".html"
    if os. path. isfile(pagepath):
        ANNOTATED_PAGES.append(Page(pagepath, GOLDEN_RULE))

TEST_PAGES = ANNOTATED_PAGES[3:]
ANNOTATED_PAGES = ANNOTATED_PAGES[:3]

print(ANNOTATED_PAGES)
print(TEST_PAGES)

#Applichiamo l'XPATH restituito dall'XSLT LEARNER alle pagine di test. Applichiamo poi la golden rule e confrointiamo nodo a nodo i risultati

POSITIVE_NODES = []
RETRIEVED_NODES = []

for t_page in TEST_PAGES:
    gr_nodes = t_page.DOM.xpath(GOLDEN_RULE)
    learned_xpath_nodes = t_page.DOM.xpath(GOLDEN_RULE)
    POSITIVE_NODES.extend(gr_nodes)
    RETRIEVED_NODES.extend(learned_xpath_nodes)

POSITIVES_RETRIEVED_NODES = [value for value in POSITIVE_NODES if value in RETRIEVED_NODES]

print(POSITIVE_NODES)
print(RETRIEVED_NODES)
print(POSITIVES_RETRIEVED_NODES)
print("---------------------")

precision = len(POSITIVES_RETRIEVED_NODES)/len(RETRIEVED_NODES)
recall = len(POSITIVES_RETRIEVED_NODES)/len(POSITIVE_NODES)


print("Precision for attribute "+ATTRIBUTE_NAME+": "+str(precision))
print("Recall for attribute "+ATTRIBUTE_NAME+": "+str(recall))









