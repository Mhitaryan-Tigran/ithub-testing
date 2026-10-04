SELECT c.id, c.full_name, SUM(oi.quantity * oi.unit_price) AS total
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
WHERE o.ordered_at >= date_trunc('month', current_date)
  AND o.ordered_at < date_trunc('month', current_date) + interval '1 month'
GROUP BY c.id, c.full_name
ORDER BY total DESC;
