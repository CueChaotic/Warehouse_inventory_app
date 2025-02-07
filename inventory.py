# ======== Importing modules ========

from tabulate import tabulate
from operator import attrgetter

# ======== The beginning of the class ========

class Shoe:
    '''
    The below attributes are initialised for the Shoe class:
    ● country,
    ● code,
    ● product,
    ● cost, and
    ● quantity.
    '''
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def read_file_method(self, code, index_no):
        '''
        Accesses the inventory file and retrieves the desired data at the
        indicated index position, with reference to the code number of the
        stock item.
        '''
        with open ("inventory.txt", "r") as inventory_data:
            data_list = inventory_data.readlines()[1:]
            for line in data_list:
                parts = line.split(", ")
                parts[4] = parts[4].strip()
                if parts[1] == code:
                    return parts[index_no]

    def get_cost(self, code):
        '''
        Method to return the cost of the shoe using the stock code.
        '''
        return self.read_file_method(self, code, 3)

    def get_quantity(self, code):
        '''
        Method to return the quantity of the shoes using the stock code.
        '''
        return self.read_file_method(self, code, 4)

    def __str__(self):
        '''
        Method to return the string representation of the Shoe object.
        '''
        return f'''{self.country},{self.code},{self.product},{self.cost},{self.quantity}'''

# ============= Shoe list ===========

# The list will be used to store a list of objects of shoes.
shoe_list = []

# Dictionary containing relevant countries wherein Nike has stores, for easy
# reference and to reduce the possibility of user input error
country_dict = {1: 'Australia', 2: 'Brazil',3: 'Britain', 4: 'Canada',
                5: 'China', 6: 'Columbia', 7: 'Egypt', 8: 'France', 9: 'India',
                10: 'Israel', 11: 'Morocco', 12: 'Pakistan', 13: 'Russia',
                14: 'South Africa', 15: 'South Korea', 16: 'Uganda',
                17: 'United States', 18: 'Vietnam', 19: 'Zimbabwe'}

# ========== Functions outside the class ==============

def check_function(item, document, index_no):
    '''
    Checks for any instances of the specified ITEM that already exist within
    a file at a specified index position. Compiles a list and appends each
    instance of that item to the list.
    
    If there is at least 1 instance of that ITEM, returns TRUE
    If the list is empty (i.e. no instances of that ITEM found), returns FALSE

    Used to prevent repetitions when unique data input is required.
    '''
    try:   
    # Try-except block for FileNotFoundError exception if there is no file available.
        checklist = []
        with open(document, "r") as document_store:
            lines_list = document_store.readlines()[1:]
        for line in lines_list:
            checklist.append(line.split(",")[index_no])
        if item in checklist:
            return True
        else:
            return False
    except FileNotFoundError:
        return False


def read_shoes_data():
    '''
    Opens the file inventory.txt and reads the data from this file, then
    creates a shoes object with this data and appends this object into the
    shoes list. One line in this file represents data to create one object
    of shoes.
    '''
    try:
    # Try-except block for FileNotFoundError exception if there is no file available.
        with open ("inventory.txt", "r") as inventory_data:
            data_list = inventory_data.readlines()[1:]
            for line in data_list:
                parts = line.split(",")
                parts[4] = parts[4].strip()
                shoe_object = Shoe(parts[0], parts[1], parts[2], int(parts[3]), int(parts[4]))
                shoe_list.append(shoe_object)
    except FileNotFoundError: # If the file is not found, the user is informed in the menu.
        print('''
No inventory data available.''')


def update_shoes_data():
    '''
    Function to update the inventory.txt file with the new data entered by the user.
    '''
    with open('inventory.txt', 'w') as file:
        file.write("Country,Code,Product,Cost,Quantity\n")
        for item in shoe_list:
            file.write(f"{item.country},{item.code},{item.product},{item.cost},{item.quantity}\n")


