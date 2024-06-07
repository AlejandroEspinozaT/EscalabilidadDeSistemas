from pymongo import MongoClient
import random
from datetime import datetime

class MongoDBClient:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='test_db'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

class DataInserter(MongoDBClient):
    def __init__(self, collection_name='products', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection = self.db[collection_name]
        self.categories = ['Electronics', 'Books', 'Clothing', 'Home', 'Toys']

    def generate_product(self, i):
        return {
            "product_id": f"prod_{i}",
            "name": f"Product {i}",
            "category": random.choice(self.categories),
            "price": round(random.uniform(10.0, 1000.0), 2),
            "stock": random.randint(1, 100),
            "created_at": datetime.now()
        }

    def insert_data(self, volume):
        self.collection.delete_many({})
        products = [self.generate_product(i) for i in range(volume)]
        self.collection.insert_many(products)
        print(f"Inserted {volume} documents")
        
    def create_indexes(self):
        self.collection.create_index("category")
        self.collection.create_index("price")
        self.collection.create_index("stock")