
# Practice 3 Query Response Times in MongoDB
## Setup
### 1. Create a  docker-compose.yml  for MongoDB

```Dockerfile

version: '3.8'
services:
mongodb:
image: mongo:latest

container_name: mongodb
ports:
- 27017:27017
volumes:
- mongodb-data:/data/db
volumes:
mongodb-data:

```
### 2. Start MongoDB Container

  

```sh

docker-compose  up  -d

```

  

## Data Insertion and Indexing

  

### 3. Create mongoData.py for Data Insertion

  

```python

from  pymongo  import  MongoClient

import  random

from  datetime  import  datetime

  

class  MongoDBClient:

def  __init__(self, uri='mongodb://localhost:27017/', db_name='test_db'):

self.client  =  MongoClient(uri)

self.db  =  self.client[db_name]

  

class  DataInserter(MongoDBClient):

def  __init__(self, collection_name='products', *args, **kwargs):

super().__init__(*args, **kwargs)

self.collection  =  self.db[collection_name]

self.categories  = ['Electronics', 'Books', 'Clothing', 'Home', 'Toys']

  

def  generate_product(self, i):

return {

"product_id": f"prod_{i}",

"name": f"Product {i}",

"category": random.choice(self.categories),

"price": round(random.uniform(10.0, 1000.0), 2),

"stock": random.randint(1, 100),

"created_at": datetime.now()

}

  

def  insert_data(self, volume):

self.collection.delete_many({})

products  = [self.generate_product(i) for  i  in  range(volume)]

self.collection.insert_many(products)

print(f"Inserted {volume} documents")

def  create_indexes(self):

self.collection.create_index("category")

self.collection.create_index("price")

self.collection.create_index("stock")

```

  

## Query Execution and Timing

  

### 5. Create mongoQuery.py for Query Execution
```python
import  time

from  pymongo  import  MongoClient

import  random

from  datetime  import  datetime

  

from  data.mongoData  import  DataInserter, MongoDBClient

  

class  QueryExecutor(MongoDBClient):

def  __init__(self, collection_name='products', *args, **kwargs):

super().__init__(*args, **kwargs)

self.collection  =  self.db[collection_name]

  

def  measure_query_time(self, query):

start_time  =  time.time()

result  =  self.collection.count_documents(query)

end_time  =  time.time()

return  end_time  -  start_time

  

def  execute_queries(self, volumes):

queries  = [

{"category": "Electronics"},

{"price": {"$gt": 500}},

{"stock": {"$lt": 20}}

]

for  volume  in  volumes:

times  = []

for  query  in  queries:

query_time  =  self.measure_query_time(query)

times.append(query_time)

print(f"Query: {query}, Volume: {volume}, Time: {query_time:.4f} seconds")

  

if  __name__  ==  "__main__":

inserter  =  DataInserter()

executor  =  QueryExecutor()

  

volumes  = [1000, 10000, 100000, 1000000]

  

for  volume  in  volumes:

inserter.insert_data(volume)

#to prove the optimization we can create indexes

#inserter.create_indexes()

executor.execute_queries([volume])
```

  

## Execution
### 6. Run the mongoQuery.py Script
```sh
python3  mongoQuery.py
```
### 6. Run again the mongoQuery.py Script but with the index creation
```sh
python3  mongoQuery.py
```