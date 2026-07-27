-- Create Database
CREATE DATABASE ecommerce_db;
USE ecommerce_db;

-- ==========================
-- Customers Table
-- ==========================
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    registration_date DATE,
    loyalty_points INT DEFAULT 0,
    customer_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

-- ==========================
-- Products Table
-- ==========================
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    brand VARCHAR(50),
    description TEXT,
    price DECIMAL(10,2),
    stock_quantity INT,
    supplier_name VARCHAR(100),
    sku VARCHAR(50) UNIQUE,
    weight DECIMAL(8,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

-- ==========================
-- Orders Table
-- ==========================
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE,
    order_status VARCHAR(20),
    amount DECIMAL(10,2),
    discount DECIMAL(10,2),
    tax DECIMAL(10,2),
    shipping_charge DECIMAL(10,2),
    payment_method VARCHAR(30),
    payment_status VARCHAR(20),
    shipping_address VARCHAR(255),
    delivery_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ==========================
-- Order Items Table
-- ==========================
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT,
    unit_price DECIMAL(10,2),
    discount DECIMAL(10,2),
    subtotal DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- =====================================================
-- Insert Customers
-- =====================================================
INSERT INTO customers
(first_name, last_name, email, phone_number, date_of_birth, gender,
 address, city, state, country, postal_code,
 registration_date, loyalty_points, customer_status)
VALUES
('Alice','Johnson','alice@example.com','9876543210','1995-06-15','Female',
 '12 Park Street','New York','New York','USA','10001',
 '2024-01-15',250,'Active'),

('Bob','Smith','bob@example.com','9876543211','1990-02-20','Male',
 '45 Lake View','Chicago','Illinois','USA','60601',
 '2024-02-10',120,'Active'),

('Charlie','Brown','charlie@example.com','9876543212','1998-08-12','Male',
 '78 Hill Road','Los Angeles','California','USA','90001',
 '2024-03-18',50,'Inactive'),

('Diana','Miller','diana@example.com','9876543213','1992-12-10','Female',
 '90 River Lane','Dallas','Texas','USA','75201',
 '2024-04-01',300,'Active'),

('Emma','Wilson','emma@example.com','9876543214','1996-09-09','Female',
 '55 Sunset Blvd','Miami','Florida','USA','33101',
 '2024-05-12',180,'Active');

-- =====================================================
-- Insert Products
-- =====================================================
INSERT INTO products
(product_name, category, brand, description,
 price, stock_quantity, supplier_name, sku, weight)
VALUES
('Laptop','Electronics','Dell','15-inch business laptop',
950.00,30,'Dell Inc.','LAP1001',2.10),

('Wireless Mouse','Electronics','Logitech','Wireless optical mouse',
25.00,200,'Logitech','MOU1002',0.15),

('Mechanical Keyboard','Electronics','Keychron','RGB Mechanical Keyboard',
80.00,100,'Keychron','KEY1003',0.90),

('Smartphone','Electronics','Samsung','Android smartphone',
700.00,50,'Samsung','PHN1004',0.25),

('Office Chair','Furniture','IKEA','Ergonomic office chair',
180.00,20,'IKEA','CHR1005',12.50),

('Monitor','Electronics','LG','27-inch IPS Monitor',
250.00,40,'LG','MON1006',5.50);

-- =====================================================
-- Insert Orders
-- =====================================================
INSERT INTO orders
(customer_id, order_date, order_status,
 amount, discount, tax, shipping_charge,
 payment_method, payment_status,
 shipping_address, delivery_date)
VALUES
(1,'2025-07-01','Delivered',
1000.00,20.00,70.00,10.00,
'Credit Card','Paid',
'12 Park Street, New York','2025-07-05'),

(2,'2025-07-03','Shipped',
275.00,10.00,18.00,8.00,
'UPI','Paid',
'45 Lake View, Chicago','2025-07-07'),

(1,'2025-07-10','Pending',
250.00,0.00,17.50,5.00,
'PayPal','Pending',
'12 Park Street, New York',NULL),

(4,'2025-07-12','Delivered',
880.00,30.00,60.00,15.00,
'Debit Card','Paid',
'90 River Lane, Dallas','2025-07-16'),

(5,'2025-07-15','Cancelled',
180.00,0.00,12.60,10.00,
'Credit Card','Refunded',
'55 Sunset Blvd, Miami',NULL);

-- =====================================================
-- Insert Order Items
-- =====================================================
INSERT INTO order_items
(order_id, product_id, quantity,
 unit_price, discount, subtotal)
VALUES

-- Order 1
(1,1,1,950.00,20.00,930.00),
(1,2,2,25.00,0.00,50.00),

-- Order 2
(2,6,1,250.00,10.00,240.00),
(2,2,1,25.00,0.00,25.00),

-- Order 3
(3,6,1,250.00,0.00,250.00),

-- Order 4
(4,4,1,700.00,20.00,680.00),
(4,3,1,80.00,10.00,70.00),
(4,2,5,25.00,0.00,125.00),

-- Order 5
(5,5,1,180.00,0.00,180.00);