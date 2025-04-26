SELECT c.first_name, c.last_name, f.title, cat.name AS category_name
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id
LEFT JOIN inventory i ON r.inventory_id = i.inventory_id
LEFT JOIN film f ON i.film_id = f.film_id
LEFT JOIN film_category fc ON f.film_id = fc.film_id
LEFT JOIN category cat ON fc.category_id = cat.category_id
WHERE cat.name = 'Action';


SELECT f.title, COUNT(r.rental_id) AS rental_count
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
LEFT JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id, f.title
ORDER BY rental_count DESC
LIMIT 10;


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

-
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


SELECT a.first_name, a.last_name, total_rentals
FROM actor a
JOIN (
    SELECT fa.actor_id, COUNT(r.rental_id) AS total_rentals
    FROM film_actor fa
    JOIN inventory i ON fa.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY fa.actor_id
) AS actor_rentals ON a.actor_id = actor_rentals.actor_id
WHERE total_rentals = (
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



WITH actor_rentals AS (
    SELECT fa.actor_id, COUNT(r.rental_id) AS total_rentals
    FROM film_actor fa
    JOIN inventory i ON fa.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY fa.actor_id
)
SELECT a.first_name, a.last_name, total_rentals
FROM actor a
JOIN actor_rentals ON a.actor_id = actor_rentals.actor_id;



SELECT DISTINCT
    si.WORKSTATIONNAME AS "Machine Name", 
    MAX(aaaUser.FIRST_NAME) AS "Assigned User", 
    MAX(si.LOGGEDUSER) AS "Last Logged In User", 
    FORMAT(DATEADD(SECOND, ah.audittime / 1000, '1970-01-01'), 'MM/dd/yyyy hh:mm:ss tt') AS "Last Audit Time", 
    state.DISPLAYSTATE AS "Asset State", 
    MAX(resource.ACQUISITIONDATE) AS "Acquisition Date", 
    MAX(memInfo.TOTALMEMORY / 1024 / 1024) AS "Total Memory (MB)", 
    MAX(osInfo.OSNAME) AS "Operating System", 
    CASE 
        WHEN LOWER(sl.softwarename) = 'sentinel agent' THEN 'Installed'
        ELSE 'Not Installed'
    END AS "SentinelOne Status", 
    CASE 
        WHEN LOWER(sl.softwarename) = 'forcepoint one endpoint' THEN 'Installed'
        ELSE 'Not Installed'
    END AS "Forcepoint Status" 
FROM 
    SystemInfo si
LEFT JOIN lastauditinfo la 
    ON si.WORKSTATIONID = la.workstationid
LEFT JOIN audithistory ah 
    ON la.last_auditid = ah.auditid
LEFT JOIN Resources resource 
    ON si.WORKSTATIONID = resource.RESOURCEID
LEFT JOIN ResourceState state 
    ON resource.RESOURCESTATEID = state.RESOURCESTATEID
LEFT JOIN ResourceOwner rOwner 
    ON resource.RESOURCEID = rOwner.RESOURCEID
LEFT JOIN ResourceAssociation rToAsset 
    ON rOwner.RESOURCEOWNERID = rToAsset.RESOURCEOWNERID
LEFT JOIN SDUser sdUser 
    ON rOwner.USERID = sdUser.USERID
LEFT JOIN AaaUser aaaUser 
    ON sdUser.USERID = aaaUser.USER_ID
LEFT JOIN MemoryInfo memInfo 
    ON si.WORKSTATIONID = memInfo.WORKSTATIONID
LEFT JOIN OsInfo osInfo 
    ON si.WORKSTATIONID = osInfo.WORKSTATIONID
LEFT JOIN softwareinfo si_sw 
    ON si.WORKSTATIONID = si_sw.workstationid
LEFT JOIN softwarelist sl 
    ON si_sw.softwareid = sl.softwareid
WHERE 
    state.DISPLAYSTATE = N'In Use' 
    AND aaaUser.FIRST_NAME IS NOT NULL 
    AND memInfo.TOTALMEMORY > 4294967296 -- Greater than 4GB
    AND si.WORKSTATIONID NOT IN (
        SELECT si2.workstationid 
        FROM softwareinfo si2
        LEFT JOIN softwarelist sl2 ON si2.softwareid = sl2.softwareid
        WHERE LOWER(sl2.softwarename) IN ('sentinel agent', 'forcepoint one endpoint')
    )
GROUP BY 
    si.WORKSTATIONNAME, 
    state.DISPLAYSTATE, 
    ah.audittime, 
    sl.softwarename
ORDER BY 
    si.WORKSTATIONNAME;
