import json  # Import the JSON module to work with JSON data.
import time  # Import the time module to handle time-related tasks.
import matplotlib.pyplot as plt  # Import Matplotlib's pyplot module to create graphs.
from datetime import datetime  # Import datetime class from the datetime module to handle date and time.
from prettytable import PrettyTable  # Import PrettyTable to display data in table format.
import getpass  # Import getpass to handle secure password input.

# Global variables
current_user = None  # Initialize current_user to None to keep track of the logged-in user.
inventory = {}  # Inventory dictionary to hold item data.
total_sales = 0  # Initialize total_sales to 0.

# Load inventory from JSON file for the current user
def load_inventory():
    global inventory, total_sales  # Access the global variables inventory and total_sales.
    try:
        with open('inventory.json', 'r') as file:  # Open 'inventory.json' file in read mode.
            data = file.read()  # Read the contents of the file.
            if data:  # Check if data exists (file is not empty).
                data = json.loads(data)  # Parse JSON data into a Python dictionary.
                user_data = data.get(current_user, {})  # Retrieve current user's data from JSON.
                inventory = user_data.get('inventory', {})  # Retrieve inventory data for the current user.
                total_sales = user_data.get('total_sales', 0)  # Retrieve total sales for the current user.
            else:  # If file is empty or data is None.
                inventory = {}  # Set inventory to an empty dictionary.
                total_sales = 0  # Set total_sales to 0.
    except FileNotFoundError:  # Handle exception if 'inventory.json' file is not found.
        inventory = {}  # Set inventory to an empty dictionary.
        total_sales = 0  # Set total_sales to 0.

# Save inventory to JSON file for the current user
def save_inventory():
    try:
        with open('inventory.json', 'r') as file:  # Open 'inventory.json' file in read mode.
            data = file.read()  # Read the contents of the file.
            if data:  # Check if data exists (file is not empty).
                data = json.loads(data)  # Parse JSON data into a Python dictionary.
            else:  # If file is empty or data is None.
                data = {}  # Set data to an empty dictionary.
    except FileNotFoundError:  # Handle exception if 'inventory.json' file is not found.
        data = {}  # Set data to an empty dictionary.

    data[current_user] = {'inventory': inventory, 'total_sales': total_sales}  # Update data with current user's inventory and total sales.

    with open('inventory.json', 'w') as file:  # Open 'inventory.json' file in write mode.
        json.dump(data, file, indent=4)  # Write JSON data to file with indentation for readability.

# Display the current inventory state and total sales as a table
def display_inventory():
    print("\n📦 Current Inventory and Sales")  # Print a message indicating the display of inventory and sales.
    table = PrettyTable()  # Create an instance of PrettyTable to display tabular data.
    table.field_names = ["Name", "Price", "Count", "Sales (Count)", "Sales (Price)"]  # Set column headers for the table.

    for name, details in inventory.items():  # Iterate through items in the inventory dictionary.
        sales_count = details.get('sales_count', 0)  # Retrieve 'sales_count' from details dictionary or default to 0 if not found.
        sales_price = details.get('sales_price', 0.0)  # Retrieve 'sales_price' from details dictionary or default to 0.0 if not found.
        table.add_row([name, details['price'], details['count'], sales_count, sales_price])  # Add a row to the table with item details.

    print(table)  # Print the PrettyTable displaying current inventory and sales.
    print(f"💰 Total sales: {total_sales}")  # Print total sales amount.

# Add new item to the inventory
def add_item(name, price, count):
    if name in inventory:  # Check if the item already exists in the inventory.
        print(f"⚠️ Item '{name}' already exists. Use 'update inventory' to modify count.")  # Print a message indicating item already exists.
    else:
        inventory[name] = {'price': price, 'count': count, 'sales_count': 0, 'sales_price': 0.0}  # Add new item with its details to the inventory dictionary.
        save_inventory()  # Save the updated inventory to 'inventory.json'.
        print(f"✅ Item '{name}' added to inventory.")  # Print a message indicating successful addition of the item.

