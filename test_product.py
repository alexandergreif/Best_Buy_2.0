import pytest
from products import Product
from products import NonStockedProduct
from products import LimitedProduct
from store import Store


def test_create_normal_product():

    product = Product("iPhone 14", price=999.99, quantity=10)

    assert product.name == "iPhone 14"
    assert product.price == 999.99
    assert product.quantity == 10
    assert product.active is True

def test_empty_name_raises_value_error():
    with pytest.raises(ValueError):
        Product("", price=999.99, quantity=10)

def test_invalid_name_type_raises_type_error():
    with pytest.raises(TypeError):
        Product(20, price=999.99, quantity=10)

def test_negative_price_raises_value_error():
    with pytest.raises(ValueError):
        Product("iPhone 14", price=-10, quantity=10)

def test_invalid_price_type_raises_type_error():
    with pytest.raises(TypeError):
        Product("iPhone 14", price="999.99", quantity=10)

def test_invalid_quantity_type_raises_type_error():
    with pytest.raises(TypeError):
        Product("iPhone 14", price=999.99, quantity="10")

def test_negative_quantity_raises_value_error():
    # Test: Negative Menge soll einen ValueError auslösen
    with pytest.raises(ValueError):
        Product("iPhone 14", price=999.99, quantity=-10)


def test_product_zero_quantity_deactivation():
    product = Product("iPhone 14", price=999.99, quantity=1)

    product.buy(1)
    assert product.quantity == 0
    assert product.active is False

def test_product_buy_quantity_change():
    product = Product("iPhone", price=999.99, quantity=10)

    result = product.buy(5)

    assert product.quantity == 5
    assert result == 5 * 999.99

def test_product_buy_excess_quantity_raises_exception():
    product = Product("iPhone", price=999.99, quantity=10)

    with pytest.raises(ValueError):
        product.buy(20)


def test_non_stocked_product_quantity_always_zero():
    product = NonStockedProduct("Windows License", price=125)
    # Auch wenn man versucht, eine Menge zu übergeben, sollte sie 0 sein.
    assert product.quantity == 0


def test_non_stocked_product_show_contains_non_stocked_info():
    product = NonStockedProduct("Windows License", price=125)
    output = product.show()
    # Es sollte ein Hinweis darauf enthalten sein, dass das Produkt non-stocked ist.
    assert "non-stocked" in output.lower() or "infinitely available" in output.lower()


# Tests für LimitedProduct

def test_limited_product_buy_within_limit():
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    # Ein Kauf von 1 Einheit sollte funktionieren
    total_price = product.buy(1)
    assert total_price == 10.0
    assert product.quantity == 249


def test_limited_product_buy_exceeding_limit_raises_exception():
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    with pytest.raises(ValueError):
        product.buy(2)


def test_limited_product_show_contains_limited_info():
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    output = product.show()
    # Der Output sollte den Hinweis enthalten, dass es ein limitiertes Produkt ist.
    assert "limited" in output.lower() or str(product.maximum) in output


# Integrationstest für den Store

def test_store_initialization_and_product_integration():
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]
    best_buy = Store(product_list)


    assert len(best_buy.list_of_products) == 5


    for product in best_buy.list_of_products:
        if isinstance(product, NonStockedProduct):
            assert product.quantity == 0


    outputs = [product.show() for product in best_buy.list_of_products]
    assert any("limited" in out.lower() for out in outputs)
    assert any("windows license" in out.lower() for out in outputs)

