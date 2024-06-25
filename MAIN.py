import json

# File_Operators.py (for handling file operations)

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

# Inventory Management Functions

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
        print(f"\nCurrent details of {item_name}:")
        print(f"Price: {inventory['Price'][index]}")
        print(f"Count: {inventory['Count'][index]}")

        try:
            quantity = int(input("Enter the quantity to buy: "))

            if quantity <= int(inventory['Count'][index]):
                total_cost = quantity * float(inventory['Price'][index])
                inventory['Count'][index] = str(int(inventory['Count'][index]) - quantity)
                inventory['Total Sales'] = inventory.get('Total Sales', 0.0) + total_cost
                print(f"\nYou bought {quantity} of {item_name} for ${total_cost:.2f}")
            else:
                print("\nInsufficient stock available.")
        except ValueError:
            print("\nInvalid quantity entered.")
    else:
        print(f"\nItem '{item_name}' not found in inventory.")

def change_price(inventory):
    """
    Change the price of an existing item in the inventory.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    display_inventory(inventory)

    item_name = input("\nEnter the name of the item to change the price: ")

    if item_name in inventory['Name']:
        index = inventory['Name'].index(item_name)
        print(f"\nCurrent details of {item_name}:")
        print(f"Price: {inventory['Price'][index]}")

        new_price = input("\nEnter the new price: ").strip()

        if new_price:
            inventory['Price'][index] = new_price
            print(f"\nPrice of {item_name} updated successfully!")
        else:
            print("\nInvalid price entered.")
    else:
        print(f"\nItem '{item_name}' not found in inventory.")

def delete_item(inventory):
    """
    Delete an item from the inventory.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    item_name = input("\nEnter the name of the item to delete: ")

    if item_name in inventory['Name']:
        index = inventory['Name'].index(item_name)
        del inventory['Name'][index]
        del inventory['Price'][index]
        del inventory['Count'][index]
        print(f"\nItem '{item_name}' deleted successfully!")
    else:
        print(f"\nItem '{item_name}' not found in inventory.")

def more_options(inventory):
    """
    Additional options for the inventory management.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    while True:
        print("\nMore options:")
        print("1. Get item details")
        print("2. Delete an item")
        print("3. Change item price")
        print("4. Back to main menu")

        choice = input("\nEnter your choice (1-4): ")

        if choice == '1':
            get_item_details(inventory)
        elif choice == '2':
            delete_item(inventory)
            display_inventory(inventory)
        elif choice == '3':
            change_price(inventory)
            display_inventory(inventory)
        elif choice == '4':
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 4.")

def main():
    # Print a welcome message
    print("\nWelcome to the Inventory Management System!\n")

    # Load inventory from JSON file
    inventory = load_inventory()

    # Display the initial inventory
    display_inventory(inventory)

    while True:
        # Ask user for action
        print("\nOptions:")
        print("1. Add a new item")
        print("2. Update an existing item")
        print("3. Get details of an item by name")
        print("4. Buy an item")
        print("5. Change item price")
        print("6. More options")
        print("7. Delete an item")
        print("8. Display Inventory")
        print("9. Exit")

        choice = input("\nEnter your choice (1-9): ")

        if choice == '1':
            # Ask user for new item details
            print("\nEnter details for the new item:")
            name = input("Name: ")
            price = input("Price: ")
            count = input("Count: ")

            # Add the new item to the inventory
            add_item(inventory, name, price, count)
            print("Item added successfully!")

            # Display the updated inventory
            display_inventory(inventory)

        elif choice == '2':
            # Update an existing item
            update_item(inventory)
            display_inventory(inventory)

        elif choice == '3':
            # Get details of an item by name
            get_item_details(inventory)

        elif choice == '4':
            # Buy an item
            buy_item(inventory)
            display_inventory(inventory)

        elif choice == '5':
            # Change item price
            change_price(inventory)
            display_inventory(inventory)

        elif choice == '6':
            # More options
            more_options(inventory)

        elif choice == '7':
            # Delete an item
            delete_item(inventory)
            display_inventory(inventory)

        elif choice == '8':
            # Display inventory
            display_inventory(inventory)

        elif choice == '9':
            # Save inventory to JSON file before exiting
            save_inventory(inventory)
            print("\nExiting program. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 9.")

# Only execute main() if this script is run directly
if __name__ == "__main__":
    main()
