SELECT c.id, c.full_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.id
      AND o.ordered_at >= date_trunc('year', current_date) - interval '1 year'
      AND o.ordered_at < date_trunc('year', current_date)
)
ORDER BY c.full_name;
