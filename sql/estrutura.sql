CREATE DATABASE IF NOT EXISTS fashion_db;
USE fashion_db;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT,
    product_type VARCHAR(100),
    category VARCHAR(100),
    brand VARCHAR(150),
    price DECIMAL(10,2)
);

CREATE TABLE sizes (
    size_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    size VARCHAR(20),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);