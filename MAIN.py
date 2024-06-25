#2.Defining Inventory and Sales 📊
#Define the inventory dictionary to hold item data (name, price, count):
Inventory_Dictionary = {
    'Name': ['Apple', 'Banana'],
    'Price': ['1.5$', '0.2$'],
    'Count': ['4', '3']
}
# Printing the dictionary in a clean format
for key, values in Inventory_Dictionary.items():
    print(f"{key}: {', '.join(values)}")
#Initialize total_sales to 0.
Total_Sales = 0
#Completed(Defining Inventory and Sales 📊)