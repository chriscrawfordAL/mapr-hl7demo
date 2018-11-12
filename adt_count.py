import json
import os

#set up
#os.environ['LD_LIBRARY_PATH'] = "$LD_LIBRARY_PATH:/opt/mapr/lib"
#for mac
os.environ['DYLD_LIBRARY_PATH'] = "/opt/mapr/lib"

# MapR-DB DAG client libs:
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
# noinspection PyUnresolvedReferences
from confluent_kafka import Consumer, KafkaError

# Create a connection to the mapr-db:
host = raw_input("DAG host:")
username = "mapr"
password = "maprmapr"
tbl_path = "/adt_table"

connection_str = "{}:5678?auth=basic;user={};password={};ssl=false".format(host,username,password)
connection = ConnectionFactory.get_connection(connection_str=connection_str)

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path=tbl_path):
  document_store = connection.get_store(store_path=tbl_path)
else:
  document_store = connection.create_store(store_path=tbl_path)

# Create the Kakfa Consumer
c = Consumer({'group.id': 'mygroup',
              'default.topic.config': {'auto.offset.reset': 'earliest'}})
c.subscribe(['/hl7stream:adt_topic'])

#  Wait for new messages to be produced to the stream
running = True
while running:
    msg = c.poll(timeout=1.0)
    if msg is None:
        print("No messages on queue...sleeping")
        continue
    else:
        msg_json = json.loads(msg.value())['msh']
        if 'message_type' in msg_json:
            if msg_json['message_type']['message_code']['id'] == "ADT":
                print("Writing to ADT Document Store")
                event = msg_json['message_type']['trigger_event']['id']
                document_store.insert_or_replace(d=msg_json, _id=event)

