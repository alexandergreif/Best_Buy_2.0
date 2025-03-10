from abc import ABC, abstractmethod

class Promotion(ABC):
    """
    Abstract base class representing a promotion.
    """
    def __init__(self, name: str):
        """
        Initialize a Promotion.

        Args:
            name (str): The name of the promotion.
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        """
        Apply the promotion to a product for a specified quantity.

        Args:
            product (Product): The product instance.
            quantity (int): The quantity to purchase.

        Returns:
            float: The total price after applying the promotion.
        """
        pass

class PercentDiscount(Promotion):
    """
    Applies a percentage discount to the total price.
    """
    def __init__(self, percent: float):
        """
        Initialize a PercentDiscount promotion.

        Args:
            percent (float): The percentage discount to apply.
        """
        super().__init__("Percent Discount")
        self.percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Calculate the total price after applying a percentage discount.

        Args:
            product (Product): The product instance.
            quantity (int): The quantity to purchase.

        Returns:
            float: The discounted total price.
        """
        total = product.price * quantity
        discount = total * (self.percent / 100)
        return total - discount

class SecondHalfPrice(Promotion):
    """
    Applies a promotion where every second item is half price.
    """
    def __init__(self):
        """
        Initialize a SecondHalfPrice promotion.
        """
        super().__init__("Second Half Price")

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Calculate the total price applying half price for every second item.

        Args:
            product (Product): The product instance.
            quantity (int): The quantity to purchase.

        Returns:
            float: The total price after applying the promotion.
        """
        full_price = product.price
        pairs = quantity // 2
        remainder = quantity % 2
        return pairs * (full_price + full_price / 2) + remainder * full_price

class ThirdOneFree(Promotion):
    """
    Applies a promotion where for every three items, one is free (buy 2, get 1 free).
    """
    def __init__(self):
        """
        Initialize a ThirdOneFree promotion.
        """
        super().__init__("Third One Free")

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Calculate the total price applying the 'buy 2, get 1 free' promotion.

        Args:
            product (Product): The product instance.
            quantity (int): The quantity to purchase.

        Returns:
            float: The total price after applying the promotion.
        """
        groups = quantity // 3
        remainder = quantity % 3
        return groups * (2 * product.price) + remainder * product.price
