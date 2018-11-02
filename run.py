import json

from hl7_to_dict import hl7_str_to_dict

# Taken from http://hl7apy.org/tutorial/index.html#elements-manipulation
s = """MSH|^~\&|GHH_ADT||||20080115153000||ADT^A01^ADT_A01|0123456789|P|2.5||||AL
EVN||20080115153000||AAA|AAA|20080114003000
PID|1||566-554-3423^^^GHH^MR||EVERYMAN^ADAM^A|||M|||2222 HOME STREET^^ANN ARBOR^MI^^USA||555-555-2004~444-333-222|||M
NK1|1|NUCLEAR^NELDA^W|SPO|2222 HOME STREET^^ANN ARBOR^MI^^USA"""

d = hl7_str_to_dict(s)

print json.dumps(d)