def capture_shoes():
    '''
    Allows a user to capture data about a shoe, create a shoe object with this
    data and append this object inside the shoe list.
    '''
    while True:
    # a predetermined list of countries is displayed for the user to select from,
    # to reduce the possibility of user input error
        print('''
    Please enter the below information as prompted
_________________________________________________________________________________''')
        enter_country = input('''
    Select the number of the country below:
     1: Australia        2: Brazil           3: Britain 
     4: Canada           5: China            6: Columbia
     7: Egypt            8: France           9: India
    10: Israel          11: Morocco         12: Pakistan
    13: Russia          14: South Africa    15: South Korea
    16: Uganda          17: United States   18: Vietnam
    19: Zimbabwe
        
    Go back ("e")
    
    Selection: ''')
        
        if enter_country == "e": # Takes user back to main menu
            break

        else:
            # Validation check to ensure correct entry of a valid, numerical digit
            while enter_country.isnumeric() == False or int(enter_country) not in country_dict:
                enter_country = input('''
    Invalid input. Please enter the digit of the country to select
            
    Selection: ''')
            country_selection = country_dict[int(enter_country)]
            print(f'''
    Selected: {country_selection}''')

            enter_code = input('''
    Enter the 5-digit code: SKU-''')
            # Validation check to prevent use of anything other than numbers, from 0 upwards.
            while enter_code.isnumeric() == False or len(enter_code) != 5:  
                enter_code = input('''                                      
    You must enter a 5-digit code. Please re-enter the code:
    SKU-''')
            # Calling check function to ensure new code entered is unique.
            while check_function((f"SKU{enter_code}"), "inventory.txt", 1) == True:
                enter_code = input('''
    This code is already in use. Please re-enter a unique code below:
    SKU-''')
            
            enter_product = input('''
    Enter the product name: ''')
            
            enter_cost = input('''
    Enter the cost: ZAR ''')
            while enter_cost.isnumeric() == False:
                enter_cost = input('''
    You may only use digits. Please re-enter the cost:
    ZAR ''')
            
            enter_quantity = input('''
    Enter the quantity: ''')
            while enter_quantity.isnumeric() == False:
                enter_quantity = input('''
    You may only use digits. Please re-enter the quantity:
    ''')
            # The new shoe object is added to the inventory file.
            # Important to note that the cost and quantity are converted to integers.
            new_shoe_object = Shoe(country_selection,f"SKU{enter_code}", enter_product, int(enter_cost), int(enter_quantity))
            shoe_list.append(new_shoe_object)
            shoe_value = new_shoe_object.cost * new_shoe_object.quantity
           
            # The user is then given a summary of the new shoe added on the console.
            print(f'''
_________________________________________________________________________________
----- NEW SHOE ADDED -----  
            
    Country:    {new_shoe_object.country}
    Code:       {new_shoe_object.code}
    Product:    {new_shoe_object.product}
    Cost:       ZAR {float(new_shoe_object.cost):.2f}
    Quantity:   {new_shoe_object.quantity}
    Value:      ZAR {float(shoe_value):.2f}
_________________________________________________________________________________''')
            update_shoes_data() # The inventory file is updated with the new data.
        
        # The user is given the option to add another shoe, or return to the main menu.
        last_option = input('''
    Add a new shoe?
    Yes ("y")
    No  ("n")
    
    ''').lower()
        if last_option == "y":
            continue
        elif last_option == "n":
            break
        else:
            while last_option != "y" and last_option != "n":
                last_option = input('''
    Invalid input. Please select an option from above.
    ''').lower()
            if last_option == "y":
                continue
            elif last_option == "n":
                break


def view_all():
    '''
    Iterates over the shoes list and prints the details of the shoes returned
    from the __str__ function into an readable list.

    The tabulate module is then used to display the data in a table format
    for much better readability.
    '''
    while True:
        updated_shoe_list = []
        for item in shoe_list:
            str_item = item.__str__()
            split_item = str_item.split(",")
            updated_shoe_list.append(split_item)
        updated_shoe_list.sort()
        data_table = ["Country", "Code", "Product", "Cost", "Quantity"]
        updated_shoe_list.insert(0, data_table)
        print('''
_________________________________________________________________________________
----- SHOE STOCK -----
''')
        print(tabulate(updated_shoe_list, headers = 'firstrow', tablefmt = 'grid')) # The data is displayed using the tabulate module.
        print('''
_________________________________________________________________________________''')

        # The user is given the option to return to the main menu.           
        last_option = input('''   
    Go back ("e")
    ''').lower()
        if last_option == "e":
            break
        else:
            while last_option != "e":
                last_option = input('''
    Invalid input. Please select an option from above.
    ''').lower()
            break
                
    # NOTE: Assistance with the use of the TABULATE module was taken from the
    # AskPython website:
    # https://www.askpython.com/python-modules/tabulate-tables-in-python


