import pytest
from products import Product
from products import NonStockedProduct
from products import LimitedProduct
from products import Percentage, Second_item_half_price, Buy_two_get_one_free
from store import Store

# Test: Erzeugt ein normales Produkt und überprüft Attribute.
def test_create_normal_product():
    product = Product("iPhone 14", price=999.99, quantity=10)
    assert product.name == "iPhone 14"
    assert product.price == 999.99
    assert product.quantity == 10
    assert product.active is True

# Test: Leerer Name löst ValueError aus.
def test_empty_name_raises_value_error():
    with pytest.raises(ValueError):
        Product("", price=999.99, quantity=10)

# Test: Ungültiger Name-Typ löst TypeError aus.
def test_invalid_name_type_raises_type_error():
    with pytest.raises(TypeError):
        Product(20, price=999.99, quantity=10)

# Test: Negativer Preis löst ValueError aus.
def test_negative_price_raises_value_error():
    with pytest.raises(ValueError):
        Product("iPhone 14", price=-10, quantity=10)

# Test: Ungültiger Preis-Typ löst TypeError aus.
def test_invalid_price_type_raises_type_error():
    with pytest.raises(TypeError):
        Product("iPhone 14", price="999.99", quantity=10)

# Test: Ungültiger Mengen-Typ löst TypeError aus.
def test_invalid_quantity_type_raises_type_error():
    with pytest.raises(TypeError):
        Product("iPhone 14", price=999.99, quantity="10")

# Test: Negative Menge löst ValueError aus.
def test_negative_quantity_raises_value_error():
    with pytest.raises(ValueError):
        Product("iPhone 14", price=999.99, quantity=-10)

# Test: Produkt wird bei 0 Menge deaktiviert.
def test_product_zero_quantity_deactivation():
    product = Product("iPhone 14", price=999.99, quantity=1)
    product.buy(1)
    assert product.quantity == 0
    assert product.active is False

# Test: Kauf ändert die Menge korrekt und berechnet den Preis.
def test_product_buy_quantity_change():
    product = Product("iPhone", price=999.99, quantity=10)
    result = product.buy(5)
    assert product.quantity == 5
    assert result == 5 * 999.99

# Test: Kauf einer zu hohen Menge löst ValueError aus.
def test_product_buy_excess_quantity_raises_exception():
    product = Product("iPhone", price=999.99, quantity=10)
    with pytest.raises(ValueError):
        product.buy(20)

# Test: NonStockedProduct hat immer 0 Menge.
def test_non_stocked_product_quantity_always_zero():
    product = NonStockedProduct("Windows License", price=125)
    assert product.quantity == 0

# Test: show() von NonStockedProduct enthält non-stocked Info.
def test_non_stocked_product_show_contains_non_stocked_info():
    product = NonStockedProduct("Windows License", price=125)
    output = product.show()
    assert "non-stocked" in output.lower() or "infinitely available" in output.lower()

# Test: LimitedProduct-Kauf innerhalb des Limits.
def test_limited_product_buy_within_limit():
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    total_price = product.buy(1)
    assert total_price == 10.0
    assert product.quantity == 249

# Test: Kauf bei LimitedProduct über dem Limit löst ValueError aus.
def test_limited_product_buy_exceeding_limit_raises_exception():
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    with pytest.raises(ValueError):
        product.buy(2)

# Test: show() von LimitedProduct enthält limitierten Hinweis.
def test_limited_product_show_contains_limited_info():
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    output = product.show()
    assert "limited" in output.lower() or str(product.maximum) in output

# Test: Store-Initialisierung und Integration der Produkte.
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

# Test: Percentage-Promotion wird korrekt angewendet.
def test_percentage_promotion():
    product = Product("Test Product", price=100.0, quantity=10)
    percentage_promo = Percentage("20% off", 20)
    product.set_promotion(percentage_promo)
    total_price = product.buy(2)
    assert total_price == pytest.approx(160.0)
    assert product.quantity == 8

# Test: Second_item_half_price-Promotion wird korrekt angewendet.
def test_second_item_half_price_promotion():
    product = Product("Test Product", price=100.0, quantity=10)
    second_item_half = Second_item_half_price("Second Item Half Price")
    product.set_promotion(second_item_half)
    total_price = product.buy(3)
    assert total_price == pytest.approx(250.0)
    assert product.quantity == 7

# Test: Buy_two_get_one_free-Promotion wird korrekt angewendet.
def test_buy_two_get_one_free_promotion():
    product = Product("Test Product", price=100.0, quantity=10)
    buy2get1 = Buy_two_get_one_free("Buy 2 Get 1 Free")
    product.set_promotion(buy2get1)
    total_price = product.buy(4)
    assert total_price == pytest.approx(300.0)
    assert product.quantity == 6

# Test: show() mit aktiver Promotion zeigt den Promotion-Namen an.
def test_show_with_promotion():
    product = Product("Test Product", price=100.0, quantity=10)
    percentage_promo = Percentage("20% off", 20)
    product.set_promotion(percentage_promo)
    show_str = product.show()
    assert "Promotion: 20% off" in show_str

# Test: show() ohne Promotion enthält keinen Promotion-Hinweis.
def test_show_without_promotion():
    product = Product("Test Product", price=100.0, quantity=10)
    show_str = product.show()
    assert "Promotion:" not in show_str
