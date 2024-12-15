#!/bin/bash

source ../.secrets.sh

export PGPASSWORD="$DB_PASSWORD"

psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    is_sale BOOLEAN DEFAULT FALSE,
    inventory INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"

echo "Table 'products' created successfully."

psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "
INSERT INTO products (name, price, is_sale, inventory) VALUES
('Wireless Mouse', 25.99, FALSE, 100),
('Gaming Keyboard', 49.99, TRUE, 50),
('4K Monitor', 299.99, FALSE, 25),
('Bluetooth Speaker', 19.99, TRUE, 75),
('External SSD', 89.99, FALSE, 40),
('USB-C Hub', 34.99, TRUE, 60),
('Noise Cancelling Headphones', 199.99, FALSE, 30),
('Webcam 1080p', 45.99, TRUE, 45),
('Ergonomic Office Chair', 129.99, FALSE, 20),
('Portable Charger', 29.99, TRUE, 150);
"

echo "Mock data inserted into 'products' table successfully."

