
## Escalando una Base de Datos Relacional con Docker

- tener una base de datos relacional  con datos ya cargados.

### Configuración de la Replicación (Replication) en PostgreSQL

#### 1. Crear el archivo `docker-compose.yml`

```yaml
version: '3.8'
services:
  postgres-master:
    image: postgres:13
    container_name: postgres-master
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - ./master-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  postgres-replica1:
    image: postgres:13
    container_name: postgres-replica1
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_MASTER_HOST: postgres-master
    volumes:
      - ./replica1-data:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    depends_on:
      - postgres-master

  postgres-replica2:
    image: postgres:13
    container_name: postgres-replica2
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_MASTER_HOST: postgres-master
    volumes:
      - ./replica2-data:/var/lib/postgresql/data
    ports:
      - "5434:5432"
    depends_on:
      - postgres-master
```

#### 2. Iniciar los contenedores

```bash
docker-compose up -d
```

#### 3. Configurar la replicación en el maestro

Accede al contenedor del maestro:

```bash
docker exec -it postgres-master bash
```

Dentro del contenedor, conéctate a PostgreSQL:

```bash
psql -U myuser -d mydatabase
```

Ejecuta los siguientes comandos SQL para crear un usuario de replicación:

```sql
CREATE USER replicator REPLICATION LOGIN CONNECTION LIMIT 100 PASSWORD 'password';
```

Edita el archivo `postgresql.conf`:

```bash
nano /var/lib/postgresql/data/postgresql.conf
```

Añade 

```conf
listen_addresses = '*'
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64
```

Edita el archivo `pg_hba.conf`:

```bash
nano /var/lib/postgresql/data/pg_hba.conf
```

Añade la siguiente línea para permitir conexiones de replicación:

```conf
host replication replicator 0.0.0.0/0 md5
```

Reinicia el contenedor del maestro para aplicar los cambios:

```bash
exit
docker restart postgres-master
```

#### 4. Configurar la replicación en las réplicas

Accede a cada contenedor de las réplicas:

```bash
docker exec -it postgres-replica1 bash
```

Dentro del contenedor, elimina los datos iniciales y configura la replicación:

```bash
rm -rf /var/lib/postgresql/data/*
pg_basebackup -h postgres-master -D /var/lib/postgresql/data -U replicator -v -P --wal-method=stream
```

Crea un archivo `recovery.conf` dentro del directorio de datos (`/var/lib/postgresql/data`) con el siguiente contenido:

```text
standby_mode = 'on'
primary_conninfo = 'host=postgres-master port=5432 user=replicator password=password'
trigger_file = '/tmp/postgresql.trigger'
```

Repite estos pasos para la segunda réplica (`postgres-replica2`).

#### 5. Reiniciar los contenedores de las réplicas

```bash
docker restart postgres-replica1
docker restart postgres-replica2
```

### Creación de Datos en PostgreSQL

Para crear datos en tu base de datos PostgreSQL dentro del contenedor, sigue estos pasos:

#### 1. Acceder al contenedor del maestro

```bash
docker exec -it postgres-master bash
```

#### 2. Conectarse a PostgreSQL

```bash
psql -U myuser -d mydatabase
```

#### 3. Crear una tabla y agregar datos

```sql
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
```

#### 4. Verificar los datos

```sql
SELECT * FROM employees;
```


### Resumen de los pasos

1. **Crear el archivo `docker-compose.yml`**: Definir los servicios para el maestro y las réplicas de PostgreSQL.
2. **Iniciar los contenedores**: Utilizar Docker Compose para iniciar todos los contenedores definidos.
3. **Configurar la replicación en el maestro**: Crear un usuario de replicación y configurar los archivos `postgresql.conf` y `pg_hba.conf`.
4. **Configurar la replicación en las réplicas**: Configurar cada réplica para conectarse al maestro y recibir datos.
5. **Reiniciar los contenedores de las réplicas**: Asegurarse de que todos los cambios se apliquen correctamente.
6. **Crear datos en la base de datos**: Crear una tabla y agregar datos para verificar la configuración.
