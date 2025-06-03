-- Tabla: countries
CREATE TABLE IF NOT EXISTS countries (
    country_id INT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(10) NOT NULL
);

-- Tabla: cities
CREATE TABLE IF NOT EXISTS cities (
    city_id INT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    zipcode INT NOT NULL,
    country_id INT NOT NULL  
);

-- Tabla: customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_initial CHAR(1),
    last_name VARCHAR(100) NOT NULL,
    city_id INT NOT NULL,  
    address VARCHAR(255)
);

-- Tabla: categories
CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- Tabla: employees
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_initial CHAR(1),
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    gender CHAR(1) NOT NULL,
    city_id INT NOT NULL,  
    hire_date DATE NOT NULL
);

-- Tabla: products
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category INT NOT NULL,  
    class_type VARCHAR(50),
    modify_date DATE NOT NULL,
    resistant VARCHAR(50),
    is_allergic BOOLEAN,
    vitality_days INT NOT NULL
);

-- Tabla: sales
CREATE TABLE IF NOT EXISTS sales (
    sales_id INT PRIMARY KEY,
    sales_person_id INT NOT NULL,  
    customer_id INT NOT NULL,      
    product_id INT NOT NULL,       
    quantity INT NOT NULL,
    discount DECIMAL(5, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    sales_date DATETIME NOT NULL,
    transaction_number VARCHAR(50) NOT NULL
);
