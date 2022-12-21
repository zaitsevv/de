SELECT city.city_id,
       city.city,
       COUNT(customer) FILTER (WHERE customer.activebool = TRUE)  AS number_of_active_customers,
       COUNT(customer) FILTER (WHERE customer.activebool = FALSE) AS number_of_inactive_customers
FROM city
         INNER JOIN address USING (city_id)
         INNER JOIN customer USING (address_id)
GROUP BY city.city_id,
         city.city
ORDER BY number_of_inactive_customers DESC;
