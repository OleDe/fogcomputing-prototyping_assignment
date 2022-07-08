import pymongo, sys

class cldb:
    def __init__(self, location: str, port=27017):
        self.hostname = location
        self.port = port
        self.username = 'cl'
        self.password = 'cl123'
        self.db_name = 'cl_db'
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
    
    def get_data_latter_than(self, time):
        """
        Returns data that was created after time.
        """
        return list(self.collection.find({'time' : { '$gt':  time }}).sort('time', pymongo.ASCENDING))

    def erase_data_starting_from(self, time):

        """
        Erases data that is older than or equal time.
        """
        return self.collection.delete_many({'time' : { '$lte':  time }})


if __name__ == '__main__':
    db = cldb()
    db.insert({'air_pressure': 1013.25, 'air_temperature': 25, 'time': 12345})
    db.insert({'air_pressure': 1015.25, 'air_temperature': 27, 'time': 12347})
    db.insert({'air_pressure': 1014.25, 'air_temperature': 26, 'time': 12346})
    print(db.get_data_newer_than(12346))
    db.erase_old_data_starting_from(12346)
