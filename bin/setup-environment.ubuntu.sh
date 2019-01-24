#! /bin/bash

set -x
set -e

#set up streams demo bits
#Run this on the edge node as user mapr

#Configure
#echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib" >> /home/mapr/.bashrc
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib

#hadoop fs -mkdir /demos
#hadoop fs -mkdir /demos/hl7demo
#hadoop fs -mkdir /demos/hl7demo/d3
#hadoop fs -put datasets/hl7_data.json /demos/hl7demo

#Installs
#curl -sL https://deb.nodesource.com/setup_8.x | sudo bash -
#sudo apt-get update
#sudo apt-get install gcc make -y
#sudo apt-get install nodejs -y
#sudo npm install npm@latest -g

#setup PIP
#curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
#sudo python get-pip.py

#Install and configure the python streams client
#sudo pip install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" mapr-streams-python
#sudo pip install maprdb-python-client
#sudo pip install hl7apy

#Create stream and topic
#maprcli stream create -path /demos/hl7demo/hl7stream -produceperm p -consumeperm p -topicperm p
#maprcli stream topic create -path /demos/hl7demo/hl7stream -topic allMessages -partitions 1
#maprcli stream topic create -path /demos/hl7demo/hl7stream -topic adt_topic -partitions 1

# create database tables
#maprcli table create -path /demos/hl7demo/hl7table -tabletype json
#maprcli table create -path /demos/hl7demo/adt_table -tabletype json
#maprcli table create -path /demos/hl7demo/d3/barChartCount -tabletype json
#maprcli table create -path /demos/hl7demo/totalMsgCount -tabletype json


# Install NPM Packages for Webserver
#npm install --prefix dashboard/
#npm install --prefix webserver/

# Load Starting Data
#hadoop fs -put datasets/hospitalsAndBedCounts.json /tmp
hadoop fs -put datasets/totalMsgCount.json /tmp
mapr importJSON -src /tmp/hospitalsAndBedCounts.json -dst /demos/hl7demo/d3/barChartCount
mapr importJSON -src /tmp/totalMsgCount.json -dst /demos/hl7demo/totalMsgCount
