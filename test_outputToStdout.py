import json
import time

from hl7_to_dict import hl7_str_to_dict

str_msg=''
with open("hl7_records_random.txt") as f:
    for line in f:
        if line != '\n':
            str_msg = str_msg+line
        else:
            print(str_msg)
            # Put our json encoding and/or producer code here
            d = hl7_str_to_dict(str_msg)

            print json.dumps(d)
            str_msg=''
            time.sleep(5)
