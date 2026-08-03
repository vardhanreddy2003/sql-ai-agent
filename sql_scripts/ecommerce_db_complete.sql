
DROP DATABASE IF EXISTS ecommerce_db;
CREATE DATABASE ecommerce_db;
USE ecommerce_db;

-- ==========================
-- CUSTOMERS
-- ==========================
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    registration_date DATE,
    loyalty_points INT,
    customer_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ==========================
-- CATEGORIES
-- ==========================
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- SUPPLIERS
-- ==========================
CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_name VARCHAR(100),
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- PRODUCTS
-- ==========================
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100),
    category_id INT,
    supplier_id INT,
    description TEXT,
    price DECIMAL(10,2),
    stock_quantity INT,
    sku VARCHAR(50) UNIQUE,
    weight DECIMAL(8,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- ==========================
-- ORDERS
-- ==========================
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

-- ==========================
-- ORDER ITEMS
-- ==========================
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    discount DECIMAL(10,2),
    subtotal DECIMAL(10,2),
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    payment_date DATE,
    payment_method VARCHAR(30),
    amount DECIMAL(10,2),
    payment_status VARCHAR(20),
    transaction_id VARCHAR(100),
    FOREIGN KEY(order_id) REFERENCES orders(order_id)
);

CREATE TABLE shipments (
    shipment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    courier_name VARCHAR(100),
    tracking_number VARCHAR(100),
    shipped_date DATE,
    delivered_date DATE,
    shipment_status VARCHAR(30),
    FOREIGN KEY(order_id) REFERENCES orders(order_id)
);

CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    product_id INT,
    rating INT,
    review_text TEXT,
    review_date DATE,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

CREATE TABLE inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    warehouse_location VARCHAR(100),
    available_stock INT,
    reserved_stock INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    department VARCHAR(50),
    designation VARCHAR(50),
    hire_date DATE,
    salary DECIMAL(10,2)
);

CREATE TABLE coupons (
    coupon_id INT PRIMARY KEY AUTO_INCREMENT,
    coupon_code VARCHAR(30),
    discount_percentage DECIMAL(5,2),
    minimum_order_amount DECIMAL(10,2),
    expiry_date DATE,
    status VARCHAR(20)
);

