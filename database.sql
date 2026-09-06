-- ==========================================
-- FinSight AI Database
-- Financial Advisor & Expense Manager
-- ==========================================

-- Create Database
DROP DATABASE IF EXISTS financial_advisor;
CREATE DATABASE financial_advisor;
USE financial_advisor;

-- ==========================================
-- USERS TABLE
-- ==========================================

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- INCOME TABLE
-- ==========================================

CREATE TABLE income (
    income_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    source VARCHAR(100),
    amount DECIMAL(10,2) NOT NULL,
    income_date DATE,

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);

-- ==========================================
-- EXPENSES TABLE
-- ==========================================

CREATE TABLE expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    amount DECIMAL(10,2) NOT NULL,

    merchant_name VARCHAR(150),

    category ENUM(
        'Food',
        'Travel',
        'Shopping',
        'Bills',
        'Entertainment',
        'Health',
        'Education',
        'Other'
    ) DEFAULT 'Other',

    payment_method VARCHAR(50),

    transaction_id VARCHAR(100),

    expense_date DATE,

    image_path VARCHAR(255),

    ocr_status ENUM(
        'Pending',
        'Completed',
        'Failed'
    ) DEFAULT 'Completed',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);

-- ==========================================
-- BUDGET TABLE
-- ==========================================

CREATE TABLE budget (

    budget_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    category ENUM(
        'Food',
        'Travel',
        'Shopping',
        'Bills',
        'Entertainment',
        'Health',
        'Education',
        'Other'
    ),

    monthly_limit DECIMAL(10,2),

    budget_month DATE,

    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);

-- ==========================================
-- BOOKS TABLE
-- ==========================================

CREATE TABLE books (

    book_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    title VARCHAR(255),

    author VARCHAR(150),

    file_path VARCHAR(255),

    file_type VARCHAR(20),

    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);

-- ==========================================
-- CHAT HISTORY
-- ==========================================

CREATE TABLE chats (

    chat_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    question TEXT,

    response TEXT,

    chat_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);

-- ==========================================
-- SAMPLE DATA
-- ==========================================

INSERT INTO users(name,email,password)
VALUES
('Pawan','pawan@gmail.com','123456');

INSERT INTO income
(user_id,source,amount,income_date)
VALUES
(1,'Monthly Salary',50000,'2026-08-01');

INSERT INTO expenses
(
user_id,
amount,
merchant_name,
category,
payment_method,
transaction_id,
expense_date,
image_path,
ocr_status
)

VALUES
(
1,
450.00,
'Swiggy',
'Food',
'UPI',
'UPI123456789',
'2026-07-26',
'uploads/swiggy.png',
'Completed'
);

INSERT INTO budget
(
user_id,
category,
monthly_limit,
budget_month
)

VALUES
(
1,
'Food',
5000,
'2026-08-01'
);

INSERT INTO books
(
user_id,
title,
author,
file_path,
file_type
)

VALUES
(
1,
'Rich Dad Poor Dad',
'Robert Kiyosaki',
'uploads/books/richdad.pdf',
'PDF'
);

INSERT INTO chats
(
user_id,
question,
response
)

VALUES
(
1,
'How can I save more money?',
'Reduce unnecessary food expenses and follow a monthly budget.'
);

-- ==========================================
-- VERIFY TABLES
-- ==========================================

SHOW TABLES;

-- ==========================================
-- VIEW DATA
-- ==========================================

SELECT * FROM users;

SELECT * FROM income;

SELECT * FROM expenses;

SELECT * FROM budget;

SELECT * FROM books;

SELECT * FROM chats;