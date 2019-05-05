#!/bin/sh
PREFIX="hdfs://sandbox-hdp.hortonworks.com:8020/user/maria_dev/data"

docker exec -t sandbox-hdp /usr/bin/hdfs dfs -rm -r -f $PREFIX
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -mkdir $PREFIX
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -put /root/input/products_seed.txt $PREFIX
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -put /root/input/training_set_cluster_pages.txt $PREFIX
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -put /root/input/training_set_home_pages.txt $PREFIX