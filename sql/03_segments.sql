SELECT
    channel,
    COUNT(*) AS sessions,
    SUM(reached_cart) AS carts,
    SUM(reached_pay) AS paid,
    ROUND(100.0 * SUM(reached_cart) / COUNT(*), 2) AS cart_rate,
    ROUND(100.0 * SUM(reached_pay) / COUNT(*), 2) AS conv_rate,
    ROUND(100.0 * (SUM(reached_cart) - SUM(reached_pay)) / SUM(reached_cart), 2) AS cart_drop,
    ROUND(AVG(CASE WHEN converted = 1 THEN cart_value END), 2) AS aov
FROM sessions
GROUP BY channel
ORDER BY conv_rate DESC;

SELECT
    channel,
    COUNT(*) AS new_sessions,
    SUM(reached_cart) AS carts,
    SUM(reached_pay) AS paid,
    ROUND(100.0 * (SUM(reached_cart) - SUM(reached_pay)) / SUM(reached_cart), 2) AS new_cart_drop
FROM sessions
WHERE is_new = 1
GROUP BY channel
ORDER BY new_cart_drop;

SELECT
    CASE WHEN fee_stage = 'payment' THEN 'Fee shown late' ELSE 'Fee shown at cart' END AS fee_bucket,
    COUNT(*) AS sessions,
    SUM(reached_cart) AS carts,
    SUM(reached_pay) AS paid,
    ROUND(100.0 * (SUM(reached_cart) - SUM(reached_pay)) / SUM(reached_cart), 2) AS cart_drop
FROM sessions
WHERE is_new = 1
GROUP BY fee_bucket;

SELECT
    addr_steps,
    COUNT(*) AS sessions,
    SUM(reached_cart) AS carts,
    SUM(reached_addr) AS reached_addr,
    ROUND(100.0 * SUM(reached_addr) / SUM(reached_cart), 2) AS addr_rate,
    ROUND(100.0 * (SUM(reached_cart) - SUM(reached_pay)) / SUM(reached_cart), 2) AS cart_drop
FROM sessions
WHERE is_new = 1
GROUP BY addr_steps
ORDER BY addr_steps;

SELECT
    device,
    COUNT(*) AS sessions,
    ROUND(100.0 * SUM(converted) / COUNT(*), 2) AS conv_rate,
    ROUND(100.0 * (SUM(reached_cart) - SUM(reached_pay)) / SUM(reached_cart), 2) AS cart_drop
FROM sessions
GROUP BY device
ORDER BY conv_rate DESC;

SELECT
    city_tier,
    COUNT(*) AS sessions,
    ROUND(100.0 * SUM(converted) / COUNT(*), 2) AS conv_rate,
    ROUND(100.0 * (SUM(reached_cart) - SUM(reached_pay)) / SUM(reached_cart), 2) AS cart_drop
FROM sessions
GROUP BY city_tier
ORDER BY conv_rate DESC;

SELECT
    payment_method,
    COUNT(*) AS paid_orders,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS share,
    ROUND(AVG(amount), 2) AS aov
FROM orders
GROUP BY payment_method
ORDER BY paid_orders DESC;

SELECT
    is_new,
    COUNT(*) AS sessions,
    ROUND(100.0 * SUM(converted) / COUNT(*), 2) AS conv_rate,
    ROUND(AVG(cart_value), 2) AS avg_cart_value
FROM sessions
GROUP BY is_new;
