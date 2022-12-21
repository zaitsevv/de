SELECT category.category_id,
       category.name,
       SUM(film.replacement_cost) AS sum_of_replacement_cost
FROM category
         INNER JOIN film_category USING (category_id)
         INNER JOIN film USING (film_id)
GROUP BY category.category_id,
         category.name
ORDER BY sum_of_replacement_cost DESC
LIMIT 1;
