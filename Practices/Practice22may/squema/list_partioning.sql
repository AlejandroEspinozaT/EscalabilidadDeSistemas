CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_status TEXT NOT NULL,
    order_date DATE NOT NULL,
    PRIMARY KEY (id, order_date)
) PARTITION BY LIST (order_status);
CREATE TABLE orders_pending PARTITION OF orders
    FOR VALUES IN ('Pending');
CREATE TABLE orders_completed PARTITION OF orders
    FOR VALUES IN ('Completed');
CREATE TABLE orders_cancelled PARTITION OF orders
    FOR VALUES IN ('Cancelled');
