import pytest

from src.classes import (
    BaseProduct,
    Category,
    LawnGrass,
    Order,
    Product,
    ProductIterator,
    Smartphone,
)


@pytest.fixture
def product_iphone():
    return Product("iPhone", "Хороший телефон", 90000, 100)


def test_product_init(product_iphone):
    assert product_iphone.name == "iPhone"
    assert product_iphone.description == "Хороший телефон"
    assert product_iphone.price == 90000
    assert product_iphone.quantity == 100


@pytest.fixture
def category_devices(product_iphone):
    return Category("devices", "мобильные устройства", [product_iphone])


def test_category_init(category_devices):
    assert category_devices.name == "devices"
    assert category_devices.description == "мобильные устройства"
    assert isinstance(category_devices.products, list)


def test_product_count(product_iphone):
    Category.product_count = 0
    Category("devices", "мобильные устройства", [product_iphone])
    assert Category.product_count == 1


def test_category_count(product_iphone):
    Category.category_count = 0
    Category("devices", "мобильные устройства", [product_iphone])
    assert Category.category_count == 1


@pytest.fixture
def product_samsung():
    return Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )


def test_add_product(product_samsung, product_iphone):
    category_devices = Category("devices", "мобильные устройства", [product_iphone])
    category_devices.add_product(product_samsung)
    assert len(category_devices.products) == 2


def test_new_product():
    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    assert isinstance(new_product, Product)


def test_price(product_samsung):
    assert product_samsung.price == 180000.0


def test_new_price_increases(product_samsung):
    product_samsung.price = 280000
    assert product_samsung.price == 280000


def test_new_price_negative(product_samsung):
    product_samsung.price = -100
    assert "Цена не должна быть нулевая или отрицательная"
    assert product_samsung.price == 180000.0


def test_str_product(product_iphone):
    assert product_iphone.__str__() == "iPhone, 90000 руб. Остаток: 100 шт."


def test_str_category(category_devices):
    assert category_devices.__str__() == "devices, количество продуктов: 100 шт."


def test_add_function(product_iphone, product_samsung):
    assert product_iphone + product_samsung == 9900000.0


def test_add_different_function(product_samsung, category_devices):
    with pytest.raises(TypeError):
        product_samsung + category_devices


# @pytest.fixture
# def category():
#     class CategorySmall:
#         def __init__(self):
#             self.products = ["товар1", "товар2", "товар3"]
#             self.product_count = len(self.products)
#
#     return CategorySmall()
@pytest.fixture
def category_2():
    return Category("category_test", "for test", ["товар1", "товар2", "товар3"])


def test_iterator_returns_products_in_order(category_2):
    iterator = ProductIterator(category_2)
    products = list(iterator)  # прогон итератора
    assert products == ["товар1", "товар2", "товар3"]


def test_iterator_stop_iteration(category_2):
    iterator = ProductIterator(category_2)
    # вручную прогоняем до конца
    next(iterator)
    next(iterator)
    next(iterator)
    with pytest.raises(StopIteration):
        next(iterator)


@pytest.fixture
def smartphone_1():
    return Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )


def test_smartphone_init(smartphone_1):
    assert smartphone_1.efficiency == 95.5
    assert smartphone_1.model == "S23 Ultra"
    assert smartphone_1.memory == 256
    assert smartphone_1.color == "Серый"


@pytest.fixture
def lawn_grass_1():
    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )


def test_lawn_grass_init(lawn_grass_1):
    assert lawn_grass_1.country == "Россия"
    assert lawn_grass_1.germination_period == "7 дней"
    assert lawn_grass_1.color == "Зеленый"


@pytest.fixture
def lawn_grass_2():
    return LawnGrass(
        "Газонная трава 2",
        "Выносливая трава",
        450.0,
        15,
        "США",
        "5 дней",
        "Темно-зеленый",
    )


@pytest.fixture
def category_grass(lawn_grass_1):
    return Category("Газонная трава", "Различные виды газонной травы", [lawn_grass_1])


def test_similar_product_added_grass(category_grass, lawn_grass_2):
    category_grass.add_product(lawn_grass_2)
    assert category_grass.product_count == 2


def test_wrong_product_added(category_grass):
    with pytest.raises(TypeError):
        category_grass.add_product("Not a product")


def test_sum_of_similar_grass(lawn_grass_1, lawn_grass_2):
    assert lawn_grass_1 + lawn_grass_2 == 16750.0


def test_sum_of_different_grass(lawn_grass_1, smartphone_1):
    with pytest.raises(TypeError):
        lawn_grass_1 + smartphone_1


@pytest.fixture
def smartphone_2():
    return Smartphone(
        "Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space"
    )


def test_sum_of_similar_smartphone(smartphone_1, smartphone_2):
    assert smartphone_1 + smartphone_2 == 2580000.0


def test_sum_of_different_smartphone(smartphone_1, lawn_grass_1):
    with pytest.raises(TypeError):
        smartphone_1 + lawn_grass_1


def test_base_product():
    assert issubclass(Product, BaseProduct)


def test_mixinlog_repr(product_iphone):
    assert repr(product_iphone) == 'Product("iPhone", "Хороший телефон", 90000, 100)'


@pytest.fixture
def order_iphone(product_iphone):
    return Order(product_iphone, 10)


def test_order_init(order_iphone):
    assert order_iphone.product.name == "iPhone"
    assert order_iphone.quantity == 10


def test_order_init_to_many(product_iphone):
    with pytest.raises(ValueError):
        Order(product_iphone, 111)


def test_product_iterator_init(category_2):
    with pytest.raises(ValueError):
        ProductIterator("Not a category")