import File_Operators

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
    Display the current inventory.

    Parameters:
    - inventory (dict): The inventory dictionary.

    Returns:
    - None
    """
    print("\nCurrent Inventory:")
    for i in range(len(inventory['Name'])):
        print(f"Name: {inventory['Name'][i]}, Price: {inventory['Price'][i]}, Count: {inventory['Count'][i]}")

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
    # Display the available items in the inventory
    display_inventory(inventory)

    item_name = input("\nEnter the name of the item to buy: ")

    if item_name in inventory['Name']:
        index = inventory['Name'].index(item_name)
        print(f"\nCurrent details of {item_name}:")
        print(f"Price: {inventory['Price'][index]}")
        print(f"Count: {inventory['Count'][index]}")

        quantity = int(input("Enter the quantity to buy: "))

        if quantity <= int(inventory['Count'][index]):
            try:
                total_cost = quantity * float(inventory['Price'][index])
                inventory['Count'][index] = str(int(inventory['Count'][index]) - quantity)
                inventory['Total Sales'] = inventory.get('Total Sales', 0.0) + total_cost
                print(f"\nYou bought {quantity} of {item_name} for ${total_cost:.2f}")
            except ValueError:
                print("\nError: The price of the item is not a valid number.")
        else:
            print("\nInsufficient stock available.")
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
        print("3. Back to main menu")

        choice = input("\nEnter your choice (1-3): ")

        if choice == '1':
            get_item_details(inventory)
        elif choice == '2':
            delete_item(inventory)
            # Display the updated inventory after deletion
            display_inventory(inventory)
        elif choice == '3':
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 3.")

def main():
    # Print a welcome message
    print("\nWelcome to the Inventory Management System!\n")

    # Load inventory from JSON file
    inventory = File_Operators.load_inventory()

    # Initialize total sales if not already present
    if 'Total Sales' not in inventory:
        inventory['Total Sales'] = 0.0

    # Display the initial inventory
    display_inventory(inventory)

    while True:
        # Ask user for action
        print("\nOptions:")
        print("1. Add a new item")
        print("2. Update an existing item")
        print("3. Get details of an item by name")
        print("4. Buy an item")
        print("5. More options")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

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
            # Display the updated inventory after update
            display_inventory(inventory)

        elif choice == '3':
            # Get details of an item by name
            get_item_details(inventory)

        elif choice == '4':
            # Buy an item
            buy_item(inventory)
            # Display the updated inventory after purchase
            display_inventory(inventory)

        elif choice == '5':
            # More options
            more_options(inventory)

        elif choice == '6':
            # Save inventory to JSON file before exiting
            File_Operators.save_inventory(inventory)
            print("\nExiting program. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.")

# Only execute main() if this script is run directly
if __name__ == "__main__":
    main()
