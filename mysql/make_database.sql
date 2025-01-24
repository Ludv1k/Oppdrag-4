CREATE DATABASE geir_book;

USE geir_book;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_of_book VARCHAR(50) NOT NULL,
    author VARCHAR(50) NOT NULL,
    language_for_translation VARCHAR(50) NOT NULL
);