CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0)
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    ordered_at DATE NOT NULL
);

CREATE TABLE order_items (
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

CREATE INDEX orders_customer_date ON orders (customer_id, ordered_at);
CREATE INDEX order_items_product ON order_items (product_id);
