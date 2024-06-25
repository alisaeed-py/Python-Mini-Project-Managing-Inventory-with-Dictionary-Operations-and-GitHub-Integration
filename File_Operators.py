import json
import os

INVENTORY_FILE = 'inventory.json'

def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            'Name': [],
            'Price': [],
            'Count': []
        }

def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f)
