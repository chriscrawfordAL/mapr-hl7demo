import json
import os
import requests
import time
import random

#set up
os.environ['LD_LIBRARY_PATH'] = "$LD_LIBRARY_PATH:/opt/mapr/lib"

# MapR-DB DAG client libs:
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
# noinspection PyUnresolvedReferences
from confluent_kafka import Consumer, KafkaError

# Create a connection to the mapr-db:
#host = raw_input("DAG host:")
host = "dag"
username = "mapr"
password = "maprmapr"
tbl_path = "/demos/hl7demo/adt_table"

def incrementCount():
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"$increment":{"count":1}}'

    requests.post(
        'https://dag:8243/api/v2/table/%2Fdemos%2Fhl7demo%2FtotalMsgCount/document/adtMessages',
        headers=headers, data=data, verify=False, auth=('mapr', 'maprmapr'))

def update(location, crud):
    headers = {
        'Content-Type': 'application/json',
    }

    if location == 'MidWsUnvMC':
        location = 'MED_BAY_1'
    elif location == 'BgCtyChldrnUrgntCar':
        location = 'MED_BAY_2'
    elif location == 'LakeMichMC':
        location = 'MED_BAY_3'
    elif location == 'MidTwnUrgentC':
        location = 'MED_BAY_4'
    elif location == 'PacNWHosED':
        location = 'MED_BAY_5'
    elif location == 'SmvUrgentC':
        location = 'MED_BAY_' + str(random.randint(1, 5))
    elif location == 'SthrnMdwstMedCntr':
        location = 'MED_BAY_' + str(random.randint(1, 5))
    elif location == 'WstrnRgnlMedCntr':
        location = 'MED_BAY_' + str(random.randint(1, 5))
    else:
        location = 'MED_BAY_' + str(random.randint(1, 5))

    if crud == 'ADT_A01':
        data = '{"$increment":{"openBeds":1}}'
    elif crud == 'ADT_A02':
        data = '{"$increment":{"openBeds":1}}'
    elif crud == 'ADT_A03':
        data = '{"$decrement":{"openBeds":1}}'
    else:
        return

    requests.post(
        'https://dag:8243/api/v2/table/%2Fdemos%2Fhl7demo%2Fd3%2FbarChartCount/document/' + location,
        headers=headers, data=data, verify=False, auth=('mapr', 'maprmapr'))

    incrementCount()

#Unsecure system connection
connection_str = "{}:5678?auth=basic;user={};password={};ssl=false".format(host,username,password)
#SECURE Systen connection string
#connection_str = "{}:5678?auth=basic;user={};password={};ssl=true;sslCA=/opt/mapr/conf/ssl_truststore.pem;sslTargetNameOverride={}".format(host,username,password,host)
connection = ConnectionFactory.get_connection(connection_str=connection_str)

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path=tbl_path):
    document_store = connection.get_store(store_path=tbl_path)
else:
    document_store = connection.create_store(store_path=tbl_path)

# Create the Kakfa Consumer
c = Consumer({'group.id': 'mygroup',
              'enable.partition.eof': 'false',
              'default.topic.config': {'auto.offset.reset': 'earliest'}})
c.subscribe(['/demos/hl7demo/hl7stream:adt_topic'])

#  Wait for new messages to be produced to the stream
running = True
while running:
    msg = c.poll(timeout=1.0)
    if msg is None:
        print("No messages on queue...sleeping")
        continue
    else:
        print(msg)

    if not msg.error():
        msg_json = json.loads(msg.value())['msh']
        if 'message_code' in msg_json['message_type']:
            print(msg_json)
            if msg_json['message_type']['message_code']['id'] == "ADT":
                print("Writing message_type.message_code to ADT Document Store")
                #event = msg_json['message_type']['trigger_event']['id']
                event = msg_json['message_type']['message_structure']['id']
                if 'sending_facility' in msg_json:
                    facility = msg_json['sending_facility']['namespace_id']['is']
                elif 'reciving_application' in msg_json:
                    facility = msg_json['receiving_application']['namespace_id']['is']
                else:
                    continue
                document_store.insert_or_replace(doc=msg_json, _id=facility)
                update(facility, event)
        elif 'message_type' in msg_json['message_type']:
            print(msg_json)
            if msg_json['message_type']['message_type']['id'] == 'ADT':
                print("Writing message_type.message_type to ADT Document Store")
                #event = msg_json['message_type']['trigger_event']['id']
                event = msg_json['message_type']['message_structure']['id']
                msg_control = msg_json['message_control_id']['st']['st']
                document_store.insert_or_replace(doc=msg_json, _id=msg_control)
                update(msg_control, event)
        elif msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
            running = False
    else:
        print(msg.error())

#    time.sleep(2)
c.close()


