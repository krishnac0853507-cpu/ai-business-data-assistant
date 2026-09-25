CREATE TABLE sales (
    order_id SERIAL PRIMARY KEY,
    order_date DATE,
    customer_name VARCHAR(100),
    region VARCHAR(50),
    product VARCHAR(100),
    category VARCHAR(50),
    quantity INT,
    unit_price NUMERIC(10,2),
    discount_pct NUMERIC(5,2),
    revenue NUMERIC(12,2)
);


INSERT INTO sales
(order_date, customer_name, region, product, category, quantity, unit_price, discount_pct, revenue)
VALUES
('2026-08-01', 'Arun', 'South', 'Laptop', 'Electronics', 2, 65000, 5, 123500),
('2026-08-02', 'Meera', 'West', 'Headphones', 'Electronics', 5, 3000, 10, 13500),
('2026-08-03', 'Rahul', 'South', 'Office Chair', 'Furniture', 3, 8500, 5, 24225),
('2026-08-05', 'Anjali', 'North', 'Laptop', 'Electronics', 1, 70000, 10, 63000),
('2026-08-07', 'Vishnu', 'East', 'Keyboard', 'Accessories', 10, 1500, 5, 14250),
('2026-08-10', 'Akhil', 'South', 'Monitor', 'Electronics', 4, 18000, 5, 68400),
('2026-08-12', 'Sneha', 'West', 'Laptop', 'Electronics', 2, 68000, 8, 124800),
('2026-08-15', 'Fahad', 'North', 'Mouse', 'Accessories', 15, 1200, 5, 17100),
('2026-08-18', 'Devika', 'East', 'Office Desk', 'Furniture', 2, 15000, 10, 27000),
('2026-08-20', 'Nikhil', 'South', 'Headphones', 'Electronics', 8, 3500, 5, 26600),
('2026-08-22', 'Amal', 'West', 'Monitor', 'Electronics', 3, 17500, 10, 47250),
('2026-08-25', 'Athira', 'North', 'Keyboard', 'Accessories', 12, 1600, 5, 18240),
('2026-08-27', 'Joel', 'East', 'Laptop', 'Electronics', 1, 72000, 5, 68400),
('2026-08-29', 'Gokul', 'South', 'Office Chair', 'Furniture', 4, 9000, 10, 32400),
('2026-08-30', 'Diya', 'West', 'Mouse', 'Accessories', 20, 1100, 5, 20900);

SELECT * FROM sales;
drop table sales;