WITH ranked AS (
    SELECT
        user_id,
        order_ts,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts) AS rn
    FROM orders
),
agg AS (
    SELECT
        user_id,
        MIN(order_ts) AS first_ts,
        COUNT(*) AS orders
    FROM orders
    GROUP BY user_id
),
sec AS (
    SELECT user_id, order_ts AS second_ts
    FROM ranked
    WHERE rn = 2
),
j AS (
    SELECT
        a.user_id,
        a.orders,
        CAST(JULIANDAY(s.second_ts) - JULIANDAY(a.first_ts) AS INTEGER) AS gap2
    FROM agg a
    LEFT JOIN sec s ON a.user_id = s.user_id
)
SELECT
    COUNT(*) AS buyers,
    SUM(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) AS repeat_buyers,
    ROUND(100.0 * SUM(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_rate,
    ROUND(100.0 * SUM(CASE WHEN orders >= 2 AND gap2 <= 30 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_rate_30d,
    ROUND(AVG(orders), 2) AS orders_per_buyer
FROM j;

WITH ranked AS (
    SELECT
        user_id,
        order_ts,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts) AS rn
    FROM orders
),
agg AS (
    SELECT user_id, MIN(order_ts) AS first_ts, COUNT(*) AS orders
    FROM orders
    GROUP BY user_id
),
sec AS (
    SELECT user_id, order_ts AS second_ts FROM ranked WHERE rn = 2
),
j AS (
    SELECT
        a.user_id,
        a.first_ts,
        a.orders,
        CAST(JULIANDAY(s.second_ts) - JULIANDAY(a.first_ts) AS INTEGER) AS gap2
    FROM agg a
    LEFT JOIN sec s ON a.user_id = s.user_id
)
SELECT
    STRFTIME('%Y-W%W', first_ts) AS cohort_week,
    COUNT(*) AS buyers,
    ROUND(100.0 * SUM(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_rate,
    ROUND(100.0 * SUM(CASE WHEN orders >= 2 AND gap2 <= 30 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_rate_30d,
    ROUND(AVG(orders), 2) AS orders_per_buyer
FROM j
GROUP BY cohort_week
ORDER BY cohort_week;

WITH ranked AS (
    SELECT
        user_id,
        order_ts,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts) AS rn
    FROM orders
),
agg AS (
    SELECT user_id, MIN(order_ts) AS first_ts, COUNT(*) AS orders
    FROM orders
    GROUP BY user_id
),
sec AS (
    SELECT user_id, order_ts AS second_ts FROM ranked WHERE rn = 2
),
j AS (
    SELECT
        a.user_id,
        u.acq_channel AS channel,
        a.orders,
        CAST(JULIANDAY(s.second_ts) - JULIANDAY(a.first_ts) AS INTEGER) AS gap2
    FROM agg a
    LEFT JOIN sec s ON a.user_id = s.user_id
    JOIN users u ON a.user_id = u.user_id
)
SELECT
    channel,
    COUNT(*) AS buyers,
    ROUND(100.0 * SUM(CASE WHEN orders >= 2 AND gap2 <= 30 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_rate_30d,
    ROUND(AVG(orders), 2) AS orders_per_buyer
FROM j
GROUP BY channel
ORDER BY repeat_rate_30d DESC;

WITH ranked AS (
    SELECT
        user_id,
        order_ts,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts) AS rn
    FROM orders
),
agg AS (
    SELECT user_id, MIN(order_ts) AS first_ts FROM orders GROUP BY user_id
),
sec AS (
    SELECT user_id, order_ts AS second_ts FROM ranked WHERE rn = 2
),
j AS (
    SELECT
        a.user_id,
        CAST(JULIANDAY(s.second_ts) - JULIANDAY(a.first_ts) AS INTEGER) AS gap2
    FROM agg a
    LEFT JOIN sec s ON a.user_id = s.user_id
)
SELECT
    d.day,
    ROUND(100.0 * SUM(CASE WHEN gap2 <= d.day THEN 1 ELSE 0 END) / (SELECT COUNT(*) FROM j), 2) AS repeat_rate
FROM (SELECT 1 AS day UNION SELECT 3 UNION SELECT 7 UNION SELECT 14 UNION SELECT 21 UNION SELECT 30) d
CROSS JOIN j
GROUP BY d.day
ORDER BY d.day;
