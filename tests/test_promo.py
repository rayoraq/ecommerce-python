import pytest

from src.shopping_cart import InvalidPromoCodeError, ShoppingCart
from src.product import Product

@pytest.fixture
def cart():
    c = ShoppingCart([Product("prod_1", "Смартфон", 500.0, 5)])
    c.add_item("prod_1", 2)  # сумма без скидки: 1000.0
    return c

def test_givenNoPromoByDefault_thenDiscountIsZeroAndTotalIsOriginal(cart):
    assert cart.discount_percent == 0
    assert cart.get_total() == pytest.approx(1000.0)

def test_givenValidPromo_whenApplyPromo_thenDiscountApplied(cart):
    cart.apply_promo_code("SALE10")
    assert cart.discount_percent == 10
    assert cart.get_total() == pytest.approx(900.0)

def test_givenPromoWithSpacesAndLowerCase_whenApplyPromo_thenDiscountApplied(cart):
    cart.apply_promo_code("  sale20 ")
    assert cart.get_total() == pytest.approx(800.0)

def test_givenHalfPromo_whenApplyPromo_thenHalfPriceApplied(cart):
    cart.apply_promo_code("HALF")
    assert cart.get_total() == pytest.approx(500.0)

def test_givenHotPromo_whenApplyPromo_then90PercentDiscountApplied(cart):
    cart.apply_promo_code("HOT")
    assert cart.discount_percent == 90
    assert cart.get_total() == pytest.approx(100.0)

def test_givenNewPromo_whenApplyPromo_thenOldPromoReplaced(cart):
    cart.apply_promo_code("SALE10")
    cart.apply_promo_code("SALE20")
    assert cart.discount_percent == 20

@pytest.mark.parametrize("bad_code", ["WRONG", "", "   ", None, 123])
def test_givenInvalidPromo_whenApplyPromo_thenRaisesInvalidPromoCodeError(cart, bad_code):
    with pytest.raises(InvalidPromoCodeError):
        cart.apply_promo_code(bad_code)
    assert cart.discount_percent == 0

def test_givenEmptyCart_whenApplyPromo_thenTotalIsZero():
    c = ShoppingCart([])
    c.apply_promo_code("SALE10")
    assert c.get_total() == 0