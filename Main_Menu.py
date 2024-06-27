import json  # Import the JSON module for reading and writing JSON data
import time  # Import the time module for time-related functions
import matplotlib.pyplot as plt  # Import matplotlib for plotting graphs
from datetime import datetime  # Import datetime module for date and time manipulation
from prettytable import PrettyTable  # Import PrettyTable for displaying tables
import getpass  # Import getpass for secure password input

# Global variables
current_user = None  # Variable to store the current logged-in user
inventory = {}  # Dictionary to hold item data in the inventory
total_sales = 0  # Variable to store the total sales across all items, initialized to 0

# Load inventory from JSON file for the current user
def load_inventory():
    global inventory, total_sales
    try:
        with open('inventory.json', 'r') as file:  # Open the inventory JSON file in read mode
            data = file.read()  # Read the entire contents of the file
            if data:  # Check if data is not empty
                data = json.loads(data)  # Parse the JSON data into a Python dictionary
                user_data = data.get(current_user, {})  # Retrieve the current user's data from JSON
                inventory = user_data.get('inventory', {})  # Retrieve the inventory dictionary for the current user
                total_sales = user_data.get('total_sales', 0)  # Retrieve the total sales for the current user
            else:  # If data is empty (file is empty or doesn't exist)
                inventory = {}  # Initialize an empty inventory dictionary
                total_sales = 0  # Initialize total sales to 0
    except FileNotFoundError:  # Handle the case where the inventory.json file doesn't exist
        inventory = {}  # Initialize an empty inventory dictionary
        total_sales = 0  # Initialize total sales to 0

# Save inventory to JSON file for the current user
def save_inventory():
    try:
        with open('inventory.json', 'r') as file:  # Open the inventory JSON file in read mode
            data = file.read()  # Read the entire contents of the file
            if data:  # Check if data is not empty
                data = json.loads(data)  # Parse the JSON data into a Python dictionary
            else:  # If data is empty (file is empty or doesn't exist)
                data = {}  # Initialize an empty dictionary
    except FileNotFoundError:  # Handle the case where the inventory.json file doesn't exist
        data = {}  # Initialize an empty dictionary

    # Update the data dictionary with current user's inventory and total sales
    data[current_user] = {'inventory': inventory, 'total_sales': total_sales}

    with open('inventory.json', 'w') as file:  # Open the inventory JSON file in write mode
        json.dump(data, file, indent=4)  # Write the updated data dictionary to the JSON file with formatting

# Display the current inventory state and total sales as a table
def display_inventory():
    print("\n📦 Current Inventory and Sales")  # Print a header for inventory and sales
    table = PrettyTable()  # Create a PrettyTable instance for displaying data in tabular format
    table.field_names = ["Name", "Price", "Count", "Sales (Count)", "Sales (Price)"]  # Define table column headers
    
    for name, details in inventory.items():  # Iterate through each item in the inventory dictionary
        sales_count = details.get('sales_count', 0)  # Retrieve 'sales_count' or default to 0 if not found
        sales_price = details.get('sales_price', 0.0)  # Retrieve 'sales_price' or default to 0.0 if not found
        table.add_row([name, details['price'], details['count'], sales_count, sales_price])  # Add a row to the table
    
    print(table)  # Print the PrettyTable containing inventory details
    print(f"💰 Total sales: {total_sales}")  # Print total sales at the end

# Add new item to the inventory
def add_item(name, price, count):
    if name in inventory:  # Check if item already exists in inventory
        print(f"⚠️ Item '{name}' already exists. Use 'update inventory' to modify count.")  # Print warning message
    else:
        # Add new item details to inventory dictionary with initial sales metrics
        inventory[name] = {'price': price, 'count': count, 'sales_count': 0, 'sales_price': 0.0}
        save_inventory()  # Save updated inventory to JSON file
        print(f"✅ Item '{name}' added to inventory.")  # Print success message

