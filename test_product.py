import pytest
from products import Product

# Test that creating a normal product works.
def test_normal_product_creation():
    p = Product("MacBook Air M2", 1450, 100)
    assert p.name == "MacBook Air M2"
    assert p.price == 1450
    assert p.quantity == 100
    assert p.active is True
    assert p.promotion is None

# Test that creating a product with an empty name raises an exception.
def test_product_creation_empty_name():
    with pytest.raises(ValueError):
        Product("", 1450, 100)

# Test that creating a product with a negative price raises an exception.
def test_product_creation_negative_price():
    with pytest.raises(ValueError):
        Product("MacBook Air M2", -10, 100)

# Test that creating a product with a negative quantity raises an exception.
def test_product_creation_negative_quantity():
    with pytest.raises(ValueError):
        Product("MacBook Air M2", 1450, -5)

# Test that when a product reaches 0 quantity, it becomes inactive.
def test_product_becomes_inactive_when_quantity_zero():
    p = Product("Test Product", 100, 10)
    p.buy(10)  # Purchasing all available units
    assert p.quantity == 0
    assert p.active is False

# Test that a product purchase reduces the quantity and returns the correct total.
def test_product_purchase_reduces_quantity_and_returns_correct_total():
    p = Product("Test Product", 100, 20)
    total = p.buy(5)
    assert total == 500   # 5 * 100 = 500
    assert p.quantity == 15

# Test that purchasing a specific quantity returns the expected total price.
def test_product_purchase_exact_total_price():
    p = Product("Test Product", 100, 10)
    total = p.buy(3)
    assert total == 300   # 3 * 100 = 300

# Test that buying a larger quantity than available invokes an exception.
def test_product_purchase_exceeding_quantity():
    p = Product("Test Product", 100, 5)
    with pytest.raises(ValueError):
        p.buy(6)

# Test that purchasing 0 quantity raises an exception.
def test_product_purchase_invalid_quantity_zero():
    p = Product("Test Product", 100, 10)
    with pytest.raises(ValueError):
        p.buy(0)

# Test multiple purchases: verify quantity updates correctly, deactivation when reaching 0,
# and that further purchase attempts raise an exception.
def test_multiple_purchases_reduce_quantity_and_deactivate():
    p = Product("Test Product", 50, 50)
    total1 = p.buy(10)
    total2 = p.buy(15)
    total3 = p.buy(25)  # This purchase should bring the quantity to 0.
    assert total1 == 500      # 10 * 50
    assert total2 == 750      # 15 * 50
    assert total3 == 1250     # 25 * 50
    assert p.quantity == 0
    assert p.active is False
    # Now, trying to purchase further should raise an exception.
    with pytest.raises(ValueError):
        p.buy(1)
