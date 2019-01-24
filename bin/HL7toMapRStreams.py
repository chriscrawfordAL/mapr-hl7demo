import time
import json

# noinspection PyUnresolvedReferences
from confluent_kafka import Producer
from hl7_to_dict import hl7_str_to_dict

#Set up my producer
p = Producer({'streams.producer.default.stream': '/demos/hl7demo/hl7stream'})

str_msg=''
with open("../datasets/hl7_records.txt") as f:
    for line in f:
        if line!='\n':
            str_msg=str_msg+line
        else:
            #print(str_msg)
            d = hl7_str_to_dict(str_msg)
            #f = open("/Users/ccrawford/eclipse-workspace/demoJam/data/streamsOuput.json", "w")
            #f.write(json.dumps(d));
            print json.dumps(d)
            print ("\n\n")
            json_hl7 = json.dumps(d)

            p.produce('allMessages', json_hl7)
            p.produce('adt_topic', json_hl7)
            # Or - just do a json.dumps(your_json) instead of str_msg
            p.flush()
            str_msg=''
            time.sleep(5)
