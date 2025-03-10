from promotions import Promotion


class Product:
    """
    Represents a product in the store.

    Attributes:
        name (str): The product's name.
        price (float): The product's price.
        quantity (int): The available quantity.
        active (bool): Indicates if the product is available for purchase.
        promotion (Promotion or None): An optional promotion applied to the product.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initialize a new Product instance with validated attributes.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
            quantity (int): The available quantity.
        """
        self.name = name  # Uses setter for validation
        self.price = price  # Uses setter for validation
        self.quantity = quantity  # Uses setter for validation
        self.active = True
        self.promotion = None

    @property
    def name(self):
        """str: Get or set the product's name."""
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not value:
            raise ValueError("Name should not be empty.")
        self._name = value

    @property
    def price(self):
        """float: Get or set the product's price."""
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
        if value < 0:
            raise ValueError("Price should not be negative.")
        self._price = value

    @property
    def quantity(self):
        """int: Get or set the product's quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int):
            raise TypeError("Quantity must be an integer.")
        if value < 0:
            raise ValueError("Quantity should not be negative.")
        self._quantity = value
        if self._quantity == 0:
            self.active = False

    @property
    def active(self):
        """bool: Get or set the product's active status."""
        return self._active

    @active.setter
    def active(self, value):
        if not isinstance(value, bool):
            raise TypeError("Active must be a boolean.")
        self._active = value

    @property
    def promotion(self):
        """Promotion or None: Get or set the product's promotion."""
        return self._promotion

    @promotion.setter
    def promotion(self, value):
        if value is not None and not isinstance(value, Promotion):
            raise TypeError("Promotion must be a Promotion instance or None.")
        self._promotion = value

    def show(self) -> str:
        """
        Return a string representation of the product.

        Returns:
            str: The product's details, including any applied promotion.
        """
        base_info = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotion:
            base_info += f", Promotion: {self.promotion.name}"
        return base_info

    def buy(self, quantity: int) -> float:
        """
        Process a purchase for the product.

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
            raise ValueError("Not enough quantity in storage.")
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity
        self.quantity -= quantity  # Uses setter, which may deactivate the product
        return total_price


class NonStockedProduct(Product):
    """
    A product that is non-stocked, meaning it is available with infinite supply.
    """

    def __init__(self, name: str, price: float):
        """
        Initialize a non-stocked product with quantity always set to 0.

        Args:
            name (str): The product's name.
            price (float): The product's price.
        """
        super().__init__(name, price, 0)

    def show(self) -> str:
        """
        Return a string representation specific to non-stocked products.

        Returns:
            str: Details indicating that the product is non-stocked.
        """
        return f"{self.name} is non-stocked and infinitely available. Price: {self.price}"


class LimitedProduct(Product):
    """
    A product with a purchase limit per order.
    """

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """
        Initialize a limited product with a per-order purchase limit.

        Args:
            name (str): The product's name.
            price (float): The product's price.
            quantity (int): The available quantity.
            maximum (int): The maximum quantity allowed per order.
        """
        super().__init__(name, price, quantity)
        self.maximum = maximum

    @property
    def maximum(self):
        """int: Get or set the maximum quantity allowed per order."""
        return self._maximum

    @maximum.setter
    def maximum(self, value):
        if not isinstance(value, int):
            raise TypeError("Maximum must be an integer.")
        if value <= 0:
            raise ValueError("Maximum must be positive.")
        self._maximum = value

    def buy(self, quantity: int) -> float:
        """
        Process a purchase for a limited product, enforcing the purchase limit.

        Args:
            quantity (int): The quantity to purchase.

        Returns:
            float: The total price for the purchase.

        Raises:
            ValueError: If the quantity exceeds the per-order maximum.
        """
        if quantity > self.maximum:
            raise ValueError(f"Quantity {quantity} exceeds the limit of {self.maximum}.")
        return super().buy(quantity)

    def show(self) -> str:
        """
        Return a string representation of the limited product, including its limit.

        Returns:
            str: The product's details with its purchase limit.
        """
        base_info = super().show()
        return f"{base_info}, Limited to {self.maximum} per order."
