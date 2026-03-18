import json

with open('data/regulations/risk_data/train_set.json', 'r') as f:
    train = json.load(f)

with open('data/regulations/risk_data/test_set.json', 'r') as f:
    test = json.load(f)

print(f"Train records: {len(train)}")
print(f"Test records: {len(test)}")

# check the first key
first_key = list(train.keys())[0]
print(f"First key: {first_key}")
print(f"First value: {train[first_key]}")
