#! /bin/bash

#set up streams demo bits
#Run this on the edge node as user mapr

#create stream and topic
maprcli stream create -path /hl7stream -produceperm p -consumeperm p -topicperm p
maprcli stream topic create -path /hl7stream -topic topic1 -partitions 3


#Install and configure the python streams client
sudo apt-get install gcc -y

echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib" >> /home/mapr/.bashrc

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib
sudo pip install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" mapr-streams-python