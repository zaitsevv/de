SELECT film.film_id,
       film.title
FROM film
WHERE NOT EXISTS(SELECT 1
                 FROM inventory
                 WHERE inventory.film_id = film.film_id);
