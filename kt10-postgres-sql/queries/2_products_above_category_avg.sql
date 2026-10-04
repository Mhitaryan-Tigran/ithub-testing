SELECT p.id, p.name, cat.name AS category, p.price
FROM products p
JOIN categories cat ON cat.id = p.category_id
WHERE p.price > (SELECT AVG(p2.price) FROM products p2 WHERE p2.category_id = p.category_id)
ORDER BY p.price ASC;
