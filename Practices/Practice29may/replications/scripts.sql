CREATE USER replicator REPLICATION LOGIN CONNECTION LIMIT 100 PASSWORD 'password';

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(100),
    salary NUMERIC
);

INSERT INTO employees (name, position, salary) VALUES
('Alice', 'Engineer', 75000),
('Bob', 'Construct', 85000),
('Charlie', 'Candyman', 50000);
