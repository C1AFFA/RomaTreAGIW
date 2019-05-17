from extractor import extractor

df = pd.read_parquet("output__bikes/classifier/evaluation_cluster_pages.parquet")
df = df.loc[df['cluster_label'] == "products"]["referring_url"]
data = df.values

extractor = Extractor()
cbreak = 0
for line in data:
    url , label = line.strip().split("\t")
    if label == "1":
        extractor.extract(url)
        print(extractor.url_img_extracted)
        cbreak += 1
        if cbreak > 20 :
            break
    
extractor.close()
