import json
import time
import matplotlib.pyplot as plt
from datetime import datetime
from prettytable import PrettyTable
import getpass  # For secure password input

# Global variables
current_user = None
inventory = {}  # Inventory dictionary to hold item data
total_sales = 0  # Initialize total_sales to 0

# Load inventory from JSON file for the current user
def load_inventory():
    global inventory, total_sales
    try:
        with open('inventory.json', 'r') as file:
            data = file.read()
            if data:
                data = json.loads(data)
                user_data = data.get(current_user, {})
                inventory = user_data.get('inventory', {})
                total_sales = user_data.get('total_sales', 0)
            else:
                inventory = {}
                total_sales = 0
    except FileNotFoundError:
        inventory = {}
        total_sales = 0

# Save inventory to JSON file for the current user
def save_inventory():
    try:
        with open('inventory.json', 'r') as file:
            data = file.read()
            if data:
                data = json.loads(data)
            else:
                data = {}
    except FileNotFoundError:
        data = {}

    data[current_user] = {'inventory': inventory, 'total_sales': total_sales}

    with open('inventory.json', 'w') as file:
        json.dump(data, file, indent=4)

# Display the current inventory state and total sales as a table
def display_inventory():
    print("\n📦 Current Inventory and Sales")
    table = PrettyTable()
    table.field_names = ["Name", "Price", "Count", "Sales (Count)", "Sales (Price)"]
    
    for name, details in inventory.items():
        sales_count = details.get('sales_count', 0)  # Default to 0 if 'sales_count' is missing
        sales_price = details.get('sales_price', 0.0)  # Default to 0.0 if 'sales_price' is missing
        table.add_row([name, details['price'], details['count'], sales_count, sales_price])
    
    print(table)
    print(f"💰 Total sales: {total_sales}")

# Add new item to the inventory
def add_item(name, price, count):
    if name in inventory:
        print(f"⚠️ Item '{name}' already exists. Use 'update inventory' to modify count.")
    else:
        inventory[name] = {'price': price, 'count': count, 'sales_count': 0, 'sales_price': 0.0}
        save_inventory()
        print(f"✅ Item '{name}' added to inventory.")

# Buy item from the inventory
def buy_item(name, quantity):
    global total_sales
    if name in inventory:
        if inventory[name]['count'] >= quantity:
            inventory[name]['count'] -= quantity
            inventory[name]['sales_count'] += quantity
            inventory[name]['sales_price'] += quantity * inventory[name]['price']
            total_sales += quantity * inventory[name]['price']
            save_inventory()
            print(f"🛒 Purchased {quantity} of '{name}'.")
        else:
            print(f"❌ Insufficient stock for '{name}'.")
    else:
        print(f"❌ Item '{name}' not found in inventory.")

# Change price of an existing item
def change_price(name, new_price):
    if name in inventory:
        inventory[name]['price'] = new_price
        save_inventory()
        print(f"💲 Price of '{name}' updated to {new_price}.")
    else:
        print(f"❌ Item '{name}' not found in inventory.")

# Update the count of an item in the inventory
def update_inventory(name, count):
    if name in inventory:
        inventory[name]['count'] = count
        save_inventory()
        print(f"🔄 Inventory of '{name}' updated to {count}.")
    else:
        print(f"❌ Item '{name}' not found in inventory.")

# Display statistics for a specific item by its name
def detail_by_name(name, period):
    if name in inventory:
        now = datetime.now()
        if period == 'day':
            print(f"\n📅 Statistics for '{name}' on {now.strftime('%Y-%m-%d')}:")
        elif period == 'month':
            print(f"\n📅 Statistics for '{name}' in {now.strftime('%Y-%m')}:")
        elif period == 'year':
            print(f"\n📅 Statistics for '{name}' in {now.strftime('%Y')}:")
        print(f"Price: {inventory[name]['price']}, Stock: {inventory[name]['count']}, Sales (Count): {inventory[name]['sales_count']}, Sales (Price): {inventory[name]['sales_price']}")
    else:
        print(f"❌ Item '{name}' not found in inventory.")

# Delete an item from the inventory
def delete_item(name):
    if name in inventory:
        del inventory[name]
        save_inventory()
        print(f"🗑️ Item '{name}' deleted from inventory.")
    else:
        print(f"❌ Item '{name}' not found in inventory.")

