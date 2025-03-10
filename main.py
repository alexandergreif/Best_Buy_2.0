import sys
from products import Product, NonStockedProduct, LimitedProduct
from store import Store
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree


def quit_program():
    """
    Exit the application and print a goodbye message.
    """
    print("Exiting the shop. Goodbye")
    sys.exit()


def list_all_products(store_object):
    """
    Display a numbered list of all active products in the store.

    Args:
        store_object (Store): The store instance containing products.
    """
    all_products = store_object.get_all_products()
    print("------")
    for idx, product in enumerate(all_products, start=1):
        print(f"{idx}. {product.show()}")
    print("-----")


def get_all_quantity(store_object):
    """
    Display the total quantity of all products available in the store.

    Args:
        store_object (Store): The store instance containing products.
    """
    total_quantity = store_object.get_total_quantity()
    print("------")
    print(f"The total quantity is {total_quantity}")
    print("------")


def wrap_order(store_object):
    """
    Handle the interactive process for placing an order:
    - Display all active products.
    - Prompt user for product selection and quantity.
    - Build a shopping list and process the order.

    Args:
        store_object (Store): The store instance to order products from.
    """
    all_products = store_object.get_all_products()
    for idx, product in enumerate(all_products, start=1):
        print(f"{idx}. {product.show()}")

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
        print("Product added to shopping list!")
        print("-------")

    if shopping_list:
        try:
            total_price = store_object.order(shopping_list)
            print("--------")
            print(f"Order placed. Total price is {total_price}€")
            print("--------")
        except ValueError as error:
            print(f"Order failed: {error}")
    else:
        print("No products selected, returning to menu.")


def start(store_object):
    """
    Launch the interactive command-line interface for the store.

    Args:
        store_object (Store): The store instance to interact with.
    """
    funct_dict = {
        "1": lambda: list_all_products(store_object),
        "2": lambda: get_all_quantity(store_object),
        "3": lambda: wrap_order(store_object),
        "4": quit_program
    }

    while True:
        print("\n      Store Menu      ")
        print("1: List all products in store")
        print("2: Show total amount in store")
        print("3: Make an order")
        print("4: Exit")
        user_input = input("Please enter a number of your choice: ")

        if user_input not in funct_dict:
            print("Wrong input. Please choose one of the menu options.\n")
            continue
        else:
            funct_dict[user_input]()


def main():
    """
    Set up the store with sample products and promotions, then start the CLI.
    """
    # Create a sample product list with various product types.
    product_list = [
        Product("MacBook Air M2", 1450, 100),
        Product("Bose QuietComfort Earbuds", 250, 500),
        Product("Google Pixel 7", 500, 250),
        NonStockedProduct("Unlimited Warranty", 100),
        LimitedProduct("Exclusive Sneakers", 150, 50, maximum=2)
    ]

    # Assign sample promotions to specific products.
    product_list[0].promotion = PercentDiscount(30)  # 30% off for the MacBook Air M2
    product_list[1].promotion = SecondHalfPrice()  # Second item half price for Bose Earbuds
    product_list[2].promotion = ThirdOneFree()  # Buy 2, get 1 free for Google Pixel 7

    store = Store(product_list)
    start(store)


if __name__ == "__main__":
    main()
