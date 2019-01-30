import sys, datetime, time, json, os, hashlib, requests

os.environ['LD_LIBRARY_PATH'] = "$LD_LIBRARY_PATH:/opt/mapr/lib"
# Since the above doesn't seem to work:
#ask = raw_input("did you set export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mapr/lib or source .bashrc?")

from confluent_kafka import Producer, Consumer, KafkaError

# MapR-DB DAG client libs:
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

os.environ['LD_LIBRARY_PATH'] = "$LD_LIBRARY_PATH:/opt/mapr/lib"

# Create a connection to the mapr-db:
#host = raw_input("DAG host:")
host = "dag"
username = "mapr"
password = "maprmapr"
tbl_path = "/demos/hl7demo/hl7table"

def incrementCount():
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"$increment":{"count":1}}'

    requests.post(
        'https://dag:8243/api/v2/table/%2Fdemos%2Fhl7demo%2FtotalMsgCount/document/allMessages',
        headers=headers, data=data, verify=False, auth=('mapr', 'maprmapr'))

#UNSECURED connection string
connection_str = "{}:5678?auth=basic;user={};password={};ssl=false".format(host,username,password)
#SECURED connection string
#connection_str = "{}:5678?auth=basic;user={};password={};ssl=true;sslCA=/opt/mapr/conf/ssl_truststore.pem;sslTargetNameOverride={}".format(host,username,password,host)

connection = ConnectionFactory.get_connection(connection_str=connection_str)

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path=tbl_path):
  document_store = connection.get_store(store_path=tbl_path)
else:
  document_store = connection.create_store(store_path=tbl_path)

# Create the Kakfa Consumer
c = Consumer({'group.id': 'mygroup',
              'default.topic.config': {'auto.offset.reset': 'earliest'}})
c.subscribe(['/demos/hl7demo/hl7stream:allMessages'])

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
        # msg.value is the raw string - if we assume it's in json, that's cool, we can do a json.loads and manipulate
        # We can grab the "pid" object from the full json - that is the patient info
        msg_json = json.loads(msg.value())['pid']

        #Debug
        print("JSON MSG:")
        print(msg_json)

        # Test to see if patient_identifier_list is actually a list or a string and create hashId for db insert
        if isinstance(msg_json['patient_identifier_list'], (list,)):
            if 'id_number' in msg_json['patient_identifier_list'][0]:
                pidlist = msg_json['patient_identifier_list'][0]['id_number']['st']
                hashId=hashlib.sha224(pidlist).hexdigest()
            elif 'id' in msg_json['patient_identifier_list'][0]:
                pidlist = msg_json['patient_identifier_list'][0]['id']['st']
                hashId=hashlib.sha224(pidlist).hexdigest()
        else:
            if 'id_number' in msg_json['patient_identifier_list']:
                pidlist = msg_json['patient_identifier_list']['id_number']['st']
                hashId=hashlib.sha224(pidlist).hexdigest()
            elif 'id' in msg_json['patient_identifier_list']:
                pidlist = msg_json['patient_identifier_list']['id']['st']
                hashId=hashlib.sha224(pidlist).hexdigest()

        # Create OJAI document and insert it into the database using a single ID
        msg_json = json.loads(msg.value())
        d = connection.new_document(dictionary=msg_json)

        # Insert or Replace Document
        document_store.insert_or_replace(doc=d, _id=hashId)
        print("User record with ID {} successfully written to the table".format(hashId))

        # Increment Document Processed Counter
        incrementCount()
#        time.sleep(2)
      
    elif msg.error().code() != KafkaError._PARTITION_EOF:
        print(msg.error())
        running = False

c.close()
