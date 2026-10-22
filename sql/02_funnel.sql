WITH base AS (
    SELECT COUNT(*) AS sessions FROM sessions
),
steps AS (
    SELECT
        SUM(reached_view) AS view_n,
        SUM(reached_cart) AS cart_n,
        SUM(reached_addr) AS addr_n,
        SUM(reached_pay)  AS pay_n
    FROM sessions
)
SELECT
    b.sessions,
    s.view_n,
    ROUND(100.0 * s.view_n / b.sessions, 2) AS view_pct,
    s.cart_n,
    ROUND(100.0 * s.cart_n / b.sessions, 2) AS cart_pct,
    s.addr_n,
    ROUND(100.0 * s.addr_n / b.sessions, 2) AS addr_pct,
    s.pay_n,
    ROUND(100.0 * s.pay_n / b.sessions, 2) AS pay_pct
FROM base b, steps s;

WITH f AS (
    SELECT
        SUM(reached_cart) AS cart_n,
        SUM(reached_addr) AS addr_n,
        SUM(reached_pay)  AS pay_n
    FROM sessions
    WHERE is_new = 1
)
SELECT
    cart_n,
    addr_n,
    pay_n,
    ROUND(100.0 * (cart_n - addr_n) / cart_n, 2) AS cart_to_addr_drop,
    ROUND(100.0 * (addr_n - pay_n) / addr_n, 2) AS addr_to_pay_drop,
    ROUND(100.0 * (cart_n - pay_n) / cart_n, 2) AS cart_to_pay_drop
FROM f;

SELECT
    ROUND(100.0 * (SUM(reached_cart) - SUM(reached_pay)) / SUM(reached_cart), 2) AS cart_to_pay_drop
FROM sessions
WHERE is_new = 0;

WITH e AS (
    SELECT
        session_id,
        MAX(CASE WHEN event = 'item_view' THEN 1 ELSE 0 END) AS v,
        MAX(CASE WHEN event = 'add_to_cart' THEN 1 ELSE 0 END) AS c,
        MAX(CASE WHEN event = 'select_address' THEN 1 ELSE 0 END) AS a,
        MAX(CASE WHEN event = 'payment_success' THEN 1 ELSE 0 END) AS p,
        MAX(CASE WHEN event = 'payment_failed' THEN 1 ELSE 0 END) AS f
    FROM events
    GROUP BY session_id
)
SELECT
    COUNT(*) AS sessions,
    SUM(v) AS view_n,
    SUM(c) AS cart_n,
    SUM(a) AS addr_n,
    SUM(f) AS failed_n,
    SUM(p) AS pay_n,
    ROUND(100.0 * SUM(f) / NULLIF(SUM(a), 0), 2) AS fail_rate_on_attempt
FROM e;

SELECT
    event,
    COUNT(*) AS n,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(DISTINCT session_id) FROM events), 2) AS per_session
FROM events
GROUP BY event
ORDER BY n DESC;
