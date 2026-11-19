"""Обработка заказов интернет магазина"""

import re
from dataclasses import dataclass
from pathlib import Path

PHONE_PATTERN = re.compile(r"^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$")

PRIORITY_ORDER = {
    "MAX": 0,
    "MIDDLE": 1,
    "LOW": 2,
}
RUSSIAN_COUNTRIES = {
    "россия",
    "российская федерация",
}
AddressParts = tuple[str, str, str, str]


@dataclass(frozen=True)
class Order:
    """Заказ"""

    number: str
    products: tuple[str, ...]
    customer: str
    address: str
    phone: str
    priority: str

    def format_products(self) -> str:
        """Объединяет подобные товары и их кол-во"""
        counts: dict[str, int] = {}
        for product in self.products:
            counts[product] = counts.get(product, 0) + 1
        formatted_products = []
        for product, count in counts.items():
            if count > 1:
                formatted_products.append(f"{product} x{count}")
            else:
                formatted_products.append(product)

        return ", ".join(formatted_products)

    def format_valid_order(self, address_parts: AddressParts) -> str:
        """Делает строку правильного заказа"""
        _, region, city, street = address_parts

        return (
            f"{self.number};"
            f"{self.format_products()};"
            f"{self.customer};"
            f"{region}. {city}. {street};"
            f"{self.phone};"
            f"{self.priority}"
        )


def is_valid_phone(phone: str) -> bool:
    """Проверка номера телефона"""
    return PHONE_PATTERN.fullmatch(phone) is not None


def parse_address(address: str) -> AddressParts | None:
    """Проверка наличия четырёх частей вдреса"""
    parts = tuple(part.strip() for part in address.split("."))
    if len(parts) != 4:
        return None
    if any(not part for part in parts):
        return None
    return parts[0], parts[1], parts[2], parts[3]


def parse_order(line: str, line_number: int = 1) -> Order:
    """Разбор строки файла и создание заказа"""
    columns = [column.strip() for column in line.rstrip("\r\n").split(";")]

    if len(columns) != 6:
        raise ValueError(
            f"Строка {line_number}: ожидалось 6 полей, " f"получено {len(columns)}."
        )
    number, products_text, customer, address, phone, priority = columns

    if not re.fullmatch(r"[0-9]{5}", number):
        raise ValueError(
            f"Строка {line_number}: номер заказа должен состоять " "из пяти цифр."
        )
    if not products_text:
        raise ValueError(f"Строка {line_number}: список продуктов пуст.")
    products = tuple(product.strip() for product in products_text.split(","))
    if any(not product for product in products):
        raise ValueError(f"Строка {line_number}: обнаружено пустое название продукта.")
    if len(customer.split()) not in (2, 3):
        raise ValueError(f"Строка {line_number}: некорректное ФИО заказчика.")
    if priority not in PRIORITY_ORDER:
        raise ValueError(f"Строка {line_number}: неизвестный приоритет доставки.")
    return Order(
        number=number,
        products=products,
        customer=customer,
        address=address,
        phone=phone,
        priority=priority,
    )


def order_sort_key(order: Order) -> tuple[int, str, int]:
    """Возвращает ключ по стране, приоритету"""
    address_parts = parse_address(order.address)

    if address_parts is None:
        raise ValueError("Нельзя сортировать заказ с неправильным адресом.")
    country = address_parts[0].casefold()
    if country in RUSSIAN_COUNTRIES:
        country_group = 0
        country_name = ""
    else:
        country_group = 1
        country_name = country
    return (
        country_group,
        country_name,
        PRIORITY_ORDER[order.priority],
    )


def write_lines(path: Path, lines: list[str]) -> None:
    """Записывает строки в UTF-8"""
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(lines)
    if content:
        content += "\n"

    path.write_text(content, encoding="utf-8")


def process_orders(
    input_path: Path,
    valid_output_path: Path,
    invalid_output_path: Path,
) -> None:
    """Читает, проверяет, сортирует,сохраняет заказы."""
    valid_orders: list[tuple[Order, AddressParts]] = []
    invalid_lines = []

    with input_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            order = parse_order(line, line_number)

            address_parts = parse_address(order.address)
            phone_is_valid = is_valid_phone(order.phone)

            # Сначала записываем ошибку телефона.
            if not phone_is_valid:
                phone_value = order.phone or "no data"
                invalid_lines.append(f"{order.number};2;{phone_value}")

            # Затем записываем ошибку адреса.
            if address_parts is None:
                address_value = order.address or "no data"
                invalid_lines.append(f"{order.number};1;{address_value}")

            # В итоговый файл попадают только полностью правильные заказы.
            if phone_is_valid and address_parts is not None:
                valid_orders.append((order, address_parts))

    valid_orders.sort(key=lambda item: order_sort_key(item[0]))
    valid_lines = [
        order.format_valid_order(address_parts) for order, address_parts in valid_orders
    ]
    write_lines(valid_output_path, valid_lines)
    write_lines(invalid_output_path, invalid_lines)


def main() -> None:
    """Запускает обработку заказов"""
    process_orders(
        input_path=Path("orders.txt"),
        valid_output_path=Path("order_country.txt"),
        invalid_output_path=Path("non_valid_orders.txt"),
    )
    print("Обработка заказов завершена.")
    print("Правильные заказы сохранены в order_country.txt.")
    print("Ошибки сохранены в non_valid_orders.txt.")


if __name__ == "__main__":
    main()
