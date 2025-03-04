from abc import ABC, abstractmethod


class Product:
    """
    A class representing a product in the store.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
        quantity (int): The available quantity of the product.
        active (bool): Flag indicating if the product is active (available for purchase).
        promotion (Discount or None): An optional promotion applied to the product.
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
        self.promotion = None  # type: Discount or None

    def get_promotion(self):
        """
        Get the promotion applied to the product.

        Returns:
            Discount or None: The current promotion, or None if no promotion is set.
        """
        return self.promotion

    def set_promotion(self, promotion):
        """
        Set a promotion for the product.

        Args:
            promotion (Discount or None): A Discount instance or None to remove the promotion.
        """
        self.promotion = promotion

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
            quantity (int): The new quantity to set. If zero, the product will be deactivated.

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
            str: A string showing the product's name, price, quantity, and promotion (if any).
        """
        base_info = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotion:
            base_info += f", Promotion: {self.promotion.name}"
        return base_info

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

        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity

        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return total_price


class NonStockedProduct(Product):
    """
    A product that does not have a stock quantity.
    """

    def __init__(self, name, price):
        """
        Initialize a NonStockedProduct with quantity always set to zero.

        Args:
            name (str): The product's name.
            price (float): The product's price.
        """
        super().__init__(name, price, 0)

    def show(self):
        """
        Create a string representation indicating non-stocked availability.

        Returns:
            str: A string indicating that the product is non-stocked and infinitely available.
        """
        super().show()
        return f"The product {self.name} is a non-stocked-product and infinitely available."


class LimitedProduct(Product):
    """
    A product that can only be purchased up to a certain limit per order.
    """

    def __init__(self, name, price, quantity, maximum):
        """
        Initialize a LimitedProduct.

        Args:
            name (str): The product's name.
            price (float): The product's price.
            quantity (int): The available quantity.
            maximum (int): The maximum units that can be purchased in one order.
        """
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity):
        """
        Process a purchase for a limited product, enforcing a maximum per order.

        Args:
            quantity (int): The quantity to purchase.

        Returns:
            float: The total price for the purchase.

        Raises:
            ValueError: If quantity exceeds the maximum allowed per order.
        """
        if quantity > self.maximum:
            raise ValueError(f"Quantity {quantity} exceeds the limit of {self.maximum}.")
        total_cost = super().buy(quantity)
        return total_cost

    def show(self):
        """
        Create a string representation of the limited product.

        Returns:
            str: A string showing the product's details along with its purchase limit.
        """
        base_info = super().show()
        return f"{base_info}, Limited: {self.maximum} per customer."


class Discount(ABC):
    """
    An abstract class representing a promotion or discount.
    """

    def __init__(self, name):
        """
        Initialize a Discount.

        Args:
            name (str): The name of the discount.
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        """
        Apply the discount promotion to the product for a given quantity.

        Args:
            product (Product): The product instance.
            quantity (int): The number of items to purchase.

        Returns:
            float: The total price after the discount is applied.
        """
        pass


class Percentage(Discount):
    """
    A discount that applies a percentage off the total price.
    """

    def __init__(self, name: str, percent: float):
        """
        Initialize a Percentage discount.

        Args:
            name (str): The name of the discount.
            percent (float): The percentage discount to apply.
        """
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity):
        """
        Apply the percentage discount to the product's total price.

        Args:
            product (Product): The product instance.
            quantity (int): The quantity to purchase.

        Returns:
            float: The discounted total price.
        """
        total_price = product.price * quantity
        discount_amount = total_price * (self.percent / 100)
        return total_price - discount_amount


class Second_item_half_price(Discount):
    """
    A discount that applies half price to every second item.
    """

    def __init__(self, name: str):
        """
        Initialize a Second_item_half_price discount.

        Args:
            name (str): The name of the discount.
        """
        super().__init__(name)

    def apply_promotion(self, product, quantity):
        """
        Calculate the total price such that every second item is half price.

        Args:
            product (Product): The product instance.
            quantity (int): The quantity to purchase.

        Returns:
            float: The total price after the discount.
        """
        full_price = product.price
        pairs = quantity // 2
        remainder = quantity % 2
        total_price = pairs * (full_price + full_price / 2) + remainder * full_price
        return total_price


class Buy_two_get_one_free(Discount):
    """
    A discount where for every three items purchased, one is free.
    """

    def apply_promotion(self, product, quantity):
        """
        Calculate the total price by charging only for two out of every three items.

        Args:
            product (Product): The product instance.
            quantity (int): The quantity to purchase.

        Returns:
            float: The total price after applying the discount.
        """
        full_price = product.price
        groups = quantity // 3
        remainder = quantity % 3
        total_price = groups * (2 * full_price) + remainder * full_price
        return total_price
