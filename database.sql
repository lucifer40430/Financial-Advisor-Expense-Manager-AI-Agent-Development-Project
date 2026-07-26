CREATE DATABASE financial_advisor;
USE financial_advisor;
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    merchant VARCHAR(100),
    category VARCHAR(50),
    payment_method VARCHAR(50),
    expense_date DATE,
    image_path VARCHAR(255),

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);
CREATE TABLE budget (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(50),
    monthly_limit DECIMAL(10,2),

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255),
    file_path VARCHAR(255),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);
CREATE TABLE chats (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question TEXT,
    response TEXT,
    chat_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);
SHOW TABLES;
INSERT INTO users(name,email,password)
VALUES
('Pawan','pawan@gmail.com','123456');
INSERT INTO expenses
(user_id,amount,merchant,category,payment_method,expense_date,image_path)

VALUES
(1,450.00,'Swiggy','Food','UPI','2026-07-26','uploads/swiggy.png');
INSERT INTO budget(user_id,category,monthly_limit)

VALUES
(1,'Food',5000);
INSERT INTO books(user_id,title,file_path)

VALUES
(1,'Rich Dad Poor Dad','uploads/books/richdad.pdf');
SELECT * FROM users;
