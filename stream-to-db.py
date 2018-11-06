import sys, datetime, time, json, os

# No Kafka Client import confluent_kafka

# MapR-DB DAG client libs:
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

# Create a connection to the mapr-db:
host = raw_input("DAG host:")
username = "mapr"
password = "mapr"
tbl_path = "/hl7table"

connection_str = "{}:5678?auth=basic;user={};password={};ssl=false".format(host,username,password) 
connection = ConnectionFactory.get_connection(connection_str=connection_str)

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path=tbl_path):
  document_store = connection.get_store(store_path=tbl_path)
else:
  document_store = connection.create_store(store_path=tbl_path)

# Create our sample json object from a larger json document (test-record.json)
# Here we're using an input file - this could just as easily be the stream
with open("test-record.json") as f:
    for line in f:
        # now that we've read the line - in this case json, lets create a json object and take some fields
	
	# Some test/play json paths
	# This seems to be who ordered the vaccine:
        # msg_json = json.loads(line)['vxu_v04_order']['orc']
	
	#NK1 - looks like a responsible party like mother, etc.?:
        #msg_json = json.loads(line)['nk1']
	
	#******Now the real stuff*****
	# Let's pull out the patient information and add a record in mapr-db json
	# the map named "pid" is the patient info, and we can use their id as document ID
	msg_json = json.loads(line)['pid']
	#Patient ID:
	#patient_id = json.loads(line)['pid']['patient_identifier_list']['id_number']['st']
	
	# Create OJAI document and insert it into the database using a single ID
    	d = connection.new_document(dictionary=msg_json)
    	document_store.insert_or_replace(doc=d, _id=msg_json['patient_identifier_list']['id_number']['st'])
	print("User record with ID {} successfully written to the table".format(msg_json['patient_identifier_list']['id_number']['st']))
