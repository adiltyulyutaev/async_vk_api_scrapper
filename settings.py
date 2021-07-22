import json

file = open('config.json', 'rb')
json_obj = json.loads(file.read())



DATABASE_URL = json_obj['DATABASE_URL']
VK_API = json_obj['VK_API']
GROUPS = json_obj["GROUPS"]
GROUPS_FIELDS = {k: v for k, v in json_obj['GROUPS_FIELDS'].items() if v == True}
USERS_FIELDS = {k: v for k, v in json_obj['USERS_FIELDS'].items() if v == True}
BATCH_SIZE = json_obj['BATCH_SIZE']