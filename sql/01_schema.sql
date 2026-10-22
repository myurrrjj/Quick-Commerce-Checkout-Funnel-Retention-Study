DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id      INTEGER PRIMARY KEY,
    acq_channel  TEXT,
    device       TEXT,
    city_tier    TEXT,
    signup_date  DATE
);

CREATE TABLE sessions (
    session_id    INTEGER PRIMARY KEY,
    user_id       INTEGER,
    ts            TIMESTAMP,
    channel       TEXT,
    device        TEXT,
    city_tier     TEXT,
    is_new        INTEGER,
    cart_value    REAL,
    delivery_fee  REAL,
    fee_stage     TEXT,
    addr_steps    INTEGER,
    reached_view  INTEGER,
    reached_cart  INTEGER,
    reached_addr  INTEGER,
    reached_pay   INTEGER,
    converted     INTEGER,
    payment_method TEXT
);

CREATE TABLE events (
    event_id     INTEGER PRIMARY KEY,
    session_id   INTEGER,
    user_id      INTEGER,
    ts           TIMESTAMP,
    event        TEXT,
    channel      TEXT,
    is_new       INTEGER,
    cart_value   REAL,
    delivery_fee REAL,
    fee_stage    TEXT
);

CREATE TABLE orders (
    order_id       INTEGER PRIMARY KEY,
    user_id        INTEGER,
    session_id     INTEGER,
    order_ts       TIMESTAMP,
    amount         REAL,
    delivery_fee   REAL,
    payment_method TEXT,
    status         TEXT
);

CREATE INDEX idx_sess_user ON sessions (user_id);
CREATE INDEX idx_sess_channel ON sessions (channel);
CREATE INDEX idx_ev_session ON events (session_id);
CREATE INDEX idx_ev_name ON events (event);
CREATE INDEX idx_ord_user ON orders (user_id);
