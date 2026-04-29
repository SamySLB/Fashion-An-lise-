SELECT 
    p.product_id,
    p.name,
    COUNT(s.size) AS size_count
FROM products p
LEFT JOIN sizes s ON p.product_id = s.product_id
GROUP BY p.product_id, p.name;