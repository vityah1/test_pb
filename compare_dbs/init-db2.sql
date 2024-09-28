CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    ProductId  VARCHAR(29),
    ProductName VARCHAR(255),
    ProductProperty1 VARCHAR(255),
    ProductProperty2 VARCHAR(255),
    ProductProperty3 VARCHAR(255),
    ProductProperty4 VARCHAR(255),
    ProductProperty5 VARCHAR(255),
    ProductProperty6 VARCHAR(255),
    ProductProperty7 VARCHAR(255),
    ProductProperty8 VARCHAR(255),
    ProductProperty9 VARCHAR(255),
    ProductProperty10 VARCHAR(255),
    qty INT,
    price DECIMAL(10, 2),
    TotalCost DECIMAL(10, 2)
);

INSERT INTO inventory (ProductId, ProductName, ProductProperty1, ProductProperty2, ProductProperty3, qty, price, TotalCost)
VALUES
    ('0001', 'Product A', 'Red', 'Large', 'Electronics', 100, 10.00, 1000.00),
    ('0002', 'Product B', 'Blue', 'Large', 'Clothing', 150, 16.00, 2400.00),
    ('0003', 'Product C', 'Green', 'Small', 'Kitchen', 180, 22.00, 3960.00),
    ('0006', 'Product F', 'Orange', 'Standard', 'Gadgets', 75, 30.00, 2250.00),
    ('0007', 'Product G', 'Pink', 'Compact', 'Beauty', 250, 8.00, 2000.00);