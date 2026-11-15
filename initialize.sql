-- Create database
CREATE DATABASE library_management;
USE library_management;

-- Create users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    user_type ENUM('admin', 'user') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create books table
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    quantity INT DEFAULT 1,
    available_quantity INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id INT,
    transaction_type ENUM('issue', 'return') NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE,
    status ENUM('active', 'completed') DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Insert default admin user
INSERT INTO users (username, password, user_type) 
VALUES ('admin', 'admin123', 'admin');

-- Insert some sample books
INSERT INTO books (title, author, isbn, quantity, available_quantity) VALUES
('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 3, 3),
('1984', 'George Orwell', '9780451524935', 2, 2),
('Pride and Prejudice', 'Jane Austen', '9780141439518', 4, 4),
('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 2, 2);