customers (
    customer_id      INT PRIMARY KEY,
    first_name       VARCHAR(50),
    last_name        VARCHAR(50),
    email            VARCHAR(100) UNIQUE,
    phone_number     VARCHAR(20),
    date_of_birth    DATE,
    gender           VARCHAR(10),
    address          VARCHAR(255),
    city             VARCHAR(100),
    state            VARCHAR(100),
    country          VARCHAR(100),
    postal_code      VARCHAR(20),
    registration_date DATE,
    loyalty_points   INT,
    customer_status  VARCHAR(20),
    created_at       TIMESTAMP,
    updated_at       TIMESTAMP
);

orders (
    order_id         INT PRIMARY KEY,
    customer_id      INT,
    order_date       DATE,
    order_status     VARCHAR(20),
    amount           DECIMAL(10,2),
    discount         DECIMAL(10,2),
    tax              DECIMAL(10,2),
    shipping_charge  DECIMAL(10,2),
    payment_method   VARCHAR(30),
    payment_status   VARCHAR(20),
    shipping_address VARCHAR(255),
    delivery_date    DATE,
    created_at       TIMESTAMP,
    updated_at       TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

products (
    product_id       INT PRIMARY KEY,
    product_name     VARCHAR(100),
    category         VARCHAR(50),
    brand            VARCHAR(50),
    description      TEXT,
    price            DECIMAL(10,2),
    stock_quantity   INT,
    supplier_name    VARCHAR(100),
    sku              VARCHAR(50),
    weight           DECIMAL(8,2),
    created_at       TIMESTAMP,
    updated_at       TIMESTAMP
);

order_items (
    order_item_id    INT PRIMARY KEY,
    order_id         INT,
    product_id       INT,
    quantity         INT,
    unit_price       DECIMAL(10,2),
    discount         DECIMAL(10,2),
    subtotal         DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);