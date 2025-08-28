class Product:
    """Класс для получения данных о товаре"""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_info):
        infos = []
        for info in product_info.values():
            infos.append(info)

        name, description, price, quantity = infos
        return cls(name, description, price, quantity)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price > 0:
            if new_price < self.__price:
                user_input = input("Cогласны ли вы с понижением цены: ")
                if user_input.lower() == "y":
                    self.__price = new_price
            else:
                self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        return self.__price * self.quantity + other.price * other.quantity


class Category:
    """Класс категорий"""

    name: str
    description: str
    products: list[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products

        Category.product_count += len(products)
        Category.category_count += 1

    def add_product(self, product):
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1

    def __str__(self):
        pieces_count = 0
        for product in self.__products:
            pieces_count += product.quantity
        return f"{self.name}, количество продуктов: {pieces_count} шт."

    @property
    def products(self):
        return self.__products


class ProductIterator:
    """Производит итерацию по товарам, которые находятся в данной категории"""

    category: Category

    def __init__(self, category):
        # if not isinstance(category, Category):
        #     raise ValueError("Объект должен быть класса Category")
        self.category = category
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.category.product_count:
            product = self.category.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration
