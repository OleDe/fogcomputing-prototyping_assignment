import pymongo, sys

# TODO: make shared db module

class svdb:
    def __init__(self):
        self.hostname = 'localhost'
        self.port = 27018
        self.username = 'serv'
        self.password = 'serv123'
        self.db_name = 'serv_db'
        self.collection_name = 'sensor_data'
        self.client = pymongo.MongoClient(self.hostname,
                                            self.port,
                                            username=self.username,
                                            password=self.password)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        self.collection.create_index([('time', pymongo.ASCENDING)],
                                    unique=True)
    
    def insert(self, doc):
        """
        Insert a document in sensor_data collection.
        """
        try:
            self.collection.insert_one(doc)
        except pymongo.errors.DuplicateKeyError:
            print('cldb.insert: Document already exists!', file=sys.stderr)
    
    def get_latest_timestamp(self):
        """
        Returns latest timestamp. In case of empty database, 0 will be returned
        """
        docs = self.collection.find().sort('time', pymongo.DESCENDING)
        try:
            return docs[0]['time']
        except IndexError:
            return 0.0


if __name__ == '__main__':
    db = svdb()
    print(db.get_latest_timestamp())
    db.insert({'air_pressure': 1013.25, 'air_temperature': 25, 'time': 12345})
    db.insert({'air_pressure': 1015.25, 'air_temperature': 27, 'time': 12347})
    db.insert({'air_pressure': 1014.25, 'air_temperature': 26, 'time': 12346})
    print(db.get_latest_timestamp())
