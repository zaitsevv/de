SELECT category.category_id,
       category.name,
       COUNT(film_category.film_id) AS number_of_films
FROM category
         LEFT JOIN film_category USING (category_id)
GROUP BY category.category_id,
         category.name
ORDER BY number_of_films DESC;
