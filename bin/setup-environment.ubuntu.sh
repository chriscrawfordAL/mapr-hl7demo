#! /bin/bash

set -x
set -e

#Configure
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib" >> /home/mapr/.bashrc
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib

sudo -u mapr hadoop fs -mkdir /demos
sudo -u mapr hadoop fs -mkdir /demos/hl7demo
sudo -u mapr hadoop fs -mkdir /demos/hl7demo/d3
sudo -u mapr hadoop fs -put datasets/hl7_data.json /demos/hl7demo

#Installs
curl -sL https://deb.nodesource.com/setup_8.x | sudo bash -
sudo apt-get update
sudo apt-get install gcc make -y
sudo apt-get install nodejs -y
sudo npm install npm@latest -g

#setup PIP
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py

#Install and configure the python streams client
sudo pip install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" mapr-streams-python
sudo pip install maprdb-python-client
sudo pip install hl7apy
sudo pip install requests

#Create stream and topic
sudo -u mapr maprcli stream create -path /demos/hl7demo/hl7stream -produceperm p -consumeperm p -topicperm p
sudo -u mapr maprcli stream topic create -path /demos/hl7demo/hl7stream -topic allMessages -partitions 1
sudo -u mapr maprcli stream topic create -path /demos/hl7demo/hl7stream -topic adt_topic -partitions 1

# create database tables
sudo -u mapr maprcli table create -path /demos/hl7demo/hl7table -tabletype json
sudo -u mapr maprcli table create -path /demos/hl7demo/adt_table -tabletype json
sudo -u mapr maprcli table create -path /demos/hl7demo/d3/barChartCount -tabletype json
sudo -u mapr maprcli table create -path /demos/hl7demo/totalMsgCount -tabletype json


# Install NPM Packages for Webserver
npm install --prefix webserver/
npm install --prefix dashboard/

# Load Starting Data
sudo -u mapr hadoop fs -put datasets/hospitalsAndBedCounts.json /tmp
sudo -u mapr hadoop fs -put datasets/totalMsgCount.json /tmp
sudo -u mapr mapr importJSON -src /tmp/hospitalsAndBedCounts.json -dst /demos/hl7demo/d3/barChartCount
sudo -u mapr mapr importJSON -src /tmp/totalMsgCount.json -dst /demos/hl7demo/totalMsgCount

#Insert edge FQDN into DASHBOARD Webserver
sed -i "s/localhost/edge-${DEPLOYMENT_HASH}.se.corp.maprtech.com/g" dashboard/js/d3index.js
sed -i "s/localhost/edge-${DEPLOYMENT_HASH}.se.corp.maprtech.com/g" dashboard/index.html

#Start Node.JS Webserver
npm start --prefix webserver/ &

#Start DASHBOARD Webserver
node dashboard/webserver.js &