CREATE TABLE wishlists (
    wishlist_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    product_id INT,
    added_date DATE,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

-- SAMPLE DATA

INSERT INTO categories(category_name,description) VALUES
('Electronics','Electronic products'),
('Furniture','Home furniture'),
('Books','Books'),
('Clothing','Apparel'),
('Sports','Sports equipment');

INSERT INTO suppliers(supplier_name,contact_person,email,phone,city,country) VALUES
('Dell','John Carter','john@dell.com','1111111111','Austin','USA'),
('Samsung','Emily Watson','emily@samsung.com','2222222222','Seoul','South Korea'),
('Logitech','Sophia Brown','sophia@logitech.com','3333333333','Lausanne','Switzerland'),
('LG','Kevin Lee','kevin@lg.com','4444444444','Seoul','South Korea'),
('IKEA','David Miller','david@ikea.com','5555555555','Stockholm','Sweden');

INSERT INTO customers(first_name,last_name,email,phone_number,date_of_birth,gender,address,city,state,country,postal_code,registration_date,loyalty_points,customer_status) VALUES
('Alice','Johnson','alice@example.com','9876543210','1995-06-15','Female','12 Park Street','New York','New York','USA','10001','2024-01-15',250,'Active'),
('Bob','Smith','bob@example.com','9876543211','1990-02-20','Male','45 Lake View','Chicago','Illinois','USA','60601','2024-02-10',120,'Active'),
('Charlie','Brown','charlie@example.com','9876543212','1998-08-12','Male','78 Hill Road','Los Angeles','California','USA','90001','2024-03-18',50,'Inactive'),
('Diana','Miller','diana@example.com','9876543213','1992-12-10','Female','90 River Lane','Dallas','Texas','USA','75201','2024-04-01',300,'Active'),
('Emma','Wilson','emma@example.com','9876543214','1996-09-09','Female','55 Sunset Blvd','Miami','Florida','USA','33101','2024-05-12',180,'Active');

INSERT INTO products(product_name,category_id,supplier_id,description,price,stock_quantity,sku,weight) VALUES
('Laptop',1,1,'15-inch business laptop',950,30,'LAP1001',2.1),
('Wireless Mouse',1,3,'Wireless mouse',25,200,'MOU1002',0.15),
('Mechanical Keyboard',1,3,'RGB keyboard',80,100,'KEY1003',0.9),
('Smartphone',1,2,'Android smartphone',700,50,'PHN1004',0.25),
('Office Chair',2,5,'Ergonomic chair',180,20,'CHR1005',12.5),
('Monitor',1,4,'27-inch IPS monitor',250,40,'MON1006',5.5);

INSERT INTO orders(customer_id,order_date,order_status,amount,discount,tax,shipping_charge,payment_method,payment_status,shipping_address,delivery_date) VALUES
(1,'2025-07-01','Delivered',1000,20,70,10,'Credit Card','Paid','12 Park Street','2025-07-05'),
(2,'2025-07-03','Shipped',275,10,18,8,'UPI','Paid','45 Lake View','2025-07-07'),
(1,'2025-07-10','Pending',250,0,17.5,5,'PayPal','Pending','12 Park Street',NULL),
(4,'2025-07-12','Delivered',880,30,60,15,'Debit Card','Paid','90 River Lane','2025-07-16'),
(5,'2025-07-15','Cancelled',180,0,12.6,10,'Credit Card','Refunded','55 Sunset Blvd',NULL);

INSERT INTO order_items(order_id,product_id,quantity,unit_price,discount,subtotal) VALUES
(1,1,1,950,20,930),
(1,2,2,25,0,50),
(2,6,1,250,10,240),
(2,2,1,25,0,25),
(3,6,1,250,0,250),
(4,4,1,700,20,680),
(4,3,1,80,10,70),
(4,2,5,25,0,125),
(5,5,1,180,0,180);

INSERT INTO payments(order_id,payment_date,payment_method,amount,payment_status,transaction_id) VALUES
(1,'2025-07-01','Credit Card',1000,'Paid','TXN10001'),
(2,'2025-07-03','UPI',275,'Paid','TXN10002'),
(3,'2025-07-10','PayPal',250,'Pending','TXN10003'),
(4,'2025-07-12','Debit Card',880,'Paid','TXN10004'),
(5,'2025-07-15','Credit Card',180,'Refunded','TXN10005');

INSERT INTO shipments(order_id,courier_name,tracking_number,shipped_date,delivered_date,shipment_status) VALUES
(1,'FedEx','FDX10001','2025-07-02','2025-07-05','Delivered'),
(2,'UPS','UPS10002','2025-07-04',NULL,'In Transit'),
(3,'DHL','DHL10003',NULL,NULL,'Pending'),
(4,'FedEx','FDX10004','2025-07-13','2025-07-16','Delivered'),
(5,'UPS','UPS10005',NULL,NULL,'Cancelled');

INSERT INTO reviews(customer_id,product_id,rating,review_text,review_date) VALUES
(1,1,5,'Excellent laptop','2025-07-08'),
(2,2,4,'Good mouse','2025-07-09'),
(3,3,5,'Amazing keyboard','2025-07-15'),
(4,4,3,'Average phone','2025-07-18'),
(5,5,4,'Comfortable chair','2025-07-20');

INSERT INTO inventory(product_id,warehouse_location,available_stock,reserved_stock) VALUES
(1,'Warehouse A',25,5),
(2,'Warehouse A',180,20),
(3,'Warehouse B',90,10),
(4,'Warehouse B',40,10),
(5,'Warehouse C',15,5),
(6,'Warehouse A',35,5);

INSERT INTO employees(first_name,last_name,email,department,designation,hire_date,salary) VALUES
('Michael','Scott','michael@company.com','Sales','Manager','2020-01-10',85000),
('Jim','Halpert','jim@company.com','Sales','Executive','2021-03-15',55000),
('Pam','Beesly','pam@company.com','HR','HR Executive','2022-06-20',50000),
('Dwight','Schrute','dwight@company.com','Warehouse','Supervisor','2019-11-05',70000),
('Angela','Martin','angela@company.com','Finance','Accountant','2020-09-12',65000);

INSERT INTO coupons(coupon_code,discount_percentage,minimum_order_amount,expiry_date,status) VALUES
('SAVE10',10,100,'2026-12-31','Active'),
('SAVE20',20,500,'2026-10-31','Active'),
('WELCOME15',15,150,'2026-08-31','Expired'),
('FREESHIP',5,50,'2026-11-30','Active'),
('NEWUSER',25,300,'2026-09-30','Inactive');

INSERT INTO wishlists(customer_id,product_id,added_date) VALUES
(1,4,'2025-07-02'),
(1,5,'2025-07-05'),
(2,1,'2025-07-03'),
(3,6,'2025-07-08'),
(4,2,'2025-07-10'),
(5,3,'2025-07-12');