# Buy item from the inventory
def buy_item(name, quantity):
    global total_sales  # Access the global total_sales variable
    if name in inventory:  # Check if item exists in inventory
        if inventory[name]['count'] >= quantity:  # Check if sufficient stock is available
            # Update item count, sales count, and total sales
            inventory[name]['count'] -= quantity
            inventory[name]['sales_count'] += quantity
            inventory[name]['sales_price'] += quantity * inventory[name]['price']
            total_sales += quantity * inventory[name]['price']
            save_inventory()  # Save updated inventory to JSON file
            print(f"🛒 Purchased {quantity} of '{name}'.")  # Print purchase confirmation
        else:
            print(f"❌ Insufficient stock for '{name}'.")  # Print insufficient stock message
    else:
        print(f"❌ Item '{name}' not found in inventory.")  # Print item not found message

# Change price of an existing item
def change_price(name, new_price):
    if name in inventory:  # Check if item exists in inventory
        inventory[name]['price'] = new_price  # Update item price
        save_inventory()  # Save updated inventory to JSON file
        print(f"💲 Price of '{name}' updated to {new_price}.")  # Print success message
    else:
        print(f"❌ Item '{name}' not found in inventory.")  # Print item not found message

# Update the count of an item in the inventory
def update_inventory(name, count):
    if name in inventory:  # Check if item exists in inventory
        inventory[name]['count'] = count  # Update item count
        save_inventory()  # Save updated inventory to JSON file
        print(f"🔄 Inventory of '{name}' updated to {count}.")  # Print success message
    else:
        print(f"❌ Item '{name}' not found in inventory.")  # Print item not found message

# Display statistics for a specific item by its name
def detail_by_name(name, period):
    if name in inventory:  # Check if item exists in inventory
        now = datetime.now()  # Get current date and time
        if period == 'day':  # Check if period is 'day'
            print(f"\n📅 Statistics for '{name}' on {now.strftime('%Y-%m-%d')}:")
        elif period == 'month':  # Check if period is 'month'
            print(f"\n📅 Statistics for '{name}' in {now.strftime('%Y-%m')}:")
        elif period == 'year':  # Check if period is 'year'
            print(f"\n📅 Statistics for '{name}' in {now.strftime('%Y')}:")
        # Print item details including price, stock, sales count, and sales price
        print(f"Price: {inventory[name]['price']}, Stock: {inventory[name]['count']}, Sales (Count): {inventory[name]['sales_count']}, Sales (Price): {inventory[name]['sales_price']}")
    else:
        print(f"❌ Item '{name}' not found in inventory.")  # Print item not found message

# Delete an item from the inventory
def delete_item(name):
    if name in inventory:  # Check if item exists in inventory
        del inventory[name]  # Delete item from inventory dictionary
        save_inventory()  # Save updated inventory to JSON file
        print(f"🗑️ Item '{name}' deleted from inventory.")  # Print success message
    else:
        print(f"❌ Item '{name}' not found in inventory.")  # Print item not found message

