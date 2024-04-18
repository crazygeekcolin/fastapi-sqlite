import json
with open('../osvar/secretkey.txt') as f:
    a = f.read()
system_variable = json.loads(a)