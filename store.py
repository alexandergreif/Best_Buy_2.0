from products import Product

class Store:
    """
    Manages a collection of products in the store.
    """
    def __init__(self, list_of_products: list):
        """
        Initialize the store with a list of products.

        Args:
            list_of_products (list): A list containing Product instances.

        Raises:
            TypeError: If list_of_products is not a list or if items are not valid Product instances.
        """
        if not isinstance(list_of_products, list):
            raise TypeError("list_of_products must be a list.")
        for item in list_of_products:
            if not hasattr(item, "buy"):
                raise TypeError("All items must be product instances.")
        self.list_of_products = list_of_products

    def add_product(self, product):
        """
        Add a product to the store.

        Args:
            product (Product): The product instance to add.

        Raises:
            ValueError: If the product is None or falsy.
        """
        if not product:
            raise ValueError("Product should not be empty.")
        self.list_of_products.append(product)
        print(f"Added {product.show()} to the store.")

    def remove_product(self, product):
        """
        Remove a product from the store.

        Args:
            product (Product): The product instance to remove.

        Raises:
            ValueError: If the product is None or not found in the store.
        """
        if not product:
            raise ValueError("Product should not be empty.")
        if product in self.list_of_products:
            self.list_of_products.remove(product)
        else:
            raise ValueError("Product not found in the store.")

    def get_total_quantity(self) -> int:
        """
        Calculate the total quantity of all products in the store.

        Returns:
            int: The sum of the quantities of all products.
        """
        return sum(product.quantity for product in self.list_of_products)

    def get_all_products(self) -> list:
        """
        Retrieve all active products from the store.

        Returns:
            list: A list of active Product instances.
        """
        return [product for product in self.list_of_products if product.active]

    def order(self, shopping_list: list) -> float:
        """
        Process an order based on the provided shopping list.

        Args:
            shopping_list (list): A list of tuples, where each tuple contains a Product and the quantity to purchase.

        Returns:
            float: The total price for the order.

        Raises:
            ValueError: If the shopping list is improperly formatted or if any product's quantity is insufficient.
        """
        if not all(isinstance(item, tuple) and len(item) == 2 for item in shopping_list):
            raise ValueError("Shopping list must contain tuples of (Product, quantity).")
        total_price = 0.0
        # Validate each item before processing the order.
        for product, quantity in shopping_list:
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            if quantity > product.quantity:
                raise ValueError(
                    f"Not enough quantity for product {product.name}. "
                    f"Requested: {quantity}, Available: {product.quantity}"
                )
        # Process the order.
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price
