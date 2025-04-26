SELECT c.first_name, c.last_name, f.title, cat.name AS category_name
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id
LEFT JOIN inventory i ON r.inventory_id = i.inventory_id
LEFT JOIN film f ON i.film_id = f.film_id
LEFT JOIN film_category fc ON f.film_id = fc.film_id
LEFT JOIN category cat ON fc.category_id = cat.category_id
WHERE cat.name = 'Action';




SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS film_count
FROM actor a
LEFT JOIN film_actor fa ON a.actor_id = fa.actor_id
GROUP BY a.actor_id, a.first_name, a.last_name
HAVING COUNT(fa.film_id) > 5
ORDER BY film_count DESC;




SELECT ci.city, COUNT(r.rental_id) AS rental_count
FROM city ci
LEFT JOIN address ad ON ci.city_id = ad.city_id
LEFT JOIN customer c ON ad.address_id = c.address_id
LEFT JOIN rental r ON c.customer_id = r.customer_id
GROUP BY ci.city
ORDER BY rental_count DESC
LIMIT 5;



SELECT c.first_name, c.last_name, total_spent
FROM (
    SELECT p.customer_id, SUM(p.amount) AS total_spent
    FROM payment p
    GROUP BY p.customer_id
) AS customer_spending
JOIN customer c ON customer_spending.customer_id = c.customer_id
WHERE total_spent > (
    SELECT AVG(total_spent)
    FROM (
        SELECT SUM(p.amount) AS total_spent
        FROM payment p
        GROUP BY p.customer_id
    ) AS avg_spending
)
ORDER BY total_spent DESC;



SELECT cat.name AS category_name, ranked_films.title, ranked_films.rental_count
FROM (
    SELECT fc.category_id, f.film_id, f.title, COUNT(r.rental_id) AS rental_count,
           RANK() OVER (PARTITION BY fc.category_id ORDER BY COUNT(r.rental_id) DESC) AS rank
    FROM film f
    LEFT JOIN film_category fc ON f.film_id = fc.film_id
    LEFT JOIN inventory i ON f.film_id = i.film_id
    LEFT JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY fc.category_id, f.film_id, f.title
) AS ranked_films
LEFT JOIN category cat ON ranked_films.category_id = cat.category_id
WHERE ranked_films.rank <= 3
ORDER BY category_name, rental_count DESC;


SELECT cat.name AS category_name, total_rentals
FROM (
    SELECT fc.category_id, COUNT(r.rental_id) AS total_rentals
    FROM film_category fc
    LEFT JOIN inventory i ON fc.film_id = i.film_id
    LEFT JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY fc.category_id
) AS category_rentals
JOIN category cat ON category_rentals.category_id = cat.category_id
WHERE total_rentals > 50
ORDER BY total_rentals DESC;


SELECT a.first_name, a.last_name, actor_rentals.total_rentals
FROM actor a
JOIN (
    SELECT fa.actor_id, COUNT(r.rental_id) AS total_rentals
    FROM film_actor fa
    JOIN inventory i ON fa.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY fa.actor_id
) AS actor_rentals ON a.actor_id = actor_rentals.actor_id
WHERE actor_rentals.total_rentals = (
    SELECT MAX(total_rentals)
    FROM (
        SELECT fa.actor_id, COUNT(r.rental_id) AS total_rentals
        FROM film_actor fa
        JOIN inventory i ON fa.film_id = i.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        GROUP BY fa.actor_id
    ) AS actor_totals
);



SELECT c.first_name, c.last_name, rental_count
FROM (
    SELECT r.customer_id, COUNT(r.rental_id) AS rental_count
    FROM rental r
    GROUP BY r.customer_id
) AS customer_rentals
JOIN customer c ON customer_rentals.customer_id = c.customer_id
WHERE rental_count > (
    SELECT AVG(rental_count)
    FROM (
        SELECT COUNT(r.rental_id) AS rental_count
        FROM rental r
        GROUP BY r.customer_id
    ) AS avg_rentals
)
ORDER BY rental_count DESC;


