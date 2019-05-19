import pandas as pd
from extractor import Extractor


def get_line_generator():
    testfile = open("./../test_set_cluster_pages.txt")

    for line in testfile:
        url, category = line.strip().split("\t")
        yield url, category


def get_text_from_url(url):
    try:
        #html = urllib.request.urlopen(url, timeout=3)
        # soup = BeautifulSoup(html)
        # body = soup.find('body')
        # [x.extract() for x in body.findAll('script')]
        # [x.extract() for x in body.findAll('style')]
        # text=re.sub("\s\s+", " ", body.get_text())
        extractor = Extractor()
        text = extractor.get_body_text(url)

    except:
        return "parsing error"

    return text


df = pd.read_parquet("./../output__bikes/data_may-17/classifier/evaluation_cluster_pages.parquet")
df.drop(df.index, inplace=True)

cont = 0
for url, cat in get_line_generator():
    print(str(cont)+": "+url)
    df = df.append({'category': cat, 'cluster_label': "product", "domain": url,"referring_url": url, "text": get_text_from_url(url), "url": url}, ignore_index=True)
    cont += 1
    # if cont >1:
    #     break


df.to_parquet("./../evaluation_cluster_pages__NEW.parquet")
print(df)
