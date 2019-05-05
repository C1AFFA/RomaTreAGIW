#!/bin/sh
PREFIX="hdfs://sandbox-hdp.hortonworks.com:8020/user/maria_dev/data"

sudo rm -rf sandbox_output/*
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -get $PREFIX /root/output