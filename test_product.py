import pytest
from products import Product

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


