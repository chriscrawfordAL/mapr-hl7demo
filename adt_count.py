import json

with open("out.json") as f:
    for line in f:
        #print(line)
        msg_json = json.loads(line)['msh']
        if 'message_type' in msg_json:
            if msg_json['message_type']['message_code']['id'] == "ADT":
                event = msg_json['message_type']['trigger_event']['id']