SELECT 
    c.first_name || ' ' || c.last_name AS customer_name,
    f.title AS movie_title,
    cat.name AS category_name,
    r.rental_date,
    a.first_name || ' ' || a.last_name AS actor_name,
    p.amount AS payment_amount
FROM 
    public.customer c
JOIN 
    public.rental r ON c.customer_id = r.customer_id
JOIN 
    public.inventory i ON r.inventory_id = i.inventory_id
JOIN 
    public.film f ON i.film_id = f.film_id
JOIN 
    public.film_category fc ON f.film_id = fc.film_id
JOIN 
    public.category cat ON fc.category_id = cat.category_id
JOIN 
    public.film_actor fa ON f.film_id = fa.film_id
JOIN 
    public.actor a ON fa.actor_id = a.actor_id
JOIN 
    public.payment p ON r.rental_id = p.rental_id
WHERE 
    cat.name IN ('Action', 'Comedy')
ORDER BY 
    customer_name, rental_date;


SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    a.address AS customer_address,
    ci.city AS customer_city,
    COUNT(r.rental_id) AS total_rentals,
    SUM(p.amount) AS total_amount_spent,
    GROUP_CONCAT(f.title) AS rented_films
FROM
    customer c  -- Start with the customer table
LEFT JOIN
    address a ON c.address_id = a.address_id  -- Get customer's address
LEFT JOIN
    city ci ON a.city_id = ci.city_id  -- Get the city where the customer lives
LEFT JOIN
    rental r ON c.customer_id = r.customer_id  -- Get the customer's rentals
LEFT JOIN
    inventory i ON r.inventory_id = i.inventory_id  -- Link to the inventory to get film details
LEFT JOIN
    film f ON i.film_id = f.film_id  -- Get the film names
LEFT JOIN
    payment p ON r.rental_id = p.rental_id  -- Get payment information for each rental
WHERE
    c.customer_id IN (SELECT customer_id FROM customer WHERE activebool = TRUE) -- Subquery to filter active customers
GROUP BY
    c.customer_id, c.first_name, c.last_name, a.address, ci.city  -- Group results by customer and address
ORDER BY
    c.customer_id;  -- Order the output by customer ID

SELECT
    f.title AS film_title,  -- Select the film's title
    c.name AS category_name,  -- Select the category name
    f.rental_rate,  -- Select the rental rate
    f.replacement_cost,  -- Select the replacement cost
    f.rating,  -- Select the film's rating
    f.special_features,  -- Select any special features
    COUNT(r.rental_id) AS total_rentals,  -- Count the total rentals for each film
    SUM(p.amount) AS total_revenue,  -- Calculate the total revenue generated by each film
    -- Calculate the average rental duration for each film
    AVG(r.return_date - r.rental_date) AS average_rental_duration,
    -- Extract a list of actors featuring in the film
    GROUP_CONCAT(DISTINCT a.first_name || ' ' || a.last_name) AS actors
FROM
    film f  -- Start with the 'film' table
JOIN
    film_category fc ON f.film_id = fc.film_id  -- Join with 'film_category' to get category information
JOIN
    category c ON fc.category_id = c.category_id  -- Join with 'category' to get category names
LEFT JOIN
    inventory i ON f.film_id = i.film_id  -- Left join with 'inventory' to include rental details
LEFT JOIN
    rental r ON i.inventory_id = r.inventory_id  -- Left join with 'rental' to access rental records
LEFT JOIN
    payment p ON r.rental_id = p.rental_id  -- Left join with 'payment' to include payment information
LEFT JOIN  
    film_actor fa ON f.film_id = fa.film_id  -- Left join with 'film_actor' to get actor details
LEFT JOIN
    actor a ON fa.actor_id = a.actor_id  -- Left join with 'actor' to get actor names
GROUP BY
    f.film_id, f.title, c.name, f.rental_rate, f.replacement_cost, f.rating, f.special_features  -- Group by film-specific attributes
HAVING
    COUNT(r.rental_id) > 50  -- Filter out films with less than or equal to 50 rentals
ORDER BY
    total_revenue DESC;  -- Order the results by total revenue in descending order