# Buy item from the inventory
def buy_item(name, quantity):
    global total_sales  # Access the global variable total_sales.
    if name in inventory:  # Check if the item exists in the inventory.
        if inventory[name]['count'] >= quantity:  # Check if there is enough stock of the item.
            inventory[name]['count'] -= quantity  # Decrease the item count by the purchased quantity.
            inventory[name]['sales_count'] += quantity  # Increase the sales count of the item.
            inventory[name]['sales_price'] += quantity * inventory[name]['price']  # Increase the sales price by the purchased quantity times the item price.
            total_sales += quantity * inventory[name]['price']  # Increase the total sales by the purchased quantity times the item price.
            save_inventory()  # Save the updated inventory to 'inventory.json'.
            print(f"🛒 Purchased {quantity} of '{name}'.")  # Print a message indicating successful purchase of the item.
        else:
            print(f"❌ Insufficient stock for '{name}'.")  # Print a message indicating insufficient stock of the item.
    else:
        print(f"❌ Item '{name}' not found in inventory.")  # Print a message indicating item not found in the inventory.

# Change price of an existing item
def change_price(name, new_price):
    if name in inventory:  # Check if the item exists in the inventory.
        inventory[name]['price'] = new_price  # Update the price of the item.
        save_inventory()  # Save the updated inventory to 'inventory.json'.
        print(f"💲 Price of '{name}' updated to {new_price}.")  # Print a message indicating successful price change of the item.
    else:
        print(f"❌ Item '{name}' not found in inventory.")  # Print a message indicating item not found in the inventory.

# Update the count of an item in the inventory
def update_inventory(name, count):
    if name in inventory:  # Check if the item exists in the inventory.
        inventory[name]['count'] = count  # Update the count of the item.
        save_inventory()  # Save the updated inventory to 'inventory.json'.
        print(f"🔄 Inventory of '{name}' updated to {count}.")  # Print a message indicating successful update of the item count.
    else:
        print(f"❌ Item '{name}' not found in inventory.")  # Print a message indicating item not found in the inventory.

# Display statistics for a specific item by its name
def detail_by_name(name, period):
    if name in inventory:  # Check if the item exists in the inventory.
        now = datetime.now()  # Get the current date and time.
        if period == 'day':  # Check if the period is 'day'.
            print(f"\n📅 Statistics for '{name}' on {now.strftime('%Y-%m-%d')}:")  # Print statistics for the item on the current day.
        elif period == 'month':  # Check if the period is 'month'.
            print(f"\n📅 Statistics for '{name}' in {now.strftime('%Y-%m')}:")  # Print statistics for the item in the current month.
        elif period == 'year':  # Check if the period is 'year'.
            print(f"\n📅 Statistics for '{name}' in {now.strftime('%Y')}:")  # Print statistics for the item in the current year.
        print(f"Price: {inventory[name]['price']}, Stock: {inventory[name]['count']}, Sales (Count): {inventory[name]['sales_count']}, Sales (Price): {inventory[name]['sales_price']}")  # Print detailed statistics for the item.
    else:
        print(f"❌ Item '{name}' not found in inventory.")  # Print a message indicating item not found in the inventory.

# Delete an item from the inventory
def delete_item(name):
    if name in inventory:  # Check if the item exists in the inventory.
        del inventory[name]  # Delete the item from the inventory.
        save_inventory()  # Save the updated inventory to 'inventory.json'.
        print(f"🗑️ Item '{name}' deleted from inventory.")  # Print a message indicating successful deletion of the item.
    else:
        print(f"❌ Item '{name}' not found in inventory.")  # Print a message indicating item not found in the inventory.

# Generate graphs based on inventory data
def generate_graph():
    print("\n📊 Graph Generator")  # Print a message indicating the start of graph generation.
    print("Data Options:")  # Print available data options for graph generation.
    print("1. All product sales")
    print("2. All product stock")
    print("3. All product sales and stock")

    data_option = int(input("Enter data option (1-3): "))  # Prompt user to choose a data option (1-3).

    if data_option == 1:  # If user chooses data option 1.
        print("\nGraph Types:")  # Print available graph types for sales data.
        print("1. Bar Graph")
        print("2. Pie Chart")
        print("3. Histogram")
        graph_option = int(input("Enter graph option (1-3): "))  # Prompt user to choose a graph option (1-3).

        if graph_option == 1:  # If user chooses graph option 1.
            names = list(inventory.keys())  # Get a list of item names from the inventory.
            plt.bar(names, [inventory[name]['sales_count'] for name in names])  # Create a bar graph of sales count for each item.
            plt.xlabel('Items')  # Set the label for the x-axis.
            plt.ylabel('Sales (Count)')  # Set the label for the y-axis.
            plt.title('Bar Graph: Sales (Count) of all items')  # Set the title of the graph.
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability.
            plt.show()  # Display the bar graph.
        elif graph_option == 2:  # If user chooses graph option 2.
            names = list(inventory.keys())  # Get a list of item names from the inventory.
            plt.figure(figsize=(8, 8))  # Set the figure size for the pie chart.
            plt.pie([inventory[name]['sales_count'] for name in names], labels=names, autopct='%1.1f%%')  # Create a pie chart of sales count distribution.
            plt.title('Pie Chart: Sales (Count) Distribution')  # Set the title of the pie chart.
            plt.show()  # Display the pie chart.
        elif graph_option == 3:  # If user chooses graph option 3.
            plt.hist([inventory[name]['sales_count'] for name in inventory.keys()], bins=10)  # Create a histogram of sales count distribution.
            plt.xlabel('Sales (Count)')  # Set the label for the x-axis.
            plt.ylabel('Frequency')  # Set the label for the y-axis.
            plt.title('Histogram: Sales (Count) Distribution')  # Set the title of the histogram.
            plt.show()  # Display the histogram.
        else:  # If user enters an invalid graph option.
            print("❌ Invalid option.")  # Print a message indicating invalid option.
    
    elif data_option == 2:  # If user chooses data option 2.
        print("\nGraph Types:")  # Print available graph types for stock data.
        print("1. Bar Graph")
        graph_option = int(input("Enter graph option (1): "))  # Prompt user to choose a graph option (1).

        if graph_option == 1:  # If user chooses graph option 1.
            names = list(inventory.keys())  # Get a list of item names from the inventory.
            plt.bar(names, [inventory[name]['count'] for name in names])  # Create a bar graph of item stock for each item.
            plt.xlabel('Items')  # Set the label for the x-axis.
            plt.ylabel('Stocks')  # Set the label for the y-axis.
            plt.title('Bar Graph: Stocks of all items')  # Set the title of the graph.
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability.
            plt.show()  # Display the bar graph.
        else:  # If user enters an invalid graph option.
            print("❌ Invalid option.")  # Print a message indicating invalid option.

    elif data_option == 3:  # If user chooses data option 3.
        print("\nGraph Types:")  # Print available graph types for combined data.
        print("1. Bar Graph: Stocks")
        print("2. Bar Graph: Sales (Count)")
        graph_option = int(input("Enter graph option (1-2): "))  # Prompt user to choose a graph option (1-2).

        if graph_option == 1:  # If user chooses graph option 1.
            names = list(inventory.keys())  # Get a list of item names from the inventory.
            plt.figure(figsize=(10, 5))  # Set the figure size for the bar graph.
            plt.bar(names, [inventory[name]['count'] for name in names], label='Stocks')  # Create a bar graph of item stocks.
            plt.xlabel('Items')  # Set the label for the x-axis.
            plt.ylabel('Quantity')  # Set the label for the y-axis.
            plt.title('Bar Graph: Stocks of all items')  # Set the title of the graph.
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability.
            plt.legend()  # Display legend for the graph.
            plt.show()  # Display the bar graph.
        elif graph_option == 2:  # If user chooses graph option 2.
            names = list(inventory.keys())  # Get a list of item names from the inventory.
            plt.figure(figsize=(10, 5))  # Set the figure size for the bar graph.
            plt.bar(names, [inventory[name]['sales_count'] for name in names], label='Sales (Count)')  # Create a bar graph of item sales count.
            plt.xlabel('Items')  # Set the label for the x-axis.
            plt.ylabel('Quantity')  # Set the label for the y-axis.
            plt.title('Bar Graph: Sales (Count) of all items')  # Set the title of the graph.
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability.
            plt.legend()  # Display legend for the graph.
            plt.show()  # Display the bar graph.
        else:  # If user enters an invalid graph option.
            print("❌ Invalid option.")  # Print a message indicating invalid option.

    else:  # If user enters an invalid data option.
        print("❌ Invalid option.")  # Print a message indicating invalid option.

