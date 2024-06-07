# Configuración y Ejecución de una Partioning BD en PostgreSQL

Este redame explica la realizacion de la pratica de Horizontal Pationing paso a paso

## Prerrequisitos

- Docker
- Postgres

## Paso 1: Configuración del entorno con Docker Compose

Crea un archivo `docker-compose.yml` 
```yaml
version: '3.1'

services:
  db:
    image: postgres:latest
    restart: always
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: exampledb
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

## Paso 2: Levantar el contenedor de Docker

levantar el contenedor

```bash
docker-compose up -d
```

## Paso 3: Conectarse al contenedor PostgreSQL

Conéctate al contenedor utilizando el comando

```bash
docker exec -it <nombre_del_contenedor> psql -U user -d exampledb
```

`<nombre_del_contenedor>` es el nombre del contenedor que se crea tambien puedes ver el nombre con `docker ps`.

## Paso 4: Crear Tablas Particionadas

### Range Partitioning
puedes ejecutar los escripts copiando el contenido en el carpeta `squema` por el nombre de `range_partioning` a la terminal o query de la base de datos 
```
CREATE  TABLE  sales (
id SERIAL,
sale_date DATE  NOT NULL,
amount DECIMAL(10, 2),
PRIMARY KEY (id, sale_date)

) PARTITION  BY  RANGE (sale_date);
CREATE  TABLE  sales_2024_04  PARTITION OF sales
FOR  VALUES  FROM ('2024-04-01') TO ('2024-05-01');
CREATE  TABLE  sales_2024_05  PARTITION OF sales
FOR  VALUES  FROM ('2024-05-01') TO ('2024-06-01');
```


### Hash Partitioning
puedes ejecutar los escripts copiando el contenido en el carpeta `squema` por el nombre de `hash_partioning` a la terminal o query de la base de datos 
```
CREATE  TABLE  users (
id SERIAL  PRIMARY KEY,
userame TEXT  NOT NULL,
created_at DATE  NOT NULL
) PARTITION  BY  HASH (id);
CREATE  TABLE  users_0  PARTITION OF users
FOR  VALUES  WITH (MODULUS 2, REMAINDER 0);
CREATE  TABLE  users_1  PARTITION OF users
FOR  VALUES  WITH (MODULUS 2, REMAINDER 1);
```

### List Partitioning
puedes ejecutar los escripts copiando el contenido en el carpeta `squema` por el nombre de `list_partioning` a la terminal o query de la base de datos 
```
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

```
## Paso 5 Insertar y verificar los datos 
puedes realizar esta accion copiando los valores del archivos `insert_data` y `read_data`en scripts

```
INSERT INTO sales (sale_date, amount) VALUES ('2024-04-15', 100.00);
INSERT INTO sales (sale_date, amount) VALUES ('2024-05-15', 200.00);

INSERT INTO orders (order_status, order_date) VALUES ('Pending', '2024-05-10');
INSERT INTO orders (order_status, order_date) VALUES ('Completed', '2024-05-11');
INSERT INTO orders (order_status, order_date) VALUES ('Cancelled', '2024-05-12');

INSERT INTO users (username, created_at) VALUES ('user1', '2024-04-01');
INSERT INTO users (username, created_at) VALUES ('user2', '2024-05-02');
```

Y para verificar la existencia de estos datos en las tablas puedes correr el siguiente query
```
SELECT * FROM sales_2024_04;
SELECT * FROM sales_2024_05;

SELECT * FROM orders_pending;
SELECT * FROM orders_completed;

SELECT * FROM users_0;
SELECT * FROM users_1;

```