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
    ('0002', 'Product B', 'Blue', 'Medium', 'Clothing', 150, 15.00, 2250.00),
    ('0003', 'Product C', 'Green', 'Small', 'Kitchen', 200, 20.00, 4000.00),
    ('0004', 'Product D', 'Yellow', 'Extra Large', 'Furniture', 50, 25.00, 1250.00),
    ('0005', 'Product E', 'Purple', 'Tiny', 'Accessories', 300, 5.00, 1500.00);