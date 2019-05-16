#!/bin/sh

dsdir=$PWD/dataset
inputpath=$PWD/sandbox_input
outputpath=$PWD/sandbox_output

help() {
  echo "Usage: $0 -d <datasetName>"
  exit 1
}

while getopts "d:" opt
do
   case $opt in
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

echo "Loading dataset \"$dsname\" into sandbox_input"
sudo rm "$inputpath/*"
cp -a "$dspath/." "$inputpath/"
# ls $inputpath

if [ -z "$(docker ps | grep -e sandbox-hdp -e mongodb -e searx)" ]; then 
  echo "Not all required containers are running (sandbox-hdp, mongodb, searx)"
  exit 1
fi

hdfsdatapath="hdfs://sandbox-hdp.hortonworks.com:8020/user/maria_dev/data"
echo "Overwriting input into HDFS..."
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -rm -r -f $hdfsdatapath
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -mkdir $hdfsdatapath
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -put /root/input/products_seed.txt $hdfsdatapath
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -put /root/input/training_set_cluster_pages.txt $hdfsdatapath
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -put /root/input/training_set_home_pages.txt $hdfsdatapath
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -ls $hdfsdatapath

echo "================="
echo "LAUNCHING FOXLINK"
docker exec -t sandbox-hdp spark-submit --py-files utils.zip foxlink.py
echo "================="


echo "Pulling output from HDFS..."
sudo rm -rf "outputpath/*"
docker exec -t sandbox-hdp /usr/bin/hdfs dfs -get $hdfsdatapath /root/output

echo "Output available at $outputpath"



