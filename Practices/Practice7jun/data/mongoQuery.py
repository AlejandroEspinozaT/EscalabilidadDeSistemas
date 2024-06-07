import time
from pymongo import MongoClient
import random
from datetime import datetime

from data.mongoData import DataInserter, MongoDBClient

class QueryExecutor(MongoDBClient):
    def __init__(self, collection_name='products', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection = self.db[collection_name]

    def measure_query_time(self, query):
        start_time = time.time()
        result = self.collection.count_documents(query)
        end_time = time.time()
        return end_time - start_time

    def execute_queries(self, volumes):
        queries = [
            {"category": "Electronics"},
            {"price": {"$gt": 500}},
            {"stock": {"$lt": 20}}
        ]
        for volume in volumes:
            times = []
            for query in queries:
                query_time = self.measure_query_time(query)
                times.append(query_time)
                print(f"Query: {query}, Volume: {volume}, Time: {query_time:.4f} seconds")

if __name__ == "__main__":
    inserter = DataInserter()
    executor = QueryExecutor()

    volumes = [1000, 10000, 100000, 1000000]

    for volume in volumes:
        inserter.insert_data(volume)
        #to prove the optimization we can create indexes 
        #inserter.create_indexes() 
        executor.execute_queries([volume])