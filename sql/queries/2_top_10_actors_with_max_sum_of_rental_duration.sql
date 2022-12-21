SELECT actor.actor_id,
       actor.first_name,
       actor.last_name,
       SUM(film.rental_duration) AS sum_of_rental_duration
FROM actor
         INNER JOIN film_actor USING (actor_id)
         INNER JOIN film USING (film_id)
GROUP BY actor.actor_id,
         actor.first_name,
         actor.last_name
ORDER BY sum_of_rental_duration DESC
LIMIT 10;
