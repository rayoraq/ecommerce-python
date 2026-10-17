PROMO_CODES = {
    "SALE10": 10,
    "SALE20": 20,
    "HALF": 50,
    "HOT": 90,
}

class CartError(Exception):
    pass

class InvalidQuantityError(CartError):
    pass

class ProductNotFoundError(CartError):
    pass

class NotEnoughStockError(CartError):
    pass

class ItemNotInCartError(CartError):
    pass

class InvalidPromoCodeError(CartError):
    pass

class ShoppingCart:
    def __init__(self, products):
        self._products = {p.id: p for p in products}
        self._items = {}
        self._discount_percent = 0

    @property
    def items(self):
        return dict(self._items)

    @property
    def discount_percent(self):
        return self._discount_percent

    @staticmethod
    def _check_quantity(quantity):
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise InvalidQuantityError("Количество должно быть целым числом больше 0")

    def add_item(self, product_id, quantity):
        self._check_quantity(quantity)
        product = self._products.get(product_id)
        if product is None:
            raise ProductNotFoundError(f"Товар {product_id} не найден")
        new_quantity = self._items.get(product_id, 0) + quantity
        if new_quantity > product.stock:
            raise NotEnoughStockError(f"На складе только {product.stock} шт. товара {product_id}")
        self._items[product_id] = new_quantity

    def remove_item(self, product_id, quantity=None):
        if product_id not in self._items:
            raise ItemNotInCartError(f"Товара {product_id} нет в корзине")
        if quantity is None:
            del self._items[product_id]
            return
        self._check_quantity(quantity)
        if quantity >= self._items[product_id]:
            del self._items[product_id]
        else:
            self._items[product_id] -= quantity

    def get_total(self):
        subtotal = sum(self._products[pid].price * qty for pid, qty in self._items.items())
        return round(subtotal * (100 - self._discount_percent) / 100, 2)

    def apply_promo_code(self, code):
        if not isinstance(code, str) or code.strip().upper() not in PROMO_CODES:
            raise InvalidPromoCodeError(f"Промокод {code!r} недействителен")
        self._discount_percent = PROMO_CODES[code.strip().upper()]