def re_stock():
    '''
    Will find the shoe object with the lowest quantity, which is the shoe
    that needs to be re-stocked.
        
    Asks the user if they want to add any amount to this quantity of shoes and
    then updates it on the file.
    '''
    while True:
        
        # Lowest stock quantity is found using the min function and the attrgetter module.
        lowest_stock = min(shoe_list, key = attrgetter ("quantity"))
        print(f'''
_________________________________________________________________________________
----- LOWEST STOCK QUANTITY -----
        
    Country:    {lowest_stock.country}
    Code:       {lowest_stock.code}
    Product:    {lowest_stock.product}
    Cost:       ZAR {float(lowest_stock.cost):.2f}
    Quantity:   {lowest_stock.quantity}
    Value:      ZAR {float(lowest_stock.cost * lowest_stock.quantity):.2f}
_________________________________________________________________________________''')
        
        # The user is asked if they would like to order more of this stock.
        # with alphanumeric checks to ensure the user inputs a valid response.
        re_stock_query = input('''
    Would you like to order more of this stock?
    YES  ("y")
    NO   ("n") ------> Back to Main Menu
    ''').lower()
        while re_stock_query.isalpha() == False:
            re_stock_query = input('''
    Invalid. Please select an option from above:
    ''').lower()
        if re_stock_query == "y":
            order_entry = input('''
    Enter the quantity you'd like to order:
    ''')
            while order_entry.isnumeric() == False:
                order_entry = input('''
    Invalid. Please input digits only:
    ''')
            order_entry = int(order_entry)
            lowest_stock.quantity += order_entry # The quantity of the shoe is updated with the new order.
            print(f'''
_________________________________________________________________________________
----- UPDATED STOCK QUANTITY -----
        
    Country:    {lowest_stock.country}
    Code:       {lowest_stock.code}
    Product:    {lowest_stock.product}
    Cost:       ZAR {float(lowest_stock.cost):.2f}
    Quantity:   {lowest_stock.quantity}
    Value:      ZAR {float(lowest_stock.cost * lowest_stock.quantity):.2f}
_________________________________________________________________________________''')
            update_shoes_data() # The inventory file is updated with the new data.
        elif re_stock_query == "n":
            break
        else:
            while re_stock_query != "y" and re_stock_query != "n":
                re_stock_query = input('''
    Invalid. Please input a response as indicated
    ''')
            if re_stock_query == "y":
                continue
            elif re_stock_query == "n":
                break
        
        # The user is given the option to re-stock another shoe.
        last_option = input('''     
    Check new lowest quantity?
    Yes ("y")
    No  ("n") ------> Back to Main Menu
    
    ''').lower()
        if last_option == "y":
            continue
        elif last_option == "n":
            break
        else:
            while last_option != "y" and last_option != "n":
                last_option = input('''
    Invalid input. Please select an option from above.
    ''').lower()
            if last_option == "y":
                continue
            elif last_option == "n":
                break
            
    # NOTE: The idea for the "attrgetter" module was obtained from user
    # mechanical_meat from StackOverflow:
    # https://stackoverflow.com/questions/6085467/python-min-function-with-a-list-of-objects
    # This was used to develop a quick way to access the minimum quantity
    # attribute from a Shoe object in a list.


