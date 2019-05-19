from pyspark import SparkContext, SparkConf
from web_discovery import web_discovery_searx
from clustering import foxlink_structural_clustering,foxlink_shingler
from mongodb_middleware import mongodb_interface
from crawler import foxlink_crawler
from cluster_linkage_analysis import referring_url_analysis
from classifier import naive_bayes_classifier
from xpath_analysis import xpath_patterns
import math,json


f = open('/root/config.json','r')
config = json.loads(f.read())
f.close()


conf = SparkConf().setAppName('foxlink')
sc = SparkContext(conf=conf)

# we run classifier without using an RDD.
# we also skip parquet generation for the training set, because we already provided
# both parquets (training and evalutaion) on the HDFS path.

#cluster pages classifier
category_clusters = naive_bayes_classifier.keywords_naive_bayes_classifier(
  sc,
  config['cluster_pages_classifier']['training_path_cluster_classifier'], 
  int(math.pow(2,int(config['cluster_pages_classifier']['number_of_features_exponent']))),
  config['cluster_pages_classifier']['ouput_train_cluster_page_path_parquet'],
  config['cluster_pages_classifier']['output_eval_cluster_page_path_parquet'],
  config['cluster_pages_classifier']['save_cluster_page_evaluation'],
  config['cluster_pages_classifier']['path_to_save_cluster_pages']
  )

sc.stop()