# Generate graphs based on inventory data
def generate_graph():
    print("\n📊 Graph Generator")
    print("Data Options:")
    print("1. All product sales")
    print("2. All product stock")
    print("3. All product sales and stock")

    data_option = int(input("Enter data option (1-3): "))
    
    if data_option == 1:
        print("\nGraph Types:")
        print("1. Bar Graph")
        print("2. Pie Chart")
        print("3. Histogram")
        graph_option = int(input("Enter graph option (1-3): "))

        if graph_option == 1:
            names = list(inventory.keys())
            plt.bar(names, [inventory[name]['sales_count'] for name in names])
            plt.xlabel('Items')
            plt.ylabel('Sales (Count)')
            plt.title('Bar Graph: Sales (Count) of all items')
            plt.xticks(rotation=45)
            plt.show()
        elif graph_option == 2:
            names = list(inventory.keys())
            plt.figure(figsize=(8, 8))
            plt.pie([inventory[name]['sales_count'] for name in names], labels=names, autopct='%1.1f%%')
            plt.title('Pie Chart: Sales (Count) Distribution')
            plt.show()
        elif graph_option == 3:
            plt.hist([inventory[name]['sales_count'] for name in inventory.keys()], bins=10)
            plt.xlabel('Sales (Count)')
            plt.ylabel('Frequency')
            plt.title('Histogram: Sales (Count) Distribution')
            plt.show()
        else:
            print("❌ Invalid option.")
    
    elif data_option == 2:
        print("\nGraph Types:")
        print("1. Bar Graph")
        graph_option = int(input("Enter graph option (1): "))

        if graph_option == 1:
            names = list(inventory.keys())
            plt.bar(names, [inventory[name]['count'] for name in names])
            plt.xlabel('Items')
            plt.ylabel('Stocks')
            plt.title('Bar Graph: Stocks of all items')
            plt.xticks(rotation=45)
            plt.show()
        else:
            print("❌ Invalid option.")

    elif data_option == 3:
        print("\nGraph Types:")
        print("1. Bar Graph: Stocks")
        print("2. Bar Graph: Sales (Count)")
        graph_option = int(input("Enter graph option (1-2): "))

        if graph_option == 1:
            names = list(inventory.keys())
            plt.figure(figsize=(10, 5))
            plt.bar(names, [inventory[name]['count'] for name in names], label='Stocks')
            plt.xlabel('Items')
            plt.ylabel('Quantity')
            plt.title('Bar Graph: Stocks of all items')
            plt.xticks(rotation=45)
            plt.legend()
            plt.show()
        elif graph_option == 2:
            names = list(inventory.keys())
            plt.figure(figsize=(10, 5))
            plt.bar(names, [inventory[name]['sales_count'] for name in names], label='Sales (Count)')
            plt.xlabel('Items')
            plt.ylabel('Quantity')
            plt.title('Bar Graph: Sales (Count) of all items')
            plt.xticks(rotation=45)
            plt.legend()
            plt.show()
        else:
            print("❌ Invalid option.")

    else:
        print("❌ Invalid option.")

# Registration function
def register_user():
    with open('login.json', 'r') as file:
        try:
            users = json.load(file)
        except json.JSONDecodeError:
            users = {}

    username = input("Enter a new username: ")
    if username in users:
        print("❌ Username already exists. Try logging in.")
        return False

    password = getpass.getpass("Enter a new password: ")
    users[username] = password

    with open('login.json', 'w') as file:
        json.dump(users, file, indent=4)
    
    print("✅ Registration successful. You can now log in.")
    return True

# Login function
def login_user():
    global current_user
    with open('login.json', 'r') as file:
        try:
            users = json.load(file)
        except json.JSONDecodeError:
            users = {}

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    if username in users and users[username] == password:
        current_user = username
        print("✅ Login successful.")
        return True
    else:
        print("❌ Invalid credentials. Please try again.")
        return False

def main():
    while True:
        print("\n🔑 Login Menu")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            if login_user():
                break
        elif choice == '2':
            register_user()
        elif choice == '3':
            print("\n🚪 Exiting Program. Thank you!")
            return
        else:
            print("\n❌ Invalid choice. Please enter a number from 1 to 3.")

    load_inventory()
    
    while True:
        print("\n📋 Main Menu")
        print("1. Add Item")
        print("2. Buy Item")
        print("3. Change Item Price")
        print("4. Display Inventory")
        print("5. Update Inventory")
        print("6. Search and View Item Statistics")
        print("7. Delete Item")
        print("8. Generate Graphs")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            display_inventory()
            print("\n➕ Adding Item")
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            count = int(input("Enter item count: "))
            add_item(name, price, count)
        
        elif choice == '2':
            display_inventory()
            print("\n🛒 Buying Item")
            name = input("Enter item name: ")
            quantity = int(input("Enter quantity to buy: "))
            buy_item(name, quantity)
        
        elif choice == '3':
            display_inventory()
            print("\n💲 Changing Item Price")
            name = input("Enter item name: ")
            new_price = float(input("Enter new price: "))
            change_price(name, new_price)
        
        elif choice == '4':
            display_inventory()
        
        elif choice == '5':
            display_inventory()
            print("\n🔄 Updating Inventory")
            name = input("Enter item name: ")
            count = int(input("Enter new count: "))
            update_inventory(name, count)
        
        elif choice == '6':
            display_inventory()
            print("\n🔍 Searching and Viewing Item Statistics")
            name = input("Enter item name: ")
            period = input("Enter period (day/month/year): ").lower()
            detail_by_name(name, period)
        
        elif choice == '7':
            display_inventory()
            print("\n🗑️ Deleting Item")
            name = input("Enter item name: ")
            delete_item(name)
        
        elif choice == '8':
            display_inventory()
            generate_graph()
        
        elif choice == '9':
            print("\n🚪 Exiting Program. Thank you!")
            break
        
        else:
            print("\n❌ Invalid choice. Please enter a number from 1 to 9.")

if __name__ == "__main__":
    main()
