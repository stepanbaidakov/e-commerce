import pytest

from src.classes import Category, Product


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
    assert category_devices.__str__() == "devices, количество продуктов: 5 шт."


def test_add_function(product_iphone, product_samsung):
    assert product_iphone.__add__(product_samsung) == 9900000.0
