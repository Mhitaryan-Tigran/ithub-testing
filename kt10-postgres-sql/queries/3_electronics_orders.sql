SELECT o.id, o.ordered_at, c.full_name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE EXISTS (
    SELECT 1 FROM order_items oi
    JOIN products p ON p.id = oi.product_id
    JOIN categories cat ON cat.id = p.category_id
    WHERE oi.order_id = o.id AND cat.name = 'Электроника'
)
ORDER BY o.ordered_at, o.id;
