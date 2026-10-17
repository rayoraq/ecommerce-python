class Product:
    def __init__(self, id, name, price, stock):
        if not isinstance(id, str) or not id.strip():
            raise ValueError("id должен быть непустой строкой")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name должен быть непустой строкой")
        if price < 0:
            raise ValueError("price не может быть отрицательным")
        if stock < 0:
            raise ValueError("stock не может быть отрицательным")
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock