class Product:
    """
       A class representing a product in the store.

       Attributes:
           name (str): The name of the product.
           price (float): The price of the product.
           quantity (int): The available quantity of the product.
           active (bool): Flag indicating if the product is active (available for purchase).
       """

    def __init__(self, name, price, quantity):
        """
        Initialize a new Product instance.

        Args:
            name (str): The product's name.
            price (float): The product's price.
            quantity (int): The available quantity.

        Raises:
            TypeError: If the type of name, price, or quantity is incorrect.
            ValueError: If name is empty or if price/quantity is negative.
        """

        if not isinstance(name, str):
            raise TypeError("Name muss ein String sein.")
        if not isinstance(price, (int, float)):
            raise TypeError("Preis muss eine Zahl sein.")
        if not isinstance(quantity, int):
            raise TypeError("Menge muss ein Integer sein.")
        if not name:
            raise ValueError("Name should not be empty.")
        if price < 0:
            raise ValueError("Price should not be negative.")
        if quantity < 0:
            raise ValueError("Quantity should not be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self):
        """
        Retrieve the current quantity of the product.

        Returns:
            int: The current quantity.
        """
        return self.quantity

    def set_quantity(self, quantity):
        """
        Set a new quantity for the product.

        Args:
            quantity (int): The new quantity to set. If zero, the product should be deactivated.

        Raises:
            ValueError: If the quantity is negative.
        """
        if quantity < 0:
            raise ValueError("Quantity should not be negative.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self):
        """
        Check whether the product is active.

        Returns:
            bool: True if the product is active, False otherwise.
        """
        return self.active

    def activate(self):
        """
        Activate the product by setting its active flag to True.
        """
        self.active = True

    def deactivate(self):
        """
        Deactivate the product by setting its active flag to False.
        """
        self.active = False

    def show(self):
        """
        Create a string representation of the product.

        Returns:
            str: A string showing the product's name, price, and quantity.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity):
        """
        Process a purchase for a specified quantity of the product.

        Args:
            quantity (int): The quantity to purchase.

        Returns:
            float: The total price for the purchase.

        Raises:
            ValueError: If the quantity is not positive or exceeds available stock.
        """
        if quantity <= 0:
            raise ValueError("The quantity has to be positive.")
        if quantity > self.quantity:
            raise ValueError("Not enough quantity in the storage")

        total_price = self.price * quantity

        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return total_price

