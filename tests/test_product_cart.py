import pytest
from src.shopping_cart import ShoppingCart, InvalidQuantityError, ProductNotFoundError, NotEnoughStockError, ItemNotInCartError
from src.product import Product

@pytest.fixture
def cart():
    return ShoppingCart(
        [
            Product("prod_1", "Смартфон", 500.0, 5),
            Product("prod_2", "Чехол", 10.5, 100),
        ]
    )

# ---------- Product ----------
def test_givenValidData_whenCreateProduct_thenAttributesAreSet():
    p = Product("prod_102", "Смартфон", 999.99, 3)
    assert (p.id, p.name, p.price, p.stock) == ("prod_102", "Смартфон", 999.99, 3)

@pytest.mark.parametrize("bad_id", ["", "   ", None, 123])
def test_givenInvalidId_whenCreateProduct_thenRaisesValueError(bad_id):
    with pytest.raises(ValueError):
        Product(bad_id, "Имя", 1, 1)

@pytest.mark.parametrize("bad_name", ["", "  ", None])
def test_givenInvalidName_whenCreateProduct_thenRaisesValueError(bad_name):
    with pytest.raises(ValueError):
        Product("p", bad_name, 1, 1)

def test_givenNegativePrice_whenCreateProduct_thenRaisesValueError():
    with pytest.raises(ValueError):
        Product("p", "Имя", -1, 1)

def test_givenNegativeStock_whenCreateProduct_thenRaisesValueError():
    with pytest.raises(ValueError):
        Product("p", "Имя", 1, -1)


# ---------- add_item ----------
def test_givenNewCart_thenItemsAreEmpty(cart):
    assert cart.items == {}

def test_givenEmptyCart_whenAddItem_thenItemIsAdded(cart):
    cart.add_item("prod_1", 2)
    assert cart.items == {"prod_1": 2}

def test_givenItemInCart_whenAddSameItem_thenQuantityIncreases(cart):
    cart.add_item("prod_1", 2)
    cart.add_item("prod_1", 3)
    assert cart.items == {"prod_1": 5}

def test_givenCart_whenAddExactlyStock_thenItemIsAdded(cart):
    cart.add_item("prod_1", 5)
    assert cart.items["prod_1"] == 5

@pytest.mark.parametrize("bad_qty", [0, -1, -100, 2.5, "3", None, True])
def test_givenInvalidQuantity_whenAddItem_thenRaisesInvalidQuantityError(cart, bad_qty):
    with pytest.raises(InvalidQuantityError):
        cart.add_item("prod_1", bad_qty)
    assert cart.items == {}

def test_givenUnknownProduct_whenAddItem_thenRaisesProductNotFoundError(cart):
    with pytest.raises(ProductNotFoundError):
        cart.add_item("nope", 1)

def test_givenQuantityExceedingStock_whenAddItem_thenRaisesNotEnoughStockError(cart):
    with pytest.raises(NotEnoughStockError):
        cart.add_item("prod_1", 6)

def test_givenItemInCart_whenAddMore_thanStockLeft_thenRaisesNotEnoughStockError(cart):
    cart.add_item("prod_1", 3)
    with pytest.raises(NotEnoughStockError):
        cart.add_item("prod_1", 3)
    assert cart.items == {"prod_1": 3}

def test_whenGetItems_thenReturnsCopy(cart):
    cart.add_item("prod_1", 1)
    cart.items["prod_1"] = 999
    assert cart.items == {"prod_1": 1}

# ---------- remove_item ----------
def test_givenItemInCart_whenRemovePartOfQuantity_thenQuantityDecreases(cart):
    cart.add_item("prod_1", 4)
    cart.remove_item("prod_1", 1)
    assert cart.items == {"prod_1": 3}

def test_givenItemInCart_whenRemoveWithoutQuantity_thenItemIsRemoved(cart):
    cart.add_item("prod_1", 4)
    cart.remove_item("prod_1")
    assert cart.items == {}

def test_givenItemInCart_whenRemoveQuantityEqualOrMore_thenItemIsRemoved(cart):
    cart.add_item("prod_1", 2)
    cart.add_item("prod_2", 2)
    cart.remove_item("prod_1", 2)
    cart.remove_item("prod_2", 50)
    assert cart.items == {}

def test_givenItemNotInCart_whenRemoveItem_thenRaisesItemNotInCartError(cart):
    with pytest.raises(ItemNotInCartError):
        cart.remove_item("prod_1")

@pytest.mark.parametrize("bad_qty", [0, -1, 1.5])
def test_givenItemInCart_whenRemoveInvalidQuantity_thenRaisesInvalidQuantityError(cart, bad_qty):
    cart.add_item("prod_1", 3)
    with pytest.raises(InvalidQuantityError):
        cart.remove_item("prod_1", bad_qty)
    assert cart.items == {"prod_1": 3}

# ---------- get_total ----------
def test_givenEmptyCart_whenGetTotal_thenReturnsZero(cart):
    assert cart.get_total() == 0

def test_givenCartWithItems_whenGetTotal_thenReturnsSum(cart):
    cart.add_item("prod_1", 2)
    cart.add_item("prod_2", 3)
    assert cart.get_total() == pytest.approx(1031.5)

def test_givenCartWithRemovedItem_whenGetTotal_thenReturnsUpdatedSum(cart):
    cart.add_item("prod_1", 2)
    cart.remove_item("prod_1", 1)
    assert cart.get_total() == pytest.approx(500.0)