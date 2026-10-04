INSERT INTO categories (name) VALUES ('Электроника'), ('Книги'), ('Одежда');

INSERT INTO products (name, category_id, price) VALUES
    ('Ноутбук', 1, 95000), ('Наушники', 1, 7000), ('Смартфон', 1, 60000), ('Кабель USB-C', 1, 900),
    ('Чистый код', 2, 1200), ('Мастер и Маргарита', 2, 600), ('SQL для чайников', 2, 1800),
    ('Футболка', 3, 1500), ('Худи', 3, 4500), ('Носки', 3, 300);

INSERT INTO customers (full_name, email) VALUES
    ('Анна Волкова', 'anna@example.com'), ('Борис Егоров', 'boris@example.com'), ('Вера Захарова', 'vera@example.com'),
    ('Глеб Иванов', 'gleb@example.com'), ('Дарья Ким', 'darya@example.com');

INSERT INTO orders (customer_id, ordered_at) VALUES
    (1, date_trunc('month', current_date)::date + 1),
    (2, date_trunc('month', current_date)::date + 2),
    (1, date_trunc('month', current_date)::date + 3),
    (3, (date_trunc('year', current_date) - interval '1 year')::date + 40),
    (4, (date_trunc('month', current_date) - interval '2 month')::date + 5),
    (2, (date_trunc('year', current_date) - interval '1 year')::date + 200);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 2, 1, 7000), (1, 5, 2, 1200),
    (2, 1, 1, 95000),
    (3, 8, 3, 1500),
    (4, 3, 1, 60000), (4, 6, 1, 600),
    (5, 9, 1, 4500),
    (6, 7, 1, 1800);
