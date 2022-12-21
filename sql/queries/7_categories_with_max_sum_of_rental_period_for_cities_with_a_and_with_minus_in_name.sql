WITH categories_with_rental_period_for_city AS (SELECT category.category_id,
                                                       category.name,
                                                       city.city,
                                                       SUM(EXTRACT(HOURS FROM rental.return_date) -
                                                           EXTRACT(HOURS FROM rental.rental_date)) AS sum_of_rental_hours
                                                FROM category
                                                         INNER JOIN film_category USING (category_id)
                                                         INNER JOIN film USING (film_id)
                                                         INNER JOIN inventory USING (film_id)
                                                         INNER JOIN rental USING (inventory_id)
                                                         INNER JOIN customer USING (customer_id)
                                                         INNER JOIN address USING (address_id)
                                                         INNER JOIN city USING (city_id)
                                                GROUP BY category.category_id,
                                                         category.name,
                                                         city.city_id,
                                                         city.city)
(SELECT categories.category_id,
        categories.name,
        categories.sum_of_rental_hours
FROM categories_with_rental_period_for_city AS categories
WHERE categories.city LIKE '%a%'
LIMIT 1)
UNION ALL
(SELECT categories.category_id,
        categories.name,
        categories.sum_of_rental_hours
 FROM categories_with_rental_period_for_city AS categories
 WHERE categories.city LIKE '%-%'
 LIMIT 1);
