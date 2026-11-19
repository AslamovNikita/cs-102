"""Тесты обработки заказов"""
import pytest

from src.lab4.main import (
    Order,
    is_valid_phone,
    parse_address,
    parse_order,
    process_orders,
)


@pytest.mark.parametrize(
    "phone",
    [
        "+7-921-456-78-90",
        "+3-214-020-50-50",
        "+1-416-123-45-67",
    ],
)
def test_valid_phone(phone):
    """Проверка правильных тел. номеров"""
    assert is_valid_phone(phone)


@pytest.mark.parametrize(
    "phone",
    [
        "",
        "+4-989-234-56",
        "+34-93-1234-567",
        "7-921-456-78-90",
        "+7-921-456-78-9",
        "+A-921-456-78-90",
    ],
)
def test_invalid_phone(phone):
    """проверка неправильных тел. номеров"""
    assert not is_valid_phone(phone)


def test_parse_valid_address():
    """Проверка разбора адреса"""
    assert parse_address("Россия. Московская область. Москва. улица Пушкина") == (
        "Россия",
        "Московская область",
        "Москва",
        "улица Пушкина",
    )


@pytest.mark.parametrize(
    "address",
    [
        "",
        "Россия. Москва. Улица",
        "Россия..Москва.Улица",
        "Россия. Москва. . Улица",
        "Россия. Москва. Улица.",
    ],
)
def test_invalid_address(address):
    """Проверка неверных адресов"""
    assert parse_address(address) is None


def test_product_counting():
    """Проверка подсчёта одинаковых продуктов"""
    order = Order(
        number="12345",
        products=("Бананы", "Гречка", "Бананы", "Сметана", "Гречка"),
        customer="Иванов Иван",
        address="Россия. Москва. Москва. Пушкина",
        phone="+7-921-456-78-90",
        priority="MAX",
    )
    assert order.format_products() == ("Бананы x2, Гречка x2, Сметана")


def test_parse_order_without_patronymic():
    """Проверка, случая когда ФИО из двух слов"""
    order = parse_order(
        "12345;Молоко, Хлеб;Иванов Иван;"
        "Россия. Москва. Москва. Пушкина;"
        "+7-921-456-78-90;MAX"
    )
    assert order.customer == "Иванов Иван"
    assert order.priority == "MAX"


def test_parse_order_invalid_column_count():
    """Проверка обрабтки строки с неправильным кол-вом полей"""
    with pytest.raises(ValueError):
        parse_order("12345;Молоко;Иванов Иван")


def test_process_orders(tmp_path):
    """проверка обработки набора заказов"""
    input_path = tmp_path / "orders.txt"
    valid_path = tmp_path / "order_country.txt"
    invalid_path = tmp_path / "non_valid_orders.txt"
    input_data = """\
31987;Сыр, Колбаса, Сыр, Макароны, Колбаса;Петрова Анна;Россия. Ленинградская область. Санкт-Петербург. набережная реки Фонтанки;+7-921-456-78-90;MIDDLE
87459;Молоко, Яблоки, Хлеб, Яблоки, Молоко;Иванов Иван Иванович;Россия. Московская область. Москва. улица Пушкина;+7-912-345-67-89;MAX
31987;Сыр, Колбаса, Макароны, Сыр, Колбаса;Петрова Анна Сергеевна;Франция. Иль-де-Франс. Париж. Шанз-Элизе;+3-214-020-50-50;MIDDLE
56342;Хлеб, Молоко, Хлеб, Молоко;Смирнова Мария Леонидовна;Германия. Бавария. Мюнхен. Мариенплац;+4-989-234-56;LOW
48276;Яблоки, Макароны, Яблоки;Алексеев Алексей Алексеевич;Италия. Лацио. Рим. Колизей;+3-061-234-56-78;MAX
65829;Сок, Вода, Сок, Вода;Белова Екатерина Михайловна;Испания. Каталония. Барселона. Рамбла;+34-93-1234-567;LOW
72901;Чай, Кофе, Чай, Кофе;Михайлов Сергей Петрович;Великобритания. Англия. Лондон. Бейкер-стрит;+4-207-946-09-58;LOW
84756;Печенье, Сыр, Печенье, Сыр;Васильева Анна Владимировна;Япония. Шибуя. Шибуя-кроссинг;+8-131-234-5678;MAX
90385;Макароны, Сыр, Макароны, Сыр;Николаев Николай;;+1-416-123-45-67;LOW
"""

    input_path.write_text(input_data, encoding="utf-8")
    process_orders(input_path, valid_path, invalid_path)
    expected_valid = (
        "87459;Молоко x2, Яблоки x2, Хлеб;Иванов Иван Иванович;"
        "Московская область. Москва. улица Пушкина;"
        "+7-912-345-67-89;MAX\n"
        "31987;Сыр x2, Колбаса x2, Макароны;Петрова Анна;"
        "Ленинградская область. Санкт-Петербург. "
        "набережная реки Фонтанки;+7-921-456-78-90;MIDDLE\n"
        "72901;Чай x2, Кофе x2;Михайлов Сергей Петрович;"
        "Англия. Лондон. Бейкер-стрит;+4-207-946-09-58;LOW\n"
        "48276;Яблоки x2, Макароны;Алексеев Алексей Алексеевич;"
        "Лацио. Рим. Колизей;+3-061-234-56-78;MAX\n"
        "31987;Сыр x2, Колбаса x2, Макароны;Петрова Анна Сергеевна;"
        "Иль-де-Франс. Париж. Шанз-Элизе;+3-214-020-50-50;MIDDLE\n"
    )
    expected_invalid = (
        "56342;2;+4-989-234-56\n"
        "65829;2;+34-93-1234-567\n"
        "84756;2;+8-131-234-5678\n"
        "84756;1;Япония. Шибуя. Шибуя-кроссинг\n"
        "90385;1;no data\n"
    )
    assert valid_path.read_text(encoding="utf-8") == expected_valid
    assert invalid_path.read_text(encoding="utf-8") == expected_invalid


def test_missing_address_and_phone(tmp_path):
    """проверка пустого адреса и телефона"""
    input_path = tmp_path / "orders.txt"
    valid_path = tmp_path / "order_country.txt"
    invalid_path = tmp_path / "non_valid_orders.txt"
    input_path.write_text(
        "12345;Молоко, Хлеб;Иванов Иван;; ;MAX\n",
        encoding="utf-8",
    )
    process_orders(input_path, valid_path, invalid_path)
    assert valid_path.read_text(encoding="utf-8") == ""
    assert invalid_path.read_text(encoding="utf-8") == (
        "12345;2;no data\n" "12345;1;no data\n"
    )
