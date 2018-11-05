import time
import json

from confluent_kafka import Producer
from hl7_to_dict import hl7_str_to_dict

#Set up my producer
p = Producer({'streams.producer.default.stream': '/hl7stream'})

str_msg=''
with open("HL7_records.txt") as f:
    for line in f:
        if line!='\n':
            str_msg=str_msg+line
        else:
            #print(str_msg)
            d = hl7_str_to_dict(str_msg)
            print json.dumps(d)
            json_hl7 = json.dumps(d)

            #ORIG:  I think this is wrong: p.produce('topic1', str_msg)
            p.produce('topic1', json_hl7)
            # Or - just do a json.dumps(your_json) instead of str_msg
            p.flush()
            str_msg=''
            time.sleep(10)
