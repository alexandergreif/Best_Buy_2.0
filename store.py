

class Store:
    """
    A class representing a store that manages a collection of products.

    Attributes:
        list_of_products (List[Product]): A list of Product instances available in the store.
    """
    def __init__(self, list_of_products):
        """
        Initialize the store with a list of products.

        Args:
            list_of_products (List[Product]): The initial list of products.
        """
        self.list_of_products = list_of_products

    def add_product(self, product):
        """
        Add a new product to the store inventory.

        Args:
            product (Product): The product to add.
        """
        if not product:
            raise ValueError("Product should not be empty.")
        self.list_of_products.append(product)
        print(f"Added {product} to the list of Products.")

    def remove_product(self, product):
        """
        Remove a product from the store inventory.

        Args:
            product (Product): The product to remove.

        Raises:
            ValueError: If the product is not found in the inventory.
        """
        if not product:
            raise ValueError("Product should not be empty.")
        if product in self.list_of_products:
            self.list_of_products.remove(product)
        else:
            raise ValueError("Product not found in the store.")


    def get_total_quantity(self):
        """
        Calculate the total quantity of items available in the store.

        Returns:
             int: The sum of quantities for all products in the store.
        """
        total_quantity = 0
        for product in self.list_of_products:
            total_quantity += product.quantity
        return total_quantity


    def get_all_products(self):
        """
        Retrieve a list of all active products in the store.

        Returns:
            List[Product]: A list of Product instances that are active.
        """
        return [product for product in self.list_of_products if product.is_active()]

    def order(self, shopping_list):
        """
        Process an order based on a shopping list.

        Args:
            shopping_list (List[Tuple[Product, int]]): A list of tuples where each tuple
                contains a Product and the quantity to purchase.

        Returns:
            float: The total price for the order.

        Raises:
            ValueError: If a product does not have sufficient quantity or if an invalid
            quantity is provided.
        """
        if not isinstance(shopping_list[0], tuple):
            raise ValueError("Shopping list need to contain Item name and quantity as tuple.")
        total_price = 0
        for product, quantity in shopping_list:
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            if quantity > product.quantity:
                raise ValueError(
                f"Not enough quantity for product {product.name}. "
                f"Requested: {quantity}, Available: {product.quantity}"
            )
            total_price += product.buy(quantity)

        return total_price
