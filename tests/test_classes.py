import pytest
from src.classes import Product, Category


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
    for product in category_devices.products:
        assert isinstance(product, Product)


def test_product_count(product_iphone):
    Category.product_count = 0
    Category("devices", "мобильные устройства", [product_iphone])
    assert Category.product_count == 1


def test_category_count(product_iphone):
    Category.category_count = 0
    Category("devices", "мобильные устройства", [product_iphone])
    assert Category.category_count == 1
