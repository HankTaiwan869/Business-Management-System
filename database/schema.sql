-- Create customers table
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    discount REAL
);

-- Create cycles table
CREATE TABLE cycles (
    id INTEGER PRIMARY KEY,
    start_date TEXT NOT NULL,
    end_date TEXT
);

-- Create products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Create suppliers table
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Create customer_orders table
CREATE TABLE customer_orders (
    cycle_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    actual_price REAL NOT NULL,
    created_at_timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (cycle_id, customer_id, product_id),
    FOREIGN KEY (cycle_id) REFERENCES cycles(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Create product_prices table
CREATE TABLE product_prices (
    cycle_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    price REAL NOT NULL,
    created_at_timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (cycle_id, product_id),
    FOREIGN KEY (cycle_id) REFERENCES cycles(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Create supply_orders table
CREATE TABLE supply_orders (
    cycle_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    created_at_timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (cycle_id, supplier_id, product_id),
    FOREIGN KEY (cycle_id) REFERENCES cycles(id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
