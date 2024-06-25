import json

# File operations

def load_inventory():
    try:
        with open('inventory.json', 'r') as file:
            inventory = json.load(file)
    except FileNotFoundError:
        inventory = {'Name': [], 'Price': [], 'Count': [], 'Total Sales': 0.0}
    return inventory

def save_inventory(inventory):
    with open('inventory.json', 'w') as file:
        json.dump(inventory, file, indent=4)

# Inventory management functions

def add_item(inventory, name, price, count):
    """
    Add a new item to the inventory.

    Parameters:
    - inventory (dict): The inventory dictionary.
    - name (str): Name of the item.
    - price (str): Price of the item.
    - count (str): Count of the item.

    Returns:
    - None
    """
    inventory['Name'].append(name)
    inventory['Price'].append(price)
    inventory['Count'].append(count)

def display_inventory(inventory):
    """
    Display the current inventory and total sales.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    print("\nCurrent Inventory:")
    if not inventory['Name']:
        print("No items in inventory.")
    else:
        for i in range(len(inventory['Name'])):
            name = inventory['Name'][i]
            price = inventory['Price'][i]
            count = inventory['Count'][i]
            print(f"Name: {name}, Price: {price}, Count: {count}")

    total_sales = inventory.get('Total Sales', 0.0)
    print(f"\nTotal Sales: ${total_sales:.2f}")

def update_item(inventory):
    """
    Update an existing item in the inventory.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    item_name = input("\nEnter the name of the item to update: ")

    if item_name in inventory['Name']:
        index = inventory['Name'].index(item_name)
        print(f"\nCurrent details of {item_name}:")
        print(f"Price: {inventory['Price'][index]}")
        print(f"Count: {inventory['Count'][index]}")

        new_price = input("\nEnter the new price (press Enter to keep current): ").strip()
        new_count = input("Enter the new count (press Enter to keep current): ").strip()

        if new_price:
            inventory['Price'][index] = new_price

        if new_count:
            inventory['Count'][index] = new_count

        print(f"\n{item_name} updated successfully!")
    else:
        print(f"\nItem '{item_name}' not found in inventory.")

def get_item_details(inventory):
    """
    Get details of an item in the inventory.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    item_name = input("\nEnter the name of the item to get details: ")

    if item_name in inventory['Name']:
        index = inventory['Name'].index(item_name)
        print(f"\nDetails of {item_name}:")
        print(f"Price: {inventory['Price'][index]}")
        print(f"Count: {inventory['Count'][index]}")
    else:
        print(f"\nItem '{item_name}' not found in inventory.")

def buy_item(inventory):
    """
    Handle the purchase of an item from the inventory.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    display_inventory(inventory)

    item_name = input("\nEnter the name of the item to buy: ")

    if item_name in inventory['Name']:
        index = inventory['Name'].index(item_name)
        print(f"Buying {item_name}...")
        quantity = int(input(f"Enter the quantity to buy (Available: {inventory['Count'][index]}): "))
        
        if quantity <= int(inventory['Count'][index]):
            inventory['Count'][index] -= quantity
            total_cost = quantity * float(inventory['Price'][index])
            inventory['Total Sales'] += total_cost
            print(f"Successfully bought {quantity} {item_name}(s) for ${total_cost:.2f}.")
        else:
            print("Insufficient quantity available.")
    else:
        print(f"Item '{item_name}' not found in inventory.")

def change_price(inventory):
    """
    Change the price of an existing item in the inventory.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    item_name = input("\nEnter the name of the item to change the price: ")

    if item_name in inventory['Name']:
        index = inventory['Name'].index(item_name)
        print(f"\nCurrent price of {item_name}: {inventory['Price'][index]}")

        new_price = input("Enter the new price: ").strip()
        inventory['Price'][index] = new_price

        print(f"\nPrice of {item_name} updated successfully to {new_price}.")
    else:
        print(f"\nItem '{item_name}' not found in inventory.")

def update_inventory(inventory):
    """
    Update the count of an existing item in the inventory.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    item_name = input("\nEnter the name of the item to update count: ")

    if item_name in inventory['Name']:
        index = inventory['Name'].index(item_name)
        print(f"\nCurrent count of {item_name}: {inventory['Count'][index]}")

        new_count = input("Enter the new count: ").strip()
        inventory['Count'][index] = new_count

        print(f"\nCount of {item_name} updated successfully to {new_count}.")
    else:
        print(f"\nItem '{item_name}' not found in inventory.")

def more_options(inventory):
    """
    Additional options for inventory management.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    while True:
        print("\nMore options:")
        print("1. Get item details")
        print("2. Back to main menu")

        choice = input("\nEnter your choice (1-2): ")

        if choice == '1':
            get_item_details(inventory)
        elif choice == '2':
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 2.")

def main():
    # Print a welcome message
    print("\nWelcome to the Inventory Management System!\n")

    # Load inventory from JSON file
    inventory = load_inventory()

    while True:
        # Display the main menu
        print("\nOptions:")
        print("1. Add a new item")
        print("2. Update an existing item")
        print("3. Get details of an item by name")
        print("4. Buy an item")
        print("5. Change item price")
        print("6. Update item count")
        print("7. More options")
        print("8. Display inventory")
        print("9. Save and exit")

        choice = input("\nEnter your choice (1-9): ")

        if choice == '1':
            # Add a new item
            print("\nEnter details for the new item:")
            name = input("Name: ")
            price = input("Price: ")
            count = input("Count: ")
            add_item(inventory, name, price, count)
            print(f"{name} added to inventory.")

        elif choice == '2':
            # Update an existing item
            update_item(inventory)

        elif choice == '3':
            # Get details of an item by name
            get_item_details(inventory)

        elif choice == '4':
            # Buy an item
            buy_item(inventory)

        elif choice == '5':
            # Change item price
            change_price(inventory)

        elif choice == '6':
            # Update item count
            update_inventory(inventory)

        elif choice == '7':
            # More options
            more_options(inventory)

        elif choice == '8':
            # Display current inventory
            display_inventory(inventory)

        elif choice == '9':
            # Save inventory to JSON file and exit
            save_inventory(inventory)
            print("\nInventory saved. Exiting program. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 9.")

if __name__ == "__main__":
    main()
