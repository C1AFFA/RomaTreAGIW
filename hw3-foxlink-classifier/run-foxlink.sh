#!/bin/sh

dsdir=$PWD/dataset
inputpath=$PWD/sandbox_input
outputpath=$PWD/sandbox_output
hdfsdatapath="hdfs://sandbox-hdp.hortonworks.com:8020/user/maria_dev/data"
skip=0

help() {
  echo "Usage: $0 -d <datasetName>"
  exit 1
}

while getopts "s?d:" opt
do
   case $opt in
      s ) 
          echo "Skipping loading dataset"
          skip=1 ;;
      d ) dsname="$OPTARG" ;;
      ? ) help ;;
   esac
done

if [ -z $dsname ] 
  then help 
fi

dspath="${dsdir}/${dsname}"

if [ ! -d "$dspath" ]; then
  echo "Dataset not found at $dspath"
  exit 1
fi

if [ ! -d $inputpath ] && [ ! -d $outputpath ]; then 
  echo "Input or output directories missing."
  exit 1
fi

if [ -z "$(docker ps | grep -e sandbox-hdp -e mongodb -e searx)" ]; then 
  echo "Not all required containers are running (sandbox-hdp, mongodb, searx)"
  exit 1
fi

load() {
  echo "Loading dataset \"$dsname\" into sandbox_input..."
  cd $inputpath
  cp -a "$dspath/." .
  cd ..
}
if [ ! $skip -eq 1 ]; then
  load
fi

pushtohdfs() {
  echo "Overwriting input into HDFS..."
  docker exec -t sandbox-hdp /usr/bin/hdfs dfs -rm -r -f $hdfsdatapath
  docker exec -t sandbox-hdp /usr/bin/hdfs dfs -mkdir $hdfsdatapath
  docker exec -t sandbox-hdp /usr/bin/hdfs dfs -put /root/input/products_seed.txt $hdfsdatapath
  docker exec -t sandbox-hdp /usr/bin/hdfs dfs -put /root/input/training_set_cluster_pages.txt $hdfsdatapath
  docker exec -t sandbox-hdp /usr/bin/hdfs dfs -put /root/input/training_set_home_pages.txt $hdfsdatapath
  docker exec -t sandbox-hdp /usr/bin/hdfs dfs -ls $hdfsdatapath
}
if [ ! $skip -eq 1 ]; then
  pushtohdfs
fi

launch() {
  echo "================="
  echo "LAUNCHING FOXLINK"
  docker exec -ti sandbox-hdp /bin/bash -c "
    cd /root/ && \
    source ./.bashrc && \
    source /etc/environment && \
    source activate base && \
    spark-submit --py-files utils.zip foxlink.py"
  # docker exec -t sandbox-hdp /bin/bash -c " spark-submit --py-files /root/utils.zip /root/foxlink.py"
  echo "================="
}
launch


pullfromdfs() {
  echo "Pulling output from HDFS..."
  cd $outputpath
  sudo rm -rf "data"
  docker exec -t sandbox-hdp /usr/bin/hdfs dfs -get $hdfsdatapath /root/output
  sudo chmod a+x "data"
  cd ..
  echo "Output available at $outputpath"
}
pullfromdfs




