# Додаток для звірки залишків товарів на складах

## Опис завдання

Необхідно розробити додаток на Python, який здійснюватиме звірку залишків товарів на двох різних складах. Залишки на складах ведуться в таблицях у різних базах даних (СУБД можна використовувати PostgreSQL або Oracle будь-яких версій).

### Перелік полів таблиці із залишками:

- `ProductId` (primary key)
- `ProductName`
- `ProductProperty1`
- `ProductProperty2`
- `ProductProperty3` ... `ProductProperty10`
- `qty`
- `price`
- `TotalCost`

### Вимоги до звірки:

Звіряння потрібно здійснити за допомогою **PySpark**. В результаті необхідно отримати три CSV файли:

1. **Товари, які є на складі №1 і відсутні на складі №2**:
    - Поля результуючого файлу: `ProductId`, `ProductName`, `qty`, `TotalCost`.

2. **Товари, які є на складі №2 і відсутні на складі №1**:
    - Поля результуючого файлу: `ProductId`, `ProductName`, `qty`, `TotalCost`.

3. **Товари, які є на обох складах, але у яких відрізняються властивості**:
    - Поля результуючого файлу: `ProductId`, `PropertyName`, `Value1`, `Value2`.

## Використання Docker

Бази даних та додаток необхідно "підняти" в окремих контейнерах за допомогою **docker-compose**. Підставте своє значення IP у файлі **docker-compose.yml**

### Запуск проєкту

Для запуску проєкту скористайтесь командою:

```bash
docker-compose up --build