# Generate graphs based on inventory data
def generate_graph():
    print("\n📊 Graph Generator")  # Print header for graph generator
    print("Data Options:")  # Print options for data selection
    print("1. All product sales")
    print("2. All product stock")
    print("3. All product sales and stock")

    data_option = int(input("Enter data option (1-3): "))  # Prompt user to choose data option
    
    if data_option == 1:  # If user chooses option 1 (All product sales)
        print("\nGraph Types:")  # Print options for graph types
        print("1. Bar Graph")
        print("2. Pie Chart")
        print("3. Histogram")
        graph_option = int(input("Enter graph option (1-3): "))  # Prompt user to choose graph option

        if graph_option == 1:  # If user chooses option 1 (Bar Graph)
            names = list(inventory.keys())  # Get list of item names
            plt.bar(names, [inventory[name]['sales_count'] for name in names])  # Plot bar graph of sales count
            plt.xlabel('Items')  # Set x-axis label
            plt.ylabel('Sales (Count)')  # Set y-axis label
            plt.title('Bar Graph: Sales (Count) of all items')  # Set title of the graph
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
            plt.show()  # Display the graph
        elif graph_option == 2:  # If user chooses option 2 (Pie Chart)
            names = list(inventory.keys())  # Get list of item names
            plt.figure(figsize=(8, 8))  # Set figure size
            plt.pie([inventory[name]['sales_count'] for name in names], labels=names, autopct='%1.1f%%')  # Plot pie chart of sales count
            plt.title('Pie Chart: Sales (Count) Distribution')  # Set title of the graph
            plt.show()  # Display the graph
        elif graph_option == 3:  # If user chooses option 3 (Histogram)
            plt.hist([inventory[name]['sales_count'] for name in inventory.keys()], bins=10)  # Plot histogram of sales count
            plt.xlabel('Sales (Count)')  # Set x-axis label
            plt.ylabel('Frequency')  # Set y-axis label
            plt.title('Histogram: Sales (Count) Distribution')  # Set title of the graph
            plt.show()  # Display the graph
        else:
            print("❌ Invalid option.")  # Print error message for invalid option
        
    elif data_option == 2:  # If user chooses option 2 (All product stock)
        print("\nGraph Types:")  # Print options for graph types
        print("1. Bar Graph")
        graph_option = int(input("Enter graph option (1): "))  # Prompt user to choose graph option

        if graph_option == 1:  # If user chooses option 1 (Bar Graph)
            names = list(inventory.keys())  # Get list of item names
            plt.bar(names, [inventory[name]['count'] for name in names])  # Plot bar graph of item stocks
            plt.xlabel('Items')  # Set x-axis label
            plt.ylabel('Stocks')  # Set y-axis label
            plt.title('Bar Graph: Stocks of all items')  # Set title of the graph
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
            plt.show()  # Display the graph
        else:
            print("❌ Invalid option.")  # Print error message for invalid option

    elif data_option == 3:  # If user chooses option 3 (All product sales and stock)
        print("\nGraph Types:")  # Print options for graph types
        print("1. Bar Graph: Stocks")
        print("2. Bar Graph: Sales (Count)")
        graph_option = int(input("Enter graph option (1-2): "))  # Prompt user to choose graph option

        if graph_option == 1:  # If user chooses option 1 (Bar Graph: Stocks)
            names = list(inventory.keys())  # Get list of item names
            plt.figure(figsize=(10, 5))  # Set figure size
            plt.bar(names, [inventory[name]['count'] for name in names], label='Stocks')  # Plot bar graph of item stocks
            plt.xlabel('Items')  # Set x-axis label
            plt.ylabel('Quantity')  # Set y-axis label
            plt.title('Bar Graph: Stocks of all items')  # Set title of the graph
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
            plt.legend()  # Display legend
            plt.show()  # Display the graph
        elif graph_option == 2:  # If user chooses option 2 (Bar Graph: Sales (Count))
            names = list(inventory.keys())  # Get list of item names
            plt.figure(figsize=(10, 5))  # Set figure size
            plt.bar(names, [inventory[name]['sales_count'] for name in names], label='Sales (Count)')  # Plot bar graph of sales count
            plt.xlabel('Items')  # Set x-axis label
            plt.ylabel('Quantity')  # Set y-axis label
            plt.title('Bar Graph: Sales (Count) of all items')  # Set title of the graph
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
            plt.legend()  # Display legend
            plt.show()  # Display the graph
        else:
            print("❌ Invalid option.")  # Print error message for invalid option

    else:
        print("❌ Invalid option.")  # Print error message for invalid option

# Registration function
def register_user():
    with open('login.json', 'r') as file:  # Open the login JSON file in read mode
        try:
            users = json.load(file)  # Load existing user data from JSON
        except json.JSONDecodeError:  # Handle JSON decoding error
            users = {}  # Initialize empty dictionary if file is empty or not JSON formatted

    username = input("Enter a new username: ")  # Prompt user to enter a new username
    if username in users:  # Check if username already exists in the users dictionary
        print("❌ Username already exists. Try logging in.")  # Print error message if username exists
        return False  # Return False to indicate registration failure

    password = getpass.getpass("Enter a new password: ")  # Prompt user to enter a new password securely
    users[username] = password  # Add new username-password pair to the users dictionary

    with open('login.json', 'w') as file:  # Open the login JSON file in write mode
        json.dump(users, file, indent=4)  # Write updated users dictionary to JSON file with formatting
    
    print("✅ Registration successful. You can now log in.")  # Print success message
    return True  # Return True to indicate registration success

# Login function
def login_user():
    global current_user  # Access the global current_user variable
    with open('login.json', 'r') as file:  # Open the login JSON file in read mode
        try:
            users = json.load(file)  # Load existing user data from JSON
        except json.JSONDecodeError:  # Handle JSON decoding error
            users = {}  # Initialize empty dictionary if file is empty or not JSON formatted

    username = input("Enter username: ")  # Prompt user to enter username
    password = getpass.getpass("Enter password: ")  # Prompt user to enter password securely

    if username in users and users[username] == password:  # Check if username exists and password is correct
        current_user = username  # Set current_user to the logged-in username
        print("✅ Login successful.")  # Print success message
        load_inventory()  # Load inventory data for the logged-in user
        main_menu()  # Display the main menu for further actions
    else:
        print("❌ Invalid username or password. Please try again.")  # Print error message

# Main menu function
def main_menu():
    while True:  # Loop to display menu until user chooses to exit
        print("\n🔑 Main Menu")  # Print main menu header
        print("1. Display Inventory")
        print("2. Add Item")
        print("3. Buy Item")
        print("4. Change Item Price")
        print("5. Update Inventory Count")
        print("6. Item Details")
        print("7. Delete Item")
        print("8. Generate Graph")
        print("9. Save and Logout")
        choice = input("Enter your choice (1-9): ")  # Prompt user to enter choice

        if choice == '1':  # Option to display inventory
            display_inventory()
        elif choice == '2':  # Option to add new item
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            count = int(input("Enter item count: "))
            add_item(name, price, count)
        elif choice == '3':  # Option to buy item
            name = input("Enter item name: ")
            quantity = int(input("Enter quantity to buy: "))
            buy_item(name, quantity)
        elif choice == '4':  # Option to change item price
            name = input("Enter item name: ")
            new_price = float(input("Enter new price: "))
            change_price(name, new_price)
        elif choice == '5':  # Option to update item count
            name = input("Enter item name: ")
            new_count = int(input("Enter new count: "))
            update_inventory(name, new_count)
        elif choice == '6':  # Option to view item details
            name = input("Enter item name: ")
            period = input("Enter period (day/month/year): ")
            detail_by_name(name, period.lower())
        elif choice == '7':  # Option to delete item
            name = input("Enter item name: ")
            delete_item(name)
        elif choice == '8':  # Option to generate graphs
            generate_graph()
        elif choice == '9':  # Option to save and logout
            save_inventory()  # Save current inventory to JSON file
            print("🔒 Logged out.")  # Print logout message
            break  # Exit the loop and end the program
        else:  # Handle invalid menu choices
            print("❌ Invalid choice. Please enter a number from 1 to 9.")

# Entry point of the program
def main():
    while True:  # Loop to handle login and registration until successful
        print("\n🔒 Login or Register")  # Print login or register header
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")  # Prompt user to enter choice

        if choice == '1':  # Option to login
            login_user()  # Call login function
        elif choice == '2':  # Option to register
            if register_user():  # Call register function and check if successful
                login_user()  # If registration successful, proceed to login
        elif choice == '3':  # Option to exit
            print("👋 Goodbye!")  # Print farewell message
            break  # Exit the loop and end the program
        else:  # Handle invalid menu choices
            print("❌ Invalid choice. Please enter a number from 1 to 3.")

if __name__ == "__main__":
    main()  # Start the main function when the script is executed