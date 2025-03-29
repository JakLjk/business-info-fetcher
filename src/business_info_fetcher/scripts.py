import json

def save_to_json(data: dict, filepath: str):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
