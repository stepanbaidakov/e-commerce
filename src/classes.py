from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Базовый класс для всех продуктов"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __str__(self):
        pass


class MixinLog:

    def __init__(self):
        print(repr(self))
        super().__init__()

    def __repr__(self):
        return f"{self.__class__.__name__}(\"{self.name}\", \"{self.description}\", {self.price}, {self.quantity})"


class Product(MixinLog, BaseProduct):
    """Класс для получения данных о товаре"""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен.")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__()

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
        if type(self) is type(other):
            return self.__price * self.quantity + other.price * other.quantity
        else:
            raise TypeError


class BaseModel(ABC):
    """Базовый класс для заказов и категорий"""

    @abstractmethod
    def __init__(self, name):
        self.name = name


class Order(BaseModel):
    """Класс для заказов ссылающейся на один купленный товар"""

    def __init__(self, product: Product, quantity):
        self.product = product
        if quantity > product.quantity:
            raise ValueError
        try:
            if product.quantity != 0:
                self.quantity = quantity
        except AddingProductException as e:
            print(e)
        else:
            print("Товар успешно добавлен.")
        finally:
            print("Обработка добавления товара завершена.")


class Category(BaseModel):
    """Класс категорий"""

    name: str
    description: str
    products: list[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        super().__init__(name)
        self.description = description
        self.__products = products

        Category.product_count = len(products)
        Category.category_count += 1

    def add_product(self, product):
        if isinstance(product, Product):
            try:
                if product.quantity != 0:
                    self.__products.append(product)
                    Category.product_count += 1
            except AddingProductException as e:
                return e
            else:
                return "Товар успешно добавлен."
            finally:
                return "Обработка добавления товара завершена."
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    def __str__(self):
        pieces_count = 0
        for product in self.__products:
            pieces_count += product.quantity
        return f"{self.name}, количество продуктов: {pieces_count} шт."

    @property
    def products(self):
        return self.__products

    def middle_price(self):
        try:
            result = 0
            for product in self.__products:
                result += product.price
            return result / len(self.__products)
        except ZeroDivisionError:
            return 0


class AddingProductException(Exception):
    """Класс для проверки количества товара"""

    def __init__(self, *args):
        self.message = args[0] if args else "Добавляется товар с нулевым количеством."

    def __str__(self):
        return self.message


class ProductIterator:
    """Производит итерацию по товарам, которые находятся в данной категории"""

    category: Category

    def __init__(self, category):
        if not isinstance(category, Category):
            raise TypeError("Объект должен быть класса Category")
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


class Smartphone(Product):
    """Класс для товаров смартфонов"""

    efficiency: float
    model: str
    memory: int
    color: str

    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для товаров газонной травы"""

    country: str
    germination_period = str
    color: str

    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


if __name__ == "__main__":
    # pr1 = Product("iPhone", "Хороший телефон", 90000, 10)
    # order = Order(pr1, 11)
    # print(order.quantity)
    product_iphone = Product("iPhone", "Хороший телефон", 90000, 10)
    product_samsung = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 1
    )
    cat = Category("cat", "nothing", [product_samsung])

    cat.add_product(product_samsung)