# Registration function
def register_user():
    with open('login.json', 'r') as file:  # Open 'login.json' file in read mode.
        try:
            users = json.load(file)  # Load existing user data from 'login.json'.
        except json.JSONDecodeError:  # Handle JSON decode error.
            users = {}  # If file is empty or not valid JSON, initialize users dictionary.

    username = input("Enter a new username: ")  # Prompt user to enter a new username.
    if username in users:  # Check if the entered username already exists.
        print("❌ Username already exists. Try logging in.")  # Print a message indicating username already exists.
        return False  # Return False to indicate registration failure.

    password = getpass.getpass("Enter a new password: ")  # Prompt user to enter a new password securely.
    users[username] = password  # Add new username and password to the users dictionary.

    with open('login.json', 'w') as file:  # Open 'login.json' file in write mode.
        json.dump(users, file, indent=4)  # Write updated user data to 'login.json' with indentation for readability.
    
    print("✅ Registration successful. You can now log in.")  # Print a message indicating successful registration.
    return True  # Return True to indicate registration success.

# Login function
def login_user():
    global current_user  # Access the global variable current_user.
    with open('login.json', 'r') as file:  # Open 'login.json' file in read mode.
        try:
            users = json.load(file)  # Load existing user data from 'login.json'.
        except json.JSONDecodeError:  # Handle JSON decode error.
            users = {}  # If file is empty or not valid JSON, initialize users dictionary.

    username = input("Enter username: ")  # Prompt user to enter username.
    password = getpass.getpass("Enter password: ")  # Prompt user to enter password securely.

    if username in users and users[username] == password:  # Check if username exists and password matches.
        current_user = username  # Set current_user to the logged-in username.
        print("✅ Login successful.")  # Print a message indicating successful login.
        return True  # Return True to indicate login success.
    else:  # If username doesn't exist or password doesn't match.
        print("❌ Invalid credentials. Please try again.")  # Print a message indicating invalid credentials.
        return False  # Return False to indicate login failure.

def main():
    while True:  # Start an indefinite loop for the main program.
        print("\n🔑 Login Menu")  # Print the login menu header.
        print("1. Login")  # Print option for logging in.
        print("2. Register")  # Print option for registering a new user.
        print("3. Exit")  # Print option for exiting the program.
        choice = input("Enter your choice (1-3): ")  # Prompt user to enter their choice (1-3).

        if choice == '1':  # If user chooses option 1 (Login).
            if login_user():  # Call login_user() function to attempt login.
                break  # Exit the login loop if login is successful.
        elif choice == '2':  # If user chooses option 2 (Register).
            if register_user():  # Call register_user() function to attempt registration.
                continue  # Continue to the next iteration of the loop after successful registration.
        elif choice == '3':  # If user chooses option 3 (Exit).
            print("👋 Exiting program. Goodbye!")  # Print a goodbye message.
            break  # Exit the program loop to end the program.
        else:  # If user enters an invalid choice.
            print("❌ Invalid choice. Please enter a valid option (1-3).")  # Print a message indicating invalid choice.

if __name__ == "__main__":
    main()  # Call the main() function to start the program.
