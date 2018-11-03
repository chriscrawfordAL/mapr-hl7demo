import json
import time

from hl7_to_dict import hl7_str_to_dict

str_msg=''
with open("HL7_records.txt") as f:
    for line in f:
        if line != '\n':
            str_msg = str_msg+line
        else:
            #print(str_msg)
            # Put our json encoding and/or producer code here
            d = hl7_str_to_dict(str_msg)

            print json.dumps(d)
            str_msg=''
            time.sleep(5)


# Taken from http://hl7apy.org/tutorial/index.html#elements-manipulation
s = """MSH|^~\&|GHH_ADT||||20080115153000||ADT^A01^ADT_A01|0123456789|P|2.5||||AL
EVN||20080115153000||AAA|AAA|20080114003000
PID|1||566-554-3423^^^GHH^MR||EVERYMAN^ADAM^A|||M|||2222 HOME STREET^^ANN ARBOR^MI^^USA||555-555-2004~444-333-222|||M
NK1|1|NUCLEAR^NELDA^W|SPO|2222 HOME STREET^^ANN ARBOR^MI^^USA"""
