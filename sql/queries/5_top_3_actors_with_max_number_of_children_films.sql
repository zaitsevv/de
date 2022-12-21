WITH actors_with_number_of_children_films AS (SELECT actor.actor_id,
                                                     actor.first_name,
                                                     actor.last_name,
                                                     COUNT(film.film_id) AS number_of_children_films
                                              FROM actor
                                                       INNER JOIN film_actor USING (actor_id)
                                                       INNER JOIN film USING (film_id)
                                                       INNER JOIN film_category USING (film_id)
                                                       INNER JOIN category USING (category_id)
                                              WHERE category.name = 'Children'
                                              GROUP BY actor.actor_id,
                                                       actor.first_name,
                                                       actor.last_name),
     top_3_distinct_numbers_of_children_films AS (SELECT DISTINCT actors_with_films.number_of_children_films AS number
                                                  FROM actors_with_number_of_children_films AS actors_with_films
                                                  ORDER BY actors_with_films.number_of_children_films DESC
                                                  LIMIT 3)
SELECT actors_with_films.actor_id,
       actors_with_films.first_name,
       actors_with_films.last_name,
       actors_with_films.number_of_children_films
FROM actors_with_number_of_children_films AS actors_with_films
WHERE actors_with_films.number_of_children_films IN (SELECT top_3.number
                                                     FROM top_3_distinct_numbers_of_children_films AS top_3)
ORDER BY actors_with_films.number_of_children_films DESC;
