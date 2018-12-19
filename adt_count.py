import json
import os

#set up
os.environ['LD_LIBRARY_PATH'] = "$LD_LIBRARY_PATH:/opt/mapr/lib"

# MapR-DB DAG client libs:
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
# noinspection PyUnresolvedReferences
from confluent_kafka import Consumer, KafkaError

# Create a connection to the mapr-db:
host = raw_input("DAG host:")
username = "mapr"
password = "maprmapr18"
tbl_path = "/demos/hl7demo/adt_table"

#Unsecure system connection
#connection_str = "{}:5678?auth=basic;user={};password={};ssl=false".format(host,username,password)
connection_str = "{}:5678?auth=basic;user={};password={};ssl=true;sslCA=/opt/mapr/conf/ssl_truststore.pem;sslTargetNameOverride={}".format(host,username,password,host)
connection = ConnectionFactory.get_connection(connection_str=connection_str)

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path=tbl_path):
  document_store = connection.get_store(store_path=tbl_path)
else:
  document_store = connection.create_store(store_path=tbl_path)

# Create the Kakfa Consumer
c = Consumer({'group.id': 'mygroup',
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
        if 'message_type' in msg_json:
            print(msg_json)
            if 'message_code' in msg_json:
                if msg_json['message_type']['message_code']['id'] == "ADT":
                    print("Writing to ADT Document Store")
                    event = msg_json['message_type']['trigger_event']['id']
                    facility = msg_json['sending_facility']['namespace_id']['is']
                    document_store.insert_or_replace(doc=msg_json, _id=facility)
                if msg_json['message_type']['message_type']['id'] == "ADT":
                    print("Writing to ADT Document Store")
                    event = msg_json['message_type']['trigger_event']['id']
                    facility = msg_json['sending_facility']['namespace_id']['is']
                    document_store.insert_or_replace(doc=msg_json, _id=facility)
            #elif msg.error().code() != KafkaError._PARTITION_EOF:
            #    print(msg.error())
            #    running = False

c.close()

