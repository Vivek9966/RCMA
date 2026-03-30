import json
location = 'data/regulations/risk_data/test_set.json'

with open(location, 'r') as file:
    data = json.load(file)

print(len(data))