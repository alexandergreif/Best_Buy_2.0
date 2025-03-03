import sys
from products import Product
from store import Store


def quit_program():
    """
    Exit the shop and terminate the program.

    This function prints a goodbye message and then calls sys.exit() to stop execution.
    """
    print("Exiting the shop. Goodbye")
    sys.exit()

def start(store_object):
    """
    Starts the store and initiates the store object. Launches the cli menu

    This function prints the menu and waits for user input.

    The function loops until user chooses to exit
    """
    funct_dict = {
        "1": list_all_products,
        "2": get_all_quantity,
        "3": wrap_order,
        "4": quit_program
    }

    while True:
        print("      Store Menu      ")
        print("1: List all products in store")
        print("2: Show total amount in store")
        print("3: Make an order")
        print("4: exit ")
        user_input = input("Please enter a number of your choice: ")

        if user_input not in funct_dict:
            print("Wrong input. Please choose one of the menu options.")

        if user_input == "1":
            funct_dict[user_input](store_object)
        elif user_input == "2":
            funct_dict[user_input](store_object)
        elif user_input == "3":
            funct_dict[user_input](store_object)
        elif user_input == "4":
            funct_dict[user_input]()

def get_all_quantity(store_object):
    """
    Calculate and return the total quantity of items in the store.

    This method iterates through all products in the store's inventory and sums up their
    individual quantities.

    Returns:
        int: The total number of items available across all products.
    """
    all_quantity = store_object.get_total_quantity()
    print("------")
    print(f"The total quantity is {all_quantity}")
    print("------")


def list_all_products(store_object):
    """
    Print all active products in the store.

    Parameters:
        store_object (Store): The store instance containing products.

    The function retrieves active products using store_object.get_all_products()
    and prints each product's details.
    """
    all_products = store_object.get_all_products()
    print("------")
    for idx, product in enumerate(all_products, start=1):
        print(f"{idx}. {product.name}, Price: {product.price}, Quantity: {product.quantity}")
    print("-----")

def wrap_order(store_object):
    """
        Handle user interaction for placing an order.

        Parameters:
            store_object (Store): The store instance from which products will be ordered.

        This function:
          - Displays all active products.
          - Prompts the user to select products and enter desired quantities.
          - Builds a shopping list (a list of tuples (Product, quantity)).
          - Calls store_object.order() with the shopping list and prints the total price.
          - Catches and prints errors if the order fails.
    """
    all_products = store_object.get_all_products()
    for idx, product in enumerate(all_products, start=1):
        print(f"{idx}. {product.name}, Price: {product.price}, Quantity: {product.quantity}")

    shopping_list = []
    while True:
        user_choice = input("Which product do you want to buy? (Enter empty to finish): ")
        if not user_choice:
            break

        try:
            product_idx = int(user_choice) - 1
            chosen_product = all_products[product_idx]
        except (ValueError, IndexError):
            print("Invalid Product choice. Please try again")
            continue

        quantity_str = input("Enter the amount: ")
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a positive quantity. Please try again")
            continue

        shopping_list.append((chosen_product, quantity))
        print("-------")
        print("Products added to list!!!!")
        print("-------")

    if shopping_list:
        try:
            total_price = store_object.order(shopping_list)
            print("--------")
            print(f"Order is placed. Total price is {total_price}€")
            print("--------")
        except ValueError as error:
            print(f"Order failed: {error}")
    else:
        print("No products selected, returning to menu.")




def main():

    #default product list
    product_list = [
        Product("MacBook Air M2", 1450, 100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250)
    ]

    best_buy = Store(product_list)
    # products = best_buy.get_all_products()
    # print(best_buy.get_total_quantity())
    # shopping_list = [(products[0], 1), (products[1], 2)]
    # print(type(shopping_list[0]))
    # print(best_buy.order(shopping_list))
    start(best_buy)

if __name__ == "__main__":
    main()

