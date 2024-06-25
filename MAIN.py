def main():
    # Print a welcome message
    print("\nWelcome to the Inventory Management System!\n")

    # Define the inventory dictionary to hold item data (name, price, count)
    inventory = {
        'Name': ['Ali', 'Wajhat'],
        'Price': ['1$', '2$'],
        'Count': ['4', '3']
    }

    # Initialize total_sales to 0
    total_sales = 0

    # Display the initial inventory
    print("Initial Inventory:")
    for key, values in inventory.items():
        print(f"{key}: {', '.join(values)}")

    # Additional code for program functionality can be added here

if __name__ == "__main__":
    main()
#Completed(Creating the Main Function 🎯)