def search_shoe():
    '''
    Will search for a shoe from the list using the shoe code and return the
    object so that it will be printed.
    '''
    while True:
        search_query = input('''
    Please enter the code of the shoe you're looking for:
    SKU-''')
        while search_query.isnumeric() == False or len(search_query) != 5:
            search_query = input('''
    Invalid. Please input 5 digits only:
    SKU-''')
        checklist = []   # A checklist is created to store an instance of the code if found.
        for item in shoe_list:
            if item.code == f"SKU{search_query}":
                checklist.append(item.code)
        # On finding the code, the user is given the information of the shoe they searched for.
                print(f'''
_________________________________________________________________________________
----- SHOE SEARCH -----
            
    Country:    {item.country}
    Code:       {item.code}
    Product:    {item.product}
    Cost:       ZAR {float(item.cost):.2f}
    Quantity:   {item.quantity}
    Value:      ZAR {float(item.cost * item.quantity):.2f}
_________________________________________________________________________________''')
        if checklist == []:  # If the code is not found, the list is empty and the user is informed.
            print('''
_________________________________________________________________________________
----- SHOE SEARCH -----

    NO DATA FOUND FOR THAT CODE.
_________________________________________________________________________________''')

        # The user is given the option to go back to the main menu.
        last_option = input('''
    Go back ("e")
    ''').lower()
        if last_option == "e":
            break
        else:
            while last_option != "e":
                last_option = input('''
    Invalid input. Please select an option from above.
    ''').lower()
            break


def value_per_item():
    '''
    Will calculate the total value for each item and print this information on
    the console in a table for all of the shoes.
    '''
    while True:
        updated_shoe_list = []
        for item in shoe_list:
            value =  item.cost * item.quantity  # A value is calculated for each item 
            str_item = item.__str__()           # and added as another element to the list
            str_item = str_item + f",{value}"
            split_item = str_item.split(",")
            updated_shoe_list.append(split_item)
        updated_shoe_list.sort()
        # An addition is made to the data table to include the value of each item.
        data_table = ["Country", "Code", "Product", "Cost", "Quantity", "Value"]
        updated_shoe_list.insert(0, data_table)
        print('''
_________________________________________________________________________________
----- SHOE STOCK VALUES -----
''')
        print(tabulate(updated_shoe_list, headers = 'firstrow', tablefmt = 'grid'))

        print('''
_________________________________________________________________________________''')
        last_option = input('''
    Go back ("e")
    ''').lower()
        if last_option == "e":
            break
        else:
            while last_option != "e":
                last_option = input('''
    Invalid input. Please select an option from above.
    ''').lower()
            break


def highest_qty():
    '''
    Displays the product with the highest quantity and prints a sale
    recommendation
    '''
    while True:
        highest_stock = max(shoe_list, key = attrgetter ("quantity"))
        
        # shoe object with the highest quantity is displayed on the console. 
        print(f'''
_________________________________________________________________________________
----- HIGHEST STOCK QUANTITY -----
        
    Country:    {highest_stock.country}
    Code:       {highest_stock.code}
    Product:    {highest_stock.product}
    Cost:       ZAR {float(highest_stock.cost):.2f}
    Quantity:   {highest_stock.quantity}
    Value:      ZAR {float(highest_stock.cost * highest_stock.quantity):.2f}

    RECOMMEND SALE!
_________________________________________________________________________________''')
        last_option = input('''
    Go back ("e")
    ''').lower()
        if last_option == "e":
            break
        else:
            while last_option != "e":
                last_option = input('''
    Invalid input. Please select an option from above.
    ''').lower()
            break

#========== Main Menu =============

while True:
    shoe_list = []
    read_shoes_data() # Shoe_list set to empty and populated with updated data.
    menu_selection = input('''
====== SHOE WIZZ ======
_________________________________________________________________________________
    PLEASE SELECT AN OPTION BELOW:
    1. Capture shoe data        (Enter "1")
    2. View all shoe data       (Enter "2")
    3. Re-stock                 (Enter "3")
    4. Search shoes             (Enter "4")
    5. Search values            (Enter "5")
    6. Highest quantity stock   (Enter "6")
    
    Exit ("e")
_________________________________________________________________________________

    ''').lower()

    # The user is given the option to select from the menu, with the option to exit.
    # Each menu item calls the relevant function to execute the desired task.
    
    if menu_selection == "1":
        capture_shoes()     

    elif menu_selection =="2":
        view_all()

    elif menu_selection =="3":
        re_stock()

    elif menu_selection =="4":
        search_shoe()
        
    elif menu_selection =="5":
        value_per_item()

    elif menu_selection =="6":
        highest_qty()

    elif menu_selection =="e":
        exit() # this function will exit the program

    else:
        print('''
    Please select a valid option from the menu.''')

# VOILA ===THE END===