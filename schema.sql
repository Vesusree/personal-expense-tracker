
-- Personal Expense Tracking and Analysis System
-- Database schema documentation
-- Based on the existing MySQL tables.
-- This file documents the schema; do not run against a live database
-- without first reviewing the existing tables.

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_verified TINYINT(1) NOT NULL DEFAULT 0,
    verification_token_hash CHAR(64) DEFAULT NULL,
    verification_expires_at DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE categories (
    category_id INT NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (category_id)
);


CREATE TABLE expenses (
    expense_id INT NOT NULL AUTO_INCREMENT,
    expense_date DATE NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255) DEFAULT NULL,
    payment_method VARCHAR(50) DEFAULT NULL,
    user_id INT DEFAULT NULL,
    PRIMARY KEY (expense_id),
    KEY expenses_ibfk_1 (category_id),
    CONSTRAINT expenses_ibfk_1
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);
