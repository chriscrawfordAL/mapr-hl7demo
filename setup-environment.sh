#! /bin/bash

set -x
set -e

#set up streams demo bits
#Run this on the edge node as user mapr

hadoop fs -mkdir /demos
hadoop fs -mkdir /demos/hl7demo
hadoop fs -put hl7_out/demos/hl7demo

#setup PIP
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py

#create stream and topic
maprcli stream create -path /demos/hl7demo/hl7stream -produceperm p -consumeperm p -topicperm p
maprcli stream topic create -path /demos/hl7demo/hl7stream -topic allMessages -partitions 1
maprcli stream topic create -path /demos/hl7demo/hl7stream -topic adt_topic -partitions 1


#Install and configure the python streams client
sudo yum install gcc -y

echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib" >> /home/mapr/.bashrc

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib
sudo yum install -y python-devel
sudo pip install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" mapr-streams-python
sudo pip install maprdb-python-client
sudo pip install hl7apy

# create database tables
# User Table:
maprcli table create -path /demos/hl7demo/hl7table -tabletype json
